#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scraper.common import (
    BASE_URL,
    RAW_DATA_DIR,
    PoliteFetcher,
    clean_text,
    extract_block_lines,
    url_last_segment,
    utc_now_iso,
    write_json,
)

HEROES_LIST_URL = f"{BASE_URL}/hoc-vien/tuong-skin/"
FALLBACK_ROLE_MAP = {
    28: "Đấu sĩ",
    29: "Pháp sư",
    30: "Trợ thủ",
    31: "Đỡ đòn",
    32: "Sát thủ",
    33: "Xạ thủ",
}
SKILL_SLOTS = ["passive", "skill_1", "skill_2", "ultimate"]
SKILL_LABELS = ["Nội tại", "Chiêu 1", "Chiêu 2", "Chiêu 3"]


def parse_role_map(soup: BeautifulSoup) -> dict[int, str]:
    role_map = dict(FALLBACK_ROLE_MAP)
    for a in soup.select("ul.st-heroes__types a[data-id]"):
        raw_id = (a.get("data-id") or "").strip()
        label = clean_text(a.get_text())
        if raw_id.isdigit() and label:
            role_map[int(raw_id)] = label
    return role_map


def parse_hero_skills(soup: BeautifulSoup) -> list[dict[str, Any]]:
    section = soup.select_one("section.hero__skills")
    if not section:
        return []

    icon_by_id: dict[str, str] = {}
    for a in section.select("ul.hero__skills--list a[href^='#']"):
        target_id = a["href"].lstrip("#")
        img = a.find("img")
        if img and img.get("src"):
            icon_by_id[target_id] = img["src"]

    skills: list[dict[str, Any]] = []
    for idx, detail in enumerate(section.select("div.hero__skills--detail")):
        el_id = detail.get("id") or f"heroSkill-{idx + 1}"
        h3 = detail.find("h3")
        article = detail.find("article")
        name = clean_text(h3.get_text()) if h3 else ""
        desc_lines = extract_block_lines(article)
        description = "\n".join(desc_lines)
        slot = SKILL_SLOTS[idx] if idx < len(SKILL_SLOTS) else f"extra_skill_{idx}"
        slot_label = SKILL_LABELS[idx] if idx < len(SKILL_LABELS) else f"Kỹ năng phụ {idx}"
        skills.append(
            {
                "slot": slot,
                "slot_label": slot_label,
                "name": name,
                "description": description,
                "icon_url": icon_by_id.get(el_id, ""),
            }
        )
    return skills


def scrape_heroes(delay: float = 0.5, refresh: bool = False, limit: int | None = None) -> dict[str, Any]:
    with PoliteFetcher(delay=delay, refresh=refresh) as fetcher:
        list_html = fetcher.fetch_html(HEROES_LIST_URL, "heroes_list")
        soup = BeautifulSoup(list_html, "lxml")
        role_map = parse_role_map(soup)

        cards: list[dict[str, Any]] = []
        seen_slugs: set[str] = set()
        for a in soup.select("a.st-heroes__item"):
            href = urljoin(BASE_URL, a.get("href", ""))
            slug = url_last_segment(href)
            if not slug or slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            raw_name = clean_text(
                (a.select_one("h2.st-heroes__item--name") or a).get_text()
            )
            raw_types = a.get("data-type") or ""
            role_ids = [int(x) for x in re.findall(r"\d+", raw_types)]
            roles = [role_map.get(rid, f"Role-{rid}") for rid in role_ids]

            img = a.select_one("img")
            cards.append(
                {
                    "slug": slug,
                    "raw_name": raw_name,
                    "url": href,
                    "keyword": clean_text(a.get("data-keyword")),
                    "role_ids": role_ids,
                    "roles": roles,
                    "primary_role": roles[0] if roles else "Chưa rõ",
                    "avatar_url": img.get("src", "") if img else "",
                }
            )

        # Disambiguate duplicate display names (e.g., Flowborn -> Flowborn (Xạ thủ) / Flowborn (Pháp sư))
        name_counts = Counter(c["raw_name"] for c in cards)
        for c in cards:
            if name_counts[c["raw_name"]] > 1:
                c["display_name"] = f"{c['raw_name']} ({c['primary_role']})"
            else:
                c["display_name"] = c["raw_name"]

        target_cards = cards[:limit] if limit else cards
        total = len(target_cards)
        heroes: list[dict[str, Any]] = []

        for idx, card in enumerate(target_cards, 1):
            print(f"  heroes {idx}/{total} -> {card['display_name']}")
            detail_html = fetcher.fetch_html(card["url"], f"heroes/{card['slug']}")
            detail_soup = BeautifulSoup(detail_html, "lxml")
            card["skills"] = parse_hero_skills(detail_soup)
            heroes.append(card)

    payload = {
        "source_url": HEROES_LIST_URL,
        "scraped_at": utc_now_iso(),
        "role_map": {str(k): v for k, v in role_map.items()},
        "count": len(heroes),
        "heroes": heroes,
    }
    write_json(RAW_DATA_DIR / "heroes.json", payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape AoV heroes and skills.")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--limit", type=int, default=None, help="Limit hero count for smoke testing.")
    args = parser.parse_args()
    res = scrape_heroes(delay=args.delay, refresh=args.refresh, limit=args.limit)
    print(f"Saved {res['count']} heroes to data/raw_official/heroes.json")