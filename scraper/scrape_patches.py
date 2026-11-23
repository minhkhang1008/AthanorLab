#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup, Tag

from scraper.common import (
    BASE_URL,
    RAW_DATA_DIR,
    PoliteFetcher,
    clean_text,
    table_to_markdown,
    url_last_segment,
    utc_now_iso,
    write_json,
)

UPDATES_URL = f"{BASE_URL}/cap-nhat/"

INCLUDE_TITLE_KEYWORDS = (
    "điều chỉnh",
    "cân bằng",
    "chi tiết phiên bản",
    "chi tiết bản cập nhật",
    "bản cập nhật",
    "cập nhật phiên bản",
    "chỉnh sửa",
)
EXCLUDE_TITLE_KEYWORDS = (
    "quân huy",
    "nạp thẻ",
    "cửa hàng",
    "mở bán",
    "xử phạt",
    "khóa tài khoản",
    "đổi trang phục",
    "sự kiện",
    "liên quân day",
)
NON_GAMEPLAY_SECTION_KEYWORDS = (
    "sự kiện",
    "mở bán",
    "trang phục",
    "sổ sứ mệnh",
    "cửa hàng",
    "nạp",
    "mục lục",
)
GAMEPLAY_SECTION_KEYWORDS = (
    "cân bằng",
    "tướng",
    "chiến trường",
    "trang bị",
    "phù hiệu",
    "phụ trợ",
    "điều chỉnh",
    "làm lại",
    "cơ chế",
    "bản đồ",
    "sửa lỗi",
    "tối ưu",
)


def is_balance_patch_title(title: str) -> bool:
    low = title.lower()
    if any(ex in low for ex in EXCLUDE_TITLE_KEYWORDS):
        return False
    return any(inc in low for inc in INCLUDE_TITLE_KEYWORDS)


def is_gameplay_section(heading: str) -> bool:
    low = heading.lower()
    if any(k in low for k in NON_GAMEPLAY_SECTION_KEYWORDS):
        return False
    if any(k in low for k in GAMEPLAY_SECTION_KEYWORDS):
        return True
    return True


