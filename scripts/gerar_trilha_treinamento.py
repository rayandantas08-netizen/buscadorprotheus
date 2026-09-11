#!/usr/bin/env python3
"""Gera a trilha de implantação e treinamento fiscal do Buscador Protheus.

O script não acessa a rede: ele lê o índice local já versionado em
``client/public/knowledge.json`` (gerado por ``scripts/build_knowledge.py``) e
cruza cada tópico da agenda do projeto com os links disponíveis, classificando
cada fonte por intenção de uso (implantar, treinar, customizar ou suportar).

Saídas:
  * ``client/public/trilhas.json`` — consumido pela aba "Trilha" do site estático;
  * ``docs/trilha-minerios-gerais/*.md`` — dossiê por agenda, para uso em projeto.

Uso:
    python3 scripts/gerar_trilha_treinamento.py            # gera dossiê + JSON
    python3 scripts/gerar_trilha_treinamento.py --check    # falha se houver tópico sem fonte
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_PATH = PROJECT_ROOT / 'client' / 'public' / 'knowledge.json'
TRILHAS_PATH = PROJECT_ROOT / 'client' / 'public' / 'trilhas.json'
DOCS_ROOT = PROJECT_ROOT / 'docs' / 'trilha-minerios-gerais'

PROJETO = 'Minérios Gerais — implantação e treinamento do Fiscal Protheus 12'
LIMITE_PADRAO = 12


def norm(value: str) -> str:
    """Minúsculas e sem acentos, para casar padrões com os títulos do índice."""
    return unicodedata.normalize('NFD', value.lower()).encode('ascii', 'ignore').decode()


# ---------------------------------------------------------------------------
# Grupos (blocos da agenda informada pelo cliente)
# ---------------------------------------------------------------------------
GRUPOS: list[dict[str, str]] = [
    {
        'id': 'concluidos',
        'titulo': 'Tópicos concluídos — revisão e reforço de treinamento',
        'status': 'concluido',
        'descricao': (
            'Itens já implantados no cliente. A trilha serve para revisar a parametrização feita, '
            'padronizar o discurso do treinamento e registrar evidências de validação.'
        ),
    },
    {
        'id': 'agenda-09-09',
        'titulo': 'Agenda 09/09 — Minérios Gerais',
        'status': 'pendente',
        'descricao': 'Obrigações acessórias e apurações pendentes de implantação e treinamento.',
    },
    {
        'id': 'agenda-11-09',
        'titulo': 'Agenda 11/09 — Minérios Gerais',
        'status': 'pendente',
        'descricao': (
            'Validação operacional das rotinas fiscais, integração TAF/Extrator/REINF, revisão do '
            'escopo de parametrização e temas de fronteira com Estoque, Faturamento e Comércio Exterior.'
        ),
    },
    {
        'id': 'transversal',
        'titulo': 'Apoio transversal — capacitação e referência oficial',
        'status': 'apoio',
        'descricao': 'Materiais de treinamento, guias de referência e bancos de conhecimento usados em todos os tópicos.',
    },
]

# ---------------------------------------------------------------------------
# Tópicos da trilha
# ---------------------------------------------------------------------------
TOPICOS: list[dict[str, object]] = [
    # ============================ CONCLUÍDOS ================================
    {
        'id': 'cadastros-fiscais',
        'grupo': 'concluidos',
        'titulo': 'Cadastros fiscais: produtos, fornecedores e clientes',
        'status': 'concluido',
        'resumo': (
            'Base de tudo: SB1 (produto), SA1 (cliente) e SA2 (fornecedor) carregam os atributos que '
            'alimentam TES, Configurador de Tributos, livros fiscais e SPED (registros 0150, 0200 e 0205).'
        ),
        'rotinas': [
            'MATA010 / Cadastro de Produtos (SB1)',
            'MATA030 / Cadastro de Clientes (SA1)',
            'MATA020 / Cadastro de Fornecedores (SA2)',
            'FISA164 — Perfil tributário de participantes',
            'FISA166 — Perfil tributário de produtos',
            'Atualização de Dicionário da Classificação Tributária (cClassTrib)',
        ],
        'implantar': [
            'Conferir nos produtos: tipo (B1_TIPO), NCM, CEST, unidade de medida, origem da mercadoria, '
            'alíquotas de ICMS/IPI/PIS/COFINS e, quando usado o Configurador de Tributos, a classificação tributária (cClassTrib) e o cBenef.',
            'Conferir nos participantes: inscrição estadual (validação de IE), indicador de contribuinte, '
            'município/UF, regime de tributação e os campos de retenção (A1_RECPIS/A1_RECCOFI, A2_RECPIS/A2_RECCOFI/A2_RECCSLL, A2_RECISS).',
            'Vincular os perfis tributários (FISA164/FISA166) aos participantes e produtos que exigem tratamento diferenciado.',
            'Definir quem mantém cada atributo após o go-live (governança de cadastro) e como será feita a carga/atualização em massa.',
        ],
        'treinar': [
            'Mostrar onde cada campo fiscal do cadastro impacta: TES, cálculo do imposto, livro fiscal (SF3/SFT) e SPED.',
            'Exercitar a inclusão de um produto novo completo e a validação do alerta de IE inválida no cliente/fornecedor.',
            'Treinar a rotina de atualização da classificação tributária e o conceito de pacote do Configurador de Tributos.',
        ],
        'validar': [
            'Amostra de produtos e participantes escriturados corretamente no registro 0200/0150 do SPED Fiscal.',
            'Sem helps de IE, NCM ou classificação tributária na emissão de notas de teste.',
        ],
        'observacoes': [],
        'limit': LIMITE_PADRAO,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=606084833',
        ],
        'includes': [
            (r'fisa16[46]|perfil tributario', 8),
            (r'classificacao tributaria|cclasstrib|atualizacao de dicionario classificacao|pacotes classificacao', 7),
            (r'cadastros - fiscal|configuracoes - cadastros e parametros', 7),
            (r'cadastro de (produto|cliente|fornecedor)|cadastros?.{0,12}(produto|cliente|fornecedor)', 5),
            (r'inscricao estadual|valida a inscricao|ie - valida', 5),
            (r'\bncm\b|\bcest\b|codigo do produto|a950prd|atributos de produtos', 4),
            (r'facilitador|intfac|cbenef', 4),
            (r'\bsb1\b|\bsa1\b|\bsa2\b|b1_|a1_|a2_', 3),
        ],
        'excludes': r'call center|sigatmk|crm|contratos|projetos|gpe|salarial|folha|saude|plano de contas|medicao|retail|varejo|loja',
        'exclude_modules': ['Call Center', 'Customer Relationship Management', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'tes-entrada-saida',
        'grupo': 'concluidos',
        'titulo': 'TES: entrada e saída',
        'status': 'concluido',
        'resumo': (
            'Tipo de Entrada e Saída (SF4) define CFOP, atualização de estoque/financeiro, cálculo e '
            'escrituração de cada imposto. É o ponto que mais gera retrabalho quando fica mal configurado.'
        ),
        'rotinas': [
            'MATA080 — Cadastro de TES (SF4)',
            'TES Inteligente / Réplica de TES',
            'Pontos de entrada da TES (MATA080)',
        ],
        'implantar': [
            'Para cada cenário de operação (compra, venda, devolução, remessa, retorno, transferência, '
            'uso/consumo, ativo imobilizado, industrialização em terceiros) definir TES de entrada e de saída.',
            'Conferir campo a campo: CFOP, calcula ICMS/IPI/PIS/COFINS/ISS, livro fiscal de cada imposto, '
            'material de consumo, credita ICMS, atualiza estoque, gera duplicata, poder de terceiros (F4_PODER3) e agrega valor (F4_AGREG).',
            'Definir a convivência entre TES legado e Configurador de Tributos (híbrido) e quais campos passam a ser decididos pelo FISA170.',
            'Documentar a matriz CFOP x TES x CST/CSOSN x classificação tributária usada no projeto.',
        ],
        'treinar': [
            'Explicar a leitura da TES em conjunto com o cadastro do produto e do participante (o imposto sai da combinação dos três).',
            'Exercitar a cópia de TES e a montagem de uma TES nova para um cenário inexistente.',
            'Mostrar os helps mais comuns (A900CPO, validações de CFOP) e como diagnosticá-los.',
        ],
        'validar': [
            'Notas de teste de entrada e saída gravando SF3/SFT com CFOP, base e imposto coerentes.',
            'Matriz de operações do projeto coberta por TES homologadas.',
        ],
        'observacoes': [],
        'limit': LIMITE_PADRAO,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=706121236',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/4404850575767-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Pontos-de-Entrada-TES-MATA080',
        ],
        'quotas': [
            (r'\bpe - |ponto de entrada', 3),
        ],
        'includes': [
            (r'\btes\b|tes inteligente|replica de tes|tipos? de entrada e saida', 6),
            (r'mata080|f4_|maavaltes|maevaltes', 6),
            (r'\bcfop\b', 4),
            (r'tes - ', 5),
        ],
        'excludes': r'call center|sigatmk|contratos|projetos|atestado|conteste|latest',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'conf-tributos-legado',
        'grupo': 'concluidos',
        'titulo': 'Configuração de tributos (impostos legados) e Configurador de Tributos',
        'status': 'concluido',
        'resumo': (
            'Duas camadas convivem: os impostos legados (TES, exceção fiscal, alíquotas em cadastro) e o '
            'Configurador de Tributos (FISA170), que passa a ser obrigatório para novas legislações e para IBS/CBS.'
        ),
        'rotinas': [
            'FISA170 — Configurador de Tributos',
            'FISA080 — UF x UF (FECP e interestadual)',
            'SF7 — Exceção Fiscal',
            'TaxOpJson / Operando — recepção de tributos cadastrados',
        ],
        'implantar': [
            'Mapear o escopo: quais tributos e operações ficam no Configurador e quais permanecem no legado.',
            'Cadastrar regras de tributação (operadores, vigências, cBenef, ClassTrib) por UF e por cenário de operação.',
            'Configurar exceções fiscais (SF7) para MVA/pauta/redução de base por produto ou NCM.',
            'Definir rotina de atualização dos pacotes de classificação tributária e quem aprova cada alteração.',
        ],
        'treinar': [
            'Usar os webinars e treinamentos oficiais do Configurador de Tributos como material base da capacitação.',
            'Exercitar a criação de uma regra completa (tributo, vigência, entidade, produto) e a leitura do resultado na nota.',
            'Mostrar a diferença prática entre calcular pela TES e calcular pelo FISA170 no mesmo documento.',
        ],
        'validar': [
            'Comparativo de cálculo legado x Configurador nos cenários críticos (DIFAL, ST, benefício fiscal).',
            'Notas de teste autorizadas com as tags de IBS/CBS corretas quando aplicável.',
        ],
        'observacoes': [
            'A partir de 03/08/2026 o IBS/CBS é obrigatório: revisar se o escopo do projeto já prevê o cenário híbrido (legado + Configurador).',
        ],
        'limit': LIMITE_PADRAO,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=863302293',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=1018568875',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=945408020',
        ],
        'quotas': [
            (r'cbenefit|cbenef', 4),
        ],
        'includes': [
            (r'configurador de tributos|cfgtrib|fisa170|gestao fiscal', 8),
            (r'escopo de atendimento do configurador', 8),
            (r'classificacao tributaria|cclasstrib|cbenef|taxopjson|operando|systax', 6),
            (r'excecao fiscal|\bsf7\b', 5),
            (r'hibrid|legado|descontinuacao das operacoes fiscais da tes', 6),
            (r'fisa080|uf x uf', 5),
            (r'ib[s]\/? ?cbs|reforma tributaria', 4),
        ],
        'excludes': r'call center|contratos|projetos|gpe|salarial',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'diferencial-aliquota',
        'grupo': 'concluidos',
        'titulo': 'Diferencial de alíquota (DIFAL)',
        'status': 'concluido',
        'resumo': (
            'DIFAL de aquisição (uso/consumo e ativo imobilizado) e DIFAL EC 87/2015 para não contribuinte, '
            'com ou sem base dupla, FECP e GNRE.'
        ),
        'rotinas': [
            'ICMSDIFAL — Cálculo e apuração de DIFAL (EC 87/2015)',
            'SEICMS — Base dupla de ICMS diferencial de alíquota',
            'IEDIFAL — Cadastro de IE para diferencial de alíquota',
            'MV_ESTICM / FISA080 — alíquotas internas por UF',
        ],
        'implantar': [
            'Definir a matriz de DIFAL por operação: entrada de uso/consumo, entrada para ativo imobilizado, '
            'saída para não contribuinte (EC 87) e saída interestadual com FECP.',
            'Configurar base simples x base dupla (conv. 52/91), redução de base e reflexos no Configurador de Tributos.',
            'Configurar a geração de guia (GNRE/DIFAL) e o título financeiro correspondente, incluindo a natureza do título.',
            'Cadastrar as IE de DIFAL quando houver recolhimento por operação em outra UF.',
        ],
        'treinar': [
            'Exercitar uma compra interestadual de uso/consumo com e sem base dupla e conferir o valor na nota e no livro fiscal.',
            'Mostrar onde o DIFAL aparece na apuração, na guia e no financeiro.',
            'Discutir os erros mais comuns: alíquota interna desatualizada, FECP não configurado, cliente contribuinte marcado errado.',
        ],
        'validar': [
            'Notas de teste com DIFAL calculado e destacado conforme a UF de destino.',
            'Guias e títulos gerados com natureza e vencimento corretos.',
        ],
        'observacoes': [],
        'limit': LIMITE_PADRAO,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=699815598',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=567740017',
        ],
        'includes': [
            (r'difal|diferencial de aliquota', 8),
            (r'icmsdifal|seicms|iedifal|mv_esticm', 7),
            (r'ec ?87|emenda constitucional 87|gnre|f2_gnrdif', 6),
            (r'\bfecp\b|fundo de combate a pobreza|fundo estadual', 4),
            (r'icms ?st|icmsst|substituicao tributaria|antecipacao', 2),
            (r'base dupla', 4),
        ],
        'excludes': r'call center|contratos|projetos|salarial',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'apuracao-impostos',
        'grupo': 'concluidos',
        'titulo': 'Apuração de impostos',
        'status': 'concluido',
        'resumo': (
            'Apurações de ICMS, IPI, ISS, PIS/COFINS e ST: fechamento do período, geração de guias e '
            'títulos, contabilização e conferência contra os livros fiscais.'
        ),
        'rotinas': [
            'MATA953 — Apuração de ICMS (APUICM)',
            'Apuração de IPI (APUIPI) e MATR943 — Registro de apuração do IPI',
            'APUISS — Apuração de ISS',
            'APURESST / FISA302 — Ressarcimento ou complemento de ICMS-ST',
            'FISA001 — Apuração EFD Contribuições',
            'MATA930 — Reprocessamento dos livros fiscais',
        ],
        'implantar': [
            'Definir a ordem de fechamento: livros fiscais -> acertos -> apuração -> guias/títulos -> contabilização -> SPED.',
            'Configurar regime de apuração, períodos, filiais centralizadoras e parâmetros de cada imposto.',
            'Cadastrar os lançamentos padrão (LANPAD) para contabilização das apurações.',
            'Configurar geração de guias e títulos (naturezas, códigos de recolhimento, datas de vencimento por UF).',
        ],
        'treinar': [
            'Executar uma apuração completa em ambiente de treino e conferir os valores contra MATR930/MATRAPR.',
            'Mostrar reprocessamento, estorno e bloqueio de reprocessamento (PROCAPUR).',
            'Explicar a leitura das abas de outros créditos/outros débitos e como justificar cada ajuste.',
        ],
        'validar': [
            'Apuração do período fechada sem divergência entre livro, apuração e contabilidade.',
            'Guias e títulos gerados e conferidos pelo cliente.',
        ],
        'observacoes': [],
        'limit': 14,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=627111872',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=270894388',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=270093976',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=991865200',
        ],
        'quotas': [
            (r'\bpe - ', 4),
        ],
        'includes': [
            (r'apuicm|mata953|apuiipi|apuiss|apursn|apuresst|resumef3|novas apuracoes|apuracoes - fiscal', 8),
            (r'matr941|matr943|registro de apuracao|registro apuracao', 7),
            (r'apuracao de (icms|ipi|iss|pis|cofins)|apuracao do icms|apurar', 6),
            (r'regime de apuracao|mata930|matrapr|reprocessamento dos livros', 5),
            (r'lanpad|lancamento padrao|guia de recolhimento|guias de recolhimento', 4),
            (r'fisa302|ressarcimento|complemento de icms', 4),
            (r'procapur|apurf6|cpapuicms|gdebesp|giascdeb', 5),
        ],
        'excludes': r'contabilidade gerencial - apuracao, estorno e encerramento|aprovacao de preco|gia sp|nova gia|dime/sc|sefinnet|florianopolis',
        'exclude_modules': ['Contabilidade Gerencial', 'Gestão de Contratos', 'Call Center'],
    },
    {
        'id': 'impostos-retidos',
        'grupo': 'concluidos',
        'titulo': 'Impostos retidos (PCC, IRRF, INSS, ISS)',
        'status': 'concluido',
        'observado': True,
        'resumo': (
            'Retenções na entrada e na saída, geração de títulos de imposto, cumulatividade do PCC e '
            'obrigações acessórias (DIRF/DCTFWeb).'
        ),
        'rotinas': [
            'PARÂMETROS - PIS-COFINS-CSLL / ISS / IRRF / INSS',
            'MV_BX10925, MV_VCPCCP, MV_VL13137, MV_PISNAT/MV_COFINS/MV_CSLL',
            'Configurador de Tributos — Regras Financeiras (FISA170)',
            'FINA378/FINA381 — Aglutinação de títulos de PIS/COFINS/CSLL',
        ],
        'implantar': [
            'Definir o momento da retenção (na emissão ou na baixa do título) por imposto e por tipo de operação.',
            'Configurar naturezas financeiras de imposto, valores mínimos de retenção e cumulatividade do PCC.',
            'Configurar as regras financeiras no Configurador de Tributos: vigência, tipo de entidade, fator gerador e '
            '"data base para vencimento do imposto".',
            'Ajustar cadastros de clientes/fornecedores (rec. PIS/COFINS/CSLL/ISS, órgão público, MEI, autônomo).',
        ],
        'treinar': [
            'Exercitar uma nota de entrada de serviço com retenção de PCC e IRRF e acompanhar o título gerado no financeiro.',
            'Mostrar a diferença entre retenção na emissão e na baixa, e o efeito na cumulatividade.',
            'Revisar o roteiro oficial de cálculo e apuração de PIS/COFINS/CSLL com o time.',
        ],
        'validar': [
            'Títulos de imposto com natureza, valor e data de vencimento conferidos pelo cliente.',
            'DIRF/DCTFWeb alimentados corretamente a partir das retenções.',
        ],
        'observacoes': [
            'PENDÊNCIA REPORTADA: PCC gerando data de vencimento incorreta. Tratar como item de revisão de parametrização: '
            'a data de vencimento do PCC depende do momento da retenção (MV_BX10925), da data considerada para cumulatividade '
            '(MV_VCPCCP: 1=Emissão, 2=Venc. Real, 3=Dt. Contábil), do valor mínimo (MV_VL13137 = R$ 10,00) e, no Configurador '
            'de Tributos, da "Data base p/ vencto. do imposto (Emissão)" e da "Data Cumulat" da regra financeira. '
            'Pela Lei 13.137/15 o vencimento é no segundo decêndio do mês subsequente ao fato gerador.',
            'Se a aglutinação de títulos estiver em uso, verificar se é FINA378 (aglutina por data de EMISSÃO) ou FINA381 (por data de VENCIMENTO).',
        ],
        'limit': 16,
        'pinned': [
            'https://tdn.totvs.com/display/public/PROT/Configurador+de+Tributos+-+Regras+Financeiras',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360056887693-MP-FIS-Reten%C3%A7%C3%A3o-de-PIS-COFINS-e-CSLL',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360053516414-MP-FIS-Cumulatividade-Pis-Cofins-e-CSLL',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271950709399-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-PIS-COFINS-CSLL-reten%C3%A7%C3%A3o-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=701693213',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360022030252-Cross-Segmento-Backoffice-Linha-Protheus-SIGAFIN-FINA378-%C3%89-poss%C3%ADvel-aglutinar-t%C3%ADtulos-dos-impostos-PIS-COFINS-CSLL-pela-data-de-vencimento',
        ],
        'quotas': [
            (r'\bpe - ', 3),
            (r'configuracoes - ', 3),
        ],
        'includes': [
            (r'retencao de (pis|cofins|csll|iss|inss|irrf)|retencao de imposto|impostos retidos|reter', 8),
            (r'\bpcc\b|pis-?cofins-?csll|pis, cofins e csll|cumulatividade', 8),
            (r'mv_bx10925|mv_vcpccp|mv_vl13137|mv_pisnat|mv_cofins|mv_csll|mv_ratcsll|mv_vretpis|mv_mt10925', 8),
            (r'regras financeiras|fina378|fina381|aglutinar titulos|aglutinacao', 7),
            (r'\birrf\b|\binss\b|retencao de iss|dirf|pcorgpub|vlcodret|macalirrf|a954vcto', 6),
            (r'parâmetros - pis|parametros - pis|configuracoes - (irrf|inss|iss)', 6),
            (r'natureza utilizada nos titulos de retencao|natureza do titulo', 5),
            (r'retenc|retid|retido', 4),
        ],
        'excludes': r'retenciones|percepciones|argentina|\barg\b|colombia|\bmex\b|equador|\bequ\b|chile|\bchi\b|peru|\bper\b|salario|salarial|ferias|dserh|drh|tiss|campo telefone|arquivo magnetico da dirf',
        'exclude_modules': ['Call Center', 'Gestão de Contratos'],
    },
    # =========================== AGENDA 09/09 ===============================
    {
        'id': 'efd-icms-ipi',
        'grupo': 'agenda-09-09',
        'titulo': 'Geração do EFD-ICMS/IPI (SPED Fiscal)',
        'status': 'pendente',
        'resumo': (
            'Arquivo digital que consolida documentos fiscais, livros de apuração, CIAP, inventário e Bloco K. '
            'É o principal termômetro de qualidade da parametrização fiscal.'
        ),
        'rotinas': [
            'SPEDFISCAL — geração do arquivo (wizard)',
            'MATXSPED / PCPXSPED / SPEDXFUN — fontes dos registros',
            'MATR941/MATR943 — registros de apuração de ICMS e IPI (Bloco E)',
            'PVA — validador da Receita',
        ],
        'implantar': [
            'Instalar/atualizar os fontes do SPED (SPEDFISCAL, MATXSPED, SPEDXFUN) e conferir o pacote de expedição contínua do Fiscal.',
            'Configurar o wizard: período, livro, filiais, tipo de escrituração, geração de blocos opcionais (H, K, 1600, G) e caminho do arquivo.',
            'Garantir a ordem de execução: livros fiscais reprocessados (MATA930) -> acertos fiscais -> apurações -> SPED.',
            'Definir os pontos de entrada necessários (SPDFIS03, SPDFIS06, SPED0150, SPED0205, SPEDREGD etc.) somente onde houver exigência específica.',
            'Criar rotina de agendamento (schedule) para geração mensal e responsável pela validação no PVA.',
        ],
        'treinar': [
            'Treinar a geração passo a passo no ambiente de homologação e a leitura do arquivo no PVA.',
            'Ensinar a investigação das rejeições mais comuns: 0150 (participante), 0200/0205 (item), C100/C170 (documento), C197 (ajustes), E110 (apuração).',
            'Mostrar o uso dos pontos de entrada e dos relatórios de conferência (MATRAPR, MATR930).',
            'Fechar com o cliente o calendário mensal de entrega e o checklist de conferência antes da transmissão.',
        ],
        'validar': [
            'Arquivo gerado e validado no PVA sem erros (avisos justificados).',
            'Bloco E conferido contra a apuração de ICMS/IPI do mês.',
            'Registros 0150/0200 conferidos contra cadastros de participantes e produtos.',
        ],
        'observacoes': [
            'O Bloco K, o Bloco H (inventário) e o Bloco G (CIAP) têm trilhas próprias abaixo — o SPED Fiscal é o guarda-chuva dos três.',
        ],
        'limit': 16,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=695203229',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=634514052',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001535141-Fiscal-Arquivos-Magneticos-SPED-Fiscal',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=464972771',
        ],
        'quotas': [
            (r'boletim do ponto de entrada', 2),
            (r'\bpe - |ponto de entrada', 5),
            (r'registro 1601', 1),
        ],
        'includes': [
            (r'sped fiscal|spedfiscal|efd ?icms|efd-icms|icms/ipi', 9),
            (r'manual de utilizacao sped|matxsped|spedxfun|pcpxsped', 8),
            (r'arquivos? magneticos|arq\.? ?magneticos|fiscal arquivos magneticos', 6),
            (r'registro (c100|c110|c115|c140|c170|c197|c195|c500|c600|d100|d197|d350|e110|0150|0200|0205|0450|0460|1100|1300|1390|1400|1600|1601|1900)', 6),
            (r'bloco [cdegh019]|blocos', 5),
            (r'spedfis\d|spdfis\d|sped\d{4}|spedprod|spedregd|spedalth|spedh020|spedg126|matucomp|spedrtms|spedptms', 6),
            (r'pva|validador|schedule|schedular', 4),
            (r'cat66|cat-66|cat ?85|cat-95|portaria cat', 3),
        ],
        'excludes': r'contribuicoes|contribuiç|spedpis|spdpc|efdpiscof|efd contribuic|spedpiscof|pis/cofins arquivo|inventar|bloco h',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos', 'Contabilidade Gerencial'],
    },
    {
        'id': 'efd-contribuicoes',
        'grupo': 'agenda-09-09',
        'titulo': 'Geração da EFD Contribuições (PIS/COFINS)',
        'status': 'pendente',
        'resumo': (
            'Apuração de PIS/COFINS (e CPRB) pelas regras da EFD e geração do arquivo. A apuração nova (FISA001) '
            'substitui a antiga MATA996 e alimenta a geração FISA008 (antigo SPEDPISCOF).'
        ),
        'rotinas': [
            'FISA001 — Apuração EFD Contribuições',
            'FISA008 — Geração do arquivo EFD Contribuições',
            'FISA054 — Diferimento de PIS/COFINS',
            'MATA996 / SPEDPISCOF — rotinas legadas (sem manutenção)',
        ],
        'implantar': [
            'Processar primeiro a apuração (FISA001) e só depois gerar o arquivo (FISA008): a geração lê o que a apuração gravou.',
            'Configurar regime (cumulativo/não cumulativo), diferimento, cupom fiscal, geração de títulos e lançamentos padrão (608/611).',
            'Configurar contas contábeis por natureza/centro de custo para os registros 0500/0600 e F100.',
            'Definir tratamento de receitas financeiras, exclusão do ICMS da base (MV_DICMISE/MV_EXICMPC) e deduções (MV_DEDBPIS/MV_DEDBCOF, A2_DEDBSPC).',
            'Confirmar se há bloco P (CPRB), bloco I (imobilizado) e registros F200-F211 (incorporação) no escopo do cliente.',
        ],
        'treinar': [
            'Executar apuração e geração em homologação e validar o arquivo no PVA da EFD Contribuições.',
            'Mostrar os registros M200/M400, M210/M410 e os ajustes M220/M615 usados para correções manuais.',
            'Treinar a conferência de créditos do imobilizado e das aquisições com direito a crédito.',
        ],
        'validar': [
            'Apuração de PIS/COFINS do mês fechada e conciliada com contabilidade e financeiro.',
            'Arquivo validado no PVA sem erros e títulos gerados com natureza e vencimento corretos.',
        ],
        'observacoes': [
            'Se o cliente ainda usa MATA996/SPEDPISCOF, planejar a migração: essas rotinas não recebem mais atualização de legislação.',
        ],
        'limit': 16,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=270905514',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360028967531-Cross-Segmentos-Backoffice-Protheus-FIS-Arq-Magn%C3%A9ticos-EFD-Contribui%C3%A7%C3%B5es-Nova-Apura%C3%A7%C3%A3o-e-Gera%C3%A7%C3%A3o-do-Arquivo-FISA001-e-FISA008',
        ],
        'quotas': [
            (r'\bpe - ', 5),
            (r'registro ', 4),
        ],
        'includes': [
            (r'efd ?contribuico|efd-contribuico|sped ?contribuico|spedpiscof|fisa001|fisa008|efdpiscof|efdcon\b|apuração pis/cofins|apuracao pis/cofins', 9),
            (r'spdpc\w*|spdpis\d|spdrecbrut|sped0035|spedcp210|spedm350|spdpcimob|spdpcd|spdpcant|spdpistr|sped0140', 7),
            (r'registro (f100|f120|f130|f200|f205|f210|f211|f500|f525|m200|m210|m215|m220|m350|m400|m410|m615|a100|a110|a170|0111|0140|0500|0600|1100|1500|1800|d350|d359|0035|0145)', 6),
            (r'pis ?/ ?cofins|pis e cofins|\bcprb\b|credito presumido|deducoes da base de calculo', 5),
            (r'mv_dedbpis|mv_dedbcof|mv_dicmise|mv_exicmpc|a2_dedbspc', 6),
            (r'bloco (i|m|p|d|f|a)\b', 3),
        ],
        'excludes': r'retenciones|percepciones|argentina|\barg\b|colombia|\bmex\b',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'apuracao-icms-p9',
        'grupo': 'agenda-09-09',
        'titulo': 'Registro de Apuração de ICMS — P9 (outros créditos e débitos)',
        'status': 'pendente',
        'resumo': (
            'P9 é a rotina/estrutura de outros créditos e outros débitos da apuração de ICMS (linhas além do '
            'registro padrão), com autopreenchimento por UF — no caso do cliente, o P9AUTOTEXT.MG.'
        ),
        'rotinas': [
            'MATA953 — Apuração de ICMS (abas de outros créditos/débitos)',
            'P9AUTOTEXT.MG — autopreenchimento para Minas Gerais',
            'PE-MATR941 — Registro de apuração do ICMS (Bloco E do SPED)',
            'FIS0004 — preenchimento automático de outros débitos/créditos',
            'PE GDEBESP / GIASCDEB — guias e linhas de ajuste por código de ajuste',
        ],
        'implantar': [
            'Mapear com o cliente cada código de ajuste/outras obrigações usado na apuração de MG (créditos, estornos, incentivos, taxas).',
            'Configurar o autopreenchimento P9AUTOTEXT.MG e os cadastros de códigos de ajuste (tabela 1.11/C197 e E111).',
            'Definir geração de guias e títulos a partir das linhas de ajuste (código de receita, natureza, vencimento).',
            'Garantir que as linhas apareçam corretamente no registro de apuração do ICMS (MATR941) e no Bloco E do SPED.',
        ],
        'treinar': [
            'Exercitar a inclusão manual de um outro crédito/débito e conferir o reflexo no total da apuração e no Bloco E.',
            'Mostrar como o autopreenchimento monta as linhas e quando ele não deve ser usado.',
            'Treinar a conferência mensal: apuração x livro x SPED x guia.',
        ],
        'validar': [
            'Registro de apuração do ICMS (Bloco E) batendo com a apuração MATA953 do período.',
            'Linhas de ajuste (E111/C197) com códigos oficializados pela SEF/MG.',
        ],
        'observacoes': [
            'Priorizar os documentos específicos de Minas Gerais: P9AUTOTEXT.MG, MGREDICM (redução de base Decreto 43.080/2002) e MGIVAAJUS (IVA ajustado Conv. 198/2009).',
        ],
        'limit': 14,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=6076348',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=793212524',
        ],
        'boost': [
            (r'p9autotext\.mg|minas gerais|sintegra-mg|m940gr88|m940tp88', 25),
        ],
        'quotas': [
            (r'p9autotext\.(am|go|mt|rj|rn|sc|sp|ba|pr|rs|sc)', 3),
        ],
        'includes': [
            (r'p9autotext|bt p9autotext', 10),
            (r'outros creditos|outros debitos|preenchimento_automatico_de_outros', 8),
            (r'matr941|registro de apuracao do icms|registro apuracao icms', 8),
            (r'mata953|apuicm|apuracao de icms|apuracao do icms', 6),
            (r'codigo de ajuste|codigos de ajuste|giascdeb|gdebesp|f6_cobrec|f6_iddoc', 6),
            (r'minas gerais|sintegra-mg|m940gr88|m940tp88|mgredicm|mgivaajus', 7),
            (r'fis0004|fisa302|icms complementar|doc0057|pagina centralizadora icms', 5),
            (r'apurf6|cpapuicms|titicmst|procapur', 5),
            (r'compartilhamento das tabelas sp4, sp9|sp4|sp9', 4),
        ],
        'excludes': r'retenciones|percepciones|argentina|\barg\b|colombia',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'ciap',
        'grupo': 'agenda-09-09',
        'titulo': 'CIAP — Controle de Crédito de ICMS do Ativo Permanente',
        'status': 'pendente',
        'resumo': (
            'Controle do crédito de ICMS de bens do ativo imobilizado em 48 (ou 60) parcelas, com apropriação '
            'mensal, baixa/estorno e reflexo no Bloco G do SPED Fiscal.'
        ),
        'rotinas': [
            'MATA905 — Manutenção CIAP (SF9)',
            'MATA906 — Estorno/apropriação CIAP',
            'MATR995 — Livro/Relatório CIAP',
            'MV_FSNCIAP, MV_F9ITEM, MV_F9PL/MV_F9FRT/MV_F9ICMST/MV_F9DIF',
            'Integração com SIGAATF (SN1/N1_CODCIAP)',
        ],
        'implantar': [
            'Definir o modelo de CIAP usado (A, B, C ou D) e o tipo de numeração do bem (MV_FSNCIAP).',
            'Configurar a TES de compra de ativo: credita ICMS, atualiza ativo, material de consumo, livro fiscal de ICMS = Outros e livro fiscal CIAP = Sim.',
            'Cadastrar os bens existentes (inclusive os já apropriados em outro sistema, com parcelas residuais) na Manutenção CIAP.',
            'Definir a integração com o Ativo Fixo: o bem é classificado no SIGAATF e apropriado no MATA906.',
            'Configurar a geração do Bloco G do SPED (G125/G126/G130) a partir do CIAP.',
        ],
        'treinar': [
            'Exercitar a entrada de um bem pela nota (MATA103) e a conferência do registro criado no CIAP.',
            'Executar a apropriação mensal no MATA906 e conferir o relatório MATR995.',
            'Treinar baixa por venda/transferência/perda e o estorno do crédito remanescente.',
        ],
        'validar': [
            'Bloco G do SPED coerente com o relatório CIAP do mês.',
            'Parcelas apropriadas conferindo com o valor de ICMS creditado na entrada do bem.',
        ],
        'observacoes': [
            'Divergência clássica: Bloco G diferente do Relatório CIAP — geralmente por bem não apropriado, baixa sem estorno ou campo N1_CODCIAP não preenchido.',
        ],
        'limit': 14,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=708871751',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360035400914-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Processo-de-configura%C3%A7%C3%A3o-do-CIAP-para-gerar-o-SPED-Fiscal',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001538561-Escrita-Fiscal-CIAP',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=6076087',
        ],
        'quotas': [
            (r'\bpe - ', 4),
        ],
        'includes': [
            (r'\bciap\b', 10),
            (r'mata905|mata906|matr995|mt905mnu|mt906mnu|mt906vld|\bsf9\b|f9_|mv_f9|mv_fsnciap', 8),
            (r'ativo permanente|ativo x icms|credito de icms.{0,20}ativo', 7),
            (r'bloco g|g125|g126|g130|spedg126', 7),
            (r'n1_codciap|atfa251|atfa012|ativo fixo.{0,20}(icms|credito)', 6),
            (r'apropriacao', 3),
        ],
        'excludes': r'call center|contratos|projetos',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'bloco-k',
        'grupo': 'agenda-09-09',
        'titulo': 'Bloco K — controle da produção e do estoque',
        'status': 'pendente',
        'resumo': (
            'Bloco do SPED Fiscal que substitui o Livro de Controle de Produção e Estoque: K200 (estoque escriturado), '
            'K220 (outras movimentações internas), K230/K235 (produção e insumos), K250/K255 (industrialização em terceiros) e K280 (correções).'
        ),
        'rotinas': [
            'SPEDFISCAL — pergunta "Gerar Bloco K?"',
            'MATXSPED / PCPXSPED — fontes dos registros K',
            'MATR241 — Relação do Bloco K (analítico)',
            'SC2 (ordens de produção), SG1 (estruturas), SD3 (movimentações internas), SB2/SB6 (saldos)',
            'MV_BLKTP00 / MV_SDTESN3',
        ],
        'implantar': [
            'Confirmar a obrigatoriedade e o perfil do contribuinte (IND_ATIV do registro 0000 = industrial ou equiparado) e a periodicidade exigida pela UF.',
            'Revisar o cadastro de produtos: tipo do item (00 a 10) — só os tipos 00, 01, 02, 03, 04, 05 e 10 são enviados no K200; excluir fantasma.',
            'Revisar as TES usadas nos movimentos de produção/requisição/devolução e os indicadores de estoque (0, 1 e 2) via F4_PODER3.',
            'Garantir estruturas de produto (SG1) e ordens de produção (SC2) coerentes com o processo real, incluindo perdas declaradas na estrutura.',
            'Atualizar os fontes MATXSPED, PCPXSPED, SPEDFISCAL e SPEDXFUN antes da primeira geração.',
            'Definir como serão tratadas as perdas de processo (refugo/sucata): elas não vão no K235 e exigem documento fiscal no Bloco C.',
        ],
        'treinar': [
            'Gerar o Bloco K em homologação e conferir o MATR241 contra o estoque físico/contábil.',
            'Treinar o ciclo completo: OP -> requisição de insumos (SD3) -> apontamento de produção -> K230/K235.',
            'Mostrar o tratamento de industrialização em terceiros (K250/K255) e de desmontagem/reprocesso (K210/K215/K260/K265).',
            'Revisar as correções de apontamento (K270/K275/K280) e quando usá-las.',
        ],
        'validar': [
            'K200 batendo com o saldo final do estoque (SB2 + terceiros) do período.',
            'Arquivo validado no PVA sem erros no Bloco K e sem divergência com o Bloco C.',
        ],
        'observacoes': [
            'Lacuna do índice local preenchida com fontes oficiais: o guia geral do Bloco K no TDN e os artigos de K200 na Central de Atendimento.',
            'Para mineração, validar com o cliente se há industrialização (beneficiamento) que caracterize obrigação do Bloco K ou apenas movimentação de mercadoria.',
        ],
        'limit': 14,
        'pinned': [],
        'quotas': [
            (r'error|thread|collation|cnae', 3),
        ],
        'includes': [
            (r'bloco k', 10),
            (r'k200|k210|k215|k220|k230|k235|k250|k255|k260|k265|k270|k275|k280|k290|k300', 9),
            (r'matr241|matxsped|pcpxsped|spedfisblck|mv_blktp00', 9),
            (r'ordem de producao|ordens de producao|itens produzidos|insumos consumidos|estoque escriturado', 7),
            (r'industrializacao.{0,20}terceiros|estrutura do produto|ficha tecnica|\bsg1\b|\bsc2\b', 6),
            (r'gerar bloco k|relacao do bloco k', 8),
            (r'tipos? de produto.{0,20}registro k200|tipo do item', 5),
        ],
        'excludes': r'call center|contratos|projetos|datasul|thread error|error\.log|collation',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'registro-inventario',
        'grupo': 'agenda-09-09',
        'titulo': 'Registro de inventário (Bloco H / MATR460)',
        'status': 'pendente',
        'entrega': 'Obrigação anual entregue em fevereiro (inventário de 31/12)',
        'resumo': (
            'Inventário físico escriturado no Bloco H da EFD ICMS/IPI a partir do arquivo gerado pelo relatório '
            'Registro de Inventário Modelo 7 (MATR460), além do processo de contagem e acerto no Estoque.'
        ),
        'rotinas': [
            'MATR460 — Registro de Inventário Modelo 7 (gera arquivo para o SPED)',
            'SPEDFISCAL — perguntas "Gera Inventário", "Data de fechamento do estoque" e "Motivo do Inventário"',
            'MATA270 (digitação), MATA271 (bloqueio), MATA340 (acerto) — SIGAEST',
            'MATR280/MATR270 — lista e etiquetas de contagem',
            'PE SPEDALTH (H010) e SPEDH020 (H020)',
        ],
        'implantar': [
            'Configurar o MATR460 com "Gerar Exp. SPED Fiscal = Sim" e nome do arquivo no formato AAAAMMDD igual à data de fechamento do estoque.',
            'No SPEDFISCAL, responder "Gera Inventário = Sim", informar a mesma data de fechamento e o motivo do inventário (01 = final do período, 06 = mudança de regime etc.).',
            'Atualizar os fontes MATR460, MATXSPED e SPEDXFUN (pacote essencial dos blocos H e K).',
            'Alinhar com o Estoque o processo de contagem: etiquetas, bloqueio (MATA271), digitação (MATA270) e acerto (MATA340), incluindo MV_CONTINV para múltiplas contagens.',
            'Definir o calendário anual: fechamento em 31/12, geração do arquivo em janeiro e entrega na EFD de fevereiro.',
        ],
        'treinar': [
            'Executar um inventário de ponta a ponta em homologação: bloqueio, contagem, digitação, acerto, MATR460 e Bloco H no SPED.',
            'Treinar a conferência de saldos (SB2 x SB8 x SBF) e o uso dos relatórios de conferência (MATR460, MATR260, MATR900).',
            'Mostrar como estornar um movimento de inventário errado (MATA240/MATA241) e refazer o acerto.',
        ],
        'validar': [
            'H005/H010 gerados com os mesmos valores do MATR460 do fechamento.',
            'Arquivo validado no PVA sem erro de inventário e saldo de terceiros/em terceiros corretamente segregado.',
        ],
        'observacoes': [
            'Itens sem movimentação no período com motivo 06 têm FAQ específica no índice local.',
        ],
        'limit': 16,
        'pinned': [
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360010316131-Cross-Segmentos-Backoffice-Protheus-FIS-Arq-Magn%C3%A9ticos-SPED-FISCAL-Como-gerar-bloco-H-Invent%C3%A1rio-F%C3%ADsico-e-Controle-de-Estoque',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360020799592-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-Processo-de-Invent%C3%A1rio-Conceito-Exemplo-e-D%C3%BAvidas',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360059965954-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-Guia-do-Bloco-H-do-SPED-Fiscal-no-Protheus',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001538961-SIGAEST-INVENT%C3%81RIO',
        ],
        'quotas': [
            (r'matr460', 5),
            (r'\bpe - ', 3),
        ],
        'includes': [
            (r'registro de inventario|inventário fisico|inventario fisico', 10),
            (r'\binventar|\binventario\b|\binventário\b|inventariar', 8),
            (r'bloco h|h005|h010|h020|spedalth|spedh020|spdfis07', 8),
            (r'matr460|mata270|mata271|mata340|matr280|matr270|mv_continv|blqinvent|mv_blqinva|b2_dtinv|b2_dinvent|b1_perinv', 8),
            (r'motivo de inventario|contagem|digitação do inventario|acerto de inventario', 7),
            (r'modelo 7|mod\.? ?p?7|matr243|in 1673', 7),
            (r'saldos fisicos e financeiros|conferencia dos saldos', 5),
        ],
        'excludes': r'ativo fixo - inventario|call center|contratos|projetos|error\.log|thread error|type mismatch|could not load|collation|lock request',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    # =========================== AGENDA 11/09 ===============================
    {
        'id': 'rotinas-fiscais',
        'grupo': 'agenda-11-09',
        'titulo': 'Validação das rotinas fiscais — NF manual de entrada/saída e acertos fiscais',
        'status': 'pendente',
        'resumo': (
            'Livros Fiscais como espelho dos documentos: NF manual de entrada (MATA910) e de saída (MATA920), '
            'documentos fiscais no Compras/Faturamento (MATA103/MATA461) e a rotina de acertos fiscais (MATA900).'
        ),
        'rotinas': [
            'MATA910 — NF Manual de Entrada',
            'MATA920 — NF Manual de Saída',
            'MATA103 — Documento de Entrada (Compras)',
            'MATA461 / MATA410 — Documento e Pedido de Saída (Faturamento)',
            'MATA900 — Acertos Fiscais (SF3/SFT)',
            'MATA930 — Reprocessamento dos Livros Fiscais',
        ],
        'implantar': [
            'Definir quais documentos entram pelo Livros Fiscais (sem integração com estoque/financeiro) e quais entram pelo Compras/Faturamento.',
            'Configurar séries, espécies, numeração e o compartilhamento das tabelas fiscais.',
            'Estabelecer o procedimento de acerto fiscal: o que pode ser alterado (CFOP, base, alíquota, imposto, observações) e quem aprova.',
            'Configurar pontos de entrada apenas quando houver exigência (MA900TOK, MA920SD2, VISUIMP).',
            'Fechar o ciclo: documento -> livro fiscal (SF3/SFT) -> apuração -> SPED.',
        ],
        'treinar': [
            'Exercitar a emissão de uma NF manual de entrada e de saída e conferir o reflexo nos livros e na apuração.',
            'Treinar acertos fiscais com reprocessamento do livro (MATA930) e conferência posterior no MATRAPR.',
            'Revisar os helps mais comuns (A900CPO, AF036NF) e o procedimento de estorno/exclusão de documento.',
            'Montar com o cliente um roteiro de teste (script) com os cenários de operação mapeados na matriz do projeto.',
        ],
        'validar': [
            'Notas manuais de entrada e saída gravadas corretamente em SF3/SFT e refletidas na apuração.',
            'Acertos fiscais executados sem quebrar a integração com estoque/financeiro.',
        ],
        'observacoes': [
            'Nota fiscal de saída não é incluída diretamente no Faturamento: é preciso gerar e liberar o pedido de venda (ou usar a NF manual de saída no Livros Fiscais).',
        ],
        'limit': 16,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=654100120',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=948262833',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=702352726',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=702350726',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=702351308',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/1500010811321-Cross-Segmentos-Backoffice-Protheus-SIGAFAT-Emiss%C3%A3o-de-nota-fiscal-de-sa%C3%ADda-no-m%C3%B3dulo-Faturamento',
        ],
        'quotas': [
            (r'\bpe - ', 5),
        ],
        'includes': [
            (r'acertos fiscais|acerto de livros|mata900|ma900tok|a900cpo', 9),
            (r'nf manual|nota fiscal manual|mata910|mata920|documentos fiscais de (entrada|saida)', 9),
            (r'mata103|mata461|mata410|mata100|documento de entrada|documento de saida|nota fiscal de (entrada|saida)', 6),
            (r'mata930|reprocessamento dos livros|livros fiscais|livro fiscal|mata916|\bsf3\b|\bsft\b', 5),
            (r'ma920sd2|mta920l|visuimp|mafisobs|matr921|matr931|matr932', 6),
            (r'escrituracao|fiscal escrita|fiscal esc', 4),
            (r'nota de estorno|estorno de devolucao|exclusao.{0,15}documento', 4),
        ],
        'excludes': r'call center|contratos|projetos|orcamento|prospect|\bcrm\b|loja|varejo',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos', 'Customer Relationship Management'],
    },
    {
        'id': 'taf-extrator-reinf',
        'grupo': 'agenda-11-09',
        'titulo': 'TAF, Extrator Fiscal e EFD-REINF',
        'status': 'pendente',
        'resumo': (
            'O TAF é o módulo/aplicação que consolida e transmite as obrigações (REINF, eSocial e afins). '
            'O Protheus alimenta o TAF por meio do Extrator Fiscal (EXTFISXTAF), em arquivo TXT ou banco a banco.'
        ),
        'rotinas': [
            'EXTFISXTAF — Extrator Fiscal (módulo 09)',
            'TAFA062E / TAFA062S — documentos fiscais de entrada e saída no TAF',
            'TAFA541 (despesas processuais), TAFA537 (advogados), TAFA448/TAFA535 (processos)',
            'FKW/FKY, TAFST1/TAFST2, FKF_REINF/FK2_REINF',
            'TSS — transmissor',
        ],
        'implantar': [
            'Instalar/atualizar o TAF (versão 12, segregado do ERP quando a base for 11) e o TSS, e definir a filial centralizadora quando houver mesma chave Empresa+CNPJ+IE+Município.',
            'Configurar os layouts de extração: cadastros (T003/T007/T010), movimentos, apuração/SPED, inventário, financeiro, contribuinte e empresa.',
            'No REINF: cadastrar naturezas de rendimento nos títulos e usar a pergunta "Filtra Apenas REINF" para performance; conferir FKF_REINF/FK2_REINF após a extração.',
            'Definir tipo de integração (TXT x banco a banco) e o processo de reenvio quando a flag já estiver integrada.',
            'Planejar a carga inicial de cadastros no TAF antes da primeira transmissão.',
        ],
        'treinar': [
            'Executar o extrator em homologação e acompanhar a integração no monitor do TAF (TAFA062E/TAFA062S).',
            'Treinar o ciclo do REINF: título com natureza de rendimento -> extrator -> TAF -> DCTFWeb.',
            'Mostrar o que fazer quando um documento foi lançado antes da atualização do ambiente (lançamento manual no TAF).',
        ],
        'validar': [
            'Documentos e títulos integrados no TAF sem pendência no monitor.',
            'REINF transmitido e DCTFWeb com os valores esperados.',
        ],
        'observacoes': [
            'Com IBS/CBS calculados no Configurador de Tributos, a integração de documentos fiscais pelo Extrator não carrega esses tributos — o caminho indicado é a integração via TSI.',
            'Prazo registrado no TDN: 31/12/2026 — Extrator TAF (verificar o cronograma de descontinuação no escopo do projeto).',
        ],
        'limit': 16,
        'pinned': [
            'https://tdn.totvs.com/pages/viewpage.action?pageId=233757571',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360023075011-CROSS-Segmentos-Backoffice-Linha-Protheus-TAF-REINF-Extrator-Fiscal-Layouts-para-Reinf',
            'https://tdn.totvs.com/display/public/PROT/Protheus+-+REINF+Suporte+Financeiro',
            'https://tdn.totvs.com/pages/releaseview.action?pageId=464958325',
        ],
        'includes': [
            (r'\btaf\b|automacao fiscal|totvs automacao fiscal', 9),
            (r'extrator|extfisxtaf|extraindo informacoes fiscais', 9),
            (r'\breinf\b|efd-reinf|r-1000|r-1070|r-2010|r-2030|r-2040|r-4020|dctfweb|dctf web', 9),
            (r'natureza de rendimento|fkf_reinf|fk2_reinf|tafst|\bfkw\b|\bfky\b|fkx_tribut', 8),
            (r'tafa\d{3}|\btss\b|layout unico|monitor de integracao', 7),
            (r'integracoes? - taf|configuracoes - taf|conceitos - taf|menu do modulo - taf', 8),
        ],
        'excludes': r'esocial|s-1210|s-2500|s-2501|trabalhista|folha|salarial|pessoal|\bdrh|\bdsg|\bdserh|\btiss\b|saude',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
    {
        'id': 'revisao-parametrizacoes',
        'grupo': 'agenda-11-09',
        'titulo': 'Revisão das parametrizações conforme o escopo do projeto',
        'status': 'pendente',
        'resumo': (
            'Auditoria do que foi parametrizado contra o escopo contratado: parâmetros (SX6), TES, cadastros, '
            'Configurador de Tributos, compartilhamento de tabelas, pontos de entrada e ciclo de vida das rotinas descontinuadas.'
        ),
        'rotinas': [
            'CFGX017 — Parâmetros (MV_USASPED, MV_ESTADO, MV_ESTICM, MV_LJ..., MV_FIS...)',
            'FISA170 — Configurador de Tributos',
            'Compartilhamento de tabelas (CFGTRIB)',
            'Rotinas descontinuadas em 12/2026 e Livros Fiscais descontinuados em 2024',
        ],
        'implantar': [
            'Listar os parâmetros alterados no projeto (com valor anterior, valor atual, motivo e responsável) — evidência de auditoria.',
            'Revisar a aderência ao escopo: quais obrigações estão contempladas, quais ficaram fora e quais exigem customização.',
            'Conferir compartilhamento de tabelas e dicionário (campos criados, SX3/SIX) antes do go-live.',
            'Verificar rotinas em fim de vida (descontinuação 2024/2026) e o impacto no desenho da solução.',
            'Revisar a convivência legado x Configurador de Tributos e o cronograma de IBS/CBS (obrigatoriedade a partir de 03/08/2026).',
        ],
        'treinar': [
            'Apresentar ao cliente o mapa de parametrização (o que cada parâmetro decide) e quem pode alterar cada item.',
            'Treinar o uso do dashboard/consultas fiscais e da listagem de conferência para autochecagem mensal.',
            'Formalizar o procedimento de mudança: solicitação, análise de impacto, teste em homologação e aplicação.',
        ],
        'validar': [
            'Checklist de parametrização assinado pelo cliente, item a item do escopo.',
            'Ambiente de homologação idêntico à produção em parâmetros, TES e dicionário.',
        ],
        'observacoes': [
            'Usar o pacote FISA170 já existente em docs/fisa170/ (matriz de levantamento e ciclos de operação) como instrumento da revisão.',
        ],
        'limit': 16,
        'pinned': [
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/42351363577623-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Adequa%C3%A7%C3%A3o-%C3%A0-obrigatoriedade-do-IBS-e-CBS-a-partir-de-03-de-agosto-de-2026',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=876220090',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=945408020',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=841682134',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=1063922688',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=863302293',
        ],
        'quotas': [
            (r'descontinuad', 2),
            (r'\bmv_', 3),
        ],
        'includes': [
            (r'escopo de atendimento', 9),
            (r'parametros - (icms|iss|pis|icms-st)|parametro|parâmetro|mv_\w+', 5),
            (r'configuracoes - |outras configuracoes|configurações - ', 5),
            (r'compartilhamento de tabelas|compartilhamento das tabelas|dicionario', 6),
            (r'descontinuad|ciclo de vida|rotinas que serao descontinuadas', 7),
            (r'boas praticas|checklist|dashboard fiscal|listagem de conferencia|facilitadores', 6),
            (r'ib[s]\/? ?cbs|reforma tributaria|adequacao a obrigatoriedade', 6),
            (r'pacotes de atualizacao|expedicao continua|expedição contínua', 5),
            (r'fisa170|configurador de tributos', 5),
        ],
        'excludes': r'call center|contratos|projetos|crm|orcamento|tabela de preco|salarial|ferias|ponto|turno',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos', 'Customer Relationship Management'],
    },
    {
        'id': 'quebra-estoque',
        'grupo': 'agenda-11-09',
        'titulo': 'Quebra de estoque (perdas, refugo e baixas)',
        'status': 'pendente',
        'resumo': (
            'Baixa de mercadoria por perda, roubo, deterioração ou quebra de processo: movimento interno no Estoque, '
            'documento fiscal correspondente (CFOP 5.927/6.927 ou nota de débito) e estorno do crédito de ICMS/IPI/PIS/COFINS.'
        ),
        'rotinas': [
            'MATA241 — Movimentos Internos múltiplos (MATA240 descontinuada)',
            'MATA340 — Acerto de Inventário',
            'Documento de Débito no Faturamento (tipo "Perda em Estoque")',
            'MV_ESTNEG, MA240NEGAT/MA240NEGLT',
            'Bloco K — tratamento de perdas (K235 x documento fiscal no Bloco C)',
        ],
        'implantar': [
            'Definir com o cliente o conceito de quebra no processo dele (perda de processo, refugo, deterioração, extravio) e onde ela é registrada.',
            'Criar TES/cenário de baixa sem financeiro, com CFOP adequado e escrituração fiscal correta (estorno de crédito quando aplicável).',
            'Configurar MV_ESTNEG e as validações de saldo para evitar baixas indevidas.',
            'Estabelecer evidência documental da perda (laudo, boletim, seguro) e a rotina de aprovação.',
            'Garantir que a perda alimente corretamente o Bloco H (inventário), o Bloco K e a apuração (estorno de crédito).',
        ],
        'treinar': [
            'Exercitar a baixa por movimento interno e a conferência do reflexo fiscal (livro, apuração, SPED).',
            'Treinar o estorno de um movimento de inventário/acerto errado (MATA241, F12 -> por item).',
            'Mostrar a emissão do documento fiscal de perda e o estorno de crédito correspondente.',
        ],
        'validar': [
            'Perda registrada com documento fiscal e estorno de crédito conferido na apuração do mês.',
            'Saldo físico (SB2) coerente com SB8/SBF e com o Bloco H/K.',
        ],
        'observacoes': [
            'Lacuna do índice local: havia pouquíssimas fontes sobre perda/quebra. Foram incorporados artigos oficiais de SIGAEST e SIGAFAT (nota de débito de perda em estoque, estorno de inventário, MV_ESTNEG).',
            'No Bloco K só entram as perdas declaradas na estrutura do produto; refugo e sucata de processo exigem documento fiscal demonstrado no Bloco C.',
        ],
        'limit': 14,
        'pinned': [
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/37327450272023-Cross-Segmentos-Backoffice-Protheus-SIGAFAT-Como-emitir-uma-Nota-de-D%C3%A9bito-de-Perda-em-Estoque-tpNFDebito-07',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/4402384407063-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-Como-realizar-o-estorno-exclus%C3%A3o-de-movimento-de-Invent%C3%A1rio',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/360058347413-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-MA240NEGAT-Principais-situa%C3%A7%C3%B5es-que-podem-apresentar-esse-help',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001550102-SIGAEST-MOVIMENTA%C3%87%C3%95ES',
        ],
        'includes': [
            (r'quebra|perda em estoque|nota de debito de perda|perda material', 9),
            (r'refugo|sucata|deteriora|furto|roubo|extravio|inutiliza', 8),
            (r'movimento.{0,10}interno|mata240|mata241|mata310|ma240negat|mv_estneg|\bsd3\b|d3_cf|tipos de movimentos internos', 7),
            (r'requisi(ca|ç)ao|desmontagem|estorno.{0,15}(inventario|movimento)|baixa de estoque', 6),
            (r'estorno de credito|estorno do credito|cfop 5927|5\.927|6\.927', 7),
            (r'inventario', 3),
        ],
        'excludes': r'call center|contratos|projetos|crm|salarial|folha|ferias|plano de contas|medicao|orcamento|tiss|quebra de linha|distrito federal|dfestcred|interfunctioncall|a240num|dt quebra|advpr|ctbr|thread error|nota inutilizada|decreto 64|icms st',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos', 'Contabilidade Gerencial', 'Customer Relationship Management'],
    },
    {
        'id': 'exportacao',
        'grupo': 'agenda-11-09',
        'titulo': 'Exportação',
        'status': 'pendente',
        'resumo': (
            'Operações de exportação direta e indireta: nota fiscal de exportação, formação de lote, DU-E no Portal Único '
            'Siscomex, câmbio e integrações do Easy Export Control (SIGAEEC) com Faturamento, Fiscal e Financeiro.'
        ),
        'rotinas': [
            'SIGAEEC — Easy Export Control (pedido, embarque, notas fiscais EECNF400)',
            'Transmissão DUE (DU-E) no Siscomex/Portal Único',
            'MATA410/MATA461 — pedido e documento de saída no Faturamento',
            'MV_EECFAT — integração SIGAEEC x SIGAFAT',
            'Easy Drawback Control (SIGAEDC)',
        ],
        'implantar': [
            'Definir o desenho da operação: exportação direta, indireta (trading/comercial exportadora), remessa com fim específico, drawback.',
            'Configurar cadastros: cliente estrangeiro, moeda, condição de pagamento/câmbio, TES de exportação (imunidade/não incidência de ICMS, IPI, PIS/COFINS) e CFOP 7.xxx.',
            'Configurar MV_EECFAT e a integração das notas de saída com o SIGAEEC (mensagem INVOICE / adapter EECNF400) para composição do lote de exportação.',
            'Configurar a DU-E: geração, vinculação das notas (inclusive quebra de lote), drawback e retificação.',
            'Definir tratamento de variação cambial (eventos 580/581), nota complementar de preço e títulos de câmbio.',
        ],
        'treinar': [
            'Exercitar o fluxo completo: pedido de venda -> nota de exportação -> embarque -> DU-E -> câmbio.',
            'Treinar a emissão de nota complementar de exportação e o impacto da variação cambial na contabilidade.',
            'Revisar a escrituração fiscal da exportação (imunidade/não incidência) e o reflexo na apuração e no SPED.',
        ],
        'validar': [
            'DU-E transmitida e averbada, com notas fiscais corretamente vinculadas.',
            'Apuração sem débito de ICMS/IPI/PIS/COFINS nas exportações, conforme regime do cliente.',
        ],
        'observacoes': [
            'Para mineração, confirmar com o cliente se há drawback, exportação por conta e ordem ou formação de lote com quebra — cada cenário muda a parametrização da DU-E.',
        ],
        'limit': 14,
        'pinned': [
            'https://tdn.totvs.com/pages/releaseview.action?pageId=455802907',
            'https://tdn.totvs.com/pages/releaseview.action?pageId=444609121',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001534681-Easy-Export-Control-SIGAEEC',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=284872382',
            'https://centraldeatendimento.totvs.com/hc/pt-br/sections/1500001546322-Easy-Drawback-Control-SIGAEDC',
        ],
        'quotas': [
            (r'easy import control|importa(ca|ç)|siscomex|siscoserv', 2),
        ],
        'includes': [
            (r'exporta(ca|ç)(ao|ões)|export control|sigaeeC|eecnf400|\bdu-e\b|declaracao unica de exportacao', 9),
            (r'drawback|sigaedc|siscoserv|sigaess|portal unico|siscomex', 8),
            (r'embarque|cambio|variação cambial|variacao cambial|comercio exterior', 6),
            (r'nota fiscal de exportacao|nota complementar no exportacao|lote de exportacao', 8),
            (r'mv_eecfat|eectp100|eeCAF22\d', 7),
            (r'importacao|desembaraco|easy import', 2),
        ],
        'excludes': r'importacao/exportacao do plano de contas|exportação da co|plano de contas|call center|contratos|projetos|crm|easy import control|desembaraco|entreposto|licenca de import|purchase|solicit\. de importacao|importacao de arquivo',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos', 'Contabilidade Gerencial'],
    },
    # =========================== TRANSVERSAL ================================
    {
        'id': 'treinamento-oficial',
        'grupo': 'transversal',
        'titulo': 'Materiais oficiais de treinamento e referência',
        'status': 'apoio',
        'resumo': (
            'Guias, manuais, webinars, eventos tira-dúvidas e bancos de conhecimento usados para capacitar o time '
            'do cliente em qualquer um dos tópicos da trilha.'
        ),
        'rotinas': [
            'Banco de Conhecimento - Fiscal (BC)',
            'Webinars e Treinamentos do Configurador de Tributos (FISA170)',
            'SUP.PROTHEUS - Eventos Tira Dúvidas',
            'Manuais: SPED Fiscal, CIAP, Extrator Fiscal, Apuração EFD Contribuições',
        ],
        'implantar': [
            'Definir a trilha de capacitação por perfil: usuário operacional, analista fiscal e key user/administrador.',
            'Agendar os treinamentos oficiais (eventos tira-dúvidas e webinars) e registrar as gravações no material do projeto.',
            'Montar o material do treinamento interno a partir dos guias oficiais, sempre com o print do ambiente do cliente.',
        ],
        'treinar': [
            'Usar os guias de referência como apostila e os FAQs/BC como material de consulta pós-treinamento.',
            'Aplicar exercícios práticos no ambiente de homologação ao final de cada tópico da trilha.',
            'Registrar presença e avaliação de cada sessão para evidência de entrega do projeto.',
        ],
        'validar': [
            'Usuários executando sozinhos o ciclo mensal (documentos -> apuração -> SPED -> TAF).',
            'Material de treinamento versionado e entregue ao cliente.',
        ],
        'observacoes': [],
        'limit': 16,
        'pinned': [
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/40308222614551-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-SIGAFIS-Webinars-e-Treinamentos-do-Configurador-de-Tributos-FISA170',
            'https://centraldeatendimento.totvs.com/hc/pt-br/articles/26426594441751-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Agendas-de-Eventos-EXCLUSIVA-PARA-CONSULTORES-TOTVS-Configurador-de-Tributos',
            'https://tdn.totvs.com/pages/releaseview.action?pageId=550307175',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=514454190',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=654284086',
            'https://tdn.totvs.com/pages/viewpage.action?pageId=719662649',
        ],
        'includes': [
            (r'webinar|treinamento|tira duvidas|eventos|agenda de eventos', 9),
            (r'banco de conhecimento|bc - |bc-faq|bc faq', 8),
            (r'manual de utilizacao|guia de referencia|guia prático|guia pratico|documento de referencia', 8),
            (r'conceitos - |conceito e |visao geral', 6),
            (r'dashboard fiscal|smartview|smart view|listagem de conferencia|facilitadores|consultas - fiscal', 5),
            (r'how to|como funciona', 3),
        ],
        'excludes': r'argentina|\barg\b|colombia|\bmex\b|peru|chile|equador|localizacion|espanol|retenciones|percepciones|trabalhista|s-2500|s-2501|evento s-|smart view - livros fiscais de vendas',
        'exclude_modules': ['Call Center', 'Gestão de Contratos', 'Gestão de Projetos'],
    },
]

# ---------------------------------------------------------------------------
# Classificação por intenção de uso
# ---------------------------------------------------------------------------
INTENCOES = [
    ('customizar', r'\bpe - |ponto de entrada|pontos de entrada|\bpe-|boletim do ponto de entrada|customiz|advpl|mile\b|execauto|funcao ma|função ma'),
    ('suportar', r'\bfaq\b|help\b|\berro\b|rejei(ca|ç)(ao|ões)|divergen|por que|problema|\bdt\b|how to|nao gera|não gera|mensagem de|alerta|invalid|travamento|estouro|overflow'),
    ('treinar', r'webinar|treinamento|tira duvidas|evento|conceito|manual|guia|apostila|banco de conhecimento|\bbc - |visao geral|como funciona|smart ?view|dashboard|listagem|curso|capacita'),
    ('implantar', r'configura|parametr|parâmetr|cadastro|implanta|passo a passo|como (gerar|calcular|configurar|utilizar|realizar|preencher|fazer)|processo de|geracao|geração|apuração|apuracao|rotina|procedimento|\bmv_|instala'),
]

INTENCAO_ORDEM = ['implantar', 'treinar', 'customizar', 'suportar']
INTENCAO_TITULO = {
    'implantar': 'Para implantar / parametrizar',
    'treinar': 'Para treinar (conceito, guia e material oficial)',
    'customizar': 'Pontos de entrada e customizações (ADVPL)',
    'suportar': 'Suporte, FAQ e resolução de erros',
}


def classificar(titulo: str) -> str:
    texto = norm(titulo)
    for intencao, padrao in INTENCOES:
        if re.search(padrao, texto):
            return intencao
    return 'implantar'


def rotulo(titulo: str) -> str:
    """Rótulo curto para exibição: muitos artigos vêm com a seção na frente (`Seção > Artigo`)."""
    partes = [parte.strip() for parte in titulo.split(' > ') if parte.strip()]
    if len(partes) > 1:
        return partes[-1]
    return titulo


def chave_dedupe(titulo: str) -> str:
    """Chave para não repetir o mesmo artigo que entrou por dois índices diferentes."""
    texto = norm(titulo)
    texto = re.sub(r'^\d{6,}\s*', '', texto)          # id de artigo colado no slug
    texto = re.sub(r'^pe\s*[-\s]*', '', texto)         # prefixo de ponto de entrada
    texto = re.sub(r'[^a-z0-9]+', '', texto)
    return texto[-90:]


CAP_INTENCAO = {'customizar': 0.34, 'suportar': 0.28}


def selecionar(registros: list[dict], topico: dict) -> tuple[list[dict], int]:
    """Retorna (links selecionados, total de candidatos) para um tópico."""
    includes = [(re.compile(padrao), peso) for padrao, peso in topico['includes']]
    boosts = [(re.compile(padrao), peso) for padrao, peso in topico.get('boost', [])]
    excludes = re.compile(topico['excludes']) if topico.get('excludes') else None
    excl_modulos = set(topico.get('exclude_modules') or [])
    quotas = [(re.compile(padrao), int(maximo)) for padrao, maximo in topico.get('quotas', [])]
    limite = int(topico.get('limit') or LIMITE_PADRAO)

    candidatos: list[tuple[int, dict]] = []
    for registro in registros:
        titulo = norm(registro['title'])
        if len(titulo.strip()) < 5:      # sobra de índice sem título real
            continue
        if registro['module'] in excl_modulos:
            continue
        if excludes and excludes.search(titulo):
            continue
        pontuacao = 0
        for padrao, peso in includes:
            if padrao.search(titulo):
                pontuacao += peso
        if pontuacao <= 0:
            continue
        for padrao, peso in boosts:
            if padrao.search(titulo):
                pontuacao += peso
        if len(registro['title']) <= 70:      # guia oficial curto tende a ser a referência principal
            pontuacao += 2
        if 'trilha fiscal' in titulo:         # complemento curado para este projeto
            pontuacao += 3
        candidatos.append((pontuacao, registro))

    total = len(candidatos)
    candidatos.sort(key=lambda item: (-item[0], item[1]['title'].lower()))

    pinned = [url for url in topico.get('pinned', []) if isinstance(url, str)]
    por_url = {registro['url']: registro for _, registro in candidatos}
    todos = {registro['url']: registro for registro in registros}

    selecionados: list[dict] = []
    vistos: set[str] = set()
    chaves: set[str] = set()
    usos_quota: dict[str, int] = {}
    usos_intencao: dict[str, int] = {}
    limites_intencao = {
        intencao: max(1, round(limite * proporcao)) for intencao, proporcao in CAP_INTENCAO.items()
    }

    def aceitar(registro: dict, ignorar_limites: bool = False) -> bool:
        if registro['url'] in vistos:
            return False
        chave = chave_dedupe(registro['title'])
        if chave and chave in chaves:
            return False
        intencao = classificar(registro['title'])
        titulo_norm = norm(registro['title'])
        if not ignorar_limites:
            if usos_intencao.get(intencao, 0) >= limites_intencao.get(intencao, limite):
                return False
            for indice, (padrao, maximo) in enumerate(quotas):
                if padrao.search(titulo_norm) and usos_quota.get(str(indice), 0) >= maximo:
                    return False
        for indice, (padrao, _) in enumerate(quotas):
            if padrao.search(titulo_norm):
                usos_quota[str(indice)] = usos_quota.get(str(indice), 0) + 1
        usos_intencao[intencao] = usos_intencao.get(intencao, 0) + 1
        vistos.add(registro['url'])
        if chave:
            chaves.add(chave)
        selecionados.append(registro)
        return True

    # Fontes fixadas pela curadoria entram sempre (são a referência oficial do tópico).
    for url in pinned:
        registro = por_url.get(url) or todos.get(url)
        if registro is None or len(selecionados) >= limite:
            continue
        aceitar(registro, ignorar_limites=True)

    for _, registro in candidatos:
        if len(selecionados) >= limite:
            break
        aceitar(registro)

    return selecionados, total


def montar_links(selecionados: list[dict]) -> list[dict]:
    links = []
    for registro in selecionados:
        links.append({
            'id': registro['id'],
            'title': registro['title'],
            'label': rotulo(registro['title']),
            'url': registro['url'],
            'module': registro['module'],
            'moduleCode': registro['moduleCode'],
            'source': registro['source'],
            'linkType': registro['linkType'],
            'intent': classificar(registro['title']),
        })
    links.sort(key=lambda link: (INTENCAO_ORDEM.index(link['intent']), link['label'].lower()))
    return links


def gerar() -> dict:
    if not KNOWLEDGE_PATH.exists():
        raise SystemExit('knowledge.json não encontrado. Rode scripts/build_knowledge.py antes.')
    base = json.loads(KNOWLEDGE_PATH.read_text(encoding='utf-8'))
    registros = base['records']

    topicos_saida = []
    for topico in TOPICOS:
        selecionados, total = selecionar(registros, topico)
        topicos_saida.append({
            'id': topico['id'],
            'grupo': topico['grupo'],
            'titulo': topico['titulo'],
            'status': topico['status'],
            'entrega': topico.get('entrega', ''),
            'resumo': topico['resumo'],
            'rotinas': topico['rotinas'],
            'implantar': topico['implantar'],
            'treinar': topico['treinar'],
            'validar': topico['validar'],
            'observacoes': topico['observacoes'],
            'totalCandidatos': total,
            'links': montar_links(selecionados),
        })

    payload = {
        'version': 1,
        'generatedAt': date.today().isoformat(),
        'projeto': PROJETO,
        'descricao': (
            'Trilha de implantação e treinamento fiscal montada a partir do índice local de links '
            '(TDN e Central de Atendimento TOTVS). Cada tópico traz o que implantar, o que treinar, '
            'como validar e as fontes oficiais encontradas na base.'
        ),
        'totalLinksBase': base['total'],
        'grupos': GRUPOS,
        'intencoes': [{'id': chave, 'titulo': INTENCAO_TITULO[chave]} for chave in INTENCAO_ORDEM],
        'topicos': topicos_saida,
    }
    return payload


def escrever_json(payload: dict) -> None:
    TRILHAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRILHAS_PATH.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


def render_markdown(payload: dict) -> dict[str, str]:
    grupos = {grupo['id']: grupo for grupo in payload['grupos']}
    docs: dict[str, str] = {}

    # ---- arquivos por grupo -------------------------------------------------
    arquivos_grupo = {
        'concluidos': '01-topicos-concluidos.md',
        'agenda-09-09': '02-agenda-09-09.md',
        'agenda-11-09': '03-agenda-11-09.md',
        'transversal': '04-treinamento-oficial.md',
    }
    for grupo_id, arquivo in arquivos_grupo.items():
        grupo = grupos[grupo_id]
        linhas = [
            f"# {grupo['titulo']}",
            '',
            f"> {grupo['descricao']}",
            '',
            f"Projeto: **{payload['projeto']}**  ·  Gerado em {payload['generatedAt']}  ·  "
            f"Base local com {payload['totalLinksBase']} links.",
            '',
        ]
        for numero, topico in enumerate([t for t in payload['topicos'] if t['grupo'] == grupo_id], start=1):
            linhas += render_topico(numero, topico)
        docs[arquivo] = '\n'.join(linhas).rstrip() + '\n'

    # ---- README -------------------------------------------------------------
    linhas = [
        '# Trilha de implantação e treinamento — Fiscal Protheus 12',
        '',
        f"Projeto: **{payload['projeto']}**. Dossiê gerado por `scripts/gerar_trilha_treinamento.py` "
        f"a partir do índice local (`client/public/knowledge.json`, {payload['totalLinksBase']} links do TDN e da "
        'Central de Atendimento TOTVS). Nenhum link aqui é inventado: todos existem na base versionada do repositório.',
        '',
        '## Como usar',
        '',
        '1. Abra o arquivo da agenda correspondente e siga a ordem **Implantar → Treinar → Validar → Fontes**.',
        '2. Cada fonte está classificada por intenção: implantar/parametrizar, treinar (guia, conceito, webinar), '
        'ponto de entrada (customização ADVPL) e suporte/FAQ.',
        '3. No site estático, a aba **Trilha** carrega `client/public/trilhas.json` e mostra o mesmo conteúdo com links clicáveis.',
        '',
        '## Arquivos',
        '',
        '| Arquivo | Conteúdo |',
        '| --- | --- |',
        '| `01-topicos-concluidos.md` | Cadastros fiscais, TES, configuração de tributos, DIFAL, apuração e impostos retidos (revisão + treinamento) |',
        '| `02-agenda-09-09.md` | EFD ICMS/IPI, EFD Contribuições, Apuração de ICMS-P9, CIAP, Bloco K e registro de inventário |',
        '| `03-agenda-11-09.md` | Rotinas fiscais (NF manual e acertos), TAF/Extrator/REINF, revisão de parametrizações, quebra de estoque e exportação |',
        '| `04-treinamento-oficial.md` | Materiais oficiais de capacitação (webinars, eventos tira-dúvidas, guias e BC) |',
        '| `05-cobertura-e-lacunas.md` | Quantos links a base tem por tópico e onde foi preciso complementar |',
        '| `trilha.json` | Saída estruturada consumida pelo site (`client/public/trilhas.json`) |',
        '',
        '## Regenerar',
        '',
        '```bash',
        'python3 scripts/build_knowledge.py            # atualiza o índice local',
        'python3 scripts/gerar_trilha_treinamento.py   # regenera dossiê + trilhas.json',
        'python3 scripts/gerar_trilha_treinamento.py --check  # falha se algum tópico ficar sem fonte',
        '```',
        '',
        '## Tópicos e cobertura',
        '',
        '| # | Tópico | Grupo | Status | Links na base | Selecionados |',
        '| --- | --- | --- | --- | --- | --- |',
    ]
    for numero, topico in enumerate(payload['topicos'], start=1):
        linhas.append(
            f"| {numero} | {topico['titulo']} | {grupos[topico['grupo']]['titulo'].split(' — ')[0]} | "
            f"{topico['status']} | {topico['totalCandidatos']} | {len(topico['links'])} |"
        )
    docs['README.md'] = '\n'.join(linhas).rstrip() + '\n'

    # ---- cobertura e lacunas -------------------------------------------------
    linhas = [
        '# Cobertura da base e lacunas da trilha',
        '',
        'Leitura gerada automaticamente: quantos links do índice local casam com cada tópico e quais tópicos '
        'precisaram de complemento externo (páginas oficiais localizadas em 2026-09-11 e versionadas em '
        '`data/indices/Indice_Trilha_Complementos.txt`).',
        '',
        '| Tópico | Candidatos na base | Selecionados | Complementos usados | Situação |',
        '| --- | --- | --- | --- | --- |',
    ]
    for topico in payload['topicos']:
        complementos = sum(1 for link in topico['links'] if 'trilha fiscal' in link['title'].lower())
        total = topico['totalCandidatos']
        if total == 0:
            situacao = '❌ sem fonte na base'
        elif total < 5:
            situacao = '⚠️ cobertura fraca — complementar'
        elif complementos >= max(2, len(topico['links']) // 3):
            situacao = '⚠️ dependente de complemento'
        else:
            situacao = '✅ cobertura própria'
        linhas.append(
            f"| {topico['titulo']} | {total} | {len(topico['links'])} | {complementos} | {situacao} |"
        )
    linhas += [
        '',
        '## O que foi incorporado como complemento',
        '',
        'Os 34 links de `data/indices/Indice_Trilha_Complementos.txt` cobrem as lacunas encontradas:',
        '',
        '- **Bloco K** — só havia 1 ponto de entrada na base; entraram o guia geral do Bloco K no TDN, os artigos de '
        'K200 (tabelas, tipos de produto) e a seção Legais/Fiscais do Estoque.',
        '- **Registro de inventário** — entraram o passo a passo do Bloco H, o processo de inventário do SIGAEST '
        '(MATA270/MATA271/MATA340), os relatórios de conferência (MATR460) e a página de eventos tira-dúvidas com material.',
        '- **CIAP** — entraram a página oficial do CIAP (modelos A/B/C/D, MV_FSNCIAP) e o processo de configuração para gerar o SPED.',
        '- **EFD Contribuições** — entraram o manual da apuração FISA001 e o artigo FISA001/FISA008 (substituição de MATA996/SPEDPISCOF).',
        '- **TAF/Extrator/REINF** — entraram o guia do Extrator Fiscal (EXTFISXTAF), o suporte financeiro do REINF, '
        'a documentação de EFD-Reinf no TAF e os layouts de extração.',
        '- **Impostos retidos / PCC** — entraram as Regras Financeiras do Configurador de Tributos (data base de vencimento '
        'e cumulatividade), os artigos de retenção e cumulatividade de PIS/COFINS/CSLL e a aglutinação FINA378/FINA381.',
        '- **Quebra de estoque** — entraram a nota de débito de perda em estoque, o estorno de movimento de inventário e o MV_ESTNEG.',
        '- **Exportação** — entraram a DU-E no SIGAEEC, a integração por mensagem única (EAI), a vinculação de notas para '
        'formação de lote (EECNF400) e os artigos de nota complementar/título de câmbio.',
        '- **Rotinas fiscais** — entrou o artigo sobre emissão de nota fiscal de saída no Faturamento (pedido + liberação).',
        '- **Revisão de parametrização** — entrou a documentação de adequação ao IBS/CBS obrigatório a partir de 03/08/2026.',
        '',
        '## Lacunas que continuam abertas (ação sugerida)',
        '',
        '- **Mineração**: não há na base conteúdo fiscal específico de mineração (CFEM, exportação de minério, '
        'Lei Kandir). Se o escopo incluir esses temas, é preciso abrir chamado/consultoria específica na TOTVS.',
        '- **Bloco K em mineração**: confirmar se o beneficiamento do minério caracteriza industrialização para fins '
        'do Bloco K (IND_ATIV do registro 0000) — decisão de escopo, não de documentação.',
        '- **Quebra de estoque**: o conceito fiscal de perda (estorno de crédito, CFOP 5.927) precisa ser homologado '
        'com a SEF/MG; a documentação da TOTVS cobre a mecânica, não a tese tributária.',
        '- **PCC com vencimento incorreto**: item aberto no tópico de impostos retidos; a correção passa por '
        'MV_BX10925/MV_VCPCCP e pelas regras financeiras do Configurador de Tributos.',
        '',
    ]
    docs['05-cobertura-e-lacunas.md'] = '\n'.join(linhas).rstrip() + '\n'

    docs['trilha.json'] = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    return docs


def render_topico(numero: int, topico: dict) -> list[str]:
    linhas = [
        f"## {numero}. {topico['titulo']}",
        '',
        f"**Status:** `{topico['status']}`"
        + (f"  ·  **Entrega:** {topico['entrega']}" if topico.get('entrega') else '')
        + f"  ·  **Fontes na base:** {topico['totalCandidatos']} candidatas, {len(topico['links'])} selecionadas.",
        '',
        topico['resumo'],
        '',
        '**Rotinas e objetos técnicos**',
        '',
    ]
    linhas += [f'- `{item}`' for item in topico['rotinas']]
    linhas += ['', '**Como implantar**', '']
    linhas += [f'{i}. {item}' for i, item in enumerate(topico['implantar'], start=1)]
    linhas += ['', '**Como treinar**', '']
    linhas += [f'- {item}' for item in topico['treinar']]
    linhas += ['', '**Como validar (evidência de entrega)**', '']
    linhas += [f'- {item}' for item in topico['validar']]

    if topico['observacoes']:
        linhas += ['', '**Observações do projeto**', '']
        linhas += [f'- {item}' for item in topico['observacoes']]

    linhas += ['', '**Fontes no índice local**', '']
    por_intencao: dict[str, list[dict]] = {}
    for link in topico['links']:
        por_intencao.setdefault(link['intent'], []).append(link)
    for intencao in INTENCAO_ORDEM:
        grupo_links = por_intencao.get(intencao)
        if not grupo_links:
            continue
        linhas += [f'*{INTENCAO_TITULO[intencao]}*', '']
        for link in grupo_links:
            origem = 'TDN' if link['source'] == 'TDN' else 'Central TOTVS'
            complemento = ' · complemento da trilha' if 'trilha fiscal' in link['title'].lower() else ''
            linhas.append(f"- [{link['title']}]({link['url']}) — {link['module']} ({origem}){complemento}")
        linhas.append('')
    linhas.append('---')
    linhas.append('')
    return linhas


def main() -> int:
    parser = argparse.ArgumentParser(description='Gera a trilha de implantação e treinamento fiscal.')
    parser.add_argument('--check', action='store_true', help='falha se algum tópico ficar sem fonte na base')
    args = parser.parse_args()

    payload = gerar()
    escrever_json(payload)
    docs = render_markdown(payload)

    DOCS_ROOT.mkdir(parents=True, exist_ok=True)
    for nome, conteudo in docs.items():
        destino = DOCS_ROOT / nome
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(conteudo, encoding='utf-8')

    print(f"Trilha gerada: {len(payload['topicos'])} tópicos · {TRILHAS_PATH}")
    for topico in payload['topicos']:
        print(f"  - {topico['titulo']}: {len(topico['links'])}/{topico['totalCandidatos']} links")
    print(f"Documentação: {DOCS_ROOT}")

    if args.check:
        vazios = [t['titulo'] for t in payload['topicos'] if not t['links']]
        if vazios:
            print('ERRO: tópicos sem fonte na base: ' + ', '.join(vazios), file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

# Fim do arquivo
