#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any

from bs4 import BeautifulSoup

from scraper.common import (
    BASE_URL,
    RAW_DATA_DIR,
    PoliteFetcher,
    clean_text,
    extract_block_lines,
    parse_select_map,
    slugify_vi,
    utc_now_iso,
    write_json,
)

ARCANA_URL = f"{BASE_URL}/hoc-vien/bang-ngoc/"
COLOR_NORM = {
    "NGỌC ĐỎ": "Đỏ",
    "NGỌC TÍM": "Tím",
    "NGỌC XANH": "Xanh",
}
LEVEL_NORM = {
    "NGỌC CẤP I": 1,
    "NGỌC CẤP II": 2,
    "NGỌC CẤP III": 3,
}


def scrape_arcana(delay: float = 0.5, refresh: bool = False) -> dict[str, Any]:
    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        html = fetcher.fetch_html(ARCANA_URL, "arcana")

    soup = BeautifulSoup(html, "lxml")
    type_map = parse_select_map(soup, "type")
    level_map = parse_select_map(soup, "level")

    arcana_list: list[dict[str, Any]] = []
    seen_slugs: dict[str, int] = {}

    for el in soup.select("div.st-runes__item"):
        name_el = el.select_one("h2.st-runes__item--name")
        name = clean_text(name_el.get_text()) if name_el else ""
        type_id = (el.get("data-type") or "").strip()
        level_id = (el.get("data-level") or "").strip()

        raw_color = type_map.get(type_id, f"Type-{type_id}")
        raw_level = level_map.get(level_id, f"Level-{level_id}")
        color = COLOR_NORM.get(raw_color.upper(), raw_color)
        tier = LEVEL_NORM.get(raw_level.upper(), 0)

        article = el.select_one("div.st-runes__item--content article")
        stats = extract_block_lines(article)
        img = el.select_one(".st-runes__item--img img")

        base_slug = slugify_vi(name)
        seen_slugs[base_slug] = seen_slugs.get(base_slug, 0) + 1
        slug = base_slug if seen_slugs[base_slug] == 1 else f"{base_slug}-{seen_slugs[base_slug]}"

        arcana_list.append(
            {
                "slug": slug,
                "name": name,
                "keyword": clean_text(el.get("data-keyword")),
                "color": color,
                "tier": tier,
                "stats": stats,
                "icon_url": img.get("src", "") if img else "",
            }
        )

    payload = {
        "source_url": ARCANA_URL,
        "scraped_at": utc_now_iso(),
        "type_map": type_map,
        "level_map": level_map,
        "count": len(arcana_list),
        "tier3_count": sum(1 for a in arcana_list if a["tier"] == 3),
        "arcana": arcana_list,
    }
    write_json(RAW_DATA_DIR / "arcana.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV arcana.")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    res = scrape_arcana(delay=args.delay, refresh=args.refresh)
    print(f"Saved {res['count']} arcana ({res['tier3_count']} Tier III) to data/raw_official/arcana.json")