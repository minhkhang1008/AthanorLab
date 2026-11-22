#!/usr/bin/env python3
"""
AthanorLab - Offline DOM Inspector
Extracts exact inner HTML samples from cached Phase-1 HTML files (zero network calls).
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT_DIR / "cache" / "probe_html"
OUT_FILE = ROOT_DIR / "probes" / "dom_samples.md"


def load_soup(filename: str) -> BeautifulSoup:
    html = (CACHE_DIR / filename).read_text(encoding="utf-8")
    return BeautifulSoup(html, "lxml")


def block(title: str, snippets: list[str]) -> str:
    parts = [f"## {title}"]
    for i, s in enumerate(snippets, 1):
        parts.append(f"### Sample {i}\n```html\n{s.strip()}\n```")
    return "\n\n".join(parts)


def main() -> None:
    sections: list[str] = ["# AthanorLab - Exact DOM Samples (Offline Cache)"]

    # 1. Heroes list: filter bar + role IDs + 2 hero cards
    soup = load_soup("heroes_list.html")
    hero_filters = soup.select(".st-heroes__filter, .st-heroes__head, [class*='st-heroes'] select, [class*='st-heroes'] ul, [class*='filter']")
    hero_cards = soup.select("a.st-heroes__item")[:3]
    sections.append(
        block(
            "1. heroes_list (Filters & Cards)",
            [el.prettify()[:2500] for el in hero_filters[:3]]
            + [el.prettify() for el in hero_cards],
        )
    )

    # 2. Hero detail: full section.hero__skills from Evita
    soup = load_soup("hero_evita.html")
    skills_sec = soup.select_one("section.hero__skills")
    sections.append(
        block(
            "2. hero_evita (section.hero__skills)",
            [skills_sec.prettify()[:4500] if skills_sec else "NOT FOUND"],
        )
    )

    # 3. Items: filter/tabs + 3 sample div.st-items__item (first, middle, last)
    soup = load_soup("items.html")
    item_controls = soup.select("[class*='st-items'] ul, [class*='st-items'] .filter, .st-items__filter, .st-items__tabs, .st-items__nav")
    items = soup.select("div.st-items__item")
    sample_items = [items[0], items[len(items) // 2], items[-1]] if len(items) >= 3 else items
    sections.append(
        block(
            f"3. items (Total={len(items)} | Controls & 3 Items)",
            [el.prettify()[:2000] for el in item_controls[:3]]
            + [el.prettify() for el in sample_items],
        )
    )

    # 4. Arcana: filter/tabs + 3 sample div.st-runes__item (first, middle, last)
    soup = load_soup("arcana.html")
    rune_controls = soup.select("[class*='st-runes'] ul, [class*='st-runes'] .filter, .st-runes__filter, .st-runes__tabs, .st-runes__nav")
    runes = soup.select("div.st-runes__item")
    sample_runes = [runes[0], runes[len(runes) // 2], runes[-1]] if len(runes) >= 3 else runes
    sections.append(
        block(
            f"4. arcana (Total={len(runes)} | Controls & 3 Runes)",
            [el.prettify()[:2000] for el in rune_controls[:3]]
            + [el.prettify() for el in sample_runes],
        )
    )

    # 5. Talents: 2 sample div.st-extra-skills__item
    soup = load_soup("talents.html")
    talents = soup.select("div.st-extra-skills__item")
    sections.append(
        block(
            f"5. talents (Total={len(talents)})",
            [el.prettify() for el in talents[:2]],
        )
    )

    # 6. Enchantments: 1 full faction div.st-badges__item
    soup = load_soup("enchantments.html")
    badges = soup.select("div.st-badges__item")
    sections.append(
        block(
            f"6. enchantments (Total factions={len(badges)} | Full 1st faction)",
            [badges[0].prettify()[:5000] if badges else "NOT FOUND"],
        )
    )

    # 7. Updates list & pagination + Patch article top-level structure
    soup = load_soup("updates.html")
    posts = soup.select("a.p-news__post")[:2]
    pag = soup.select(".pagination, .nav-links, .p-news__pagination, [class*='pag']")
    sections.append(
        block(
            "7. updates (Post Cards & Pagination)",
            [el.prettify() for el in posts]
            + [el.prettify()[:1500] for el in pag[:2]],
        )
    )

    soup = load_soup("sample_patch_article.html")
    article = soup.select_one("article.p-news__single--content")
    h1_summary = []
    if article:
        for h in article.find_all(["h1", "h2"]):
            h1_summary.append(f"<{h.name}> {h.get_text(' ', strip=True)}")
        # Grab Butterfly balance block sample
        bf_h2 = next((h for h in article.find_all("h2") if "Butterfly" in h.get_text()), None)
        bf_html = []
        if bf_h2:
            bf_html.append(bf_h2.prettify())
            for sib in bf_h2.find_next_siblings():
                if sib.name in {"h1", "h2"}:
                    break
                bf_html.append(sib.prettify())
        sections.append(
            block(
                "8. sample_patch_article (Headings Outline & Butterfly Block)",
                ["\n".join(h1_summary), "\n".join(bf_html)[:4500]],
            )
        )

    OUT_FILE.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Saved exact DOM samples to: {OUT_FILE}")


if __name__ == "__main__":
    main()