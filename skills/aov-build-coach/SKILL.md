---
name: aov-build-coach
description: Dynamic Itemization, Gold-Economy Adaptation, Arcana, Enchantment, and Talent Coach for Arena of Valor (Lien Quan Mobile). Use when the user asks how to build a hero, what item to buy next in a live match, how to adapt items when ahead or behind in gold, how to counter enemy healing/burst/tanks, late-game item swaps, or optimal Tier-3 arcana, enchantments, and talents.
---

# aov-build-coach

Context-aware build coach that adapts item orders to live matchups, gold difference, and late-game swaps.

## When to Use

- User asks for a full pre-game setup (6 items, Tier-3 arcana 30-slot split, enchantment tree, talent).
- User sends an **In-Game Shorthand** update (e.g. `Valhein | p8 | thot 1k5 | da co: ... | dich xanh: ...`) asking what to buy next.
- User asks how to counter enemy sustain, AP/AD burst, high armor, stealth, or heavy CC.
- User asks for minute 15+ full-build defensive swaps (Giap ho menh <-> Qua cau bang suong / Liem doat menh).

## Steps

1. Read `references/items_tier3.md`, `references/counter_items_matrix.md`, and `references/patches_coaching.md`.
2. Load additional references ONLY when needed:
   - Component buy order or early lane tech -> `references/items_components.md`
   - Arcana setup -> `references/arcana_t3.md`
   - Enchantment tree -> `references/enchantments.md`
   - Talent choice -> `references/talents.md`
3. Verify every recommended item's exact Vietnamese name, gold cost, price tier (`cheap`/`mid`/`expensive`), and passive in the reference files.
4. Apply the **Gold Economy Rule** from `references/counter_items_matrix.md`:
   - **Ahead (>1,000g lead):** Push tempo with damage/penetration spikes; if you are the sole carry, force an insurance defensive slot (slot 4-5) to protect shutdown gold.
   - **Even (+-500g):** Follow core power spike order; optionally weave 1 high-value Tier 1-2 counter component.
   - **Behind (>1,000g deficit):** Avoid greedy `expensive` (>2300g) luxury items without a defensive/utility base. Pivot to `cheap`/`mid` utility, anti-heal, or survival items to stay useful for the strongest ally.
5. Format output by scenario:
   - **In-Game Shorthand (Live Match - Ultra-Concise):**
     1. **Mua ngay mon tiep theo (+ manh uu tien):** Exact item, gold cost, and 1-line reason.
     2. **Luu y doi do / bao menh:** Next 1-2 slots or late-game swap plan.
     3. **1 cau chot loi choi 3 phut toi.**
   - **Pre-Game Full Build:**
     1. **Core (2-3 items)** + **Flex/Counter slots (2-3 items)** with exact triggers (e.g. swap X if enemy has Y) + **Late-game swap sequence**.
     2. **Bang ngoc Cap III (10 Do / 10 Tim / 10 Xanh)** using exact official names from `arcana_t3.md`.
     3. **Phu hieu (Nhanh chinh 3 tang + 2 nhanh phu)** & **Phu tro** with brief matchup condition.

## Gotchas

- **Verify item existence:** Garena removes, renames, and reworks items across seasons. Never recommend an item that is absent from `references/items_tier3.md` or `references/items_components.md`.
- **Anti-heal timing:** Against strong healers (Helen, Taara, Ming, Florentino, Lauriel), remind the player to buy the anti-heal component early instead of waiting until slot 5.
- **No static 6-item dumps:** Always separate mandatory Core items from situational Flex/Counter items.
