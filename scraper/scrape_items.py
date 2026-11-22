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
    parse_select_map,
    slugify_vi,
    utc_now_iso,
    write_json,
)

ITEMS_URL = f"{BASE_URL}/hoc-vien/trang-bi/"
TIER_NUM_MAP = {"Cấp 1": 1, "Cấp 2": 2, "Cấp 3": 3}
EFFECT_MARKERS = ("nội tại", "kích hoạt", "duy nhất", ":")


def split_stats_and_effects(lines: list[str]) -> tuple[list[str], list[str]]:
    stats: list[str] = []
    effects: list[str] = []
    for line in lines:
        low = line.lower()
        is_stat_line = line.startswith("+") and not any(m in low for m in EFFECT_MARKERS)
        if is_stat_line:
            # Handle lines like "+60 Công vật lý, +30% Tốc đánh, +900 Máu tối đa"
            parts = [clean_text(p) for p in re.split(r",\s*(?=\+)", line) if clean_text(p)]
            stats.extend(parts)
        else:
            effects.append(line)
    return stats, effects


def classify_price_tier(price: int, tier: int) -> str:
    if tier < 3:
        return "component"
    if price < 1950:
        return "cheap"
    if price <= 2250:
        return "mid"
    return "expensive"


def scrape_items(delay: float = 0.5, refresh: bool = False) -> dict[str, Any]:
    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        html = fetcher.fetch_html(ITEMS_URL, "items")

    soup = BeautifulSoup(html, "lxml")
    type_map = parse_select_map(soup, "type")
    level_map = parse_select_map(soup, "level")

    items: list[dict[str, Any]] = []
    seen_slugs: dict[str, int] = {}

    for el in soup.select("div.st-items__item"):
        name_el = el.select_one("h2.st-items__item--name")
        name = clean_text(name_el.get_text()) if name_el else ""
        type_id = (el.get("data-type") or "").strip()
        level_id = (el.get("data-level") or "").strip()
        category = type_map.get(type_id, f"Type-{type_id}")
        tier_label = level_map.get(level_id, f"Level-{level_id}")
        tier = TIER_NUM_MAP.get(tier_label, 0)

        content = el.select_one("div.st-items__item--content")
        price = 0
        raw_lines: list[str] = []
        if content:
            for p in content.find_all("p", recursive=False):
                m = re.search(r"\d+", clean_text(p.get_text()))
                if m:
                    price = int(m.group(0))
                    break
            raw_lines = extract_block_lines(content.find("article"))

        stats, effects = split_stats_and_effects(raw_lines)
        img = el.select_one(".st-items__item--img img")

        base_slug = slugify_vi(name)
        seen_slugs[base_slug] = seen_slugs.get(base_slug, 0) + 1
        slug = base_slug if seen_slugs[base_slug] == 1 else f"{base_slug}-{seen_slugs[base_slug]}"

        items.append(
            {
                "slug": slug,
                "name": name,
                "keyword": clean_text(el.get("data-keyword")),
                "category": category,
                "tier": tier,
                "tier_label": tier_label,
                "price": price,
                "price_tier": classify_price_tier(price, tier),
                "stats": stats,
                "effects": effects,
                "raw_lines": raw_lines,
                "icon_url": img.get("src", "") if img else "",
            }
        )

    payload = {
        "source_url": ITEMS_URL,
        "scraped_at": utc_now_iso(),
        "type_map": type_map,
        "level_map": level_map,
        "count": len(items),
        "items": items,
    }
    write_json(RAW_DATA_DIR / "items.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV items.")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    res = scrape_items(delay=args.delay, refresh=args.refresh)
    print(f"Saved {res['count']} items to data/raw_official/items.json")