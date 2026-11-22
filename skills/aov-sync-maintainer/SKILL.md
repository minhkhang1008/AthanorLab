---
name: aov-sync-maintainer
description: Maintainer runbook for AthanorLab data pipelines, tactical curation, and in-game stat ingestion. Use when the user wants to refresh official data from lienquan.garena.vn after a new patch, validate data integrity, record a real-match coaching correction into hero_profiles.json, ingest in-game client screenshot stats via Vision OCR, or recompile and distribute skill references.
---

# aov-sync-maintainer

Operational runbook for keeping AthanorLab synchronized with Garena patches and evolving human-curated coaching intelligence.

## When to Use

- Garena releases a new balance patch or hero and the user wants to sync `AthanorLab`.
- User wants to convert an in-game attribute/skill screenshot into `data/ingame_stats/<slug>.json`.
- User corrects an AI coaching judgment (e.g. hero power curve, archetype, matchup note) and asks to save it permanently into `data/tactical/hero_profiles.json`.
- User needs to verify data manifest status or check token budgets after recompiling.

## Steps

### Workflow A: Sync Official Website Data & Recompile Skills
1. Run full refresh scraper and validator:
   - `python -m scraper.run_all --refresh --delay 0.5`
2. Inspect `data/raw_official/manifest.json` to confirm `status == "passed"` and `error_count == 0`.
3. Run the compiler to update `data/compiled/` and distribute references into all 6 skills:
   - `python -m compiler.build_all`
4. Review `git diff data/raw_official/manifest.json data/compiled/patches_latest.md` to spot heroes whose tactical profiles in `data/tactical/hero_profiles.json` need re-review after buffs/nerfs/reworks.

### Workflow B: Ingest In-Game Screenshot Stats (Vision OCR -> JSON)
1. When the user uploads a client screenshot of a hero's attributes or skill detail panel, read ONLY the visible numbers accurately.
2. Output a clean JSON matching `data/ingame_stats/_example_richter.json` with `slug`, `captured_patch` (from `references/data_manifest.md`), `base_stats`, and `skill_overrides`.
3. Remind the user to save it as `data/ingame_stats/<slug>.json` and run `python -m compiler.build_all`.

### Workflow C: Human Coach Correction Loop
1. When the user provides real-match insight (power curve, archetype, power spikes, coach notes), generate the exact JSON patch for `data/tactical/hero_profiles.json` with `"curated": true`.
2. Never edit files inside `skills/*/references/` directly, because `compiler/build_all.py` overwrites them from `data/`.

## Gotchas

- **Single source of truth:** All manual edits belong strictly in `data/tactical/` or `data/ingame_stats/`, never inside `data/compiled/` or `skills/*/references/`.
- **Preserve curated work:** `compiler/bootstrap_tactical.py` is idempotent and preserves any hero entry with `"curated": true`.
