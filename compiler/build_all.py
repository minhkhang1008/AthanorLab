#!/usr/bin/env python3
"""
AthanorLab - Knowledge Compiler & Multi-Skill Distributor
Compiles data/raw_official + data/ingame_stats + data/tactical into token-efficient
Markdown references in data/compiled/ and syncs the exact subset into skills/*/references/.
"""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from compiler.bootstrap_tactical import bootstrap_hero_profiles, seed_static_tactical_files

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw_official"
INGAME_DIR = ROOT_DIR / "data" / "ingame_stats"
TACTICAL_DIR = ROOT_DIR / "data" / "tactical"
COMPILED_DIR = ROOT_DIR / "data" / "compiled"
SKILLS_DIR = ROOT_DIR / "skills"

ROLE_FILE_MAP = {
    "Đấu sĩ": "dau-si.md",
    "Đỡ đòn": "do-don.md",
    "Pháp sư": "phap-su.md",
    "Sát thủ": "sat-thu.md",
    "Trợ thủ": "tro-thu.md",
    "Xạ thủ": "xa-thu.md",
}

ITEM_FLAG_RULES: dict[str, tuple[str, ...]] = {
    "anti-heal": ("giảm hồi máu", "giảm 50% hồi máu", "giảm khả năng hồi phục", "trọng thương"),
    "magic-pen": ("xuyên giáp phép",),
    "armor-pen": ("xuyên giáp",),
    "save-revive": ("hồi sinh", "miễn sát thương", "bất tử", "không thể bị chọn", "lá chắn"),
    "slow": ("làm chậm",),
    "vision-cleanse": ("tầm nhìn", "hiện hình", "giải khống", "hóa giải"),
}

# Exact reference distribution per skill (keeps each skill lightweight and focused)
SKILL_REFERENCE_MATRIX: dict[str, list[str]] = {
    "aov-data-lookup": [
        "data_manifest.md",
        "heroes_index.md",
        "heroes",
        "items_tier3.md",
        "items_components.md",
        "arcana_t3.md",
        "talents.md",
        "enchantments.md",
        "patches_latest.md",
    ],
    "aov-draft-coach": [
        "data_manifest.md",
        "heroes_index.md",
        "draft_archetypes.md",
        "patches_coaching.md",
    ],
    "aov-build-coach": [
        "data_manifest.md",
        "items_tier3.md",
        "items_components.md",
        "arcana_t3.md",
        "talents.md",
        "enchantments.md",
        "counter_items_matrix.md",
        "patches_coaching.md",
    ],
    "aov-gameplay-coach": [
        "data_manifest.md",
        "heroes_index.md",
        "heroes",
        "battlefield_rules.md",
        "patches_coaching.md",
    ],
    "aov-patch-analyst": [
        "data_manifest.md",
        "patches_latest.md",
        "patch_history_index.md",
    ],
    "aov-sync-maintainer": [
        "data_manifest.md",
        "patch_history_index.md",
    ],
}


def norm_key(text: str) -> str:
    text = text.lower().strip().replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_ingame_stats() -> dict[str, dict[str, Any]]:
    stats_map: dict[str, dict[str, Any]] = {}
    if not INGAME_DIR.exists():
        return stats_map
    for f in INGAME_DIR.glob("*.json"):
        if f.name.startswith("_"):
            continue
        data = load_json(f)
        slug = data.get("slug") or f.stem
        stats_map[slug] = data
    return stats_map


def map_recent_hero_patches(patches: list[dict[str, Any]], heroes: list[dict[str, Any]], top_n: int = 5) -> dict[str, list[str]]:
    """Cross-reference recent balance patch headings with hero names."""
    name_to_slugs: dict[str, list[str]] = defaultdict(list)
    for h in heroes:
        name_to_slugs[norm_key(h["raw_name"])].append(h["slug"])
        name_to_slugs[norm_key(h["display_name"])].append(h["slug"])

    hero_patch_hits: dict[str, list[str]] = defaultdict(list)
    for p in patches[:top_n]:
        p_date = p.get("published_date") or p.get("slug", "")
        for sec in p.get("sections", []):
            if not sec.get("is_gameplay_relevant"):
                continue
            for sub in sec.get("subsections", []):
                sub_norm = norm_key(sub.get("heading", ""))
                for hero_key, slugs in name_to_slugs.items():
                    if hero_key and (sub_norm == hero_key or sub_norm.startswith(hero_key + " ")):
                        for sl in slugs:
                            if p_date not in hero_patch_hits[sl]:
                                hero_patch_hits[sl].append(p_date)
    return hero_patch_hits


