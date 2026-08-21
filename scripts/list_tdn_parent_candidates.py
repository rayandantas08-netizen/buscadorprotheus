from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PATTERNS = [
    r'Fiscal - P12', r'Fiscal P12', r'Configurações', r'Configuração', r'FAQ', r'Menu',
    r'Apurações', r'Arquivos Magnéticos', r'Livros Fiscais', r'Relatórios', r'Consultas',
    r'Atualizações', r'Pontos de Entrada', r'Banco de Conhecimento', r'Expedição',
    r'Smart ?View', r'Funções', r'Integrações', r'Conceitos', r'Ciclo de Vida',
    r'Legislações', r'Projetos', r'Rotinas', r'Localizaciones', r'RETAIL'
]
rx = re.compile('|'.join(PATTERNS), re.I)

def main():
    if len(sys.argv) != 2: raise SystemExit('Uso: ... <json>')
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    for page in data['pages']:
        if rx.search(page['title']):
            print(f"{page['id']}\t{page['title']}")

if __name__ == '__main__': main()
