---
name: aov-data-lookup
description: Exact factual lookup for Arena of Valor (Lien Quan Mobile) from official Garena data. Use when the user asks about specific hero skills, disambiguating multi-class heroes (e.g. Flowborn Archer vs Mage), item prices/stats/passives, Tier-3 arcana, talents, enchantments, or verifying exact numbers. Do NOT use as the primary skill for ban/pick drafting, full match itemization, or gameplay strategy unless verifying facts.
---

# aov-data-lookup

Single source of truth for verifying Arena of Valor (Lien Quan Mobile) official data from `lienquan.garena.vn`.

## When to Use

- User asks what a hero's passive or skills do (including recent releases like Evita or dual-class heroes like Flowborn).
- User asks for an item's gold cost, stats, passive, active, or component pieces.
- User asks for Tier-3 arcana stats, talent cooldowns/effects, or enchantment faction trees.
- Another AoV coaching skill needs to verify an exact skill mechanic or item passive before making a recommendation.

## Steps

1. Identify the requested entity type (hero, item, arcana, talent, enchantment) and check `references/data_manifest.md` if version context is needed.
2. Load ONLY the minimal reference file required:
   - **Hero:** Open `references/heroes_index.md` first to find the exact `slug`, role shard path, and recent patch dates. Then open ONLY the matching shard file under `references/heroes/`. If the hero has a recent patch date, also check `references/patches_latest.md`.
   - **Item:** Open `references/items_tier3.md` for full items or `references/items_components.md` for Tier 1-2 pieces.
   - **Arcana:** Open `references/arcana_t3.md`.
   - **Talent:** Open `references/talents.md`.
   - **Enchantment:** Open `references/enchantments.md`.
   - **CLI / IDE Agents shortcut:** If shell execution is available, run `python skills/aov-data-lookup/scripts/query_aov.py <hero|item|patch> "<query>"` for instant filtered output.
3. Resolve data conflicts strictly: if `references/patches_latest.md` modifies a hero skill, item, or mechanic listed in the base Academy file, report the newest patch value and note the update date.
4. Answer concisely with exact names, gold prices, cooldowns, and mechanics.

## Gotchas

- **Dual-class heroes:** Flowborn exists as both `flowborn` (Xa thu) and `flowborn-2` (Phap su). Always clarify which variant or show both briefly when the user only says "Flowborn".
- **Missing client base stats:** Official Garena web pages omit exact level-1 base HP/Armor and some damage ratios. Never fabricate missing numbers; state clearly that the number is not yet captured from the in-game client.
- **No bulk loading:** Never load all hero shards at once for a single-hero query.
