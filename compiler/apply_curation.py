#!/usr/bin/env python3
"""
AthanorLab - Tactical Curation Merger & Validator
Validates curated batch files in data/tactical/curated_batches/*.json against
data/raw_official/heroes.json, merges them into hero_profiles.json, and recompiles skills.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from compiler.build_all import compile_all

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_HEROES_PATH = ROOT_DIR / "data" / "raw_official" / "heroes.json"
PROFILES_PATH = ROOT_DIR / "data" / "tactical" / "hero_profiles.json"
BATCHES_DIR = ROOT_DIR / "data" / "tactical" / "curated_batches"

VALID_DURABILITY = {"squishy", "bruiser", "tank", "bruiser-or-squishy", "mixed"}
VALID_RANGE = {"melee", "short-ranged", "mid-ranged", "ranged", "long-ranged", "mixed"}


def validate_entry(entry: dict[str, Any], valid_slugs: set[str], source_file: str) -> list[str]:
    errs: list[str] = []
    slug = entry.get("slug")
    if not slug or slug not in valid_slugs:
        errs.append(f"[{source_file}] Unknown hero slug: '{slug}' (must match heroes.json exactly)")
        return errs

    if "durability_class" in entry and entry["durability_class"] not in VALID_DURABILITY:
        errs.append(f"[{source_file}] {slug}: invalid durability_class '{entry['durability_class']}'")
    if "range_class" in entry and entry["range_class"] not in VALID_RANGE:
        errs.append(f"[{source_file}] {slug}: invalid range_class '{entry['range_class']}'")

    archetypes = entry.get("archetypes")
    if not isinstance(archetypes, list) or not archetypes:
        errs.append(f"[{source_file}] {slug}: must define at least 1 archetype.")
        return errs

    for arch in archetypes:
        for req in ("id", "name", "power_curve", "power_spikes", "gameplan_by_phase"):
            if req not in arch:
                errs.append(f"[{source_file}] {slug}/{arch.get('id', '?')}: missing '{req}'")
        pc = arch.get("power_curve")
        if isinstance(pc, dict):
            for phase in ("early", "mid", "late"):
                val = pc.get(phase)
                if not isinstance(val, (int, float)) or not (1 <= val <= 5):
                    errs.append(f"[{source_file}] {slug}/{arch.get('id')}: invalid power_curve.{phase}={val}")
        else:
            errs.append(f"[{source_file}] {slug}/{arch.get('id')}: power_curve must be an object.")
    return errs


def apply_batches(skip_compile: bool = False) -> None:
    if not BATCHES_DIR.exists():
        print(f"No batch directory found at {BATCHES_DIR}")
        sys.exit(1)

    raw_heroes = json.loads(RAW_HEROES_PATH.read_text(encoding="utf-8"))["heroes"]
    valid_slugs = {h["slug"] for h in raw_heroes}

    profiles_doc = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    profiles: dict[str, Any] = profiles_doc["profiles"]

    batch_files = sorted(f for f in BATCHES_DIR.glob("*.json") if not f.name.startswith("_"))
    if not batch_files:
        print(f"No batch JSON files found in {BATCHES_DIR}")
        sys.exit(1)

    all_errors: list[str] = []
    merged_slugs: list[str] = []

    for bf in batch_files:
        batch = json.loads(bf.read_text(encoding="utf-8"))
        entries = batch if isinstance(batch, list) else batch.get("heroes", [])
        for entry in entries:
            errs = validate_entry(entry, valid_slugs, bf.name)
            if errs:
                all_errors.extend(errs)
                continue

            slug = entry["slug"]
            target = profiles[slug]
            for field in ("durability_class", "range_class", "damage_type_override", "coach_notes"):
                if field in entry and entry[field] is not None:
                    target[field] = entry[field]
            if entry.get("damage_type_override"):
                target["damage_type"] = entry["damage_type_override"]
            target["archetypes"] = entry["archetypes"]
            target["curated"] = True
            merged_slugs.append(slug)

    if all_errors:
        print("=== Curation Validation Failed ===")
        for e in all_errors:
            print(f"  [ERR] {e}")
        sys.exit(1)

    profiles_doc["curated_count"] = sum(1 for p in profiles.values() if p.get("curated"))
    PROFILES_PATH.write_text(json.dumps(profiles_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Merged {len(merged_slugs)} curated hero entries from {len(batch_files)} batch file(s). "
        f"Total curated: {profiles_doc['curated_count']}/{profiles_doc['total_heroes']}."
    )

    if not skip_compile:
        print("\nRecompiling skills...")
        compile_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply curated tactical hero batches and recompile.")
    parser.add_argument("--skip-compile", action="store_true")
    args = parser.parse_args()
    apply_batches(skip_compile=args.skip_compile)