from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def clean_api_markdown(text: str) -> str:
    # The web extractor escapes a few JSON punctuation/key characters in markdown.
    text = text.strip()
    text = text.replace('\\[', '[').replace('\\]', ']')
    text = text.replace('\\{', '{').replace('\\}', '}')
    text = text.replace('\\_', '_')
    return text


def walk(node, parent_id: str | None, pages: dict[str, dict], relations: set[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        current = node.get('id')
        if current and node.get('type') == 'page':
            current = str(current)
            pages[current] = {
                'id': current,
                'title': str(node.get('title', '')).strip(),
                'url': f'https://tdn.totvs.com/pages/viewpage.action?pageId={current}',
            }
            if parent_id and parent_id != current:
                relations.add((parent_id, current))
            parent_for_children = current
        else:
            parent_for_children = parent_id
        for key, value in node.items():
            if key == 'children':
                walk(value, parent_for_children, pages, relations)
            elif isinstance(value, (dict, list)):
                walk(value, parent_for_children, pages, relations)
    elif isinstance(node, list):
        for item in node:
            walk(item, parent_id, pages, relations)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit('Uso: python scripts/parse_tdn_expanded_tree.py <entrada.md> <saida.json>')
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    raw = clean_api_markdown(source.read_text(encoding='utf-8', errors='replace'))
    pages: dict[str, dict] = {}
    relations: set[tuple[str, str]] = set()
    try:
        data = json.loads(raw)
        walk(data, None, pages, relations)
    except json.JSONDecodeError:
        # The web extractor can truncate a large JSON response. Recover complete
        # page records from the valid-looking prefix; child/page calls fill edges.
        item_re = re.compile(r'\{"id":"(\d+)","type":"page","status":"[^"]*","title":"((?:\\.|[^"\\])*)"')
        for match in item_re.finditer(raw):
            page_id, raw_title = match.groups()
            try:
                title = json.loads('"' + raw_title + '"')
            except json.JSONDecodeError:
                title = raw_title.replace('\\"', '"').replace('\\_', '_')
            pages[page_id] = {
                'id': page_id,
                'title': title,
                'url': f'https://tdn.totvs.com/pages/viewpage.action?pageId={page_id}',
            }
        print('Aviso: resposta truncada; relações serão completadas por consultas child/page.')
    payload = {
        'pages': sorted(pages.values(), key=lambda item: (item['title'].casefold(), item['id'])),
        'relations': [{'parent_id': p, 'child_id': c} for p, c in sorted(relations)],
        'source': str(source),
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{len(payload['pages'])} páginas e {len(payload['relations'])} relações salvas em {target}")


if __name__ == '__main__':
    main()
