#!/usr/bin/env python3
"""Gera a base JSON consumida pelo site estático Buscador Protheus.

O script lê os índices Indice_*.txt disponíveis em /home/ubuntu e produz
client/public/knowledge.json, sem realizar chamadas de rede nem depender de
backend em tempo de execução.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_SOURCE_ROOT = PROJECT_ROOT / 'data' / 'indices'
SOURCE_ROOT = PROJECT_SOURCE_ROOT if PROJECT_SOURCE_ROOT.exists() else Path('/home/ubuntu')
OUTPUT_PATH = PROJECT_ROOT / 'client' / 'public' / 'knowledge.json'

MODULES = {
    'Indice_Configurador_Tributos.txt': ('Configurador de Tributos', 'FISA'),
    'Indice_SIGAFIS_Fiscal.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'Indice_SIGAFAT_Faturamento.txt': ('Faturamento', 'SIGAFAT'),
    'Indice_SIGAFIN_Financeiro.txt': ('Financeiro', 'SIGAFIN'),
    'Indice_SIGACOM_Compras.txt': ('Compras', 'SIGACOM'),
    'Indice_SIGAEST_Estoque.txt': ('Estoque e Custos', 'SIGAEST'),
    'Indice_SIGAATF_AtivoFixo.txt': ('Ativo Fixo', 'SIGAATF'),
    'Indice_SIGACTB_Contabilidade.txt': ('Contabilidade Gerencial', 'SIGACTB'),
    'Indice_SIGAGCT_GestaoContratos.txt': ('Gestão de Contratos', 'SIGAGCT'),
    'Indice_SIGAPMS_Projetos.txt': ('Gestão de Projetos', 'SIGAPMS'),
    'Indice_SIGATMK_CallCenter.txt': ('Call Center', 'SIGATMK'),
    'Indice_SIGACRM_CRM.txt': ('Customer Relationship Management', 'SIGACRM'),
    'Indice_Customizacoes_ADVPL.txt': ('Customizações', 'ADVPL'),
    'Indice_Arquivos_Magneticos.txt': ('Arquivos Magnéticos', 'SIGAFIS'),
    'Indice_Documentos_Eletronicos.txt': ('Documentos Eletrônicos Protheus', 'NFE/NFSE'),
    'Indice_SIGAEIC_Importacao.txt': ('Easy Import Control', 'SIGAEIC'),
    'sigafat_links_accumulator.txt': ('Faturamento', 'SIGAFAT'),
    'sigafis_links_accumulator.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'sigafis_links_partial.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'tdn_tree_links.txt': ('Referências gerais TDN', 'TDN'),
    'master_index_links.txt': ('Referências gerais TDN', 'TDN'),
    'all_sources_links.txt': ('Referências gerais', 'TDN/Central'),
    'tdn_links.txt': ('Referências gerais TDN', 'TDN'),
    'central_links_final.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_raw.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_p1.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_p2.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_p3.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_p4.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'central_links_p5.txt': ('Referências gerais Central TOTVS', 'CENTRAL'),
    'protheus_modules_links_final_v3.txt': ('Catálogo de módulos Protheus', 'PROTHEUS'),
    'sigaatf_subsections.txt': ('Ativo Fixo', 'SIGAATF'),
    'sigaatf_subsections_v3.txt': ('Ativo Fixo', 'SIGAATF'),
    'sigactb_subsections.txt': ('Contabilidade Gerencial', 'SIGACTB'),
    'sigagct_subsections.txt': ('Gestão de Contratos', 'SIGAGCT'),
    'sigapms_subsections.txt': ('Gestão de Projetos', 'SIGAPMS'),
    'sigatmk_subsections.txt': ('Call Center', 'SIGATMK'),
    'sigacrm_subsections.txt': ('Customer Relationship Management', 'SIGACRM'),
    'sigacom_subsections.txt': ('Compras', 'SIGACOM'),
    'sigaeic_subsections.txt': ('Easy Import Control', 'SIGAEIC'),
    'sigaest_subsections.txt': ('Estoque e Custos', 'SIGAEST'),
    'sigafin_subsections.txt': ('Financeiro', 'SIGAFIN'),
    'sigafat_subsections.txt': ('Faturamento', 'SIGAFAT'),
    'sigafat_subsections_final.txt': ('Faturamento', 'SIGAFAT'),
    'sigafat_subsections_v2.txt': ('Faturamento', 'SIGAFAT'),
    'sigafis_subsections.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'sigafis_subsections_clean.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'sigafis_subsections_final.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'sigafis_subsections_full.txt': ('Escrituração e Relatórios Fiscal', 'SIGAFIS'),
    'sigafis_mag_subsections.txt': ('Arquivos Magnéticos', 'SIGAFIS'),
    'doc_eletronicos_subsections.txt': ('Documentos Eletrônicos Protheus', 'NFE/NFSE'),
    'advpl_subsections.txt': ('Customizações', 'ADVPL'),
    'tdn_fiscal_recursive.txt': ('Fiscal - Protheus 12', 'SIGAFIS'),
    'tdn_protheus12_root.txt': ('Catálogo TDN Protheus 12', 'PROTHEUS-TDN'),
    'tdn_taf_links.txt': ('TAF - TOTVS Automação Fiscal', 'SIGATAF'),
}

MODULE_HINTS = [
    ('SIGAFIS', 'Escrituração e Relatórios Fiscal'),
    ('SIGAFAT', 'Faturamento'),
    ('SIGAFIN', 'Financeiro'),
    ('SIGACOM', 'Compras'),
    ('SIGAEST', 'Estoque e Custos'),
    ('SIGAATF', 'Ativo Fixo'),
    ('SIGACTB', 'Contabilidade Gerencial'),
    ('SIGAGCT', 'Gestão de Contratos'),
    ('SIGAPMS', 'Gestão de Projetos'),
    ('SIGATMK', 'Call Center'),
    ('SIGACRM', 'Customer Relationship Management'),
    ('SIGAEIC', 'Easy Import Control'),
    ('ADVPL', 'Customizações'),
]

URL_RE = re.compile(r'https?://[^\s|]+')

def clean(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('\ufeff', '').strip())

def parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith(('#', '=', 'ÍNDICE', 'INDICE', 'VARREDURA', 'TOTAL', '---')):
        return None

    match = URL_RE.search(line)
    if not match:
        return None

    url = match.group(0).rstrip('.,;)]}')
    title = line[:match.start()].strip().rstrip('|-:')
    if title.lower().startswith('url:'):
        title = title[4:].strip()
    if not title:
        title = urlparse(url).path.rsplit('/', 1)[-1] or url
    return clean(title), url

def source_name(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return 'TDN' if 'tdn.totvs.com' in host else 'Central de Atendimento TOTVS' if 'centraldeatendimento.totvs.com' in host else host

def record_kind(url: str) -> str:
    return 'section' if '/sections/' in url else 'article'


def link_type(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if 'centraldeatendimento.totvs.com' in host:
        if '/sections/' in path:
            return 'Central TOTVS — Seção'
        if '/articles/' in path:
            return 'Central TOTVS — Artigo'
        return 'Central TOTVS — Outro'
    if 'tdn.totvs.com' in host:
        if '/pages/releaseview.action' in path:
            return 'TDN — Release'
        if '/pages/viewpage.action' in path:
            return 'TDN — Página'
        if '/display/' in path:
            return 'TDN — Display'
        return 'TDN — Outro'
    return 'Outro domínio'

def main() -> None:
    records: list[dict[str, object]] = []
    seen: set[str] = set()

    for filename, (default_module, default_module_code) in MODULES.items():
        source_path = SOURCE_ROOT / filename
        if not source_path.exists():
            continue
        for raw_line in source_path.read_text(encoding='utf-8', errors='replace').splitlines():
            parsed = parse_line(raw_line)
            if not parsed:
                continue
            title, url = parsed
            if url in seen:
                continue
            seen.add(url)
            haystack = f'{title} {url}'.upper()
            module, module_code = default_module, default_module_code
            for hint_code, hint_module in MODULE_HINTS:
                if hint_code in haystack:
                    module, module_code = hint_module, hint_code
                    break
            records.append({
                'id': len(records) + 1,
                'title': title,
                'url': url,
                'module': module,
                'moduleCode': module_code,
                'source': source_name(url),
                'linkType': link_type(url),
                'kind': record_kind(url),
                'searchText': clean(f'{title} {url} {module} {module_code} {link_type(url)}').lower(),
            })

    records.sort(key=lambda item: (str(item['module']), str(item['title']).lower(), str(item['url'])))
    for index, record in enumerate(records, start=1):
        record['id'] = index

    modules = sorted({str(item['module']) for item in records})
    link_types = sorted({str(item['linkType']) for item in records})
    payload = {
        'version': 1,
        'generatedAt': '2026-08-20',
        'description': 'Índice local de documentação TOTVS Protheus coletada do TDN e da Central de Atendimento TOTVS.',
        'total': len(records),
        'modules': modules,
        'linkTypes': link_types,
        'records': records,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Gerados {len(records)} links em {OUTPUT_PATH}')
    print('Módulos:', ', '.join(modules))

if __name__ == '__main__':
    main()

# Fim do arquivo

