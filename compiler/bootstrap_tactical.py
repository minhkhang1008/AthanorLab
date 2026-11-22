#!/usr/bin/env python3
"""
AthanorLab - Tactical Layer Bootstrapper
1. Derives verified mechanical tags & damage profile from official hero skill text.
2. Initializes/updates data/tactical/hero_profiles.json WITHOUT overwriting curated entries.
3. Seeds starter tactical guides (counter_items_matrix.md, draft_archetypes.md, battlefield_rules.md)
   and an in-game stats example schema if they don't exist yet.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw_official"
TACTICAL_DIR = ROOT_DIR / "data" / "tactical"
INGAME_DIR = ROOT_DIR / "data" / "ingame_stats"

MECHANIC_RULES: dict[str, tuple[str, ...]] = {
    "hard-cc": (
        "choáng", "hất tung", "áp chế", "đóng băng", "câm lặng",
        "trói", "khiêu khích", "hóa đá", "kéo", "đẩy lùi", "mê hoặc", "nhấc bổng",
    ),
    "slow": ("làm chậm",),
    "mobility": ("lướt", "dịch chuyển", "nhảy", "tốc biến", "tăng tốc chạy", "lao tới", "vọt tới"),
    "shield": ("lá chắn", "giáp ảo", "hộ thuẫn"),
    "sustain": ("hồi máu", "hồi phục", "hút máu"),
    "true-dmg": ("sát thương chuẩn", "st chuẩn"),
    "percent-hp": ("% máu tối đa", "% máu đã mất", "% máu hiện tại", "máu tối đa của kẻ địch"),
    "immune-untargetable": (
        "không thể bị chọn", "không bị chọn", "miễn nhiễm", "miễn khống", "bất tử", "miễn thương",
    ),
    "stealth": ("tàng hình", "ẩn thân"),
    "anti-heal": ("giảm hồi máu", "giảm khả năng hồi phục", "trọng thương"),
    "shred": ("giảm giáp", "xuyên giáp"),
    "reset": ("hồi lại ngay lập tức", "làm mới thời gian hồi", "đặt lại hồi chiêu"),
    "vision": ("tầm nhìn", "hiện hình", "soi sáng", "lộ diện"),
    "global-semi": ("toàn bản đồ", "khoảng cách rất xa", "từ xa bay tới"),
}

DEFAULT_DURABILITY_BY_ROLE = {
    "Đỡ đòn": "tank",
    "Đấu sĩ": "bruiser",
    "Trợ thủ": "bruiser-or-squishy",
    "Sát thủ": "squishy",
    "Pháp sư": "squishy",
    "Xạ thủ": "squishy",
}

DEFAULT_RANGE_BY_ROLE = {
    "Xạ thủ": "ranged",
    "Pháp sư": "ranged",
    "Đỡ đòn": "melee",
    "Đấu sĩ": "melee",
    "Sát thủ": "melee",
    "Trợ thủ": "mixed",
}


def detect_damage_type(full_text: str, primary_role: str) -> str:
    low = full_text.lower()
    has_phys = ("sát thương vật lý" in low) or ("stvl" in low) or ("công vật lý" in low)
    has_magic = ("sát thương phép" in low) or ("stp" in low) or ("công phép" in low)
    has_true = ("sát thương chuẩn" in low) or ("st chuẩn" in low)

    types: list[str] = []
    if has_phys:
        types.append("Vật lý")
    if has_magic:
        types.append("Phép")
    if has_true:
        types.append("Chuẩn")

    if not types:
        if primary_role == "Pháp sư":
            return "Phép"
        if primary_role in {"Xạ thủ", "Sát thủ", "Đấu sĩ"}:
            return "Vật lý"
        return "Hỗn hợp/Chưa rõ"
    return "/".join(types)


def extract_mechanics(hero: dict[str, Any]) -> list[str]:
    text = " ".join(
        f"{sk.get('name', '')} {sk.get('description', '')}" for sk in hero.get("skills", [])
    ).lower()
    tags = [tag for tag, keywords in MECHANIC_RULES.items() if any(kw in text for kw in keywords)]
    return tags


def seed_static_tactical_files() -> None:
    TACTICAL_DIR.mkdir(parents=True, exist_ok=True)
    INGAME_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Counter Items & Gold Economy Matrix
    counter_path = TACTICAL_DIR / "counter_items_matrix.md"
    if not counter_path.exists():
        counter_path.write_text(
            """# Ma trận Khắc chế Trang bị & Tư duy Kinh tế (Vàng)

