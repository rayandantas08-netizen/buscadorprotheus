from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

API_FILE_RE = re.compile(r"tdn\.totvs\.com_rest_api_content_(\d+)_child_page")
ITEM_RE = re.compile(r'\{"id":"(\d+)","type":"page","status":"[^"]*","title":"((?:\\.|[^"\\])*)"')

def decode_title(value: str) -> str:
    try:
        return json.loads('"' + value + '"')
    except json.JSONDecodeError:
        return value.replace('\\"', '"').replace('\\_', '_').replace('\\/', '/')

def parse_file(path: Path) -> tuple[str | None, list[dict[str, str]]]:
    parent_match = API_FILE_RE.search(path.name)
    parent = parent_match.group(1) if parent_match else None
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    seen = set()
    for match in ITEM_RE.finditer(text):
        page_id, raw_title = match.groups()
        if page_id in seen:
            continue
        seen.add(page_id)
        title = decode_title(raw_title)
        rows.append({
            "id": page_id,
            "title": title,
            "url": f"https://tdn.totvs.com/pages/viewpage.action?pageId={page_id}",
            "parent_id": parent,
            "source_api": str(path),
        })
    return parent, rows

def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python scripts/parse_tdn_api_children.py <pasta_upload> <saida.json>")
    source_dir = Path(sys.argv[1])
    target = Path(sys.argv[2])
    all_rows: dict[str, dict[str, str]] = {}
    relations: set[tuple[str, str]] = set()
    for path in sorted(source_dir.glob("tdn.totvs.com_rest_api_content_*_child_page*.md")):
        parent, rows = parse_file(path)
        for row in rows:
            all_rows[row["id"]] = row
            if parent:
                relations.add((parent, row["id"]))
    payload = {
        "pages": sorted(all_rows.values(), key=lambda item: (item["title"].casefold(), item["id"])),
        "relations": [{"parent_id": p, "child_id": c} for p, c in sorted(relations)],
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(payload['pages'])} páginas e {len(payload['relations'])} relações consolidadas em {target}")

if __name__ == "__main__":
    main()
