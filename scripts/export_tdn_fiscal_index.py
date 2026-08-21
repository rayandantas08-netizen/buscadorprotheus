from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / 'data' / 'tdn_fiscal_inventory.json'
OUTPUT_PATH = PROJECT_ROOT / 'data' / 'indices' / 'tdn_fiscal_recursive.txt'


def main() -> None:
    payload = json.loads(INPUT_PATH.read_text(encoding='utf-8'))
    pages = payload.get('pages', [])
    lines = [
        '# Índice recursivo do TDN — Fiscal - Protheus 12',
        '# Fonte: https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12',
        f'# Páginas únicas consolidadas: {len(pages)}',
        '',
    ]
    lines.extend(f"{row['title']} | {row['url']}" for row in pages)
    OUTPUT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(pages)} páginas exportadas para {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
