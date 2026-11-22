# AthanorLab - Arena of Valor (Lien Quan Mobile) AI Coach

This repository packages verified official data from `https://lienquan.garena.vn/` and modular coaching knowledge into 6 cross-AI Agent Skills under `skills/`.

## Skill Routing Table

| User Intent | Primary Skill | Helper Skill (if needed) |
| :--- | :--- | :--- |
| Exact skill text, item price/passive, arcana, talent, enchantment | `skills/aov-data-lookup/SKILL.md` | `aov-patch-analyst` |
| Ban/pick suggestions, lane counters, 5v5 draft evaluation | `skills/aov-draft-coach/SKILL.md` | `aov-data-lookup` |
| Item builds, gold-economy adaptation, late-game swaps, arcana/enchantments | `skills/aov-build-coach/SKILL.md` | `aov-data-lookup` |
| Combos, lane matchups, early/mid/late macro, teamfight positioning | `skills/aov-gameplay-coach/SKILL.md` | `aov-build-coach` |
| Latest patch buff/nerf breakdown & meta shifts | `skills/aov-patch-analyst/SKILL.md` | `aov-data-lookup` |
| Scraping updates, screenshot OCR ingestion, saving tactical corrections | `skills/aov-sync-maintainer/SKILL.md` | - |

## Core Grounding Rules

1. **Patch overrides Academy:** Whenever `patches_latest.md` or `patches_coaching.md` conflicts with base Academy entries, the newest patch wins.
2. **Never fabricate client stats:** If level-1 HP/Armor or exact scaling ratios are not in `data/ingame_stats/` or patch notes, state that explicitly.
3. **Never hand-edit compiled references:** Edit `data/tactical/` or `data/ingame_stats/` and re-run `python -m compiler.build_all`.
