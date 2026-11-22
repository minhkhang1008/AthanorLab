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

TALENTS_URL = f"{BASE_URL}/hoc-vien/phu-tro/"


def scrape_talents(delay: float = 0.5, refresh: bool = False) -> dict[str, Any]:
    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        html = fetcher.fetch_html(TALENTS_URL, "talents")

    soup = BeautifulSoup(html, "lxml")
    talents: list[dict[str, Any]] = []

    for el in soup.select("div.st-extra-skills__item"):
        name_el = el.select_one("h3.st-extra-skills__item--name")
        content_el = el.select_one("div.st-extra-skills__item--content")
        img = el.select_one(".st-extra-skills__item--img img")

        raw_name = clean_text(name_el.get_text()) if name_el else ""
        description = "\n".join(extract_block_lines(content_el))
        cd_match = re.search(r"(\d+)\s*(?:giây|s)?\s*hồi chiêu", description, flags=re.IGNORECASE)
        cooldown = int(cd_match.group(1)) if cd_match else None

        talents.append(
            {
                "slug": slugify_vi(raw_name),
                "name": raw_name,
                "keyword": clean_text(el.get("data-keyword")),
                "cooldown_seconds": cooldown,
                "description": description,
                "icon_url": img.get("src", "") if img else "",
            }
        )

    payload = {
        "source_url": TALENTS_URL,
        "scraped_at": utc_now_iso(),
        "count": len(talents),
        "talents": talents,
    }
    write_json(RAW_DATA_DIR / "talents.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV talents.")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    res = scrape_talents(delay=args.delay, refresh=args.refresh)
    print(f"Saved {res['count']} talents to data/raw_official/talents.json")