def parse_patch_article(html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")
    article = soup.select_one("article.p-news__single--content")
    if not article:
        return []

    # Support both H1->H2 (current Garena standard) and H2->H3 (older articles)
    has_h1 = bool(article.find("h1"))
    top_tag = "h1" if has_h1 else "h2"
    sub_tag = "h2" if has_h1 else "h3"

    sections: list[dict[str, Any]] = []
    cur_sec: dict[str, Any] | None = None
    cur_sub: dict[str, Any] | None = None

    def ensure_section(title: str) -> dict[str, Any]:
        sec = {
            "heading": title,
            "is_gameplay_relevant": is_gameplay_section(title),
            "intro_lines": [],
            "subsections": [],
        }
        sections.append(sec)
        return sec

    def append_content(line: str) -> None:
        if not line or cur_sec is None:
            return
        if cur_sub is not None:
            cur_sub["lines"].append(line)
        else:
            cur_sec["intro_lines"].append(line)

    for child in article.children:
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if name == top_tag:
            heading = clean_text(child.get_text(" ", strip=False))
            if not heading or heading.lower() == "mục lục":
                continue
            cur_sec = ensure_section(heading)
            cur_sub = None
        elif name == sub_tag:
            sub_heading = clean_text(child.get_text(" ", strip=False))
            if not sub_heading:
                continue
            if cur_sec is None:
                cur_sec = ensure_section("TỔNG QUAN")
            cur_sub = {"heading": sub_heading, "lines": []}
            cur_sec["subsections"].append(cur_sub)
        elif name == "table":
            rows = child.find_all("tr")
            first_text = clean_text(child.get_text(" ", strip=False))
            # Garena hay bọc tiêu đề mục lớn (CÂN BẰNG TƯỚNG / ĐIỀU CHỈNH CHIẾN TRƯỜNG / SỬA LỖI...) trong table 1x1
            if len(rows) == 1 and len(first_text) <= 80 and (
                child.find(["h1", "h2", "strong", "b"]) or first_text.isupper()
            ):
                if first_text and not first_text.lower().startswith("mục lục"):
                    cur_sec = ensure_section(first_text)
                    cur_sub = None
                continue
            md = table_to_markdown(child)
            if md:
                append_content(md)
        elif name in {"ul", "ol"}:
            for li in child.find_all("li", recursive=False):
                txt = clean_text(li.get_text(" ", strip=False))
                if txt:
                    append_content(f"- {txt}")
        elif name in {"p", "div", "blockquote"}:
            # Skip TOC/empty image-only paragraphs
            nested_table = child.find("table")
            if nested_table:
                md = table_to_markdown(nested_table)
                if md:
                    append_content(md)
                continue
            txt = clean_text(child.get_text(" ", strip=False))
            if txt and txt.upper() != "MỤC LỤC":
                append_content(txt)

    return sections


def scrape_patches(
    max_pages: int = 6,
    max_patches: int = 10,
    delay: float = 0.5,
    refresh: bool = False,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        for page_num in range(1, max_pages + 1):
            page_url = UPDATES_URL if page_num == 1 else f"{UPDATES_URL}page/{page_num}/"
            try:
                html = fetcher.fetch_html(page_url, f"updates_page_{page_num}")
            except httpx.HTTPStatusError:
                break

            soup = BeautifulSoup(html, "lxml")
            posts = soup.select("a.p-news__post")
            if not posts:
                break

            for a in posts:
                href = urljoin(BASE_URL, a.get("href", ""))
                if not href or href in seen_urls:
                    continue
                seen_urls.add(href)

                title_el = a.select_one("h2.p-news__post--title")
                date_el = a.select_one("div.p-news__post--date")
                desc_el = a.select_one("p.p-news__post--desc")
                cats = [clean_text(s.get_text()) for s in a.select("div.p-news__post--cats span")]

                title = clean_text(title_el.get_text()) if title_el else clean_text(a.get("title"))
                candidates.append(
                    {
                        "slug": url_last_segment(href),
                        "title": title,
                        "url": href,
                        "published_date": clean_text(date_el.get_text()) if date_el else "",
                        "categories": cats,
                        "excerpt": clean_text(desc_el.get_text()) if desc_el else "",
                        "is_balance_patch": is_balance_patch_title(title),
                    }
                )

        patches: list[dict[str, Any]] = []
        selected = [c for c in candidates if c["is_balance_patch"]][:max_patches]
        for idx, post in enumerate(selected, 1):
            print(f"  [patches {idx}/{len(selected)}] {post['published_date']} | {post['title']}")
            art_html = fetcher.fetch_html(post["url"], f"patches/{post['slug']}")
            sections = parse_patch_article(art_html)
            gameplay_sections = [s for s in sections if s["is_gameplay_relevant"]]
            post["sections"] = sections
            post["gameplay_section_count"] = len(gameplay_sections)
            patches.append(post)

    payload = {
        "source_url": UPDATES_URL,
        "scraped_at": utc_now_iso(),
        "scanned_pages": max_pages,
        "total_posts_scanned": len(candidates),
        "patch_count": len(patches),
        "skipped_non_balance_titles": [c["title"] for c in candidates if not c["is_balance_patch"]],
        "patches": patches,
    }
    write_json(RAW_DATA_DIR / "patches.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV balance patch notes.")
    parser.add_argument("--pages", type=int, default=6)
    parser.add_argument("--max-patches", type=int, default=10)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    res = scrape_patches(
        max_pages=args.pages,
        max_patches=args.max_patches,
        delay=args.delay,
        refresh=args.refresh,
    )
    print(f"Saved {res['patch_count']} balance patches to data/raw_official/patches.json")