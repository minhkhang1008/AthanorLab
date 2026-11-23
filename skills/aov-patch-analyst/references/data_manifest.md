# AthanorLab Data Manifest (Single Source of Truth)

- **Official Source:** `https://lienquan.garena.vn/hoc-vien/` & `/cap-nhat/`
- **Last Synced (UTC):** `2026-11-23T10:28:51.405537+00:00`
- **Latest Balance Patch:** ĐIỀU CHỈNH GIỮA MÙA PB VẾT NỨT THỜI KHÔNG – 17.11.2026 (`16.11.2026`)
- **Dataset Counts:** 130 heroes | 112 items (53 Tier 3) | 28 Tier-3 arcana | 9 talents | 4 enchantment factions (31 skills) | 10 balance patches
- **Enrichment Status:** 17/130 curated hero tactical profiles | 130 in-game screenshot stat profiles

## Conflict Resolution Rule
1. If a hero/item/battlefield mechanic in `patches_latest.md` conflicts with the base Academy entry (`heroes/*.md`, `items_tier3.md`), **ALWAYS trust `patches_latest.md`** (newest date wins).
2. If a base stat or skill ratio is not listed in the references, state clearly that it is not yet captured from the in-game client instead of guessing.