> Nguyên tắc bắt buộc: Tên, giá vàng và thông số chính xác của từng món đồ phải luôn đối chiếu từ `items_tier3.md`, `items_components.md` và `patches_latest.md`.

## 1. Ma trận tình huống -> Nhóm trang bị / Phép xử lý
| Mối đe dọa từ đội địch | Giải pháp cho Vật lý (AD/Đấu sĩ/Sát thủ) | Giải pháp cho Phép (Mid) | Giải pháp cho Đỡ đòn / Trợ thủ | Phụ trợ / Phù hiệu cân nhắc |
| :--- | :--- | :--- | :--- | :--- |
| **Hồi máu / Hút máu mạnh** (Helen, Taara, Ming, Flo, Lauriel...) | Đao truy hồn (hoặc mua sớm mảnh giảm hồi máu) | Sách truy hồn | Đao/Sách truy hồn tùy chất ST, kết hợp Áo choàng thần Ra hoặc đồ cản hồi máu hiện hành | Thiêu đốt (nếu cần đè lane đầu) |
| **Sốc sát thương Phép / Cấu rỉa AP** | Huân chương Troy, Giáp Gaia, Kiếm Uriel (nếu tồn tại trong `items_tier3.md`), Giày kiên cường | Quả cầu băng sương, Huân chương Troy (khi quá thọt/bị bắt) | Huân chương Troy, Giáp Gaia, Giày kiên cường | Suy nhược, Quả cầu băng sương (Thành khởi nguyên) |
| **Sốc sát thương Vật lý / Sát thủ lao vào** | Giáp hộ mệnh, Liềm đoạt mệnh, Khiên thất truyền / Khiên huyền thoại | Quả cầu băng sương, Giáp hộ mệnh, Ngọc đại pháp sư (lấy máu) | Khiên thất truyền, Khiên huyền thoại, Giáp thống khổ, Giáp hộ mệnh | Suy nhược, Tốc biến, Quả cầu băng sương |
| **Địch nhiều Đỡ đòn / Giáp cao** | Thương Longinus / Thương xuyên phá (đầu-giữa), Muramasa / Diệt thần cung (giữa-cuối) | Trượng hỗn mang, Mặt nạ Berith (đốt theo % máu) | Giảm giáp/khống chế bảo kê chủ lực bắn | Ma chú / Luyện ngục tùy chất tướng |
| **Địch nhiều Khống chế cứng (Hard CC)** | Giày kiên cường (ưu tiên hàng đầu), Liềm/Giáp hộ mệnh | Giày kiên cường, Quả cầu băng sương | Giày kiên cường + Đồ trợ thủ giải khống chế (Mở trói/Thanh tẩy) | Thanh tẩy |
| **Địch tàng hình / Ẩn thân** (Ngộ Không, Quillen, Batman/Kaine, Elsu...) | Giữ vị trí sau Tank, mua sớm đồ phòng thủ chống 1 combo | Quả cầu băng sương sớm | Đồ trợ thủ soi tầm nhìn (Mắt/Nhẫn soi sáng) | Suy nhược / Tốc biến |
| **Địch nhiều Tốc đánh / Xạ thủ chí mạng** | Kiếm Fafnir (nếu cần tay đôi) + 1 món thủ cuối | Quả cầu băng sương | Khiên thất truyền (giảm tốc đánh), Giáp thống khổ (phản sát thương) | Suy nhược |