def detect_item_flags(item: dict[str, Any]) -> list[str]:
    text = " ".join(item.get("raw_lines", [])).lower()
    flags: list[str] = []
    for flag, kws in ITEM_FLAG_RULES.items():
        if flag == "armor-pen":
            # Avoid matching 'xuyên giáp phép' as armor-pen
            cleaned = text.replace("xuyên giáp phép", "")
            if any(kw in cleaned for kw in kws):
                flags.append(flag)
        elif any(kw in text for kw in kws):
            flags.append(flag)
    return flags


def format_power_curve(profile: dict[str, Any]) -> str:
    if not profile.get("curated"):
        return "unverified"
    curves = []
    for arch in profile.get("archetypes", []):
        pc = arch.get("power_curve")
        if isinstance(pc, dict):
            e, m, l = pc.get("early", "?"), pc.get("mid", "?"), pc.get("late", "?")
            curves.append(f"{arch['name']}: E{e}/M{m}/L{l}")
    return "; ".join(curves) if curves else "curated"


def build_manifest_md(manifest: dict[str, Any], ingame_count: int, curated_count: int) -> str:
    st = manifest["stats"]
    return (
        "# AthanorLab Data Manifest (Single Source of Truth)\n\n"
        f"- **Official Source:** `https://lienquan.garena.vn/hoc-vien/` & `/cap-nhat/`\n"
        f"- **Last Synced (UTC):** `{manifest['generated_at']}`\n"
        f"- **Latest Balance Patch:** {st.get('latest_patch')} (`{st.get('latest_patch_date')}`)\n"
        f"- **Dataset Counts:** {st['heroes']} heroes | {st['items_total']} items ({st['items_tier3']} Tier 3) | "
        f"{st['arcana_tier3']} Tier-3 arcana | {st['talents']} talents | "
        f"{st['enchantment_factions']} enchantment factions ({st['enchantment_skills']} skills) | "
        f"{st['patches']} balance patches\n"
        f"- **Enrichment Status:** {curated_count}/{st['heroes']} curated hero tactical profiles | "
        f"{ingame_count} in-game screenshot stat profiles\n\n"
        "## Conflict Resolution Rule\n"
        "1. If a hero/item/battlefield mechanic in `patches_latest.md` conflicts with the base Academy entry (`heroes/*.md`, `items_tier3.md`), **ALWAYS trust `patches_latest.md`** (newest date wins).\n"
        "2. If a base stat or skill ratio is not listed in the references, state clearly that it is not yet captured from the in-game client instead of guessing.\n"
    )


