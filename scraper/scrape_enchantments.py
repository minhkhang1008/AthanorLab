#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from typing import Any

from bs4 import BeautifulSoup

from scraper.common import (
    BASE_URL,
    RAW_DATA_DIR,
    PoliteFetcher,
    clean_text,
    extract_block_lines,
    slugify_vi,
    utc_now_iso,
    write_json,
)

ENCHANTMENTS_URL = f"{BASE_URL}/hoc-vien/phu-hieu/"


def scrape_enchantments(delay: float = 0.5, refresh: bool = False) -> dict[str, Any]:
    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        html = fetcher.fetch_html(ENCHANTMENTS_URL, "enchantments")

    soup = BeautifulSoup(html, "lxml")
    factions: list[dict[str, Any]] = []
    total_skills = 0

    for item in soup.select("div.st-badges__item"):
        faction_id = item.get("id") or ""
        name_el = item.select_one("h2.st-badges__item--name")
        faction_name = clean_text(name_el.get_text()) if name_el else ""

        meta_lines = extract_block_lines(item.select_one("div.st-badges__item--content"))
        suitable_for = ""
        summary_parts: list[str] = []
        for line in meta_lines:
            if line.lower().startswith("thích hợp"):
                suitable_for = clean_text(re.sub(r"^thích hợp\s*:?\s*", "", line, flags=re.IGNORECASE))
            else:
                summary_parts.append(line)

        # Map skill DOM id -> tier (1, 2, 3) from <ul class="st-badges__item--skills"><li>
        tier_by_id: dict[str, int] = {}
        for tier_idx, li in enumerate(item.select("ul.st-badges__item--skills > li"), 1):
            for a in li.select("a[href^='#']"):
                tier_by_id[a["href"].lstrip("#")] = tier_idx

        skills: list[dict[str, Any]] = []
        for sk in item.select("div.st-badges__skill"):
            sk_id = sk.get("id") or ""
            tier = tier_by_id.get(sk_id)
            if tier is None:
                m = re.search(r"group(\d+)", sk_id)
                tier = int(m.group(1)) if m else 0

            tag_el = sk.select_one(".st-badges__skill--head h3")
            title_el = sk.select_one("h4.st-badges__skill--title")
            content_el = sk.select_one("article.st-badges__skill--content")
            img = sk.select_one(".st-badges__skill--head img")

            sk_name = clean_text(title_el.get_text()) if title_el else ""
            skills.append(
                {
                    "id": sk_id,
                    "slug": slugify_vi(sk_name),
                    "tier": tier,
                    "tag": clean_text(tag_el.get_text()) if tag_el else "",
                    "name": sk_name,
                    "description": "\n".join(extract_block_lines(content_el)),
                    "icon_url": img.get("src", "") if img else "",
                }
            )

        total_skills += len(skills)
        factions.append(
            {
                "faction_id": faction_id,
                "slug": slugify_vi(faction_name),
                "name": faction_name,
                "keyword": clean_text(item.get("data-keyword")),
                "suitable_for": suitable_for,
                "summary": " ".join(summary_parts),
                "skills": skills,
            }
        )

    payload = {
        "source_url": ENCHANTMENTS_URL,
        "scraped_at": utc_now_iso(),
        "faction_count": len(factions),
        "skill_count": total_skills,
        "factions": factions,
    }
    write_json(RAW_DATA_DIR / "enchantments.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV enchantments.")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    res = scrape_enchantments(delay=args.delay, refresh=args.refresh)
    print(
        f"Saved {res['faction_count']} factions / {res['skill_count']} skills "
        "to data/raw_official/enchantments.json"
    )