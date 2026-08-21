from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / 'data' / 'indices' / 'tdn_tree_links.txt'
JSON_PATH = PROJECT_ROOT / 'data' / 'tdn_protheus12_inventory.json'
INDEX_PATH = PROJECT_ROOT / 'data' / 'indices' / 'tdn_protheus12_root.txt'
URL_RE = re.compile(r'https?://[^\s|]+')


def clean(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('\ufeff', '').strip())


def main() -> None:
    records: dict[str, dict[str, str]] = {}
    for line in SOURCE_PATH.read_text(encoding='utf-8', errors='replace').splitlines():
        match = URL_RE.search(line)
        if not match:
            continue
        url = match.group(0).rstrip('.,;)]}')
        title = clean(line[:match.start()].strip().rstrip('|-:'))
        if not title:
            title = urlparse(url).path.rsplit('/', 1)[-1] or url
        records.setdefault(url, {'title': title, 'url': url})

    pages = sorted(records.values(), key=lambda row: (row['title'].casefold(), row['url']))
    payload = {
        'root': {
            'title': 'Protheus 12',
            'url': 'https://tdn.totvs.com/display/public/PROT/Protheus++12',
        },
        'total': len(pages),
        'pages': pages,
        'source_file': str(SOURCE_PATH.relative_to(PROJECT_ROOT)),
        'coverage_status': 'tree inventory captured; recursive completeness not proven because the TDN root API returned an access block/CAPTCHA during this run',
        'source': 'TDN tree links collected in the project before the current Fiscal expansion',
    }
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Índice da árvore Protheus 12 — TDN',
        '# Fonte: https://tdn.totvs.com/display/public/PROT/Protheus++12',
        f'# Páginas/links únicos na árvore capturada: {len(pages)}',
        '',
    ]
    lines.extend(f"{row['title']} | {row['url']}" for row in pages)
    INDEX_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(pages)} links únicos em {JSON_PATH}')
    print(f'Índice textual em {INDEX_PATH}')


if __name__ == '__main__':
    main()