def build_heroes_docs(
    heroes_data: dict[str, Any],
    profiles_data: dict[str, Any],
    ingame_map: dict[str, dict[str, Any]],
    hero_patch_hits: dict[str, list[str]],
) -> tuple[str, dict[str, str]]:
    profiles = profiles_data.get("profiles", {})
    heroes = sorted(heroes_data["heroes"], key=lambda x: x["display_name"].lower())

    index_lines = [
        "# Danh mục 130 Tướng Liên Quân Mobile (Compact Index)",
        "",
        "Dùng file này để lọc nhanh bể tướng theo vai trò, loại sát thương và cơ chế, sau đó mở đúng file shard trong `heroes/<file>` để đọc chi tiết kỹ năng.",
        "",
        "| Slug | Tướng | Vai trò | Loại ST | Cơ chế chính | Power Curve | Patch gần | Shard |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    shards: dict[str, list[str]] = defaultdict(list)

    for h in heroes:
        slug = h["slug"]
        prof = profiles.get(slug, {})
        primary_role = h["primary_role"]
        base_shard = ROLE_FILE_MAP.get(primary_role, "khac.md")
        if base_shard in {"dau-si.md", "phap-su.md"}:
            first_char = norm_key(h["display_name"])[:1] or "a"
            stem = base_shard[:-3]
            shard_file = f"{stem}-a-l.md" if first_char <= "l" else f"{stem}-m-z.md"
        else:
            shard_file = base_shard
        roles_str = "/".join(h["roles"])
        dmg_type = prof.get("damage_type", "Chưa rõ")
        mechanics = ", ".join(prof.get("auto_mechanics", [])) or "-"
        pc_str = format_power_curve(prof)
        patch_dates = ", ".join(hero_patch_hits.get(slug, [])) or "-"

        index_lines.append(
            f"| `{slug}` | **{h['display_name']}** | {roles_str} | {dmg_type} | {mechanics} | {pc_str} | {patch_dates} | `heroes/{shard_file}` |"
        )

        # Build detailed shard section
        ig = ingame_map.get(slug, {})
        skill_overrides = ig.get("skill_overrides", {})

        sec: list[str] = [
            f"## {h['display_name']} (`{slug}`)",
            f"- **Vai trò:** {roles_str} | **Loại ST:** {dmg_type} | **Chống chịu/Tầm:** {prof.get('durability_class', '-')} / {prof.get('range_class', '-')}",
            f"- **Cơ chế:** {mechanics}",
        ]
        if hero_patch_hits.get(slug):
            sec.append(
                f"- **Cảnh báo Patch gần đây:** Có chỉnh sửa ngày **{', '.join(hero_patch_hits[slug])}** -> kiểm tra `patches_latest.md`."
            )

        # In-game base stats if captured
        base_stats = ig.get("base_stats")
        if isinstance(base_stats, dict):
            non_null = [f"{k}: {v}" for k, v in base_stats.items() if v is not None]
            if non_null:
                sec.append(f"- **Chỉ số in-game ({ig.get('captured_patch', 'client')}):** " + " | ".join(non_null))

        # Curated tactical archetypes if available
        if prof.get("curated"):
            sec.append("- **Hồ sơ chiến thuật (Curated):**")
            for arch in prof.get("archetypes", []):
                pc = arch.get("power_curve")
                pc_txt = f"Early {pc.get('early')}/5 · Mid {pc.get('mid')}/5 · Late {pc.get('late')}/5" if isinstance(pc, dict) else ""
                spikes = ", ".join(arch.get("power_spikes", []))
                sec.append(f"  - **{arch['name']}** ({pc_txt}) | Power Spikes: {spikes}")
                for phase, plan in arch.get("gameplan_by_phase", {}).items():
                    sec.append(f"    - *{phase}:* {plan}")
        if prof.get("coach_notes"):
            sec.append(f"- **Ghi chú Coach:** {prof['coach_notes']}")

        sec.append("- **Kỹ năng (Official):**")
        for sk in h.get("skills", []):
            slot = sk["slot"]
            ov = skill_overrides.get(slot, {})
            sk_name = sk.get("name") or ov.get("name") or "(Chưa có tên trên web)"
            desc = sk.get("description", "").replace("\n", " ")
            sec.append(f"  - **{sk['slot_label']} - {sk_name}:** {desc}")
            if ov.get("ratios"):
                sec.append(f"    - *Hệ số in-game:* {ov['ratios']}")

        shards[shard_file].append("\n".join(sec))

    shard_outputs: dict[str, str] = {}
    role_by_file = {v: k for k, v in ROLE_FILE_MAP.items()}
    for filename, blocks in shards.items():
        role_title = role_by_file.get(filename, "Khác")
        header = f"# Chi tiết Tướng - Nhóm {role_title} ({len(blocks)} tướng)\n\n"
        shard_outputs[filename] = header + "\n\n---\n\n".join(blocks) + "\n"

    return "\n".join(index_lines) + "\n", shard_outputs


def build_items_docs(items_data: dict[str, Any]) -> tuple[str, str]:
    items = items_data["items"]
    tier3 = [i for i in items if i["tier"] == 3]
    comps = [i for i in items if i["tier"] in {1, 2}]

    def render_grouped(title: str, subset: list[dict[str, Any]]) -> str:
        by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for it in subset:
            by_cat[it["category"]].append(it)

        lines = [f"# {title} ({len(subset)} món)", ""]
        for cat in sorted(by_cat.keys()):
            lines.append(f"## {cat}")
            for it in sorted(by_cat[cat], key=lambda x: (x["tier"], x["price"], x["name"])):
                stats_str = ", ".join(it["stats"]) if it["stats"] else "-"
                effects_str = " | ".join(it["effects"]) if it["effects"] else "-"
                flags = detect_item_flags(it)
                flag_str = f" `[{','.join(flags)}]`" if flags else ""
                lines.append(
                    f"- **{it['name']}** (`{it['price']}g` · {it['price_tier']}){flag_str}: "
                    f"Chỉ số: {stats_str}. Hiệu ứng: {effects_str}"
                )
            lines.append("")
        return "\n".join(lines)

    return (
        render_grouped("Trang bị Cấp 3 (Full Items)", tier3),
        render_grouped("Trang bị Mảnh Cấp 1 & Cấp 2 (Components)", comps),
    )


def build_arcana_t3_md(arcana_data: dict[str, Any]) -> str:
    t3 = [a for a in arcana_data["arcana"] if a["tier"] == 3]
    by_color: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for a in t3:
        by_color[a["color"]].append(a)

    lines = [f"# Bảng Ngọc Cấp III ({len(t3)} viên)", ""]
    for color in ("Đỏ", "Tím", "Xanh"):
        if color not in by_color:
            continue
        lines.append(f"## Ngọc {color}")
        for a in sorted(by_color[color], key=lambda x: x["name"]):
            lines.append(f"- **{a['name']}:** {' | '.join(a['stats'])}")
        lines.append("")
    return "\n".join(lines)


def build_talents_md(talents_data: dict[str, Any]) -> str:
    lines = [f"# Phép Phụ Trợ ({talents_data['count']} phép)", ""]
    for t in talents_data["talents"]:
        cd = f"{t['cooldown_seconds']}s" if t.get("cooldown_seconds") else "Xem mô tả"
        lines.append(f"- **{t['name']}** (Hồi chiêu: {cd}): {t['description']}")
    return "\n".join(lines) + "\n"


def build_enchantments_md(ench_data: dict[str, Any]) -> str:
    lines = [
        f"# Hệ thống Phù Hiệu ({ench_data['faction_count']} thế lực · {ench_data['skill_count']} kỹ năng)",
        "",
    ]
    for f in ench_data["factions"]:
        lines.append(f"## {f['name']}")
        if f.get("suitable_for"):
            lines.append(f"- **Thích hợp:** {f['suitable_for']}")
        if f.get("summary"):
            lines.append(f"- **Mô tả:** {f['summary']}")
        for tier in (1, 2, 3):
            tier_skills = [s for s in f["skills"] if s["tier"] == tier]
            if not tier_skills:
                continue
            lines.append(f"### Tầng {tier}")
            for sk in tier_skills:
                tag = f" [{sk['tag']}]" if sk.get("tag") else ""
                desc = sk["description"].replace("\n", " ")
                lines.append(f"- **{sk['name']}**{tag}: {desc}")
        lines.append("")
    return "\n".join(lines)


def build_patches_docs(patches_data: dict[str, Any], latest_n: int = 4) -> tuple[str, str]:
    patches = patches_data["patches"]

    # 1. Latest N patches (gameplay-relevant sections ONLY)
    latest_lines = [
        f"# Chi tiết {min(latest_n, len(patches))} Bản Cập nhật Cân bằng Gần nhất",
        "",
        "> Đã tự động lọc bỏ các mục SỰ KIỆN / MỞ BÁN. Xếp từ mới nhất đến cũ nhất.",
        "",
    ]
    for p in patches[:latest_n]:
        latest_lines.append(f"## {p['title']} (`{p['published_date']}`)")
        latest_lines.append(f"- **Nguồn:** {p['url']}")
        latest_lines.append("")
        for sec in p.get("sections", []):
            if not sec.get("is_gameplay_relevant"):
                continue
            latest_lines.append(f"### {sec['heading']}")
            for line in sec.get("intro_lines", []):
                latest_lines.append(line)
            for sub in sec.get("subsections", []):
                latest_lines.append(f"#### {sub['heading']}")
                for line in sub.get("lines", []):
                    latest_lines.append(line)
                latest_lines.append("")
        latest_lines.append("---\n")

    # 2. Patch history index (all scraped patches)
    hist_lines = [
        f"# Lịch sử Bản Cập nhật Cân bằng ({len(patches)} bài gần nhất)",
        "",
        "| Ngày đăng | Tiêu đề | Mục gameplay chính | Nguồn |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for p in patches:
        gp_heads = [
            f"{s['heading']} ({len(s.get('subsections', []))} mục)"
            for s in p.get("sections", [])
            if s.get("is_gameplay_relevant")
        ]
        hist_lines.append(
            f"| `{p['published_date']}` | **{p['title']}** | {'; '.join(gp_heads) or '-'} | {p['url']} |"
        )

    return "\n".join(latest_lines) + "\n", "\n".join(hist_lines) + "\n"


# Announcement-only subsections that are not balance changes (events, skins, promos).
EVENT_SUB_MARKERS: tuple[str, ...] = (
    "sự kiện",
    "trang phục",
    "hẹn gặp",
    "bình chọn",
    "hợp tác thương hiệu",
    "nhận thưởng",
    "mở bán",
    "ưu đãi",
)


def build_patches_coaching_md(patches_data: dict[str, Any], top_n: int = 2) -> str:
    """Compact patch digest for coaching skills: newest N patches, balance only."""
    patches = patches_data["patches"][:top_n]
    lines = [
        f"# Tóm tắt {len(patches)} Bản Cập nhật Cân bằng Mới nhất (Cho Coaching Thực chiến)",
        "",
        "> Chỉ giữ Cân bằng Tướng / Trang bị / Chiến trường / Phù hiệu / Phụ trợ. Đã lược mục Sửa lỗi & Sự kiện.",
        "",
    ]
    for p in patches:
        lines.append(f"## {p['title']} (`{p['published_date']}`)")
        for sec in p.get("sections", []):
            if not sec.get("is_gameplay_relevant"):
                continue
            if any(skip in sec["heading"].lower() for skip in ("sửa lỗi", "tối ưu")):
                continue
            lines.append(f"### {sec['heading']}")
            for line in sec.get("intro_lines", []):
                lines.append(line)
            for sub in sec.get("subsections", []):
                if any(marker in sub["heading"].lower() for marker in EVENT_SUB_MARKERS):
                    continue
                lines.append(f"#### {sub['heading']}")
                for line in sub.get("lines", []):
                    lines.append(line)
                lines.append("")
        lines.append("---\n")
    return "\n".join(lines) + "\n"


def approx_tokens(text: str) -> int:
    # Conservative estimate for Vietnamese Markdown (~3.2 chars/token)
    return max(1, int(len(text) / 3.2))


def sync_to_skills() -> dict[str, dict[str, int]]:
    skill_stats: dict[str, dict[str, int]] = {}
    for skill_name, refs in SKILL_REFERENCE_MATRIX.items():
        ref_dir = SKILLS_DIR / skill_name / "references"
        if ref_dir.exists():
            shutil.rmtree(ref_dir)
        ref_dir.mkdir(parents=True, exist_ok=True)

        total_chars = 0
        file_count = 0
        for rel in refs:
            src = COMPILED_DIR / rel
            dst = ref_dir / rel
            if not src.exists():
                continue
            if src.is_dir():
                shutil.copytree(src, dst)
                for f in dst.rglob("*.md"):
                    total_chars += len(f.read_text(encoding="utf-8"))
                    file_count += 1
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                total_chars += len(dst.read_text(encoding="utf-8"))
                file_count += 1

        skill_stats[skill_name] = {
            "files": file_count,
            "chars": total_chars,
            "approx_tokens_if_all_loaded": max(1, int(total_chars / 3.2)),
        }
    return skill_stats


def compile_all() -> None:
    # Ensure tactical layer exists and is synced with latest heroes
    seed_static_tactical_files()
    profiles_data = bootstrap_hero_profiles()

    manifest = load_json(RAW_DIR / "manifest.json")
    heroes_data = load_json(RAW_DIR / "heroes.json")
    items_data = load_json(RAW_DIR / "items.json")
    arcana_data = load_json(RAW_DIR / "arcana.json")
    talents_data = load_json(RAW_DIR / "talents.json")
    ench_data = load_json(RAW_DIR / "enchantments.json")
    patches_data = load_json(RAW_DIR / "patches.json")
    ingame_map = load_ingame_stats()

    hero_patch_hits = map_recent_hero_patches(patches_data["patches"], heroes_data["heroes"])

    if COMPILED_DIR.exists():
        shutil.rmtree(COMPILED_DIR)
    (COMPILED_DIR / "heroes").mkdir(parents=True, exist_ok=True)

    outputs: dict[Path, str] = {}
    outputs[COMPILED_DIR / "data_manifest.md"] = build_manifest_md(
        manifest, len(ingame_map), profiles_data.get("curated_count", 0)
    )

    heroes_idx_md, hero_shards = build_heroes_docs(heroes_data, profiles_data, ingame_map, hero_patch_hits)
    outputs[COMPILED_DIR / "heroes_index.md"] = heroes_idx_md
    for fname, content in hero_shards.items():
        outputs[COMPILED_DIR / "heroes" / fname] = content

    items_t3_md, items_comp_md = build_items_docs(items_data)
    outputs[COMPILED_DIR / "items_tier3.md"] = items_t3_md
    outputs[COMPILED_DIR / "items_components.md"] = items_comp_md
    outputs[COMPILED_DIR / "arcana_t3.md"] = build_arcana_t3_md(arcana_data)
    outputs[COMPILED_DIR / "talents.md"] = build_talents_md(talents_data)
    outputs[COMPILED_DIR / "enchantments.md"] = build_enchantments_md(ench_data)

    patches_latest_md, patch_hist_md = build_patches_docs(patches_data, latest_n=4)
    outputs[COMPILED_DIR / "patches_latest.md"] = patches_latest_md
    outputs[COMPILED_DIR / "patch_history_index.md"] = patch_hist_md
    outputs[COMPILED_DIR / "patches_coaching.md"] = build_patches_coaching_md(patches_data, top_n=2)

    # Copy curated static tactical guides into compiled/
    for static_name in ("counter_items_matrix.md", "draft_archetypes.md", "battlefield_rules.md"):
        src = TACTICAL_DIR / static_name
        if src.exists():
            outputs[COMPILED_DIR / static_name] = src.read_text(encoding="utf-8")

    print("=== Compiled Reference Token Report ===")
    report_rows: list[dict[str, Any]] = []
    for path, text in sorted(outputs.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        rel = str(path.relative_to(COMPILED_DIR))
        toks = approx_tokens(text)
        report_rows.append({"file": rel, "chars": len(text), "approx_tokens": toks})
        print(f"  - {rel:<28} {len(text):>7,} chars  (~{toks:>6,} tokens)")

    skill_stats = sync_to_skills()
    print("\n=== Synced Skill Packages (Progressive Disclosure) ===")
    for sk_name, st in skill_stats.items():
        print(
            f"  - {sk_name:<22} {st['files']:>2} files | "
            f"max ~{st['approx_tokens_if_all_loaded']:>6,} tokens (on-demand per file)"
        )

    build_report = {
        "compiled_files": report_rows,
        "skill_packages": skill_stats,
    }
    (COMPILED_DIR / "_build_report.json").write_text(
        json.dumps(build_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("\nDone! Compiled references synced into skills/*/references/.")


if __name__ == "__main__":
    compile_all()