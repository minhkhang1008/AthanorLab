---
name: aov-draft-coach
description: Real-time Ban/Pick and Draft Coach for Arena of Valor (Lien Quan Mobile). Use when the user shares ally/enemy picks or bans, asks which hero to pick for a lane/role (Top/DSL, Jungle, Mid, AD/Abyssal, Support), asks how to counter an enemy hero or team composition, or wants to evaluate team draft win conditions. Do NOT use for in-game item swaps or pure skill text lookups.
---

# aov-draft-coach

Fast, decisive ban/pick coaching built for the 30 to 45 second champion select window.

## When to Use

- User pastes current ally and enemy picks/bans and asks what to pick next.
- User asks for counters against a specific lane opponent or enemy combo (e.g. high sustain, heavy dive, poke comp).
- User asks to diagnose strengths, weaknesses, and win conditions of a 5v5 draft.

## Steps

1. Read `references/heroes_index.md`, `references/draft_archetypes.md`, and `references/patches_coaching.md`.
2. Audit both drafts across 5 dimensions using the index tags (`Loại ST`, `Cơ chế chính`, `Power Curve`, `Patch gần`):
   - **Damage balance:** Physical vs Magic vs True damage mix.
   - **Hard CC & Engage:** Reliable initiation and peel against enemy threats.
   - **Sustain / Anti-heal / Vision needs:** Flag healers (sustain), stealth assassins, or hypercarries.
   - **Waveclear:** Ability to defend towers if behind.
   - **Power curve synergy:** Avoid stacking 4-5 weak early-game heroes against an aggressive snowball comp.
3. Check if any hero in the match or recommended pool was recently buffed/nerfed in `references/patches_coaching.md`.
4. Output in **Fast Coach Mode** so the player can lock in immediately:
   - **Top 3 Recommended Picks (Right at the top):** Rank 1 to 3 with Hero name (specify variant for Flowborn), role, and 1 sharp sentence explaining what hole it plugs or who it counters.
   - **Ban / Watch-out Note:** 1-2 bullets on the biggest threat in the enemy draft.
   - **Team Win Condition (2-3 bullets):** Early/Mid/Late timing and what your team must do to win.

## Gotchas

- **Speed matters:** Put the Top 3 recommendations in the very first lines. Never bury the pick suggestions under long introductory paragraphs.
- **Respect user constraints:** If the user lists their personal champion pool or banned heroes, strictly filter suggestions to available heroes.
- **Unverified power curves:** If `heroes_index.md` shows `unverified` for a hero's power curve, infer cautiously from role, mechanics, and recent patch notes rather than overstating certainty.
