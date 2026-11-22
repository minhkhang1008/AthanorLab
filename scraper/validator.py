#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from scraper.common import RAW_DATA_DIR, sha256_json, utc_now_iso, write_json

HTML_TAG_RE = re.compile(r"</?(?:div|p|span|img|table|tr|td|br|strong|article)\b", re.IGNORECASE)


def load_json(name: str) -> dict[str, Any]:
    path = RAW_DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required dataset: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_no_html(text: str, ctx: str, errors: list[str]) -> None:
    if HTML_TAG_RE.search(text):
        errors.append(f"Raw HTML residue detected in {ctx}")


def validate_all() -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict[str, Any] = {}
    checksums: dict[str, str] = {}

    # 1. Heroes
    heroes_data = load_json("heroes.json")
    checksums["heroes.json"] = sha256_json(heroes_data["heroes"])
    heroes = heroes_data["heroes"]
    stats["heroes"] = len(heroes)
    if len(heroes) < 100:
        warnings.append(f"Hero count is {len(heroes)} (expected >= 120 unless --limit was used).")

    seen_display = set()
    for h in heroes:
        if h["display_name"] in seen_display:
            errors.append(f"Duplicate display_name not disambiguated: {h['display_name']}")
        seen_display.add(h["display_name"])

        if not h["roles"]:
            errors.append(f"Hero {h['slug']} has empty roles.")
        skills = h.get("skills", [])
        if len(skills) < 4:
            warnings.append(f"Hero {h['slug']} has only {len(skills)} skills (check manually).")
        for sk in skills:
            if not sk.get("description"):
                errors.append(f"Hero {h['slug']} skill {sk.get('slot')} missing description.")
            elif not sk.get("name"):
                warnings.append(
                    f"Hero {h['slug']} skill {sk.get('slot')} missing name on official site (description present)."
                )
            check_no_html(sk.get("description", ""), f"hero:{h['slug']}:{sk.get('slot')}", errors)

    # 2. Items
    items_data = load_json("items.json")
    checksums["items.json"] = sha256_json(items_data["items"])
    items = items_data["items"]
    tier3_items = [i for i in items if i["tier"] == 3]
    stats["items_total"] = len(items)
    stats["items_tier3"] = len(tier3_items)
    if len(items) < 90:
        errors.append(f"Too few items scraped: {len(items)}")
    for it in items:
        if not it["name"]:
            errors.append(f"Item with empty name: {it['slug']}")
        if it["tier"] == 3 and it["price"] <= 0:
            errors.append(f"Tier 3 item missing price: {it['name']}")
        if not it["raw_lines"]:
            warnings.append(f"Item has empty description lines: {it['name']}")
        for line in it["raw_lines"]:
            check_no_html(line, f"item:{it['slug']}", errors)

    # 3. Arcana
    arcana_data = load_json("arcana.json")
    checksums["arcana.json"] = sha256_json(arcana_data["arcana"])
    arcana = arcana_data["arcana"]
    tier3_arcana = [a for a in arcana if a["tier"] == 3]
    stats["arcana_total"] = len(arcana)
    stats["arcana_tier3"] = len(tier3_arcana)
    if len(tier3_arcana) < 25:
        errors.append(f"Too few Tier III arcana: {len(tier3_arcana)}")
    for r in arcana:
        if not r["stats"]:
            msg = f"Arcana missing stats on official site (Tier {r['tier']}): {r['name']}"
            if r["tier"] == 3:
                errors.append(msg)
            else:
                warnings.append(msg)

    # 4. Talents
    talents_data = load_json("talents.json")
    checksums["talents.json"] = sha256_json(talents_data["talents"])
    talents = talents_data["talents"]
    stats["talents"] = len(talents)
    if len(talents) < 8:
        errors.append(f"Too few talents scraped: {len(talents)}")
    for t in talents:
        if not t["description"]:
            errors.append(f"Talent missing description: {t['name']}")

    # 5. Enchantments
    ench_data = load_json("enchantments.json")
    checksums["enchantments.json"] = sha256_json(ench_data["factions"])
    factions = ench_data["factions"]
    stats["enchantment_factions"] = len(factions)
    stats["enchantment_skills"] = ench_data["skill_count"]
    if len(factions) != 4:
        errors.append(f"Expected 4 enchantment factions, got {len(factions)}")
    for f in factions:
        for sk in f["skills"]:
            if sk["tier"] not in {1, 2, 3}:
                errors.append(f"Enchantment skill {sk['name']} has invalid tier: {sk['tier']}")
            if not sk["description"]:
                errors.append(f"Enchantment skill missing description: {sk['name']}")

    # 6. Patches
    patches_data = load_json("patches.json")
    checksums["patches.json"] = sha256_json(patches_data["patches"])
    patches = patches_data["patches"]
    stats["patches"] = len(patches)
    stats["latest_patch"] = patches[0]["title"] if patches else None
    stats["latest_patch_date"] = patches[0]["published_date"] if patches else None
    if not patches:
        errors.append("No balance patches were extracted.")
    for p in patches:
        if p.get("gameplay_section_count", 0) == 0:
            warnings.append(f"Patch has 0 gameplay sections: {p['title']}")

    manifest = {
        "generated_at": utc_now_iso(),
        "status": "passed" if not errors else "failed",
        "stats": stats,
        "checksums": checksums,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }
    write_json(RAW_DATA_DIR / "manifest.json", manifest)
    return errors, warnings, manifest


if __name__ == "__main__":
    errs, warns, manifest = validate_all()
    print("=== AthanorLab Data Validation ===")
    print(json.dumps(manifest["stats"], ensure_ascii=False, indent=2))
    if warns:
        print(f"\nWarnings ({len(warns)}):")
        for w in warns[:20]:
            print(f"  [WARN] {w}")
    if errs:
        print(f"\nErrors ({len(errs)}):")
        for e in errs[:20]:
            print(f"  [ERR]  {e}")
        sys.exit(1)
    print("\nALL QUALITY GATES PASSED! Saved data/raw_official/manifest.json")