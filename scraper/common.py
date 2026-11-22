from __future__ import annotations

import hashlib
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://lienquan.garena.vn"
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw_official"
HTML_CACHE_DIR = ROOT_DIR / "cache" / "html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

BLOCK_TAGS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "tr"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.replace("\xa0", " ").replace("\u200b", "")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text


def slugify_vi(text: str) -> str:
    text = clean_text(text).lower().replace("đ", "d")
    norm = unicodedata.normalize("NFKD", text)
    ascii_str = "".join(ch for ch in norm if not unicodedata.combining(ch))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_str).strip("-")
    return slug or "unknown"


def url_last_segment(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] if path else ""


def extract_block_lines(container: Tag | None) -> list[str]:
    """Extract clean text lines from <article> regardless of whether it uses <p>, <li>, or nested <div>."""
    if container is None:
        return []
    lines: list[str] = []

    def walk(node: Tag) -> None:
        child_blocks = [
            c for c in node.find_all(recursive=False)
            if isinstance(c, Tag) and c.name in (BLOCK_TAGS | {"ul", "ol", "table", "section"})
        ]
        if not child_blocks:
            # Leaf block: preserve <br> as separate lines while keeping inline <strong>/<span> together
            for br in node.find_all("br"):
                br.replace_with("\n")
            raw = node.get_text(" ", strip=False)
            for part in raw.split("\n"):
                cleaned = clean_text(part)
                if cleaned:
                    lines.append(cleaned)
            return
        for child in node.children:
            if isinstance(child, Tag):
                if child.name == "table":
                    md_table = table_to_markdown(child)
                    if md_table:
                        lines.append(md_table)
                elif child.name in (BLOCK_TAGS | {"ul", "ol", "section"}):
                    walk(child)
                else:
                    cleaned = clean_text(child.get_text(" ", strip=False))
                    if cleaned:
                        lines.append(cleaned)
            else:
                cleaned = clean_text(str(child))
                if cleaned:
                    lines.append(cleaned)

    walk(container)
    return lines


def table_to_markdown(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = [
            clean_text(cell.get_text(" ", strip=False)).replace("|", "\\|")
            for cell in tr.find_all(["th", "td"])
        ]
        if any(cells):
            rows.append(cells)
    if not rows:
        return ""
    max_cols = max(len(r) for r in rows)
    padded = [r + [""] * (max_cols - len(r)) for r in rows]
    header = "| " + " | ".join(padded[0]) + " |"
    sep = "| " + " | ".join(["---"] * max_cols) + " |"
    body = ["| " + " | ".join(r) + " |" for r in padded[1:]]
    return "\n".join([header, sep, *body])


def parse_select_map(soup: BeautifulSoup, select_name: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    select = soup.select_one(f'select[name="{select_name}"]')
    if not select:
        return mapping
    for opt in select.find_all("option"):
        val = (opt.get("value") or "").strip()
        label = clean_text(opt.get_text())
        if val and label:
            mapping[val] = label
    return mapping


def sha256_json(data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PoliteFetcher:
    def __init__(self, delay: float = 0.5, refresh: bool = False, timeout: float = 25.0):
        self.delay = delay
        self.refresh = refresh
        self.client = httpx.Client(headers=HEADERS, timeout=timeout, follow_redirects=True)
        HTML_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def __enter__(self) -> "PoliteFetcher":
        return self

    def __exit__(self, *args: Any) -> None:
        self.client.close()

    def fetch_html(self, url: str, cache_key: str, retries: int = 3) -> str:
        cache_path = HTML_CACHE_DIR / f"{cache_key}.html"
        if cache_path.exists() and not self.refresh:
            return cache_path.read_text(encoding="utf-8")

        last_err: Exception | None = None
        for attempt in range(1, retries + 1):
            time.sleep(self.delay * attempt)
            try:
                resp = self.client.get(url)
                if resp.status_code == 200:
                    cache_path.parent.mkdir(parents=True, exist_ok=True)
                    cache_path.write_text(resp.text, encoding="utf-8")
                    return resp.text
                if resp.status_code == 404:
                    raise httpx.HTTPStatusError(
                        f"404 Not Found: {url}", request=resp.request, response=resp
                    )
                last_err = RuntimeError(f"HTTP {resp.status_code} for {url}")
            except httpx.HTTPStatusError:
                raise
            except Exception as exc:
                last_err = exc
        raise RuntimeError(f"Failed to fetch {url} after {retries} retries: {last_err}")