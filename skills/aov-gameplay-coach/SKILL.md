---
name: aov-gameplay-coach
description: Micro/Macro Gameplay, Laning Matchup, Combo, Jungle Pathing, and Teamfight Coach for Arena of Valor (Lien Quan Mobile). Use when the user asks how to play a specific hero, optimal skill combos, 1v1 lane matchups, early/mid/late gameplan, jungle rotation, objective control, or how to play from behind or snowball a lead.
---

# aov-gameplay-coach

Practical micro and macro coaching anchored in exact official skill mechanics, item thresholds, and gold-driven game states.

## When to Use

- User asks how to play a hero, including skill order, passive management, and practical combos.
- User asks how to play a specific lane matchup (Hero A vs Hero B) during laning and mid-game rotations.
- User asks how to adjust gameplay based on power curve (early snowball vs late scaling) and gold lead/deficit.
- User asks how to position in 5v5 teamfights or contest Caesar/Dragon objectives.

## Steps

1. Open `references/heroes_index.md` to locate the exact shard file(s) for the hero(es) mentioned and check for recent patch dates.
2. Open ONLY the relevant hero shard(s) under `references/heroes/` to read exact skill mechanics, plus `references/battlefield_rules.md` and `references/patches_coaching.md`.
3. Check whether the hero has a curated tactical profile (`Hồ sơ chiến thuật`) in its shard:
   - If curated: use its verified archetype power curve (`Early/Mid/Late`) and `Power Spikes` as the backbone.
   - If unverified: derive timing carefully from the actual skill text (base CC/utility vs multi-stat scaling) and note how build path shifts power timing (e.g. Valhein semi-tank snowball vs crit scaling).
4. Deliver an actionable coaching plan in 4 tight blocks:
   - **Core Mechanic & Combos:** 1-2 practical combos grounded strictly in the official skill descriptions (e.g. passive stacks, resets, terrain states).
   - **Phase Gameplan (Early: 0-1 item / Mid: 2-3 items / Late: 4-6 items):** Clear objective, power spike trigger, and risk tolerance for each phase based on item count and map state rather than rigid clock minutes.
   - **Matchup & Teamfight Positioning:** Key enemy cooldowns to track and target priority.
   - **Gold-State Adjustment:** 1 bullet if snowballing ahead in items vs 1 bullet if playing from behind.

## Gotchas

- **Verify reworked kits:** Always check `references/patches_coaching.md` for recent reworks (such as Butterfly's skill changes) before explaining combos, because the Academy page may lag behind the latest balance patch.
- **No rigid clock assumptions:** Judge Early/Mid/Late by completed items, tower state, and gold lead; a fed carry hitting 3 items early accelerates the match into Mid-Late tempo.
- **Concrete over generic:** Give specific cues ("hold Skill 2 stun until Nakroth commits his dash") instead of vague advice ("keep good positioning").