## 2. Ma trận Chuyển đổi Trang bị theo Chênh lệch Vàng
- **Đang Xanh (dẫn > 1.000 vàng so với đối vị):**
  - Ưu tiên đồ **khuếch đại sát thương / xuyên giáp sớm** để ép kết thúc trận đấu trước khi địch kịp lớn.
  - Nếu bản thân là **chủ lực duy nhất đang gánh team**: bắt buộc ưu tiên 1 món **bảo hiểm chuỗi mạng** (*Quả cầu băng sương*, *Giáp hộ mệnh*, *Huân chương Troy*) ở ô thứ 4–5 để tránh biếu tiền thưởng shut-down.
- **Cân bằng (±500 vàng):**
  - Đóng đúng lộ trình Power Spike của tướng. Chỉ kẹp **1 mảnh cấp 1–2 giá trị cao** (xuyên giáp nhỏ, giảm hồi máu nhỏ, kháng phép/giáp nhỏ) khi kèo đi đường thực sự cần.
- **Đang Thọt (kém > 1.000 vàng):**
  - **Không cố gom tiền cho trang bị xa xỉ (`expensive`, >2300g)** khi chưa có nền chống chịu/xuyên giáp cơ bản.
  - Chuyển sang các món **giá rẻ – trung bình (`cheap`/`mid`) giàu tiện ích/khắc chế** (giảm hồi máu, làm chậm, giảm hồi chiêu, phòng thủ) để sống sót lâu hơn trong giao tranh và tạo khoảng trống cho đồng đội xanh nhất gánh.

## 3. Nguyên tắc Đổi đồ Cuối trận (Phút 15+ / Full 6 món)
1. **Chuỗi đổi đồ bảo mệnh chuẩn:** Khi *Giáp hộ mệnh* đang hồi chiêu (hoặc đã dùng hết 2 lần) -> bán đổi ngay sang *Quả cầu băng sương* -> *Liềm đoạt mệnh* -> *Cung Tà Ma* (xạ thủ) hoặc *Nham thuẫn* (đấu sĩ/đỡ đòn).
2. **Đổi Giày siêu muộn:** Chỉ cân nhắc bán Giày đổi sang món sát thương/bảo mệnh thứ 6 khi tướng có độ cơ động sẵn hoặc đội hình đánh thủ nhà/giao tranh tại chỗ; không bán Giày khi phải thả diều liên tục.
""",
            encoding="utf-8",
        )

    # 2. Draft Archetypes & Ban/Pick Framework
    draft_path = TACTICAL_DIR / "draft_archetypes.md"
    if not draft_path.exists():
        draft_path.write_text(
            """# Khung Phân tích Cấm/Chọn (Draft Archetypes & Win Conditions)

## 1. Danh sách kiểm tra đội hình 5v5 chuẩn (Team Comp Checklist)
1. **Nguồn sát thương cân bằng:** Có đủ cả Sát thương Vật lý (AD) và Sát thương Phép (AP) để địch không thể lên thuần 1 loại giáp.
2. **Khống chế cứng (Hard CC):** Tối thiểu 2 nguồn khống chế đáng tin cậy để bắt chủ lực cơ động hoặc cắt chiêu địch.
3. **Dàn chắn & Mở giao tranh (Frontline / Engage):** Có ít nhất 1 tướng mở combat hoặc check bụi an toàn (Đỡ đòn / Đấu sĩ cứng).
4. **Dọn lính & Thủ trụ (Waveclear):** Pháp sư hoặc Xạ thủ phải dọn lính nhanh để không bị ép sập trụ khi thua thế.
5. **Nhịp độ sức mạnh (Power Curve Synergy):** Tránh chọn 4–5 tướng đều yếu đầu trận (`late-heavy`) dễ mất toàn bộ rừng trước phút 6; ngược lại nếu chọn đội hình `early-snowball` phải có chất tướng đẩy trụ nhanh.

