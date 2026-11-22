#!/usr/bin/env python3
"""
Fast CLI lookup helper for AthanorLab (Gemini CLI / Claude Code / Cursor / Codex).
Usage:
  python skills/aov-data-lookup/scripts/query_aov.py hero evita
  python skills/aov-data-lookup/scripts/query_aov.py hero flowborn
  python skills/aov-data-lookup/scripts/query_aov.py item "chuy bang"
  python skills/aov-data-lookup/scripts/query_aov.py patch butterfly
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    cur = Path(__file__).resolve()
    for parent in cur.parents:
        if (parent / "data" / "raw_official").exists():
            return parent
    raise FileNotFoundError("Could not locate data/raw_official from script path.")


def norm(text: str) -> str:
    text = text.lower().strip().replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def load_json(root: Path, rel: str) -> dict[str, Any]:
    return json.loads((root / rel).read_text(encoding="utf-8"))


def query_hero(root: Path, q: str) -> None:
    nq = norm(q)
    heroes = load_json(root, "data/raw_official/heroes.json")["heroes"]
    hits = [
        h for h in heroes
        if nq in norm(h["slug"]) or nq in norm(h["display_name"]) or nq in norm(h.get("keyword", ""))
    ]
    if not hits:
        print(f"No hero matched '{q}'.")
        return
    for h in hits:
        print(f"=== {h['display_name']} ({h['slug']}) | Roles: {', '.join(h['roles'])} ===")
        print(f"URL: {h['url']}")
        for sk in h["skills"]:
            print(f"  [{sk['slot_label']}] {sk['name'] or '(no title)'}: {sk['description']}")
        print()


def query_item(root: Path, q: str) -> None:
    nq = norm(q)
    items = load_json(root, "data/raw_official/items.json")["items"]
    hits = [i for i in items if nq in norm(i["name"]) or nq in norm(i["slug"])]
    if not hits:
        print(f"No item matched '{q}'.")
        return
    for it in hits:
        print(f"=== {it['name']} ({it['category']} · Tier {it['tier']} · {it['price']}g · {it['price_tier']}) ===")
        if it["stats"]:
            print("  Stats  :", ", ".join(it["stats"]))
        for eff in it["effects"]:
            print("  Effect :", eff)
        print()


def query_patch(root: Path, q: str) -> None:
    nq = norm(q)
    patches = load_json(root, "data/raw_official/patches.json")["patches"]
    found = 0
    for p in patches:
        for sec in p.get("sections", []):
            if not sec.get("is_gameplay_relevant"):
                continue
            for sub in sec.get("subsections", []):
                blob = norm(sub["heading"] + " " + " ".join(sub["lines"]))
                if nq in blob:
                    found += 1
                    print(f"=== [{p['published_date']}] {p['title']} -> {sec['heading']} / {sub['heading']} ===")
                    for line in sub["lines"]:
                        print(" ", line)
                    print()
    if not found:
        print(f"No gameplay patch entry matched '{q}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query AthanorLab official JSON datasets.")
    parser.add_argument("entity", choices=["hero", "item", "patch"])
    parser.add_argument("query", type=str)
    args = parser.parse_args()

    root = find_repo_root()
    if args.entity == "hero":
        query_hero(root, args.query)
    elif args.entity == "item":
        query_item(root, args.query)
    elif args.entity == "patch":
        query_patch(root, args.query)


if __name__ == "__main__":
    main()