from __future__ import annotations

import re
import sys
from pathlib import Path

PAGE_RE = re.compile(r'\{"id":"(\d+)","type":"page","status":"[^"]*","title":"((?:\\.|[^"\\])*)"')
SIZE_RE = re.compile(r'"children":\{"page":\{"results":\[')

def decode_title(raw: str) -> str:
    return raw.replace('\\"', '"').replace('\\_', '_').replace('\\u2013', '–')

def match_bracket(text: str, start: int) -> int | None:
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    return i
    return None

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('Uso: python scripts/analyze_tdn_expanded_sizes.py <arquivo.md>')
    text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')
    # Associate each children list with the nearest page record before it.
    pages = list(PAGE_RE.finditer(text))
    rows = []
    for marker in SIZE_RE.finditer(text):
        parent = None
        for page in reversed(pages):
            if page.start() < marker.start():
                parent = page
                break
        if not parent:
            continue
        end = match_bracket(text, marker.end() - 1)
        if end is None:
            continue
        tail = text[end:end + 160]
        size_match = re.search(r'"size":(\d+)', tail)
        if size_match:
            rows.append((int(size_match.group(1)), parent.group(1), decode_title(parent.group(2))))
    for size, page_id, title in sorted(set(rows), reverse=True):
        if size > 0:
            print(f'{size}\t{page_id}\t{title}')

if __name__ == '__main__':
    main()
