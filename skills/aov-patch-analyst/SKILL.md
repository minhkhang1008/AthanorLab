---
name: aov-patch-analyst
description: Official Patch Notes & Meta Shift Analyst for Arena of Valor (Lien Quan Mobile). Use when the user asks what changed in the latest update, whether a specific hero/item/battlefield mechanic was buffed, nerfed, or reworked recently, or how the current meta shifted according to lienquan.garena.vn/cap-nhat/.
---

# aov-patch-analyst

Distills official Garena balance patch notes into crisp buff/nerf verdicts and meta implications.

## When to Use

- User asks "patch moi nhat sua gi?", "cap nhat vua roi co gi moi?", or asks about a specific date's patch.
- User asks whether a specific hero, item, or battlefield mechanic (Caesar, King Kong, minions, special talents) was buffed or nerfed recently.
- User wants a meta summary of winners and losers after a balance update.

## Steps

1. Read `references/data_manifest.md` and `references/patch_history_index.md` to confirm the exact latest patch title and date.
2. Read `references/patches_latest.md` for exact `old -> new` numbers and tables.
3. For every affected hero or mechanic, classify the net impact clearly:
   - **Buff / Nerf / Adjust (Rework)** with the exact key number changes (avoid copying filler text).
   - **Practical Impact (1 line):** How this changes power spike timing, build priority, or draft priority.
4. Group the response cleanly:
   - **Patch Header:** Exact patch title, published date, and official link.
   - **Hero Changes (Winners / Losers / Reworks)** in a compact Markdown table or scannable bullets.
   - **Battlefield / Item / System Changes** (if present in the patch).

## Gotchas

- **Zero hallucinated patch dates:** Only report patches present in `references/patches_latest.md` or `references/patch_history_index.md`.
- **Ignore event noise:** The compiler already strips event/skin sections; stay strictly focused on gameplay balance and meta impact.
