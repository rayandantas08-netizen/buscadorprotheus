from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

BASE = "https://tdn.totvs.com"
ALLOWED_HOSTS = {"tdn.totvs.com", "tdn.totvs.com.br"}


def normalize_url(raw: str) -> str | None:
    raw = raw.strip().strip("<>\"'")
    if not raw:
        return None
    url = urljoin(BASE, raw)
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or parts.netloc.lower() not in ALLOWED_HOSTS:
        return None
    path = parts.path or "/"
    # Remove fragments and tracking/query parameters that do not identify a page.
    query = parts.query
    if path.endswith("/display/public/PROT"):
        path = path.rstrip("/")
    return urlunsplit(("https", parts.netloc.lower(), path, query, ""))


def extract_from_markdown(text: str) -> list[dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    # Markdown links, including optional title text.
    for match in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        url = normalize_url(match.group(2))
        if url and title:
            found.setdefault(url, {"title": title, "url": url})
    # Bare links that may be present in copied page text.
    for match in re.finditer(r"https?://tdn\.totvs\.com[^\s)<>\"']+", text):
        url = normalize_url(match.group(0))
        if url:
            found.setdefault(url, {"title": "", "url": url})
    return sorted(found.values(), key=lambda item: (item["title"].casefold(), item["url"]))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python scripts/extract_tdn_links.py <entrada.md> <saida.json>")
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    items = extract_from_markdown(source.read_text(encoding="utf-8", errors="replace"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(items)} URLs normalizadas salvas em {target}")


if __name__ == "__main__":
    main()
