from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UPLOAD_ROOT = Path('/home/ubuntu/upload')
DATA_ROOT = PROJECT_ROOT / 'data'
OUTPUT_PATH = DATA_ROOT / 'tdn_fiscal_inventory.json'

ITEM_RE = re.compile(r'\{"id":"(\d+)","type":"page","status":"[^"]*","title":"((?:\\.|[^"\\])*)"')


def decode_title(value: str) -> str:
    try:
        return json.loads('"' + value + '"')
    except json.JSONDecodeError:
        return value.replace('\\"', '"').replace('\\_', '_').replace('\\/', '/')


def page_url(page_id: str) -> str:
    return f'https://tdn.totvs.com/pages/viewpage.action?pageId={page_id}'


def load_partial(path: Path, pages: dict[str, dict[str, str]]) -> None:
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding='utf-8'))
    rows = payload if isinstance(payload, list) else payload.get('pages', [])
    for row in rows:
        page_id = str(row.get('id', '')).strip()
        title = str(row.get('title', '')).strip()
        if page_id and title:
            pages[page_id] = {
                'id': page_id,
                'title': title,
                'url': row.get('url') or page_url(page_id),
            }


def parse_api_file(path: Path, pages: dict[str, dict[str, str]], relations: set[tuple[str, str]]) -> None:
    text = path.read_text(encoding='utf-8', errors='replace')
    parent_match = re.search(r'tdn\.totvs\.com_rest_api_content_(\d+)_child_page', path.name)
    parent_id = parent_match.group(1) if parent_match else ''
    for match in ITEM_RE.finditer(text):
        page_id, raw_title = match.groups()
        title = decode_title(raw_title).strip()
        if not title:
            continue
        pages[page_id] = {
            'id': page_id,
            'title': title,
            'url': page_url(page_id),
        }
        if parent_id:
            relations.add((parent_id, page_id))


def main() -> None:
    pages: dict[str, dict[str, str]] = {}
    relations: set[tuple[str, str]] = set()

    for name in ('fiscal_tdn_root_links.json', 'fiscal_tdn_children_partial.json', 'fiscal_tdn_expanded_partial.json'):
        load_partial(DATA_ROOT / name, pages)

    for path in sorted(UPLOAD_ROOT.glob('tdn.totvs.com_rest_api_content_*_child_page*.md')):
        parse_api_file(path, pages, relations)

    # A raiz foi obtida pela expansão do conteúdo e deve aparecer explicitamente.
    pages['270093968'] = {
        'id': '270093968',
        'title': 'Fiscal - Protheus 12',
        'url': 'https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12',
    }

    rows = sorted(pages.values(), key=lambda row: (row['title'].casefold(), row['id']))
    payload = {
        'root': pages['270093968'],
        'total': len(rows),
        'pages': rows,
        'relations': [
            {'parent_id': parent, 'child_id': child}
            for parent, child in sorted(relations)
        ],
        'source': 'TDN Confluence REST child/page responses plus previously expanded Fiscal inventory',
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} páginas e {len(relations)} relações em {OUTPUT_PATH}')
    print('Fontes parciais:', ', '.join(name for name in ('fiscal_tdn_root_links.json', 'fiscal_tdn_children_partial.json', 'fiscal_tdn_expanded_partial.json') if (DATA_ROOT / name).exists()))
    print('Respostas API:', len(list(UPLOAD_ROOT.glob('tdn.totvs.com_rest_api_content_*_child_page*.md'))))


if __name__ == '__main__':
    main()
