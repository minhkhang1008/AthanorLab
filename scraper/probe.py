#!/usr/bin/env python3
"""
AthanorLab - Phase 1 Technical Probe
Inspects lienquan.garena.vn DOM, WordPress REST APIs, Sitemaps, and JS/AJAX endpoints.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://lienquan.garena.vn"
ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT_DIR / "cache" / "probe_html"
PROBE_DIR = ROOT_DIR / "probes"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

TARGET_PAGES = {
    "heroes_list": f"{BASE_URL}/hoc-vien/tuong-skin/",
    "hero_evita": f"{BASE_URL}/hoc-vien/tuong-skin/d/evita",
    "hero_flowborn_1": f"{BASE_URL}/hoc-vien/tuong-skin/d/flowborn",
    "hero_flowborn_2": f"{BASE_URL}/hoc-vien/tuong-skin/d/flowborn-2",
    "items": f"{BASE_URL}/hoc-vien/trang-bi/",
    "arcana": f"{BASE_URL}/hoc-vien/bang-ngoc/",
    "talents": f"{BASE_URL}/hoc-vien/phu-tro/",
    "enchantments": f"{BASE_URL}/hoc-vien/phu-hieu/",
    "updates": f"{BASE_URL}/cap-nhat/",
}

API_ENDPOINTS = {
    "sitemap_index": f"{BASE_URL}/sitemap_index.xml",
    "sitemap_xml": f"{BASE_URL}/sitemap.xml",
    "wp_types": f"{BASE_URL}/wp-json/wp/v2/types",
    "wp_categories": f"{BASE_URL}/wp-json/wp/v2/categories?per_page=50",
    "wp_posts_sample": f"{BASE_URL}/wp-json/wp/v2/posts?per_page=5",
}


def clean_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def truncate(text: str, limit: int = 1200) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... [TRUNCATED]"


def fetch_url(client: httpx.Client, url: str, delay: float) -> dict[str, Any]:
    time.sleep(delay)
    try:
        resp = client.get(url, follow_redirects=True)
        cf_headers = {
            k: v
            for k, v in resp.headers.items()
            if k.lower() in {"server", "cf-ray", "cf-cache-status", "content-type", "x-powered-by"}
        }
        blocked_hint = any(
            marker in resp.text.lower()
            for marker in ("cf-browser-verification", "just a moment...", "challenge-platform")
        )
        return {
            "ok": resp.status_code == 200 and not blocked_hint,
            "status_code": resp.status_code,
            "final_url": str(resp.url),
            "bytes": len(resp.content),
            "headers": cf_headers,
            "blocked_hint": blocked_hint,
            "text": resp.text,
            "error": None,
        }
    except Exception as exc:
        return {
            "ok": False,
            "status_code": None,
            "final_url": url,
            "bytes": 0,
            "headers": {},
            "blocked_hint": False,
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def find_script_hints(soup: BeautifulSoup) -> dict[str, Any]:
    """Detect inline JSON datasets, AJAX endpoints, or REST calls embedded in scripts."""
    ajax_hits: list[str] = []
    json_var_hits: list[str] = []
    external_scripts: list[str] = []

    for sc in soup.find_all("script"):
        src = sc.get("src")
        if src:
            if "lienquan.garena.vn" in src or src.startswith("/"):
                external_scripts.append(src)
            continue
        body = sc.string or sc.get_text() or ""
        if not body.strip():
            continue
        for pat in (
            r"https?://[^\s'\"`<>]+(?:wp-json|admin-ajax|api)[^\s'\"`<>]*",
            r"['\"](/wp-admin/admin-ajax\.php|/wp-json/[^'\"]+)['\"]",
            r"action['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_\-]+)['\"]",
        ):
            for m in re.findall(pat, body):
                val = m if isinstance(m, str) else " ".join(m)
                if val not in ajax_hits:
                    ajax_hits.append(val)
        for m in re.findall(
            r"(?:var|let|const|window\.)\s*([a-zA-Z0-9_$.]+)\s*=\s*(\[\s*\{|\{\s*['\"])",
            body,
        ):
            name = m[0]
            if name not in json_var_hits:
                json_var_hits.append(name)

    return {
        "site_scripts": external_scripts[:15],
        "ajax_or_api_hints": ajax_hits[:20],
        "inline_json_vars": json_var_hits[:15],
    }


def extract_top_classes(soup: BeautifulSoup, limit: int = 20) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    for tag in soup.find_all(True):
        classes = tag.get("class") or []
        for cls in classes:
            if len(cls) > 2:
                counter[f"{tag.name}.{cls}"] += 1
    return counter.most_common(limit)


def analyze_heroes_list(soup: BeautifulSoup) -> dict[str, Any]:
    hero_links: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(BASE_URL, a["href"])
        if "/hoc-vien/tuong-skin/d/" in href and href not in seen_urls:
            seen_urls.add(href)
            slug = urlparse(href).path.rstrip("/").split("/")[-1]
            parent_cls = " ".join(a.parent.get("class", [])) if isinstance(a.parent, Tag) else ""
            hero_links.append(
                {
                    "slug": slug,
                    "url": href,
                    "text": clean_ws(a.get_text(" ", strip=True)),
                    "a_class": " ".join(a.get("class", [])),
                    "parent_tag": a.parent.name if isinstance(a.parent, Tag) else "",
                    "parent_class": parent_cls,
                    "data_attrs": {k: v for k, v in a.attrs.items() if str(k).startswith("data-")},
                }
            )

    # Check duplicate display names (e.g. Flowborn variants)
    name_to_slugs: dict[str, list[str]] = {}
    for h in hero_links:
        if h["text"]:
            name_to_slugs.setdefault(h["text"], []).append(h["slug"])
    duplicates = {k: v for k, v in name_to_slugs.items() if len(v) > 1}

    # Grab sample card HTML
    sample_cards: list[str] = []
    for a in soup.find_all("a", href=re.compile(r"/hoc-vien/tuong-skin/d/"))[:2]:
        container = a.parent if isinstance(a.parent, Tag) else a
        sample_cards.append(truncate(container.prettify(), 1000))

    # Look for role filter elements
    filters = []
    for el in soup.select("[data-role], [data-type], [data-filter], [data-category], button, .filter, .tabs li"):
        txt = clean_ws(el.get_text(" ", strip=True))
        if txt and len(txt) <= 30:
            data_attrs = {k: v for k, v in el.attrs.items() if str(k).startswith("data-")}
            if data_attrs or any(w in txt.lower() for w in ("xạ thủ", "pháp sư", "sát thủ", "đấu sĩ", "đỡ đòn", "trợ thủ")):
                filters.append({"tag": el.name, "class": el.get("class", []), "text": txt, "data": data_attrs})

    return {
        "total_hero_links": len(hero_links),
        "sample_heroes": hero_links[:5],
        "duplicate_display_names": duplicates,
        "has_evita": any(h["slug"] == "evita" for h in hero_links),
        "flowborn_slugs": [h for h in hero_links if "flowborn" in h["slug"]],
        "role_filters": filters[:15],
        "sample_card_html": sample_cards,
    }


def analyze_hero_detail(soup: BeautifulSoup) -> dict[str, Any]:
    headings = [
        {"tag": h.name, "class": h.get("class", []), "text": clean_ws(h.get_text(" ", strip=True))}
        for h in soup.find_all(["h1", "h2", "h3", "h4"])
        if clean_ws(h.get_text())
    ]

    # Find sections likely describing skills
    skill_candidates = []
    for el in soup.find_all(["div", "section", "ul"]):
        cls = " ".join(el.get("class", [])).lower()
        el_id = (el.get("id") or "").lower()
        if any(k in cls or k in el_id for k in ("skill", "ki-nang", "ky-nang", "ability", "tab", "hero")):
            text = clean_ws(el.get_text(" ", strip=True))
            if 40 < len(text) < 4000:
                skill_candidates.append(
                    {
                        "selector": f"{el.name}#{el_id}.{'.'.join(el.get('class', []))}",
                        "text_preview": truncate(text, 350),
                        "html_preview": truncate(el.prettify(), 1200),
                    }
                )
    return {
        "title": clean_ws(soup.title.get_text()) if soup.title else "",
        "headings": headings[:20],
        "skill_block_candidates": skill_candidates[:5],
    }


def analyze_catalog_page(soup: BeautifulSoup, keywords: tuple[str, ...]) -> dict[str, Any]:
    """Generic analyzer for items, arcana, talents, enchantments."""
    candidates = []
    for el in soup.find_all(["div", "li", "article", "section"]):
        cls = " ".join(el.get("class", [])).lower()
        if any(k in cls for k in keywords):
            txt = clean_ws(el.get_text(" ", strip=True))
            if 20 < len(txt) < 1500:
                candidates.append(
                    {
                        "selector": f"{el.name}.{'.'.join(el.get('class', []))}",
                        "text_preview": truncate(txt, 250),
                        "html_preview": truncate(el.prettify(), 1100),
                    }
                )
        if len(candidates) >= 6:
            break

    # Check data-* attributes (often tooltips store stats in data-* or child tooltip divs)
    data_attr_samples = []
    for el in soup.find_all(True):
        d_attrs = {k: str(v)[:120] for k, v in el.attrs.items() if str(k).startswith("data-")}
        if len(d_attrs) >= 2:
            data_attr_samples.append(
                {
                    "tag": el.name,
                    "class": el.get("class", []),
                    "data_attrs": d_attrs,
                }
            )
        if len(data_attr_samples) >= 5:
            break

    # Look for price-like numbers (e.g. 2050, 2060, 710) or percentage stats
    body_text = clean_ws(soup.get_text(" ", strip=True))
    price_matches = re.findall(r"(?:giá|vàng)?\s*\b[12]\d{3}\b", body_text, flags=re.IGNORECASE)[:15]
    pct_matches = re.findall(r"[+\-]?\d+(?:[.,]\d+)?%", body_text)[:15]

    return {
        "title": clean_ws(soup.title.get_text()) if soup.title else "",
        "top_classes": extract_top_classes(soup, 15),
        "sample_items": candidates[:4],
        "data_attr_samples": data_attr_samples,
        "price_number_samples": price_matches,
        "percent_stat_samples": pct_matches,
    }


def analyze_updates_list(soup: BeautifulSoup) -> dict[str, Any]:
    articles = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(BASE_URL, a["href"])
        txt = clean_ws(a.get_text(" ", strip=True))
        if BASE_URL in href and len(txt) >= 15 and href not in seen:
            # Skip navigation links
            if any(skip in href for skip in ("/hoc-vien/", "/tai-game", "/nap-the")):
                continue
            seen.add(href)
            articles.append(
                {
                    "title": txt[:140],
                    "url": href,
                    "parent_class": " ".join(a.parent.get("class", [])) if isinstance(a.parent, Tag) else "",
                }
            )

    pagination = [
        {"text": clean_ws(a.get_text()), "href": urljoin(BASE_URL, a["href"])}
        for a in soup.select(".pagination a, .nav-links a, a.page-numbers, [class*='pag'] a")
        if a.get("href")
    ]

    return {
        "sample_articles": articles[:15],
        "pagination_links": pagination[:10],
        "top_classes": extract_top_classes(soup, 15),
    }


def analyze_patch_article(soup: BeautifulSoup) -> dict[str, Any]:
    content = (
        soup.select_one("article")
        or soup.select_one(".entry-content")
        or soup.select_one(".post-content")
        or soup.select_one("main")
        or soup.body
    )
    headings = []
    tables_count = 0
    arrow_lines = []
    if content:
        headings = [
            {"tag": h.name, "text": clean_ws(h.get_text(" ", strip=True))}
            for h in content.find_all(["h1", "h2", "h3", "h4", "strong"])
            if 3 < len(clean_ws(h.get_text())) < 100
        ][:25]
        tables_count = len(content.find_all("table"))
        raw_lines = [clean_ws(p.get_text(" ", strip=True)) for p in content.find_all(["p", "li", "tr"])]
        arrow_lines = [line for line in raw_lines if "→" in line or "->" in line or "Chỉnh" in line][:15]

    return {
        "content_container": (
            f"{content.name}.{'.'.join(content.get('class', []))}" if isinstance(content, Tag) else "none"
        ),
        "tables_count": tables_count,
        "headings_or_strong": headings,
        "balance_change_line_samples": arrow_lines,
    }


def probe_with_playwright(url: str) -> dict[str, Any]:
    """Optional fallback if static HTTP misses JS-rendered data or XHR calls."""
    from playwright.sync_api import sync_playwright

    xhr_urls: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=HEADERS["User-Agent"])
        page.on(
            "response",
            lambda r: xhr_urls.append(f"{r.status} {r.request.resource_type} {r.url}")
            if r.request.resource_type in {"xhr", "fetch"}
            else None,
        )
        page.goto(url, wait_until="networkidle", timeout=30000)
        html = page.content()
        browser.close()
    return {"bytes": len(html.encode("utf-8")), "xhr_fetch_calls": xhr_urls[:30], "html": html}


def render_markdown_summary(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# AthanorLab - Phase 1 Probe Summary",
        f"- **Generated (UTC):** `{report['generated_at']}`",
        "",
        "## 1. WordPress API & Sitemap Check",
        "| Endpoint | Status | Bytes | Note |",
        "| :--- | :---: | :---: | :--- |",
    ]
    for name, info in report["apis"].items():
        note = info.get("summary", info.get("error") or "")
        lines.append(f"| `{name}` | `{info['status_code']}` | `{info['bytes']}` | {note} |")

    lines += [
        "",
        "## 2. Target Pages Overview",
        "| Key | Status | Bytes | Blocked? | Server/CF Headers |",
        "| :--- | :---: | :---: | :---: | :--- |",
    ]
    for key, p in report["pages"].items():
        hdr = ", ".join(f"{k}={v}" for k, v in p["meta"]["headers"].items())
        lines.append(
            f"| `{key}` | `{p['meta']['status_code']}` | `{p['meta']['bytes']}` "
            f"| `{p['meta']['blocked_hint']}` | `{hdr}` |"
        )

    for key, p in report["pages"].items():
        lines += [
            "",
            f"## 3.{key} (`{p['meta']['final_url']}`)",
            "```json",
            truncate(json.dumps(p["analysis"], ensure_ascii=False, indent=2), 3500),
            "```",
            "**Script / AJAX Hints:**",
            "```json",
            truncate(json.dumps(p["scripts"], ensure_ascii=False, indent=2), 1200),
            "```",
        ]

    if report.get("sample_patch_article"):
        pa = report["sample_patch_article"]
        lines += [
            "",
            f"## 4. Sample Patch Article (`{pa['url']}`)",
            "```json",
            truncate(json.dumps(pa["analysis"], ensure_ascii=False, indent=2), 2500),
            "```",
        ]

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe lienquan.garena.vn structure for AthanorLab.")
    parser.add_argument("--delay", type=float, default=0.7, help="Seconds between HTTP requests.")
    parser.add_argument(
        "--playwright-url",
        type=str,
        default=None,
        help="Optional single URL to inspect with Playwright (captures XHR/fetch + rendered DOM).",
    )
    args = parser.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "apis": {},
        "pages": {},
        "sample_patch_article": None,
    }

    with httpx.Client(headers=HEADERS, timeout=25.0) as client:
        print("[1/3] Checking WordPress APIs & Sitemaps...")
        for name, url in API_ENDPOINTS.items():
            res = fetch_url(client, url, delay=args.delay)
            summary = ""
            parsed_preview: Any = None
            if res["ok"]:
                if "wp-json" in url:
                    try:
                        data = json.loads(res["text"])
                        if isinstance(data, dict):
                            keys = list(data.keys())[:15]
                            summary = f"JSON object keys: {keys}"
                            parsed_preview = keys
                        elif isinstance(data, list):
                            summary = f"JSON array len={len(data)}"
                            if data and isinstance(data[0], dict):
                                sample_keys = [
                                    item.get("slug") or item.get("name") or item.get("title", {}).get("rendered")
                                    for item in data[:8]
                                ]
                                summary += f" | samples: {sample_keys}"
                                parsed_preview = sample_keys
                    except Exception as exc:
                        summary = f"Non-JSON response ({exc})"
                else:
                    locs = re.findall(r"<loc>(.*?)</loc>", res["text"])[:10]
                    summary = f"XML <loc> count={len(locs)} | first={locs[:3]}"
                    parsed_preview = locs
            report["apis"][name] = {
                "url": url,
                "status_code": res["status_code"],
                "bytes": res["bytes"],
                "blocked_hint": res["blocked_hint"],
                "summary": summary,
                "preview": parsed_preview,
                "error": res["error"],
            }
            print(f"  - {name}: HTTP {res['status_code']} ({res['bytes']} bytes)")

        print("[2/3] Probing 6 Academy/Updates sections + sample heroes...")
        for key, url in TARGET_PAGES.items():
            res = fetch_url(client, url, delay=args.delay)
            html_path = CACHE_DIR / f"{key}.html"
            if res["text"]:
                html_path.write_text(res["text"], encoding="utf-8")

            soup = BeautifulSoup(res["text"], "lxml") if res["text"] else BeautifulSoup("", "lxml")
            if key == "heroes_list":
                analysis = analyze_heroes_list(soup)
            elif key.startswith("hero_"):
                analysis = analyze_hero_detail(soup)
            elif key == "items":
                analysis = analyze_catalog_page(soup, ("item", "equip", "trang-bi", "tooltip", "card", "box"))
            elif key == "arcana":
                analysis = analyze_catalog_page(soup, ("ngoc", "arcana", "rune", "tooltip", "item", "card"))
            elif key == "talents":
                analysis = analyze_catalog_page(soup, ("phu-tro", "talent", "spell", "skill", "item", "card"))
            elif key == "enchantments":
                analysis = analyze_catalog_page(soup, ("phu-hieu", "enchant", "rune", "nhanh", "item", "card"))
            elif key == "updates":
                analysis = analyze_updates_list(soup)
            else:
                analysis = {}

            report["pages"][key] = {
                "meta": {
                    "status_code": res["status_code"],
                    "final_url": res["final_url"],
                    "bytes": res["bytes"],
                    "blocked_hint": res["blocked_hint"],
                    "headers": res["headers"],
                    "error": res["error"],
                },
                "analysis": analysis,
                "scripts": find_script_hints(soup),
            }
            print(f"  - {key}: HTTP {res['status_code']} ({res['bytes']} bytes)")

        print("[3/3] Probing 1 sample balance patch article from /cap-nhat/...")
        updates_articles = report["pages"]["updates"]["analysis"].get("sample_articles", [])
        patch_candidate = next(
            (
                a
                for a in updates_articles
                if any(kw in a["title"].lower() for kw in ("điều chỉnh", "cân bằng", "cập nhật", "phiên bản"))
            ),
            updates_articles[0] if updates_articles else None,
        )
        if patch_candidate:
            res = fetch_url(client, patch_candidate["url"], delay=args.delay)
            if res["text"]:
                (CACHE_DIR / "sample_patch_article.html").write_text(res["text"], encoding="utf-8")
                soup = BeautifulSoup(res["text"], "lxml")
                report["sample_patch_article"] = {
                    "title": patch_candidate["title"],
                    "url": patch_candidate["url"],
                    "status_code": res["status_code"],
                    "analysis": analyze_patch_article(soup),
                }
                print(f"  - sample patch: {patch_candidate['title']} (HTTP {res['status_code']})")

    if args.playwright_url:
        print(f"[Extra] Running Playwright capture on {args.playwright_url}...")
        pw_res = probe_with_playwright(args.playwright_url)
        (CACHE_DIR / "playwright_capture.html").write_text(pw_res["html"], encoding="utf-8")
        report["playwright_capture"] = {
            "url": args.playwright_url,
            "bytes": pw_res["bytes"],
            "xhr_fetch_calls": pw_res["xhr_fetch_calls"],
        }

    json_out = PROBE_DIR / "probe_report.json"
    md_out = PROBE_DIR / "probe_summary.md"
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_out.write_text(render_markdown_summary(report), encoding="utf-8")

    print(f"\nDone!\n- Full JSON : {json_out}\n- Summary MD: {md_out}\n- Raw HTML  : {CACHE_DIR}")


if __name__ == "__main__":
    main()