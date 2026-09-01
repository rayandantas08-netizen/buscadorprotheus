#!/usr/bin/env python3
"""Gera a planilha de ciclos de operação (Excel) no mesmo formato da tabela
"1. A operação não é uma, é um ciclo" de docs/fisa170/03-caso-demonstracao-sp.md,
ampliada para 18 ciclos completos de CFOP de saída x CFOP de entrada.

Uso:
    python3 scripts/gerar_ciclos_operacoes_xlsx.py
    python3 scripts/gerar_ciclos_operacoes_xlsx.py --saida caminho/arquivo.xlsx

Dependência: openpyxl (pip install openpyxl)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = Path(__file__).resolve().parents[1]
SAIDA_PADRAO = RAIZ / "docs" / "fisa170" / "gerado" / "ciclos-operacoes-fisa170.xlsx"

# ---------------------------------------------------------------------------
# Paleta (tema técnico escuro do projeto, adaptado para impressão)
# ---------------------------------------------------------------------------
AZUL_ESCURO = "1F2937"
AZUL_MEDIO = "2563EB"
CINZA_FAIXA = "F1F5F9"
BRANCO = "FFFFFF"
VERDE_OK = "DCFCE7"
VERDE_TXT = "166534"
AMBAR = "FEF3C7"
AMBAR_TXT = "92400E"
VERMELHO = "FEE2E2"
VERMELHO_TXT = "991B1B"

BORDA = Border(*[Side(style="thin", color="D1D5DB")] * 4)

STATUS_LEVANTADO = "levantado"
STATUS_PARCIAL = "parcial"
STATUS_FALTANDO = "faltando"

NAO_ONEROSA_IBS = "410 / 410999 (confirmar 550 se o entendimento for suspensão)"
TRIBUTADA_IBS = "000 / 000001 (tributação integral) — confirmar"

# ---------------------------------------------------------------------------
# Dados: 18 ciclos de operação
# Cada movimento: (# , movimento, quem emite, CFOP saída, CFOP entrada,
#                  ICMS, IPI/PIS/COFINS, IBS/CBS, cBenef/base legal,
#                  TES/módulo, status, cód. matriz, o que confirmar)
# ---------------------------------------------------------------------------
CICLOS: list[dict] = [
    {
        "nome": "Demonstração / mostruário",
        "grupo": "demonstracao",
        "base": "Ajuste SINIEF 02/2018; RICMS-SP art. 319 a 325; cBenef SP053190",
        "movimentos": [
            (
                1,
                "Envio para demonstração",
                "remetente",
                "5.912 (SP→SP) / 6.912 (SP→fora)",
                "1.912 / 2.912",
                "CST 50 — suspensão, sem destaque",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "SP053190 (suspensão até a transmissão da propriedade)",
                "TES 704 — SIGAFAT",
                STATUS_LEVANTADO,
                "DEM-001 / DEM-002",
                "Já levantado: validar cBenef na saída interestadual 6.912",
            ),
            (
                2,
                "Retorno da mercadoria (prazo de 60 dias)",
                "destinatário (ou NF de entrada do remetente, se não contribuinte)",
                "5.913 / 6.913",
                "1.913 / 2.913",
                "CST 50 — suspensão encerrada sem débito",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "confirmar se usa SP053190 ou código próprio",
                "TES de entrada a definir — SIGAFAT/SIGACOM",
                STATUS_FALTANDO,
                "DEM-003",
                "CFOP e prazo de retorno; quem emite quando o detentor não é contribuinte",
            ),
            (
                3,
                "Transmissão da propriedade (venda ao detentor)",
                "remetente",
                "5.102 / 6.102 (5.101 / 6.101 se produção própria)",
                "1.102 / 2.102",
                "CST 00/20 — tributado, encerra a suspensão",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem cBenef; referenciar a NF de remessa",
                "TES de venda a definir — SIGAFAT",
                STATUS_FALTANDO,
                "DEM-004",
                "CFOP/CST da venda e como referenciar a chave da remessa no XML",
            ),
            (
                4,
                "Retorno simbólico após a venda",
                "detentor da mercadoria",
                "5.949 / 6.949",
                "1.949 / 2.949",
                "CST 90 — sem débito (movimento simbólico)",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "confirmar exigência da SEFAZ-SP",
                "TES simbólica a definir",
                STATUS_FALTANDO,
                "DEM-005",
                "O cliente emite retorno simbólico ou o fluxo é dispensado na sua UF?",
            ),
        ],
    },
    {
        "nome": "Consignação mercantil",
        "grupo": "consignacao",
        "base": "Ajuste SINIEF 02/1993; RICMS-SP art. 465 a 468",
        "movimentos": [
            (
                1,
                "Remessa em consignação mercantil",
                "consignante",
                "5.917 / 6.917",
                "1.917 / 2.917",
                "CST 00/10 — ICMS destacado normalmente",
                "IPI destacado / PIS-COFINS conforme regime",
                TRIBUTADA_IBS,
                "sem benefício; não há receita contábil",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "CON-001",
                "Há ST na consignação? O consignatário credita o imposto?",
            ),
            (
                2,
                "Reajuste de preço da mercadoria consignada",
                "consignante",
                "5.917 / 6.917 (NF complementar)",
                "1.917 / 2.917",
                "CST 00 — complemento de base/imposto",
                "IPI complementar / PIS-COFINS conforme regime",
                TRIBUTADA_IBS,
                "mencionar a NF original nos dados adicionais",
                "TES complementar a definir",
                STATUS_FALTANDO,
                "CON-002",
                "Existe reajuste no contrato? Frequência e responsável pela emissão",
            ),
            (
                3,
                "Venda da mercadoria consignada a terceiro",
                "consignatário",
                "5.115 / 6.115",
                "1.102 / 2.102 (cliente final)",
                "CST 00/60 — tributado na venda",
                "IPI n/a / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de venda — SIGAFAT",
                STATUS_FALTANDO,
                "CON-003",
                "O cliente atua como consignatário também? Se sim, precisa da regra de venda",
            ),
            (
                4,
                "Devolução simbólica ao consignante",
                "consignatário",
                "5.919 / 6.919",
                "1.919 / 2.919",
                "CST 90 — simbólico, sem novo débito",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "sem benefício",
                "TES simbólica a definir",
                STATUS_FALTANDO,
                "CON-004",
                "Baixa de estoque simbólica no Protheus (SIGAEST) está parametrizada?",
            ),
            (
                5,
                "Faturamento da venda pelo consignante",
                "consignante",
                "5.114 / 6.114 (5.113 / 6.113 se produção própria)",
                "1.102 / 2.102",
                "CST 00 — apenas diferença de preço, se houver",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem destaque de ICMS quando já debitado na remessa — confirmar",
                "TES de faturamento a definir",
                STATUS_FALTANDO,
                "CON-005",
                "O ICMS é destacado de novo ou só o complemento? Regra da UF",
            ),
            (
                6,
                "Devolução da mercadoria não vendida",
                "consignatário",
                "5.918 / 6.918",
                "1.918 / 2.918",
                "CST 00 — devolução com o mesmo imposto da remessa",
                "IPI espelhado / PIS-COFINS crédito",
                TRIBUTADA_IBS,
                "espelhar tributação da NF de remessa",
                "TES de devolução a definir",
                STATUS_FALTANDO,
                "CON-006",
                "Prazo contratual de devolução e tratamento de avarias",
            ),
        ],
    },
    {
        "nome": "Consignação industrial",
        "grupo": "consignacao",
        "base": "Protocolo ICMS 52/2000",
        "movimentos": [
            (
                1,
                "Remessa em consignação industrial",
                "consignante",
                "5.917 / 6.917",
                "1.917 / 2.917",
                "CST 00 — ICMS destacado (suspensão só onde previsto no protocolo)",
                "IPI destacado / PIS-COFINS conforme regime",
                TRIBUTADA_IBS,
                "Protocolo ICMS 52/00 — verificar adesão das UFs envolvidas",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "CIN-001",
                "As UFs de origem e destino aderiram ao protocolo?",
            ),
            (
                2,
                "Consumo do insumo no processo industrial",
                "consignatário (indústria)",
                "n/a — apuração interna do consignatário",
                "n/a",
                "n/a",
                "n/a",
                "n/a",
                "controle mensal previsto no protocolo",
                "SIGAEST — apontamento de produção",
                STATUS_FALTANDO,
                "CIN-002",
                "Periodicidade do fechamento (mensal) e relatório de consumo",
            ),
            (
                3,
                "Faturamento do insumo consumido",
                "consignante",
                "5.111 / 6.111 (5.112 / 6.112 se de terceiros)",
                "1.102 / 2.102",
                "CST 00 — complemento/valor da venda",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de faturamento a definir",
                STATUS_FALTANDO,
                "CIN-003",
                "Data-limite de emissão da NF de venda após o consumo",
            ),
            (
                4,
                "Devolução simbólica / devolução física do saldo",
                "consignatário",
                "5.919 / 6.919 (simbólica) • 5.918 / 6.918 (física)",
                "1.919 / 2.919 • 1.918 / 2.918",
                "CST 90 (simbólica) / CST 00 (física)",
                "espelhar a NF de remessa",
                NAO_ONEROSA_IBS,
                "sem benefício",
                "TES a definir",
                STATUS_FALTANDO,
                "CIN-004",
                "Quem controla o saldo consignado: cliente ou consignatário?",
            ),
        ],
    },
    {
        "nome": "Industrialização por encomenda",
        "grupo": "industrializacao",
        "base": "Convênio AE 15/1974; RICMS-SP art. 402 (suspensão, retorno em 180 dias)",
        "movimentos": [
            (
                1,
                "Remessa de insumo para industrialização",
                "encomendante",
                "5.901 / 6.901",
                "1.901 / 2.901",
                "CST 50 — suspensão",
                "IPI 55 (suspensão) / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "suspensão do art. 402 do RICMS-SP — cBenef a confirmar",
                "TES a definir — SIGAFAT/SIGAEST",
                STATUS_FALTANDO,
                "IND-001",
                "Prazo de retorno (180 dias) e controle de saldo em poder de terceiros",
            ),
            (
                2,
                "Retorno do insumo aplicado no produto",
                "industrializador",
                "5.902 / 6.902",
                "1.902 / 2.902",
                "CST 50 — suspensão encerrada",
                "IPI 55 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "mesmo fundamento da remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "IND-002",
                "O valor retornado é o mesmo da remessa? Tratamento de perdas de processo",
            ),
            (
                3,
                "Cobrança da industrialização (mão de obra + material próprio)",
                "industrializador",
                "5.124 / 6.124 (5.125 / 6.125 quando o insumo não transitou)",
                "1.124 / 2.124",
                "CST 51 — diferimento do ICMS sobre a mão de obra (SP) ou tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "diferimento do art. 402 §1º — cBenef a confirmar",
                "TES de industrialização a definir",
                STATUS_FALTANDO,
                "IND-003",
                "ICMS da mão de obra é diferido ou tributado na UF do industrializador?",
            ),
            (
                4,
                "Retorno de insumo não aplicado",
                "industrializador",
                "5.903 / 6.903",
                "1.903 / 2.903",
                "CST 50 — suspensão",
                "IPI 55 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "mesmo fundamento da remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "IND-004",
                "Sobras e refugos voltam ou são vendidos ao industrializador?",
            ),
        ],
    },
    {
        "nome": "Industrialização triangular (por conta e ordem)",
        "grupo": "industrializacao",
        "base": "RICMS-SP art. 406; Convênio AE 15/1974",
        "movimentos": [
            (
                1,
                "Venda do fornecedor com entrega direta ao industrializador",
                "fornecedor",
                "5.122 / 6.122 (5.123 / 6.123 para mercadoria de terceiros)",
                "1.122 / 2.122 (adquirente)",
                "CST 00 — venda tributada",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de compra/venda — SIGACOM/SIGAFAT",
                STATUS_FALTANDO,
                "ITR-001",
                "O cliente é o adquirente, o fornecedor ou o industrializador nesse fluxo?",
            ),
            (
                2,
                "Remessa simbólica do adquirente ao industrializador",
                "adquirente",
                "5.924 / 6.924",
                "1.924 / 2.924",
                "CST 50 — suspensão",
                "IPI 55 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "suspensão — cBenef a confirmar",
                "TES simbólica a definir",
                STATUS_FALTANDO,
                "ITR-002",
                "Emissão simbólica automática pelo Protheus ou manual?",
            ),
            (
                3,
                "Retorno do produto industrializado ao adquirente",
                "industrializador",
                "5.925 / 6.925",
                "1.925 / 2.925",
                "CST 50 — suspensão encerrada",
                "IPI 55 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "mesmo fundamento da remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "ITR-003",
                "O retorno é físico para o adquirente ou segue para o cliente final?",
            ),
            (
                4,
                "Cobrança da industrialização",
                "industrializador",
                "5.124 / 6.124",
                "1.124 / 2.124",
                "CST 51 — diferimento (SP) ou tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "art. 402 §1º — confirmar",
                "TES de serviço industrial a definir",
                STATUS_FALTANDO,
                "ITR-004",
                "Composição do valor cobrado (mão de obra x material aplicado)",
            ),
        ],
    },
    {
        "nome": "Conserto / reparo",
        "grupo": "conserto",
        "base": "Convênio ICMS 25/1981; RICMS-SP Anexo I art. 79 (isenção no retorno)",
        "movimentos": [
            (
                1,
                "Remessa para conserto ou reparo",
                "remetente",
                "5.915 / 6.915",
                "1.915 / 2.915",
                "CST 50 — suspensão",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "suspensão — cBenef a confirmar",
                "TES a definir — SIGAFAT/SIGAATF",
                STATUS_FALTANDO,
                "CSR-001",
                "É bem do ativo ou mercadoria? Muda o bloco G do SPED",
            ),
            (
                2,
                "Retorno do bem consertado",
                "prestador do conserto",
                "5.916 / 6.916",
                "1.916 / 2.916",
                "CST 50 — suspensão encerrada",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "isenção/suspensão do retorno — confirmar",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "CSR-002",
                "Prazo de retorno e tratamento se o bem não voltar (perda)",
            ),
            (
                3,
                "Peças aplicadas no conserto",
                "prestador do conserto",
                "5.101 / 5.102 (6.101 / 6.102)",
                "1.101 / 1.102 (2.101 / 2.102)",
                "CST 00 — venda de peça tributada",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício (peça em garantia: verificar 5.949 e Conv. 129/06)",
                "TES de venda de peça a definir",
                STATUS_FALTANDO,
                "CSR-003",
                "Peça em garantia tem tratamento próprio? Convênio ICMS 129/2006",
            ),
            (
                4,
                "Mão de obra do conserto (ISS)",
                "prestador do conserto",
                "5.933 (quando exigido no documento fiscal) / NFS-e municipal",
                "n/a — tomador escritura o serviço",
                "fora do campo de incidência do ICMS",
                "PIS-COFINS sobre serviço; ISS conforme município",
                "confirmar CST/cClassTrib de serviço",
                "lista de serviços LC 116/2003",
                "SIGAFAT / SIGALOJA — nota de serviço",
                STATUS_FALTANDO,
                "CSR-004",
                "Código de serviço, alíquota de ISS e retenções aplicáveis",
            ),
        ],
    },
    {
        "nome": "Comodato / locação de bens",
        "grupo": "comodato",
        "base": "Súmula STF 573 / não incidência do ICMS; RICMS-SP art. 7º",
        "movimentos": [
            (
                1,
                "Remessa de bem em comodato ou locação",
                "comodante",
                "5.908 / 6.908",
                "1.908 / 2.908",
                "CST 41 — não tributada",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "não incidência — cBenef a confirmar",
                "TES a definir — SIGAATF/SIGAFAT",
                STATUS_FALTANDO,
                "COM-001",
                "Contrato tem prazo? Bem é do ativo imobilizado (controle no SIGAATF)?",
            ),
            (
                2,
                "Retorno do bem em comodato",
                "comodatário",
                "5.909 / 6.909",
                "1.909 / 2.909",
                "CST 41 — não tributada",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "espelhar a remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "COM-002",
                "Quem emite quando o comodatário não é contribuinte?",
            ),
            (
                3,
                "Venda do bem ao comodatário (encerra o comodato)",
                "comodante",
                "5.551 / 6.551 (ativo) ou 5.102 / 6.102 (mercadoria)",
                "1.551 / 2.551 ou 1.102 / 2.102",
                "CST 00/41 — verificar não incidência na venda de ativo",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "venda de ativo imobilizado: verificar não incidência",
                "TES de venda de ativo a definir",
                STATUS_FALTANDO,
                "COM-003",
                "Baixa do ativo no SIGAATF e efeito no CIAP",
            ),
        ],
    },
    {
        "nome": "Armazém geral / depósito fechado",
        "grupo": "armazenagem",
        "base": "Convênio SINIEF s/nº 1970 art. 26 a 39; RICMS-SP Anexo VII",
        "movimentos": [
            (
                1,
                "Remessa para armazém geral / depósito fechado",
                "depositante",
                "5.905 / 6.905",
                "1.905 / 2.905",
                "CST 41/50 — não incidência (mesma UF) / suspensão",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "não incidência quando armazém na mesma UF — confirmar",
                "TES a definir — SIGAEST",
                STATUS_FALTANDO,
                "ARM-001",
                "Armazém fica na mesma UF? Muda completamente a tributação",
            ),
            (
                2,
                "Retorno físico da mercadoria depositada",
                "armazém geral",
                "5.906 / 6.906",
                "1.906 / 2.906",
                "CST 41/50 — espelha a remessa",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "espelhar a remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "ARM-002",
                "Controle de saldo por armazém no Protheus (endereçamento)",
            ),
            (
                3,
                "Retorno simbólico (venda com saída direta do armazém)",
                "armazém geral",
                "5.907 / 6.907",
                "1.907 / 2.907",
                "CST 41/90 — simbólico",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "sem benefício",
                "TES simbólica a definir",
                STATUS_FALTANDO,
                "ARM-003",
                "Sequência das três notas (venda, retorno simbólico, remessa por conta e ordem)",
            ),
            (
                4,
                "Remessa por conta e ordem ao cliente final",
                "armazém geral",
                "5.923 / 6.923 (5.934 na remessa simbólica ao depositante)",
                "1.923 / 2.923",
                "CST 41/90 — sem débito próprio",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "sem benefício",
                "TES a definir",
                STATUS_FALTANDO,
                "ARM-004",
                "O armazém emite pelo cliente? Integração/EDI com o Protheus",
            ),
        ],
    },
    {
        "nome": "Exposição / feira",
        "grupo": "exposicao",
        "base": "Convênio ICMS 30/1990; RICMS-SP Anexo I art. 34",
        "movimentos": [
            (
                1,
                "Remessa para exposição ou feira",
                "remetente",
                "5.914 / 6.914",
                "1.914 / 2.914",
                "CST 41/50 — não incidência ou suspensão (60 dias)",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "isenção/suspensão do Conv. 30/90 — cBenef a confirmar",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "EXPO-001",
                "Estande é do próprio contribuinte ou de terceiro? Muda quem emite o retorno",
            ),
            (
                2,
                "Retorno da mercadoria não vendida na feira",
                "detentor (ou NF de entrada do próprio remetente)",
                "5.949 / 6.949 (quando emitido por terceiro)",
                "1.914 / 2.914",
                "CST 41/50 — espelha a remessa",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "espelhar a remessa",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "EXPO-002",
                "Confirmar CFOP de retorno com a UF: 1.914 por NF de entrada é o usual",
            ),
            (
                3,
                "Venda realizada durante a feira",
                "remetente",
                "5.103 / 5.104 (6.103 / 6.104)",
                "1.101 / 1.102 (2.101 / 2.102)",
                "CST 00 — tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de venda fora do estabelecimento",
                STATUS_FALTANDO,
                "EXPO-003",
                "Emissão em contingência/offline no estande e integração posterior",
            ),
        ],
    },
    {
        "nome": "Venda fora do estabelecimento (pronta entrega)",
        "grupo": "venda_fora",
        "base": "RICMS-SP art. 284 a 286; Convênio SINIEF s/nº 1970",
        "movimentos": [
            (
                1,
                "Remessa para venda fora do estabelecimento",
                "remetente",
                "5.904 / 6.904",
                "n/a — mercadoria em poder do próprio vendedor",
                "CST 00 — ICMS destacado pelo total carregado",
                "IPI conforme NCM / PIS-COFINS 49",
                TRIBUTADA_IBS,
                "sem benefício; crédito na entrada do retorno",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "VFE-001",
                "Roteiro de veículos, controle de carga e prazo de retorno",
            ),
            (
                2,
                "Venda efetuada fora do estabelecimento",
                "remetente (no veículo)",
                "5.103 / 5.104 (6.103 / 6.104)",
                "1.101 / 1.102 (2.101 / 2.102)",
                "CST 00 — tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de venda a definir",
                STATUS_FALTANDO,
                "VFE-002",
                "Referência à NF de remessa nos dados adicionais",
            ),
            (
                3,
                "Retorno da mercadoria não vendida",
                "remetente (NF de entrada)",
                "n/a",
                "1.904 / 2.904",
                "CST 00 — crédito do imposto debitado na remessa",
                "IPI crédito / PIS-COFINS 49",
                TRIBUTADA_IBS,
                "crédito proporcional ao não vendido",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "VFE-003",
                "Cálculo do crédito proporcional está automatizado no Protheus?",
            ),
        ],
    },
    {
        "nome": "Venda para entrega futura",
        "grupo": "entrega_futura",
        "base": "Convênio SINIEF s/nº 1970 art. 40; RICMS-SP art. 129",
        "movimentos": [
            (
                1,
                "Simples faturamento (sem circulação da mercadoria)",
                "vendedor",
                "5.922 / 6.922",
                "1.922 / 2.922",
                "CST 41/90 — sem destaque de ICMS",
                "IPI pode ser destacado / PIS-COFINS conforme regime",
                NAO_ONEROSA_IBS,
                "sem benefício; nota sem circulação física",
                "TES de faturamento a definir — SIGAFAT",
                STATUS_FALTANDO,
                "VEF-001",
                "IPI é antecipado no faturamento? Reflexo no financeiro (SIGAFIN)",
            ),
            (
                2,
                "Entrega efetiva da mercadoria",
                "vendedor",
                "5.116 / 6.116 (produção) • 5.117 / 6.117 (terceiros)",
                "1.116 / 2.116 • 1.117 / 2.117",
                "CST 00 — ICMS destacado na entrega",
                "IPI já destacado no faturamento / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "referenciar a NF de simples faturamento",
                "TES de remessa a definir",
                STATUS_FALTANDO,
                "VEF-002",
                "Entregas parciais? Como o Protheus amarra o saldo do pedido",
            ),
        ],
    },
    {
        "nome": "Venda à ordem",
        "grupo": "venda_ordem",
        "base": "Convênio SINIEF s/nº 1970 art. 40 §3º; RICMS-SP art. 129 §2º",
        "movimentos": [
            (
                1,
                "Faturamento do vendedor remetente ao adquirente originário",
                "vendedor remetente",
                "5.118 / 6.118 (produção) • 5.119 / 6.119 (terceiros)",
                "1.102 / 2.102",
                "CST 00 — tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "VAO-001",
                "O cliente é vendedor remetente, adquirente originário ou destinatário?",
            ),
            (
                2,
                "Remessa por conta e ordem ao destinatário final",
                "vendedor remetente",
                "5.923 / 6.923",
                "1.923 / 2.923",
                "CST 41/90 — sem novo débito",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "sem benefício; referenciar a NF de venda",
                "TES simbólica a definir",
                STATUS_FALTANDO,
                "VAO-002",
                "Chave da NF de venda referenciada no XML da remessa",
            ),
            (
                3,
                "Venda do adquirente originário ao destinatário final",
                "adquirente originário",
                "5.120 / 6.120",
                "1.102 / 2.102",
                "CST 00 — tributado",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de venda a definir",
                STATUS_FALTANDO,
                "VAO-003",
                "Operação interestadual triangular: DIFAL e ST de quem?",
            ),
        ],
    },
    {
        "nome": "Transferência entre estabelecimentos do mesmo titular",
        "grupo": "transferencia",
        "base": "ADC 49/STF; LC 204/2023; Convênio ICMS 178/2023 e 109/2024",
        "movimentos": [
            (
                1,
                "Transferência de produção do estabelecimento",
                "filial remetente",
                "5.151 / 6.151",
                "1.151 / 2.151",
                "CST 00/41 — transferência de crédito (não é incidência)",
                "IPI conforme NCM / PIS-COFINS 49",
                TRIBUTADA_IBS,
                "Conv. 178/23 — transferência obrigatória do crédito; 109/24 permite opção por tributar",
                "TES a definir — SIGAEST/SIGAFAT",
                STATUS_FALTANDO,
                "TRF-001",
                "O cliente optou por equiparar a transferência a operação tributada?",
            ),
            (
                2,
                "Transferência de mercadoria adquirida de terceiros",
                "filial remetente",
                "5.152 / 6.152",
                "1.152 / 2.152",
                "CST 00/41 — idem",
                "IPI conforme NCM / PIS-COFINS 49",
                TRIBUTADA_IBS,
                "mesma base legal",
                "TES a definir",
                STATUS_FALTANDO,
                "TRF-002",
                "Base de cálculo da transferência (custo x valor de entrada mais recente)",
            ),
            (
                3,
                "Transferência de bem do ativo imobilizado",
                "filial remetente",
                "5.552 / 6.552",
                "1.552 / 2.552",
                "CST 41 — não incidência",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "não incidência; CIAP acompanha o bem",
                "TES a definir — SIGAATF",
                STATUS_FALTANDO,
                "TRF-003",
                "Saldo de CIAP transferido junto? Registro bloco G do SPED",
            ),
            (
                4,
                "Transferência de material de uso e consumo",
                "filial remetente",
                "5.557 / 6.557",
                "1.557 / 2.557",
                "CST 41/90 — sem crédito",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "sem benefício",
                "TES a definir",
                STATUS_FALTANDO,
                "TRF-004",
                "Há DIFAL de uso e consumo na entrada interestadual?",
            ),
        ],
    },
    {
        "nome": "Devolução de venda",
        "grupo": "devolucao",
        "base": "Convênio SINIEF s/nº 1970 art. 4º; RICMS-SP art. 452 a 454",
        "movimentos": [
            (
                1,
                "Venda original",
                "vendedor",
                "5.101 / 5.102 (6.101 / 6.102)",
                "1.101 / 1.102 (2.101 / 2.102)",
                "CST conforme a mercadoria",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "operação de referência do ciclo",
                "TES de venda vigente",
                STATUS_PARCIAL,
                "DEV-001",
                "Mapear todas as TES de venda que podem gerar devolução",
            ),
            (
                2,
                "Devolução por cliente contribuinte",
                "cliente",
                "5.201 / 6.201 (produção) • 5.202 / 6.202 (terceiros)",
                "1.201 / 2.201 • 1.202 / 2.202",
                "CST espelhado — mesma base e alíquota da venda",
                "IPI espelhado / PIS-COFINS crédito",
                TRIBUTADA_IBS,
                "espelhar integralmente a NF de origem",
                "TES de devolução a definir — SIGACOM",
                STATUS_FALTANDO,
                "DEV-002",
                "Devolução parcial: rateio de frete, desconto e ST",
            ),
            (
                3,
                "Devolução por não contribuinte (NF de entrada)",
                "próprio vendedor",
                "n/a",
                "1.202 / 2.202",
                "CST espelhado; crédito conforme art. 452 do RICMS-SP",
                "IPI espelhado / PIS-COFINS crédito",
                TRIBUTADA_IBS,
                "exige prova da devolução (art. 452 §1º)",
                "TES de NF de entrada a definir",
                STATUS_FALTANDO,
                "DEV-003",
                "Fluxo de aprovação da NF de entrada e prazo de emissão",
            ),
            (
                4,
                "Retorno de mercadoria não entregue",
                "próprio vendedor (NF de entrada)",
                "n/a",
                "1.949 / 2.949 (confirmar 1.201/1.202 na UF)",
                "CST espelhado — anulação do débito",
                "IPI espelhado / PIS-COFINS crédito",
                TRIBUTADA_IBS,
                "registrar o motivo da recusa no verso do DANFE / evento de NF-e",
                "TES de retorno a definir",
                STATUS_FALTANDO,
                "DEV-004",
                "Evento de NF-e (operação não realizada) está sendo transmitido?",
            ),
        ],
    },
    {
        "nome": "Remessa com fim específico de exportação",
        "grupo": "exportacao",
        "base": "LC 87/1996 art. 3º II; Convênio ICMS 84/2009",
        "movimentos": [
            (
                1,
                "Remessa com fim específico de exportação",
                "remetente",
                "5.501 / 6.501 (produção) • 5.502 / 6.502 (terceiros)",
                "1.501 / 2.501 • 1.502 / 2.502",
                "CST 41 — não incidência",
                "IPI 53 / PIS-COFINS 08 (suspensão) — confirmar",
                NAO_ONEROSA_IBS,
                "não incidência LC 87/96 art. 3º II — cBenef a confirmar",
                "TES a definir — SIGAFAT/SIGAEIC",
                STATUS_FALTANDO,
                "EXP-001",
                "Prazo de comprovação (180 dias) e controle do Memorando de Exportação",
            ),
            (
                2,
                "Exportação efetiva pela trading / comercial exportadora",
                "trading",
                "7.501 (exportação de mercadoria recebida com fim específico)",
                "n/a — destinatário no exterior",
                "CST 41 — não incidência",
                "IPI 53 / PIS-COFINS 08",
                NAO_ONEROSA_IBS,
                "registro no bloco de exportação do SPED",
                "SIGAEIC",
                STATUS_FALTANDO,
                "EXP-002",
                "Recebimento do Memorando de Exportação e baixa do controle",
            ),
            (
                3,
                "Devolução da mercadoria não exportada",
                "trading",
                "5.503 / 6.503",
                "1.503 / 2.503",
                "CST 41 + recolhimento do imposto suspenso com juros",
                "IPI espelhado / PIS-COFINS a recolher",
                NAO_ONEROSA_IBS,
                "recolhimento com atualização — art. 3º Conv. 84/09",
                "TES de devolução a definir",
                STATUS_FALTANDO,
                "EXP-003",
                "Quem recolhe o imposto quando a exportação não se confirma?",
            ),
        ],
    },
    {
        "nome": "Bonificação, brinde, doação e amostra grátis",
        "grupo": "bonificacao",
        "base": "RICMS-SP art. 455 a 457 (brindes); Anexo I art. 3º (amostra grátis)",
        "movimentos": [
            (
                1,
                "Remessa em bonificação, doação ou brinde",
                "remetente",
                "5.910 / 6.910",
                "1.910 / 2.910",
                "CST 00 — ICMS incide (não há desconto incondicional na base)",
                "IPI conforme NCM / PIS-COFINS 49",
                TRIBUTADA_IBS,
                "sem benefício; brinde tem regra própria de escrituração",
                "TES a definir — SIGAFAT",
                STATUS_FALTANDO,
                "BON-001",
                "Brinde adquirido para distribuição segue o art. 455 (NF de entrada + saída)",
            ),
            (
                2,
                "Remessa de amostra grátis",
                "remetente",
                "5.911 / 6.911",
                "1.911 / 2.911",
                "CST 40 — isento (atendidos os requisitos)",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "isenção Anexo I art. 3º RICMS-SP — cBenef a confirmar",
                "TES a definir",
                STATUS_FALTANDO,
                "BON-002",
                "A amostra atende aos requisitos (valor, indicação 'amostra grátis')?",
            ),
            (
                3,
                "Devolução de brinde / bonificação",
                "destinatário",
                "5.949 / 6.949 (confirmar 5.202 na UF)",
                "1.949 / 2.949",
                "CST espelhado",
                "IPI espelhado / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "espelhar a remessa",
                "TES de devolução a definir",
                STATUS_FALTANDO,
                "BON-003",
                "Existe devolução nesse fluxo na prática do cliente?",
            ),
        ],
    },
    {
        "nome": "Vasilhame, sacaria e paletes retornáveis",
        "grupo": "vasilhame",
        "base": "Convênio ICMS 88/1991; RICMS-SP Anexo I art. 82",
        "movimentos": [
            (
                1,
                "Remessa de vasilhame, sacaria ou palete",
                "remetente",
                "5.920 / 6.920",
                "1.920 / 2.920",
                "CST 40/41 — isento ou não tributado",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "isenção Conv. 88/91 — cBenef a confirmar",
                "TES a definir — SIGAEST",
                STATUS_FALTANDO,
                "VAS-001",
                "O vasilhame vai na mesma NF da mercadoria ou em nota separada?",
            ),
            (
                2,
                "Devolução do vasilhame",
                "destinatário",
                "5.921 / 6.921",
                "1.921 / 2.921",
                "CST 40/41 — espelha a remessa",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "mesma isenção",
                "TES de devolução a definir",
                STATUS_FALTANDO,
                "VAS-002",
                "Controle de saldo de vasilhame em poder de terceiros",
            ),
            (
                3,
                "Perda / não devolução (cobrança do vasilhame)",
                "remetente",
                "5.102 / 6.102",
                "1.102 / 2.102",
                "CST 00 — venda tributada do vasilhame",
                "IPI conforme NCM / PIS-COFINS 01",
                TRIBUTADA_IBS,
                "sem benefício",
                "TES de venda a definir",
                STATUS_FALTANDO,
                "VAS-003",
                "Prazo para caracterizar a perda e gerar o faturamento",
            ),
        ],
    },
    {
        "nome": "Ativo imobilizado em uso fora do estabelecimento",
        "grupo": "ativo",
        "base": "RICMS-SP art. 7º; Convênio ICMS 19/1991",
        "movimentos": [
            (
                1,
                "Remessa de bem do ativo para uso fora do estabelecimento",
                "remetente",
                "5.554 / 6.554",
                "1.554 / 2.554",
                "CST 41 — não incidência",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "não incidência — cBenef a confirmar",
                "TES a definir — SIGAATF",
                STATUS_FALTANDO,
                "ATV-001",
                "Bem controlado no SIGAATF? Efeito no CIAP e no bloco G",
            ),
            (
                2,
                "Devolução do bem de terceiro usado no estabelecimento",
                "detentor",
                "5.555 / 6.555",
                "1.555 / 2.555",
                "CST 41 — não incidência",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "espelhar a remessa",
                "TES de devolução a definir",
                STATUS_FALTANDO,
                "ATV-002",
                "Prazo de permanência e responsabilidade por avaria",
            ),
            (
                3,
                "Venda do bem do ativo imobilizado",
                "proprietário",
                "5.551 / 6.551",
                "1.551 / 2.551",
                "CST 41 — não incidência na venda de ativo (confirmar UF)",
                "IPI 53 / PIS-COFINS 49",
                NAO_ONEROSA_IBS,
                "não incidência — confirmar entendimento da UF",
                "TES de venda de ativo a definir",
                STATUS_FALTANDO,
                "ATV-003",
                "Baixa contábil, estorno de CIAP e ganho/perda de capital",
            ),
        ],
    },
]

COLUNAS = [
    ("Ciclo", 34),
    ("#", 5),
    ("Movimento", 44),
    ("Quem emite o documento", 26),
    ("CFOP de saída do remetente", 34),
    ("CFOP de entrada do destinatário", 26),
    ("Tratamento ICMS (CST típico)", 32),
    ("IPI / PIS / COFINS", 26),
    ("IBS/CBS (CST / cClassTrib)", 30),
    ("cBenef / base legal", 38),
    ("TES / módulo Protheus", 26),
    ("Status na matriz", 15),
    ("Cód. sugerido na matriz", 18),
    ("O que confirmar com o cliente", 52),
]


def _fill(cor: str) -> PatternFill:
    return PatternFill("solid", fgColor=cor)


def _estilo_status(celula) -> None:
    valor = str(celula.value or "").lower()
    if valor.startswith(STATUS_LEVANTADO):
        celula.fill = _fill(VERDE_OK)
        celula.font = Font(bold=True, color=VERDE_TXT, size=10)
    elif valor.startswith(STATUS_PARCIAL):
        celula.fill = _fill(AMBAR)
        celula.font = Font(bold=True, color=AMBAR_TXT, size=10)
    elif valor.startswith(STATUS_FALTANDO):
        celula.fill = _fill(VERMELHO)
        celula.font = Font(bold=True, color=VERMELHO_TXT, size=10)


def _cabecalho(ws, titulos: list[str], larguras: list[int], linha: int = 1) -> None:
    for idx, (titulo, largura) in enumerate(zip(titulos, larguras), start=1):
        cel = ws.cell(row=linha, column=idx, value=titulo)
        cel.fill = _fill(AZUL_ESCURO)
        cel.font = Font(bold=True, color=BRANCO, size=10)
        cel.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        cel.border = BORDA
        ws.column_dimensions[get_column_letter(idx)].width = largura
    ws.row_dimensions[linha].height = 34


def aba_movimentos(wb: Workbook) -> None:
    ws = wb.create_sheet("Ciclos e movimentos")
    _cabecalho(ws, [c[0] for c in COLUNAS], [c[1] for c in COLUNAS])

    linha = 2
    for indice, ciclo in enumerate(CICLOS, start=1):
        nome_ciclo = f"{indice}. {ciclo['nome']}"
        listrar = indice % 2 == 0
        primeira = linha
        for mov in ciclo["movimentos"]:
            valores = [nome_ciclo, *mov]
            for col, valor in enumerate(valores, start=1):
                cel = ws.cell(row=linha, column=col, value=valor)
                cel.alignment = Alignment(
                    vertical="top",
                    wrap_text=True,
                    horizontal="center" if col == 2 else "left",
                )
                cel.border = BORDA
                cel.font = Font(size=10)
                if listrar:
                    cel.fill = _fill(CINZA_FAIXA)
            ws.cell(row=linha, column=1).font = Font(size=10, bold=True, color=AZUL_MEDIO)
            _estilo_status(ws.cell(row=linha, column=12))
            linha += 1
        if linha - primeira > 1:
            ws.merge_cells(start_row=primeira, start_column=1, end_row=linha - 1, end_column=1)
            ws.cell(row=primeira, column=1).alignment = Alignment(
                vertical="center", wrap_text=True
            )

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUNAS))}{linha - 1}"

    validacao = DataValidation(
        type="list",
        formula1=f'"{STATUS_LEVANTADO},{STATUS_PARCIAL},{STATUS_FALTANDO}"',
        allow_blank=True,
        showDropDown=False,
    )
    ws.add_data_validation(validacao)
    validacao.add(f"L2:L{linha - 1}")

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"


def aba_resumo(wb: Workbook) -> None:
    ws = wb.create_sheet("Resumo por ciclo", 0)

    ws["A1"] = "Ciclos de operação para o Configurador de Tributos (FISA170)"
    ws["A1"].font = Font(bold=True, size=15, color=AZUL_ESCURO)
    ws["A2"] = (
        "Cada operação do cliente é um ciclo: a saída só está corretamente configurada quando o retorno, "
        "a transmissão de propriedade e os movimentos simbólicos também estão. Uma linha por ciclo aqui; "
        "o detalhe movimento a movimento está na aba 'Ciclos e movimentos'."
    )
    ws["A2"].font = Font(size=10, italic=True, color="475569")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 32

    titulos = [
        "#",
        "Ciclo",
        "Grupo",
        "Movimentos",
        "CFOPs de saída envolvidos",
        "CFOPs de entrada envolvidos",
        "Base legal / referência",
        "Status do ciclo",
    ]
    larguras = [5, 44, 18, 12, 46, 34, 52, 16]
    _cabecalho(ws, titulos, larguras, linha=4)

    import re

    linha = 5
    for indice, ciclo in enumerate(CICLOS, start=1):
        movimentos = ciclo["movimentos"]
        saidas, entradas = [], []
        for mov in movimentos:
            saidas += re.findall(r"[1-7]\.\d{3}", mov[3])
            entradas += re.findall(r"[1-7]\.\d{3}", mov[4])
        status_set = {mov[10] for mov in movimentos}
        if status_set == {STATUS_LEVANTADO}:
            status = STATUS_LEVANTADO
        elif STATUS_LEVANTADO in status_set or STATUS_PARCIAL in status_set:
            status = STATUS_PARCIAL
        else:
            status = STATUS_FALTANDO

        valores = [
            indice,
            ciclo["nome"],
            ciclo["grupo"],
            len(movimentos),
            ", ".join(dict.fromkeys(saidas)) or "n/a",
            ", ".join(dict.fromkeys(entradas)) or "n/a",
            ciclo["base"],
            status,
        ]
        for col, valor in enumerate(valores, start=1):
            cel = ws.cell(row=linha, column=col, value=valor)
            cel.alignment = Alignment(
                vertical="top",
                wrap_text=True,
                horizontal="center" if col in (1, 4, 8) else "left",
            )
            cel.border = BORDA
            cel.font = Font(size=10)
            if indice % 2 == 0:
                cel.fill = _fill(CINZA_FAIXA)
        ws.cell(row=linha, column=2).font = Font(size=10, bold=True)
        _estilo_status(ws.cell(row=linha, column=8))
        linha += 1

    total_mov = sum(len(c["movimentos"]) for c in CICLOS)
    ws.cell(row=linha + 1, column=2, value=f"{len(CICLOS)} ciclos • {total_mov} movimentos mapeados").font = Font(
        bold=True, size=10, color=AZUL_MEDIO
    )

    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:H{linha - 1}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def aba_legenda(wb: Workbook) -> None:
    ws = wb.create_sheet("Legenda e como usar")
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 108

    linha = 1

    def titulo(texto: str) -> None:
        nonlocal linha
        cel = ws.cell(row=linha, column=1, value=texto)
        cel.font = Font(bold=True, size=12, color=BRANCO)
        cel.fill = _fill(AZUL_ESCURO)
        cel2 = ws.cell(row=linha, column=2, value="")
        cel2.fill = _fill(AZUL_ESCURO)
        linha += 1

    def item(chave: str, valor: str) -> None:
        nonlocal linha
        a = ws.cell(row=linha, column=1, value=chave)
        a.font = Font(bold=True, size=10)
        a.alignment = Alignment(vertical="top", wrap_text=True)
        a.border = BORDA
        b = ws.cell(row=linha, column=2, value=valor)
        b.font = Font(size=10)
        b.alignment = Alignment(vertical="top", wrap_text=True)
        b.border = BORDA
        linha += 1

    def espaco() -> None:
        nonlocal linha
        linha += 1

    titulo("Como usar esta planilha")
    item(
        "Objetivo",
        "Fechar o levantamento por CICLO, não por documento isolado. Se a saída sai com imposto "
        "suspenso/não destacado e o retorno não tem regra, o retorno volta tributando — é o sintoma "
        "clássico de levantamento incompleto.",
    )
    item(
        "Fluxo de trabalho",
        "1) Marque na aba Resumo quais ciclos existem no cliente. 2) Na aba de movimentos, confirme "
        "CFOP, CST e cBenef de cada linha com o fiscal. 3) Transporte cada linha confirmada para "
        "docs/fisa170/modelos/matriz-operacoes.csv usando o código sugerido. 4) Rode "
        "python3 scripts/gerar_pacote_fisa170.py para gerar as fichas.",
    )
    item(
        "Coluna 'Status na matriz'",
        "levantado = linha completa na matriz; parcial = existe, mas faltam campos obrigatórios; "
        "faltando = ainda não levantado. A coluna tem lista suspensa.",
    )
    item(
        "Coluna 'O que confirmar'",
        "É a pergunta que trava o cadastro no FISA170. Sem resposta, a regra é chute e volta na "
        "homologação.",
    )
    espaco()

    titulo("Convenções de CFOP")
    item("5.xxx / 6.xxx", "Saída interna (mesma UF) / saída interestadual.")
    item("1.xxx / 2.xxx", "Entrada interna / entrada interestadual (espelho no destinatário).")
    item("7.xxx", "Saída para o exterior.")
    item(
        "'n/a'",
        "Não há documento nesse sentido — normalmente porque o movimento é escriturado por NF de "
        "entrada do próprio contribuinte.",
    )
    item(
        "'a confirmar'",
        "CFOP usado na prática pelo mercado, mas que depende da UF ou do entendimento do fiscal do "
        "cliente. Não cadastre sem confirmação.",
    )
    espaco()

    titulo("Convenções de tributação")
    item(
        "CST ICMS",
        "00 tributado integralmente • 20 redução de base • 40 isento • 41 não tributado • "
        "50 suspensão • 51 diferimento • 60 ICMS-ST cobrado anteriormente • 90 outras.",
    )
    item("CST IPI", "50/51 saídas tributadas • 52 saída isenta • 53 saída não tributada • 55 saída com suspensão.")
    item("CST PIS/COFINS", "01 alíquota básica • 08 sem incidência • 49 outras operações de saída.")
    item(
        "IBS/CBS (Reforma)",
        "CST + cClassTrib. 410/410999 = imunidade e não incidência (residual, operação não onerosa); "
        "grupo 550 = suspensão. Escolha errada distorce a apuração e é apontada em fiscalização.",
    )
    item(
        "cBenef",
        "Código do benefício fiscal. Em SP é obrigatório desde 06/04/2026 (Portaria SRE 70/2025) e "
        "precisa existir na Tabela 52 mantida na rotina FISA156 — a regra de cálculo não cria o código.",
    )
    espaco()

    titulo("Avisos")
    item(
        "Validar na UF",
        "CFOP e benefício variam por estado e por release. Os valores aqui são o padrão nacional "
        "(Convênio SINIEF s/nº 1970 e ajustes) com referência ao RICMS-SP; confirme com o fiscal do "
        "cliente antes de cadastrar.",
    )
    item(
        "Ciclo de referência",
        "O ciclo 1 (Demonstração/mostruário) é o caso já documentado em "
        "docs/fisa170/03-caso-demonstracao-sp.md com CST ICMS 50, IPI 53, PIS/COFINS 49, "
        "410/410999, cBenef SP053190 e TES 704.",
    )
    item(
        "Fonte de pesquisa",
        "Use o Buscador Protheus (pnpm dev) para achar os artigos TDN/Central sobre FISA170, cBenef, "
        "diferimento e CJ3/F2D indexados em data/indices/.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    args = parser.parse_args()

    wb = Workbook()
    wb.remove(wb.active)
    aba_movimentos(wb)
    aba_resumo(wb)
    aba_legenda(wb)
    wb.active = 0

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.saida)

    total_mov = sum(len(c["movimentos"]) for c in CICLOS)
    print(f"OK: {args.saida.relative_to(RAIZ) if args.saida.is_relative_to(RAIZ) else args.saida}")
    print(f"    {len(CICLOS)} ciclos | {total_mov} movimentos | 3 abas")


if __name__ == "__main__":
    main()