## 2. Các kiểu đội hình phổ biến & Cách khắc chế
| Kiểu đội hình địch | Đặc điểm nhận diện | Cách chọn tướng khắc chế |
| :--- | :--- | :--- |
| **Cấu rỉa / Kiểm soát (Poke)** | Tầm chiêu xa, cấu máu trước giao tranh (Elsu, Yue, Liliana, Kahlii...) | Pick tướng **lao vào mở giao tranh mạnh (Hard Engage)**, sát thủ áp sát nhanh, hoặc Trợ thủ hồi máu/giáp ảo. |
| **Lao vào dồn sát thương (Dive / All-in)** | Nhiều sát thủ/đấu sĩ cơ động băng trụ (Nakroth, Paine, Krixi, Zuka...) | Pick tướng **phản công / bảo kê (Peel / Disengage)** có khống chế cứng tức thời, miễn thương hoặc làm gián đoạn combo. |
| **Nuôi chủ lực cuối trận (Protect Hypercarry)** | Xạ thủ/Pháp sư late cực mạnh + Trợ thủ buff (Yorn/Tel'Annas + Helen/Ming/Zip) | Pick đội hình **ép mạnh đầu trận (Early Snowball)**, sát thủ cắt tuyến sau, hoặc tướng gây sát thương diện rộng + cắt hồi máu. |
| **Đẩy lẻ / Bắt lẻ (Split-push / Pick-off)** | Cơ động cao, tay đôi 1v1 mạnh (Florentino, Omen, Nakroth, Airi...) | Pick tướng **mở giao tranh ép 5v4 nhanh** tại mục tiêu lớn, hoặc tướng dọn lính/giữ cánh cứng không bị solo kill. |
| **Giao tranh tổng (Wombo-Combo)** | Chiêu cuối diện rộng kết hợp khống chế chuỗi (Maloch, Lumburr, Dirak, Lorion...) | Pick tướng **cơ động tách đội hình**, Trợ thủ giải khống chế, hoặc ép đánh rải rác không chụm 5 người trong địa hình hẹp. |
""",
            encoding="utf-8",
        )

    # 3. Battlefield Macro Framework
    macro_path = TACTICAL_DIR / "battlefield_rules.md"
    if not macro_path.exists():
        macro_path.write_text(
            """# Khung Chiến thuật Bản đồ & Nhịp độ Trận đấu (Macro Framework)

> Lưu ý: Mọi thông số cụ thể về thời gian xuất hiện, chỉ số Caesar / King Kong / Lính / Phép phụ trợ đặc biệt theo mùa phải luôn lấy bản mới nhất từ `patches_latest.md`.

## 1. Ba giai đoạn trận đấu chuẩn
- **Đầu trận (0:00 – 4:00 | Laning & First Jungle Clear):**
  - Rừng hoàn thành vòng rừng đầu để chạm **Cấp 4** (~1:30) tạo pha gank đầu tiên.
  - Đường Giữa (Mid) ưu tiên đẩy lính nhanh lấy quyền kiểm soát sông và đảo cánh hỗ trợ Rừng/Rồng.
  - Xạ thủ/Đấu sĩ đánh đúng ngưỡng sức mạnh: tướng `Early` ép lính giành quyền kiểm soát bụi/tài nguyên; tướng `Late` giữ thế lính gần trụ, tuyệt đối tránh trao đổi 1v1 mạo hiểm.
- **Giữa trận (4:00 – 10:00 | Snowball & Objective Control):**
  - Cơ chế bảo vệ trụ giảm dần -> mở nhịp đẩy trụ ngoài (T1) ở hai cánh để giải phóng bản đồ.
  - Kiểm soát Rồng / Caesar nhỏ theo thế lính: **đẩy lính trước, kiểm soát bụi quanh hang trước, ăn mục tiêu sau**.
  - Nếu đang dẫn vàng: cướp bùa rừng địch theo cặp (Rừng + Trợ thủ/Mid), không đi lẻ mất shut-down.
  - Nếu đang thọt vàng: nhường 1 mục tiêu không thể tranh để đổi lấy trụ cánh đối diện hoặc kéo giãn thời gian cho chủ lực farm.
- **Cuối trận (10:00+ -> 15:00+ | Baron/Caesar Bạo Chúa & End Game):**
  - Một mạng hạ gục lẻ ở phút 12+ có thể mất thẳng ván đấu do thời gian đếm số dài.
  - Luôn đẩy cao ít nhất 2 đường lính trước khi mở giao tranh Caesar Bạo Chúa.
  - Chuẩn bị sẵn kịch bản **đổi đồ bảo mệnh** (Giáp hộ mệnh <-> Quả cầu băng sương / Liềm đoạt mệnh) trước giao tranh quyết định.
""",
            encoding="utf-8",
        )

    # 4. In-game stats example schema (for incremental Vision OCR ingestion)
    example_stats = INGAME_DIR / "_example_richter.json"
    if not example_stats.exists():
        example_stats.write_text(
            json.dumps(
                {
                    "_comment": (
                        "Rename to <slug>.json (e.g. richter.json) to inject verified in-game stats "
                        "captured from client screenshots. Files starting with '_' are ignored by compiler."
                    ),
                    "slug": "richter",
                    "captured_patch": "17.11.2026",
                    "source": "in-game client screenshot",
                    "base_stats": {
                        "hp_lv1": None,
                        "phys_atk_lv1": None,
                        "armor_lv1": None,
                        "magic_def_lv1": None,
                        "move_speed": None,
                        "attack_range": "melee",
                        "resource": "Không tốn năng lượng",
                    },
                    "skill_overrides": {
                        "skill_2": {
                            "name": "Công thủ toàn diện",
                            "notes": "Bổ sung tên chiêu bị bỏ trống trên web chính thức Garena.",
                        }
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )


def bootstrap_hero_profiles() -> dict[str, Any]:
    heroes_data = json.loads((RAW_DIR / "heroes.json").read_text(encoding="utf-8"))
    profiles_path = TACTICAL_DIR / "hero_profiles.json"

    existing: dict[str, Any] = {}
    if profiles_path.exists():
        loaded = json.loads(profiles_path.read_text(encoding="utf-8"))
        existing = loaded.get("profiles", {})

    updated_profiles: dict[str, Any] = {}
    added = 0
    preserved_curated = 0

    for h in heroes_data["heroes"]:
        slug = h["slug"]
        full_skill_text = " ".join(
            f"{sk.get('name', '')} {sk.get('description', '')}" for sk in h.get("skills", [])
        )
        auto_mechanics = extract_mechanics(h)
        auto_damage = detect_damage_type(full_skill_text, h["primary_role"])

        if slug in existing:
            entry = existing[slug]
            # Always refresh auto-derived metadata, NEVER overwrite human-curated tactical insights
            entry["display_name"] = h["display_name"]
            entry["roles"] = h["roles"]
            entry["primary_role"] = h["primary_role"]
            entry["auto_mechanics"] = auto_mechanics
            entry["damage_type"] = entry.get("damage_type_override") or auto_damage
            if entry.get("curated"):
                preserved_curated += 1
            updated_profiles[slug] = entry
        else:
            added += 1
            updated_profiles[slug] = {
                "slug": slug,
                "display_name": h["display_name"],
                "roles": h["roles"],
                "primary_role": h["primary_role"],
                "damage_type": auto_damage,
                "durability_class": DEFAULT_DURABILITY_BY_ROLE.get(h["primary_role"], "mixed"),
                "range_class": DEFAULT_RANGE_BY_ROLE.get(h["primary_role"], "mixed"),
                "auto_mechanics": auto_mechanics,
                "curated": False,
                "archetypes": [
                    {
                        "id": f"{slug}-default",
                        "name": f"Chuẩn ({h['primary_role']})",
                        "power_curve": None,
                        "power_spikes": [],
                        "gameplan_by_phase": {},
                    }
                ],
                "coach_notes": "",
            }

    payload = {
        "schema_version": 1,
        "total_heroes": len(updated_profiles),
        "curated_count": preserved_curated,
        "profiles": updated_profiles,
    }
    TACTICAL_DIR.mkdir(parents=True, exist_ok=True)
    profiles_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Bootstrapped data/tactical/hero_profiles.json: "
        f"{len(updated_profiles)} heroes ({added} newly added, {preserved_curated} curated preserved)."
    )
    return payload


if __name__ == "__main__":
    seed_static_tactical_files()
    bootstrap_hero_profiles()