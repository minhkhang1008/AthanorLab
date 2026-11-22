#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from scraper.scrape_arcana import scrape_arcana
from scraper.scrape_enchantments import scrape_enchantments
from scraper.scrape_heroes import scrape_heroes
from scraper.scrape_items import scrape_items
from scraper.scrape_patches import scrape_patches
from scraper.scrape_talents import scrape_talents
from scraper.validator import validate_all


def main() -> None:
    parser = argparse.ArgumentParser(description="AthanorLab official data scraper pipeline.")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=["heroes", "items", "arcana", "talents", "enchantments", "patches"],
        default=["heroes", "items", "arcana", "talents", "enchantments", "patches"],
        help="Run only selected scrapers.",
    )
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between HTTP requests (seconds).")
    parser.add_argument("--refresh", action="store_true", help="Ignore HTML cache and re-download.")
    parser.add_argument("--hero-limit", type=int, default=None, help="Limit heroes for quick smoke test.")
    parser.add_argument("--patch-pages", type=int, default=6, help="Pages to scan on /cap-nhat/.")
    parser.add_argument("--max-patches", type=int, default=10, help="Max balance patches to save.")
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args()

    selected = set(args.only)

    if "items" in selected:
        print("\n[1/6] Scraping items...")
        res = scrape_items(delay=args.delay, refresh=args.refresh)
        print(f"  -> {res['count']} items saved.")

    if "arcana" in selected:
        print("\n[2/6] Scraping arcana...")
        res = scrape_arcana(delay=args.delay, refresh=args.refresh)
        print(f"  -> {res['count']} arcana saved ({res['tier3_count']} Tier III).")

    if "talents" in selected:
        print("\n[3/6] Scraping talents...")
        res = scrape_talents(delay=args.delay, refresh=args.refresh)
        print(f"  -> {res['count']} talents saved.")

    if "enchantments" in selected:
        print("\n[4/6] Scraping enchantments...")
        res = scrape_enchantments(delay=args.delay, refresh=args.refresh)
        print(f"  -> {res['faction_count']} factions / {res['skill_count']} skills saved.")

    if "patches" in selected:
        print("\n[5/6] Scraping balance patches...")
        res = scrape_patches(
            max_pages=args.patch_pages,
            max_patches=args.max_patches,
            delay=args.delay,
            refresh=args.refresh,
        )
        print(f"  -> {res['patch_count']} balance patches saved (scanned {res['total_posts_scanned']} posts).")

    if "heroes" in selected:
        print("\n[6/6] Scraping heroes...")
        res = scrape_heroes(delay=args.delay, refresh=args.refresh, limit=args.hero_limit)
        print(f"  -> {res['count']} heroes saved.")

    if not args.skip_validate:
        print("\n[Validate] Running Quality Gate...")
        errs, warns, manifest = validate_all()
        print(f"  -> Status: {manifest['status']} | Warnings: {len(warns)} | Errors: {len(errs)}")
        for w in warns[:10]:
            print(f"     [WARN] {w}")
        if errs:
            for e in errs[:15]:
                print(f"     [ERR]  {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()