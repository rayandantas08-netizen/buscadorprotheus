#!/usr/bin/env python3
"""Gera a base JSON consumida pelo site estático Buscador Protheus.

O script lê os índices Indice_*.txt disponíveis em /home/ubuntu e produz
client/public/knowledge.json, sem realizar chamadas de rede nem depender de
backend em tempo de execução.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote_plus, urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_SOURCE_ROOT = PROJECT_ROOT / 'data' / 'indices'
SOURCE_ROOT = PROJECT_SOURCE_ROOT if PROJECT_SOURCE_ROOT.exists() else Path('/home/ubuntu')
OUTPUT_PATH = PROJECT_ROOT / 'client' / 'public' / 'knowledge.json'

MODULES = {
    'Indice_Configurador_Tributos.txt': ('Configurador de Tributos', 'FISA'),
    'Indice_Cfgtrib_Documento_Entrada.txt': ('Configurador de Tributos', 'FISA'),
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
    'Indice_Trilha_Complementos.txt': ('Trilha Fiscal — Complementos', 'TRILHA'),
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
SCHEME_RE = re.compile(r'https?://')
# Marcadores de linha que não trazem título nem URL útil.
SKIP_PREFIXES = ('#', '=', 'ÍNDICE', 'INDICE', 'VARREDURA', 'TOTAL', '---')
BULLET_RE = re.compile(r'^\[[\sx*•·\-]*\]\s*|^[\*\-•·]+\s*|^\d+[\.\\)]\s*')

def clean(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('\ufeff', '').strip())

def sanitize_url(url: str) -> str:
    """Corrige URLs com o domínio duplicado na mesma string.

    Alguns índices históricos gravaram `https://host` colado ao link completo
    (ex.: `https://centraldeatendimento.totvs.comhttps://centraldeatendimento...`),
    o que gerava link quebrado no site. Mantém-se a última URL completa.
    """
    url = url.rstrip('.,;)]}')
    ocorrencias = [match.start() for match in SCHEME_RE.finditer(url)]
    if len(ocorrencias) > 1:
        url = url[ocorrencias[-1]:]
    return url

def title_from_url(url: str) -> str:
    segmento = urlparse(url).path.rsplit('/', 1)[-1] or url
    return clean(unquote_plus(segmento).replace('_', ' '))

def normalize_inline_title(raw_title: str) -> str:
    """Remove o rótulo `URL:`/`Link:` e marcadores de lista que alguns índices usam."""
    title = clean(BULLET_RE.sub('', raw_title.strip()))
    if re.match(r'^(url|link|endereço|endereco|fonte)\s*:', title, re.IGNORECASE):
        title = re.sub(r'^(url|link|endereço|endereco|fonte)\s*:\s*', '', title, flags=re.IGNORECASE)
    return title.rstrip('|-:').strip()

def is_weak_title(title: str) -> bool:
    """Título fraco: vazio, rótulo solto (`URL`) ou slug derivado do caminho."""
    if not title:
        return True
    if title.lower() in {'url', 'link', 'fonte', 'endereço', 'endereco'}:
        return True
    return ' ' not in title  # slugs de URL não têm espaço

def title_score(title: str) -> tuple[int, int]:
    """Ordena títulos candidatos: títulos reais vencem slugs; mais longo vence."""
    return (0 if is_weak_title(title) else 1, min(len(title), 400))

def parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith(SKIP_PREFIXES):
        return None

    match = URL_RE.search(line)
    if not match:
        return None

    url = sanitize_url(match.group(0))
    title = normalize_inline_title(line[:match.start()])
    if not title:
        title = title_from_url(url)
    return clean(title), url

def parse_title_line(line: str) -> str:
    """Linha sem URL que pode ser o título do próximo endereço (formato `* Título` + `URL: ...`)."""
    line = clean(BULLET_RE.sub('', line.strip()))
    if not line or line.startswith(SKIP_PREFIXES):
        return ''
    return line

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
    # url -> melhor registro candidato (título real vence rótulo "URL"/slug)
    candidatos: dict[str, dict[str, object]] = {}

    for filename, (default_module, default_module_code) in MODULES.items():
        source_path = SOURCE_ROOT / filename
        if not source_path.exists():
            continue
        pending_title = ''
        for raw_line in source_path.read_text(encoding='utf-8', errors='replace').splitlines():
            parsed = parse_line(raw_line)
            if not parsed:
                pending_title = parse_title_line(raw_line) or pending_title
                continue
            title, url = parsed
            if is_weak_title(title) and pending_title:
                title = pending_title
            pending_title = ''
            haystack = f'{title} {url}'.upper()
            module, module_code = default_module, default_module_code
            for hint_code, hint_module in MODULE_HINTS:
                if hint_code in haystack:
                    module, module_code = hint_module, hint_code
                    break
            candidato = {
                'title': title,
                'url': url,
                'module': module,
                'moduleCode': module_code,
                'source': source_name(url),
                'linkType': link_type(url),
                'kind': record_kind(url),
            }
            anterior = candidatos.get(url)
            if anterior is None or title_score(title) > title_score(str(anterior['title'])):
                candidatos[url] = candidato

    records: list[dict[str, object]] = [dict(item) for item in candidatos.values()]
    for record in records:
        record['searchText'] = clean(
            f"{record['title']} {record['url']} {record['module']} {record['moduleCode']} {record['linkType']}"
        ).lower()

    records.sort(key=lambda item: (str(item['module']), str(item['title']).lower(), str(item['url'])))
    for index, record in enumerate(records, start=1):
        record['id'] = index

    modules = sorted({str(item['module']) for item in records})
    link_types = sorted({str(item['linkType']) for item in records})
    fracos = sum(1 for item in records if is_weak_title(str(item['title'])))
    payload = {
        'version': 1,
        'generatedAt': date.today().isoformat(),
        'description': 'Índice local de documentação TOTVS Protheus coletada do TDN e da Central de Atendimento TOTVS.',
        'total': len(records),
        'modules': modules,
        'linkTypes': link_types,
        'records': records,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Gerados {len(records)} links em {OUTPUT_PATH}')
    print(f'Títulos fracos (slug/URL) remanescentes: {fracos}')
    print('Módulos:', ', '.join(modules))

if __name__ == '__main__':
    main()

# Fim do arquivo

