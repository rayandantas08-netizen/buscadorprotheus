#!/usr/bin/env python3
"""Gera o pacote de levantamento de necessidades fiscais para o Configurador de Tributos (FISA170).

O script lê a matriz de operações preenchida pelo consultor, valida a coerência das
informações mínimas exigidas para cadastrar uma regra no FISA170 e produz:

    docs/fisa170/gerado/00-resumo.md      -> visão geral de todas as operações
    docs/fisa170/gerado/01-lacunas.md    -> o que ainda falta perguntar ao cliente
    docs/fisa170/gerado/fontes.md         -> mapa de fontes TOTVS por tema
    docs/fisa170/gerado/ficha-<cod>.md    -> ficha de construção da regra por operação

Uso:
    python3 scripts/gerar_pacote_fisa170.py --init-csv
    python3 scripts/gerar_pacote_fisa170.py            # gera a partir da matriz
    python3 scripts/gerar_pacote_fisa170.py --check    # mesma coisa, mas falha se houver bloqueio
"""

from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MATRIZ_PADRAO = RAIZ / "docs/fisa170/modelos/matriz-operacoes.csv"
SAIDA_PADRAO = RAIZ / "docs/fisa170/gerado"
INDICES = [
    RAIZ / "data/indices/Indice_Configurador_Tributos.txt",
    RAIZ / "data/indices/Indice_SIGAFIS_Fiscal.txt",
]

# ----------------------------------------------------------------------------- campo


@dataclass(frozen=True)
class Campo:
    nome: str
    rotulo: str
    bloco: str
    obrig: str = "nao"  # sim | condicional | nao
    dica: str = ""


CAMPOS: tuple[Campo, ...] = (
    # 1. identificação
    Campo("cod_operacao", "Código da operação", "1. Identificação", "sim", "ex.: DEM-001"),
    Campo("nome_operacao", "Descrição para o negócio", "1. Identificação", "sim", "ex.: Remessa para demonstração"),
    Campo("grupo_operacao", "Grupo da operação", "1. Identificação", "sim", "venda, compra, remessa, retorno, devolucao, complemento, servico, transferencia, exportacao"),
    Campo("sentido", "Sentido", "1. Identificação", "sim", "saida | entrada"),
    Campo("ambito", "Abrangência", "1. Identificação", "sim", "interna | interestadual | importacao | exportacao"),
    Campo("uf_origem", "UF do estabelecimento emitente", "1. Identificação", "sim", "ex.: SP"),
    Campo("uf_destino", "UF do destinatário/remetente", "1. Identificação", "condicional", "obrigatório em operação interestadual"),
    Campo("documento", "Documento fiscal", "1. Identificação", "sim", "NF-e, NFS-e, CT-e..."),
    Campo("finalidade", "Finalidade do documento", "1. Identificação", "sim", "normal, complemento, ajuste, devolucao, simbolica"),
    Campo("mod_protheus", "Módulo/gatilho no Protheus", "1. Identificação", "sim", "pedido de venda, faturamento, MATA103, estoque, serviços, PDV"),
    Campo("vigencia_inicio", "Vigência - início", "1. Identificação", "sim", "AAAA-MM-DD"),
    Campo("vigencia_fim", "Vigência - fim", "1. Identificação", "nao", "AAAA-MM-DD"),
    Campo("base_legal", "Fundamento legal do tratamento", "1. Identificação", "condicional", "artigo/convênio/Ajuste SINIEF que sustenta CST, benefício e ClassTrib"),
    Campo("responsavel", "Dono da informação no cliente", "1. Identificação", "nao", "fiscal, consultoria, ERP"),
    Campo("status", "Status do atendimento", "1. Identificação", "nao", "levantada, configurada, testada, homologada"),
    # 2. aplicação
    Campo("produtos_aplicavel", "Recorte de produtos", "2. Aplicação", "condicional", "todos | grupo | NCM | marca | lista"),
    Campo("ncm_exemplo", "NCM representativa", "2. Aplicação", "condicional", "define se a regra será por NCM (CIS/CIT) ou geral"),
    Campo("cest", "CEST", "2. Aplicação", "nao"),
    Campo("ipi_ex", "Ex-tarifário / código IPI", "2. Aplicação", "nao"),
    Campo("origem_mercadoria", "Origem da mercadoria no produto (B1_ORIGEM)", "2. Aplicação", "condicional", "impacta CST ICMS e IBS/CBS"),
    Campo("participantes_aplicavel", "Recorte de participantes", "2. Aplicação", "condicional", "todos | grupo de clientes | fornecedor específico | contribuinte/não contribuinte"),
    Campo("destinatario_contribuinte", "Destinatário é contribuinte de ICMS?", "2. Aplicação", "condicional", "sim | nao | indiferente"),
    Campo("finalidade_item", "Finalidade/destino do item", "2. Aplicação", "nao", "consumo, produção, revenda, ativo, demonstração"),
    # 3. ICMS
    Campo("cfop_saida", "CFOP de saída", "3. ICMS", "sim", "4 dígitos, ex.: 5912"),
    Campo("cfop_entrada", "CFOP de entrada (lado do parceiro)", "3. ICMS", "condicional", "necessário quando o cliente também lança a nota do fornecedor"),
    Campo("cfop_retorno", "CFOP de retorno", "3. ICMS", "condicional", "obrigatório em remessa/depósito/beneficiamento/demonstração"),
    Campo("icms_origem", "CST ICMS - origem (1º dígito)", "3. ICMS", "sim", "0 nacional, 1/2 importada, 5 diferida..."),
    Campo("icms_cst", "CST ICMS - situação (2º/3º dígitos)", "3. ICMS", "sim", "50 suspensão, 51 diferimento, 41 não tributada, 60/61 ST..."),
    Campo("icms_modalidade", "Modalidade da base de cálculo", "3. ICMS", "nao", "própria, por dentro, por fora, dupla"),
    Campo("icms_aliquota", "Alíquota de ICMS", "3. ICMS", "condicional", "obrigatória se a operação gera débito/crédito"),
    Campo("icms_redbc_pct", "Percentual de redução de base", "3. ICMS", "condicional", "exigir regra de base + incidência da parcela reduzida"),
    Campo("icms_st_cst", "CST de ICMS-ST", "3. ICMS", "condicional", "preencher se há substituição tributária"),
    Campo("icms_st_base", "Base da ST (MVA, pauta, PLC, base dupla)", "3. ICMS", "condicional"),
    Campo("icms_st_aliquota", "Alíquota interna do destino (ST/DIFAL)", "3. ICMS", "condicional"),
    Campo("fcp_pct", "% FECOEP/FECP/FCP", "3. ICMS", "nao"),
    Campo("difal_pct", "% diferencial de alíquotas", "3. ICMS", "nao"),
    Campo("icms_credito", "A operação gera crédito de ICMS na entrada?", "3. ICMS", "condicional", "sim | nao | parcial - impacta regra de apuração"),
    # 4. IPI
    Campo("ipi_cst", "CST IPI", "4. IPI", "sim", "53 saída não tributada, 55 suspensão, 99 outras saídas"),
    Campo("ipi_aliquota", "Alíquota de IPI", "4. IPI", "condicional", "deve ser zero/nula quando o CST não gera débito"),
    Campo("ipi_classe", "Classe de enquadramento do IPI", "4. IPI", "nao"),
    Campo("ipi_credito", "Crédito de IPI na entrada", "4. IPI", "nao"),
    # 5. PIS/COFINS
    Campo("pis_cst", "CST PIS", "5. PIS/COFINS", "sim", "49 outras operações de saída"),
    Campo("pis_aliquota", "Alíquota de PIS", "5. PIS/COFINS", "condicional"),
    Campo("cofins_cst", "CST COFINS", "5. PIS/COFINS", "sim", "49 outras operações de saída"),
    Campo("cofins_aliquota", "Alíquota de COFINS", "5. PIS/COFINS", "condicional"),
    Campo("pis_cofins_regime", "Regime PIS/COFINS", "5. PIS/COFINS", "condicional", "cumulativo | não cumulativo - define base e crédito"),
    Campo("pis_cofins_credito", "Gera crédito de PIS/COFINS?", "5. PIS/COFINS", "condicional", "sim | nao - define a regra de escrituração de entrada"),
    # 6. IBS/CBS
    Campo("ibs_cst", "CST IBS/CBS", "6. IBS/CBS (Reforma)", "sim", "410 imunidade e não incidência, 550 suspensão, 510 diferimento"),
    Campo("cclasstrib", "cClassTrib", "6. IBS/CBS (Reforma)", "sim", "6 dígitos iniciados pelo próprio CST, ex.: 410 -> 410999"),
    Campo("ibs_aliquota", "Alíquota de IBS", "6. IBS/CBS (Reforma)", "condicional"),
    Campo("cbs_aliquota", "Alíquota de CBS", "6. IBS/CBS (Reforma)", "condicional"),
    Campo("credito_presumido", "Crédito presumido de IBS/CBS", "6. IBS/CBS (Reforma)", "nao", "código da tabela de crédito presumido, se houver"),
    Campo("ind_op", "Indicador da operação (IndOp)", "6. IBS/CBS (Reforma)", "nao", "usa os indicadores cadastrados no FISA170"),
    # 7. benefício
    Campo("tipo_beneficio", "Natureza do benefício", "7. Benefício fiscal", "sim", "suspensao, diferimento, isencao, reducao_bc, nao_tributada, regime_especial, nenhum"),
    Campo("cbene", "cBenef da saída", "7. Benefício fiscal", "condicional", "obrigatório quando há benefício de ICMS (em SP passou a ser exigido nas notas com incentivo)"),
    Campo("cbene_retorno", "cBenef do retorno", "7. Benefício fiscal", "nao", "confirmar se o retorno usa o mesmo código do catálogo"),
    Campo("benef_descricao", "Descrição do benefício para o documento", "7. Benefício fiscal", "condicional", "texto que sairá em dados adicionais/mensagem"),
    Campo("benef_vigencia", "Vigência do benefício na Tabela 52", "7. Benefício fiscal", "condicional", "data de início do código no catálogo (ex.: 01/01/2026)"),
    # 8. retenções e extras
    Campo("retencoes", "Tributos retidos no documento", "8. Retenções", "nao", "IRRF/CSLL/PIS/COFINS/ISS: base, alíquota, tabela progressiva"),
    Campo("iss_codigo_servico", "Código de serviço (NBS/municipal)", "8. Retenções", "nao"),
    Campo("iss_aliquota", "Alíquota de ISS", "8. Retenções", "nao"),
    Campo("iss_retencao", "ISS retido pelo tomador?", "8. Retenções", "nao", "sim | nao | conforme município"),
    Campo("outras_majoracoes", "Majorações e fundos", "8. Retenções", "nao", "FECP, FUST/FUNTTEL, fundo estadual, IS"),
    # 9. Protheus
    Campo("tes", "TES (SF1)", "9. No Protheus", "sim", "ex.: 704 - informe também a TES de entrada quando houver"),
    Campo("modo_calculo", "Motor de cálculo", "9. No Protheus", "sim", "cfgtrib | tes | hibrido"),
    Campo("tes_campos_ativeis", "Campos que permanecem na TES", "9. No Protheus", "condicional", "no modo híbrido: o que ainda é decidido pela TES"),
    Campo("perfil_produto", "Perfil tributário de produto", "9. No Protheus", "condicional", "F24/F25"),
    Campo("perfil_participante", "Perfil tributário de participante", "9. No Protheus", "condicional", "F22"),
    Campo("perfil_operacao", "Perfil tributário de operação", "9. No Protheus", "condicional", "F23/F26 - chave CFOP + tipo de documento"),
    Campo("perfil_origem_destino", "Perfil origem x destino", "9. No Protheus", "condicional", "F21 - ex.: todas as origens"),
    Campo("regra_base", "Regra de base de cálculo (F27)", "9. No Protheus", "condicional", "ex.: O:VAL_MERCADORIA"),
    Campo("regra_aliquota", "Regra de alíquota (F28)", "9. No Protheus", "condicional", "ex.: I:ALIQ_NCM"),
    Campo("regra_tributaria", "Regra tributária do documento fiscal (F2B)", "9. No Protheus", "condicional", "código numérico da regra, ex.: 000403"),
    Campo("regra_ncm", "Regra por NCM", "9. No Protheus", "condicional", "CIS/CIT quando a alíquota depende de NCM/UF"),
    # 10. escrita / DFe / apuração
    Campo("livro_fiscal", "Coluna no livro fiscal", "10. Escrita e DFe", "sim", "tributado, isento, outros, não aplica"),
    Campo("incidencia", "Incidência na Regra de Escrituração (CJ2)", "10. Escrita e DFe", "sim", "Tributado | Isento | Outros - mesma tratativa do Livro Fiscal da TES"),
    Campo("incidencia_parcela_reduzida", "Incidência da parcela reduzida (CJ2_IREDBS)", "10. Escrita e DFe", "condicional", "1 = Isento, 2 = Outros; em branco cai em Outros"),
    Campo("diferimento_pct", "% de diferimento/suspensão na escrita", "10. Escrita e DFe", "condicional", "ex.: 100 para imposto integralmente diferido"),
    Campo("mensagem_dfe", "Mensagem obrigatória no DFe (CJ8)", "10. Escrita e DFe", "condicional", "texto + parâmetro que a legislação do benefício exige"),
    Campo("dados_adicionais", "Dados adicionais do documento", "10. Escrita e DFe", "nao"),
    Campo("registros_sped", "Registros SPED exigidos", "10. Escrita e DFe", "condicional", "C100/C170/C190/C195/C197..."),
    Campo("codigo_ajuste", "Código de ajuste/ CAT", "10. Escrita e DFe", "condicional", "ex.: CAT 66/2018, ajuste de apuração"),
    Campo("reflete_em", "Reflexo entre tributos", "10. Escrita e DFe", "nao", "ex.: ICMS deduzido da base de PIS/COFINS"),
    Campo("apuracao_credito", "Efeito na apuração", "10. Escrita e DFe", "condicional", "crédito, estorno, subapuração, fora da apuração"),
    Campo("codigo_receita", "Código de receita / guia", "10. Escrita e DFe", "nao", "CJ4/CJ5/CJ6/CJ7 se houver guia de recolhimento"),
    Campo("contabilizacao", "Contabilização dos tributos genéricos", "10. Escrita e DFe", "nao", "conta Débito/Crédito quando o tributo afeta resultado"),
    # 11. governança
    Campo("aprovacao_regra", "Regra passa por aprovação?", "11. Governança", "sim", "sim | nao - mecanismo de aprovação de regras (campo Status)"),
    Campo("compartilhamento_filiais", "Compartilhamento entre filiais", "11. Governança", "condicional", "mesma tabela para quais filiais/lojas"),
    Campo("evidencias", "Evidências de aceite", "11. Governança", "sim", "XML autorizado, print do simulador, livro fiscal, consulta CJ3/F2D"),
    Campo("duvidas_abertas", "Dúvidas abertas", "11. Governança", "nao"),
    Campo("observacoes", "Observações do consultor", "11. Governança", "nao"),
)

NOMES_CAMPOS = [c.nome for c in CAMPOS]
POR_NOME = {c.nome: c for c in CAMPOS}

# Benefícios que, na prática, pedem cBenef quando o estado de origem exige o campo.
CST_ICMS_COM_BENEFICIO = {"20", "30", "40", "41", "50", "51", "53"}
CST_ICMS_SEM_BENEFICIO = {"00", "01", "02", "06", "10", "60", "70", "90"}
OPERACOES_COM_RETORNO = {"remessa", "retorno", "deposito", "consignacao", "beneficiamento", "demonstracao", "conserto", "comodato"}
DIGITOS_SAIDA = {"interna": "5", "interestadual": "6", "exportacao": "7", "importacao": ""}
DIGITOS_ENTRADA = {"interna": "1", "interestadual": "2", "exportacao": "", "importacao": "3"}
OBRIGATORIEDATE_CBENEF_SP = date(2026, 4, 6)

# ----------------------------------------------------------------------------- fontes


def sem_acento(txt: str) -> str:
    return unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii").lower()


def carregar_fontes() -> list[dict[str, str]]:
    """Lê os índices versionados em data/indices e devolve [{title, url, tema}]."""
    registros: list[dict[str, str]] = []

    caminho = INDICES[0]
    if caminho.exists():
        titulo = None
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            s = linha.strip()
            if s.startswith("[*]"):
                titulo = s[3:].strip()
            elif s.startswith("Link:") and titulo:
                registros.append({"title": titulo, "url": s.split("Link:", 1)[1].strip(), "tema": "FISA170"})
                titulo = None

    caminho = INDICES[1]
    if caminho.exists():
        titulo = None
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            s = linha.strip()
            if ">" in s and s.startswith("*"):
                titulo = s.split(">", 1)[1].strip()
            elif s.startswith("URL:") and titulo:
                registros.append({"title": titulo, "url": s.split("URL:", 1)[1].strip(), "tema": "SIGAFIS"})
                titulo = None

    vistos: set[str] = set()
    unicos: list[dict[str, str]] = []
    for reg in registros:
        if reg["url"] in vistos:
            continue
        vistos.add(reg["url"])
        unicos.append(reg)
    return unicos


TEMAS_FONTES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Estrutura do configurador (perfis, tabelas, cadastros)", ("tabelas fazem parte", "estrut", "cadastros", "o que e o configurador", "acesso a rotina", "guia de utilizacao", "guia pratico", "how to")),
    ("Perfis (produto, participante, operação, origem x destino)", ("perfil", "facilitador", "otimizador")),
    ("Regras de cálculo (base, alíquota, NCM, reflexos)", ("regra de calculo", "regras de calculo", "regra de ncm", "regra por ncm", "aliquota", "reflexo", "majorac", "calculos no configurador")),
    ("Regra de escrituração e livro fiscal", ("escrituracao", "livro", "incidencia")),
    ("Ajuste de lançamento, cBenef e mensagens", ("ajuste de lan", "cbene", "mensagem", "dados adicionais", "complementar")),
    ("ICMS: suspensão, diferimento e ST", ("diferid", "suspen", "st -", "icms-st", "fecom", "fcp", "monofas", "difal", "diferencial")),
    ("PIS/COFINS e IPI", ("pis", "cofins", "ipi")),
    ("Reforma Tributária: IBS/CBS, cClassTrib e IS", ("ibs", "cbs", "cclasstrib", "classificacao tributaria", "reforma", "creditos", "ncm")),
    ("TES, integração e modo híbrido", ("tes", "legad", "hibrid", "descontinu", "cj3", "f2d", "sft", "f2b_regra")),
    ("DFe, validação e simuladores", ("simulad", "nfe", "nota tecnica", "transmiss", "rejeic", "diagnostico")),
    ("Governança: aprovação, vigência e compartilhamento", ("aprovac", "vigen", "compartilh", "menu", "vers")),
    ("Erros conhecidos e sustentação", ("error", "erro", "ajuste", "webinars", "perguntas")),
)


def render_fontes(fontes: list[dict[str, str]]) -> str:
    linhas = [
        "# Mapa de fontes TOTVS por tema",
        "",
        "Gerado a partir dos índices versionados em `data/indices/` (TDN + Central de Atendimento).",
        "Nada aqui foi digitado à mão: todo link existe no repositório.",
        "",
    ]
    MAX_POR_TEMA = 14
    usados: set[str] = set()
    for tema, chaves in TEMAS_FONTES:
        chaves_norm = [sem_acento(c) for c in chaves]
        itens = [
            f
            for f in fontes
            if any(c in sem_acento(f["title"]) for c in chaves_norm)
        ]
        for f in itens:
            usados.add(f["url"])
        linhas.append(f"## {tema}")
        linhas.append("")
        if not itens:
            linhas.append("_Nenhum link marcado no índice para este tema._")
        for f in sorted(itens, key=lambda r: sem_acento(r["title"]))[:MAX_POR_TEMA]:
            linhas.append(f"- [{f['title']}]({f['url']})")
        if len(itens) > MAX_POR_TEMA:
            linhas.append(f"- _+{len(itens) - MAX_POR_TEMA} links do mesmo tema: buscar no Buscador Protheus ou em `data/indices/`._")
        linhas.append("")
    restantes = [f for f in fontes if f["url"] not in usados]
    linhas += [
        "## Links do índice ainda não classificados",
        "",
        f"_Total: {len(restantes)} disponíveis em `data/indices/` (busque por CFOP, NCM, TES, IBSCBS ou pelo app do Buscador Protheus)._",
        "",
    ]
    for f in sorted(restantes, key=lambda r: sem_acento(r["title"]))[:25]:
        linhas.append(f"- [{f['title']}]({f['url']})")
    linhas.append("")
    return "\n".join(linhas)


def fontechave(fontes: list[dict[str, str]], *chaves: str) -> str:
    """Devolve `- [Título](URL)` para o primeiro título que contenha todas as chaves."""
    norm = [sem_acento(c) for c in chaves]
    for f in fontes:
        t = sem_acento(f["title"])
        if all(c in t for c in norm):
            return f"- [{f['title']}]({f['url']})"
    for f in fontes:
        t = sem_acento(f["title"])
        if any(c in t for c in norm):
            return f"- [{f['title']}]({f['url']})"
    return "- _fonte não localizada no índice local: revisar manualmente_"


# ----------------------------------------------------------------------------- matriz


def ler_matriz(caminho: Path) -> list[dict[str, str]]:
    with caminho.open(encoding="utf-8-sig", newline="") as fh:
        leitor = csv.DictReader(fh, delimiter=";")
        if not leitor.fieldnames:
            raise SystemExit(f"Matriz {caminho} sem cabeçalho.")
        faltando = [n for n in NOMES_CAMPOS if n not in leitor.fieldnames]
        if faltando:
            raise SystemExit(
                "Matriz incompleta: faltam colunas " + ", ".join(faltando) + ". Regere com --init-csv."
            )
        linhas: list[dict[str, str]] = []
        for row in leitor:
            linhas.append({chave: (row.get(chave) or "").strip() for chave in leitor.fieldnames})
        return linhas


def escrever_csv(caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", lineterminator="\n")
        writer.writerow(NOMES_CAMPOS)
        for exemplo in EXEMPLOS:
            writer.writerow([exemplo.get(nome, "") for nome in NOMES_CAMPOS])


EXEMPLOS: tuple[dict[str, str], ...] = (
    {
        "cod_operacao": "DEM-001",
        "nome_operacao": "Remessa de mercadoria para demonstração (SP)",
        "grupo_operacao": "demonstracao",
        "sentido": "saida",
        "ambito": "interna",
        "uf_origem": "SP",
        "uf_destino": "SP",
        "documento": "NF-e",
        "finalidade": "simbolica",
        "mod_protheus": "faturamento",
        "vigencia_inicio": "2026-01-01",
        "base_legal": "Suspensão na saída para demonstração - confirmar artigo do RICMS/SP e Ajuste SINIEF aplicável",
        "responsavel": "a definir",
        "status": "levantada",
        "produtos_aplicavel": "todos",
        "origem_mercadoria": "0",
        "participantes_aplicavel": "clientes contribuintes e não contribuintes",
        "destinatario_contribuinte": "indiferente",
        "finalidade_item": "demonstração",
        "livro_fiscal": "Outros",
        "incidencia": "Outros",
        "diferimento_pct": "suspensão integral - sem débito de ICMS",
        "registros_sped": "C100/C170 (confirmar C190/C195 para o ajuste)",
        "codigo_ajuste": "confirmar se a SEFAZ-SP exige ajuste específico para a suspensão",
        "reflete_em": "nenhum",
        "contabilizacao": "sem efeito no resultado (imposto não debitado)",
        "pis_cofins_credito": "nao",
        "cfop_saida": "5912",
        "icms_origem": "5",
        "icms_cst": "50",
        "icms_credito": "nao",
        "ipi_cst": "53",
        "pis_cst": "49",
        "cofins_cst": "49",
        "pis_cofins_regime": "confirmar (cumulativo/não cumulativo)",
        "ibs_cst": "410",
        "cclasstrib": "410999",
        "tipo_beneficio": "suspensao",
        "cbene": "SP053190",
        "benef_descricao": "Suspensão - Saída de mercadoria remetida para demonstração, inclusive com destino a consumidor ou usuário final, até o momento em que ocorrer a transmissão de sua propriedade",
        "benef_vigencia": "2026-01-01",
        "tes": "704",
        "modo_calculo": "hibrido",
        "tes_campos_ativeis": "CFOP, cálculo de ICMS/PIS/COFINS e flag de IBS/CBS zerado - validar contra a lista de campos remanescentes",
        "aprovacao_regra": "sim",
        "evidencias": "pendiente",
        "duvidas_abertas": "CFOP de retorno (5913); tratamento da transmissão da propriedade; cBenef do retorno; IBS/CBS é suspensão (550) ou não incidência (410)?",
        "observacoes": "Operação sem deslocamento tributário: não gera débito de ICMS, mas precisa escrever corretamente no livro e no DFe.",
    },
    {
        "cod_operacao": "DEM-002",
        "nome_operacao": "Remessa de mercadoria para demonstração (interestadual a partir de SP)",
        "grupo_operacao": "demonstracao",
        "sentido": "saida",
        "ambito": "interestadual",
        "uf_origem": "SP",
        "uf_destino": "MG",
        "documento": "NF-e",
        "finalidade": "simbolica",
        "mod_protheus": "faturamento",
        "vigencia_inicio": "2026-01-01",
        "base_legal": "confirmar",
        "responsavel": "a definir",
        "status": "levantada",
        "produtos_aplicavel": "todos",
        "origem_mercadoria": "0",
        "destinatario_contribuinte": "indiferente",
        "cfop_saida": "6912",
        "livro_fiscal": "Outros",
        "incidencia": "Outros",
        "icms_origem": "5",
        "icms_cst": "50",
        "icms_credito": "nao",
        "ipi_cst": "53",
        "pis_cst": "49",
        "cofins_cst": "49",
        "ibs_cst": "410",
        "cclasstrib": "410999",
        "tipo_beneficio": "suspensao",
        "tes": "704",
        "modo_calculo": "hibrido",
        "aprovacao_regra": "sim",
        "evidencias": "pendiente",
        "duvidas_abertas": "Benefício paulista se aplica à saída interestadual? Qual o cBenef correspondente? O destino exige informação complementar?",
    },
)

# ----------------------------------------------------------------------------- análise


@dataclass
class Achado:
    campo: str
    nivel: str  # bloqueio | atencao
    problema: str
    pergunta: str


@dataclass
class Operacao:
    linha: dict[str, str]
    gaps: list[Achado] = field(default_factory=list)
    alertas: list[str] = field(default_factory=list)

    def get(self, nome: str) -> str:
        return (self.linha.get(nome) or "").strip()

    def tem(self, nome: str) -> bool:
        v = self.get(nome).lower()
        return bool(v) and v not in {"-", "nenhum", "na", "n/a", "pendente", "confirmar", "a definir", "tbd"}


def data_valida(txt: str) -> date | None:
    txt = (txt or "").strip()
    try:
        return date.fromisoformat(txt)
    except ValueError:
        pass
    partes = txt.split("/")
    if len(partes) == 3:
        try:
            dia, mes, ano = (int(p) for p in partes)
            return date(ano, mes, dia)
        except ValueError:
            return None
    return None


def analisar(linha: dict[str, str]) -> Operacao:
    op = Operacao(linha=linha)

    # campos obrigatórios vazios
    for campo in CAMPOS:
        if campo.obrig == "sim" and not op.tem(campo.nome):
            op.gaps.append(
                Achado(
                    campo.nome,
                    "bloqueio",
                    f"{campo.rotulo} não informado",
                    campo.dica or f"Informar {campo.rotulo}",
                )
            )

    cfop = op.get("cfop_saida")
    if cfop and not (cfop.isdigit() and len(cfop) == 4):
        op.gaps.append(Achado("cfop_saida", "bloqueio", f"CFOP `{cfop}` fora do formato AAAA", "Confirmar o CFOP de 4 dígitos sem pontuação"))
    elif cfop:
        esperado = DIGITOS_SAIDA.get(op.get("ambito"), "") or DIGITOS_ENTRADA.get(op.get("ambito"), "")
        if op.get("sentido") == "entrada":
            esperado = DIGITOS_ENTRADA.get(op.get("ambito"), "") or esperado
        if esperado and cfop[0] != esperado:
            op.gaps.append(
                Achado(
                    "ambito",
                    "atencao",
                    f"CFOP {cfop} não combina com sentido `{op.get('sentido')}` + abrangência `{op.get('ambito')}`",
                    "A operação é interna (1/5), interestadual (2/6) de importação/exportação (3/7)?",
                )
            )

    if op.get("cfop_entrada") and len(op.get("cfop_entrada")) != 4:
        op.gaps.append(Achado("cfop_entrada", "bloqueio", "`cfop_entrada` fora do formato AAAA", "Confirmar o CFOP usado no lado do parceiro"))

    if op.get("grupo_operacao").lower() in OPERACOES_COM_RETORNO and not op.tem("cfop_retorno"):
        op.gaps.append(
            Achado(
                "cfop_retorno",
                "bloqueio",
                "Operação de remessa/devolução sem CFOP de retorno mapeado",
                "Qual o CFOP de retorno e em quantos dias o retorno precisa ocorrer? O retorno usa o mesmo cBenef?",
            )
        )

    cst = op.get("icms_cst")
    cbene = op.get("cbene")
    if cst in CST_ICMS_COM_BENEFICIO:
        if op.get("uf_origem").upper() == "SP" and not op.tem("cbene"):
            op.gaps.append(
                Achado(
                    "cbene",
                    "bloqueio",
                    f"CST ICMS {cst} indica benefício e SP exige o cBenef na NF-e",
                    "Qual código da Tabela cBenef da SEFAZ-SP corresponde exatamente a esta operação?",
                )
            )
        elif op.get("uf_origem").upper() != "SP" and not cbene:
            op.alertas.append(
                f"CST ICMS {cst} costuma exigir cBenef. Confirmar se a UF {op.get('uf_origem') or '?'} exige o campo e qual código usar."
            )
    elif cst in CST_ICMS_SEM_BENEFICIO and cbene:
        op.alertas.append(f"CST ICMS {cst} normalmente não carrega benefício, mas há cBenef `{cbene}` informado.")

    if cst and cst in CST_ICMS_COM_BENEFICIO and not op.tem("base_legal"):
        op.gaps.append(
            Achado(
                "base_legal",
                "atencao",
                "Benefício informado sem fundamento legal",
                "Qual artigo/convênio sustenta a suspensão ou o diferimento? (vira regra de ajuste de lançamento e mensagem no documento)",
            )
        )

    # IBS/CBS
    ibs_cst, classif = op.get("ibs_cst"), op.get("cclasstrib")
    if ibs_cst and classif:
        if len(classif) != 6 or not classif.isdigit():
            op.gaps.append(Achado("cclasstrib", "bloqueio", f"cClassTrib `{classif}` deve ter 6 dígitos numéricos", "Copiar o código exato da tabela cClassTrib vigente"))
        elif classif[:3] != ibs_cst:
            op.gaps.append(
                Achado(
                    "cclasstrib",
                    "bloqueio",
                    f"cClassTrib `{classif}` não pertence ao CST IBS/CBS `{ibs_cst}`",
                    "Os 3 primeiros dígitos do cClassTrib devem ser iguais ao CST de IBS/CBS",
                )
            )
    if classif.startswith("4109") and classif.endswith("99"):
        op.alertas.append(
            "`410999` é o código residual de não incidência. Use apenas se nenhum código específico descrever a operação; a escolha errada distorce a apuração."
        )
    if ibs_cst in {"410", "500", "510", "515", "550"} and not op.tem("base_legal"):
        op.alertas.append(
            f"CST IBS/CBS `{ibs_cst}` sem fundamento legal informado: registrar o artigo da LC 214/2025 para suportar a escolha."
        )

    if op.tem("ipi_cst") and op.get("ipi_cst") in {"51", "52", "53", "54", "55"} and op.tem("ipi_aliquota"):
        try:
            if float(op.get("ipi_aliquota").replace("%", "").replace(",", ".")) > 0:
                op.alertas.append(f"IPI com CST {op.get('ipi_cst')} e alíquota {op.get('ipi_aliquota')}: rever, o CST não gera débito.")
        except ValueError:
            pass

    for cst_tri, ali in (("pis_cst", "pis_aliquota"), ("cofins_cst", "cofins_aliquota")):
        if op.get(cst_tri) in {"49"} and op.tem(ali):
            op.alertas.append(
                f"{cst_tri.split('_')[0].upper()} com CST 49 e alíquota informada: confirmar se o cadastro de tributos não vai calcular valor indevido (ver 'Desligamento Automático de PIS/COFINS')."
            )

    # motor de cálculo
    modo = op.get("modo_calculo").lower()
    if modo in {"hibrido", "cfgtrib", "configurador", "fisa170"}:
        obrigatorios_cfg = ["perfil_operacao", "regra_base", "regra_aliquota", "regra_tributaria"]
        for nome in obrigatorios_cfg:
            if not op.tem(nome):
                campo = POR_NOME[nome]
                op.gaps.append(
                    Achado(
                        nome,
                        "bloqueio",
                        f"Modo `{modo}` exige `{campo.rotulo}` antes de a regra funcionar no documento",
                        campo.dica or f"Informar {campo.rotulo}",
                    )
                )
        if modo == "hibrido" and not op.tem("tes_campos_ativeis"):
            op.gaps.append(
                Achado(
                    "tes_campos_ativeis",
                    "atencao",
                    "Modo híbrido sem definição do que ainda é decidido pela TES",
                    "Quais campos da TES continuam ativos para esta operação? (ver lista de campos remanescentes/descontinuados no TDN)",
                )
            )

    if not op.tem("regra_ncm") and op.tem("ncm_exemplo") and (op.tem("icms_aliquota") or op.tem("regra_aliquota")):
        op.gaps.append(
            Achado(
                "regra_ncm",
                "atencao",
                "Há NCM de exemplo e alíquota, mas nenhuma regra por NCM declarada",
                "A alíquota varia por NCM e por UF? Se sim, a regra será cadastrada em Regras por NCM (CIS/CIT)",
            )
        )

    if op.tem("icms_st_cst") and not (op.tem("icms_st_base") and op.tem("icms_st_aliquota")):
        op.gaps.append(
            Achado(
                "icms_st_base",
                "bloqueio",
                "Há ICMS-ST sem base (MVA/pauta/dupla) e sem alíquota interna do destino",
                "Qual o critério de formação da base da ST e a alíquota do estado de destino?",
            )
        )

    if op.tem("icms_redbc_pct") and not op.tem("incidencia_parcela_reduzida"):
        op.gaps.append(
            Achado(
                "incidencia_parcela_reduzida",
                "bloqueio",
                "Redução de base sem definir a incidência da parcela reduzida (CJ2_IREDBS)",
                "A parcela reduzida vai para Isento ou Outros? Em branco o sistema grava em Outros",
            )
        )

    if cst in CST_ICMS_COM_BENEFICIO and not op.tem("incidencia"):
        op.gaps.append(
            Achado(
                "incidencia",
                "bloqueio",
                "Operação desonerada sem incidência declarada na regra de escrituração",
                "Qual coluna do livro fiscal recebe esta operação (Tributado/Isento/Outros)?",
            )
        )

    if op.tem("cbene") and not op.tem("mensagem_dfe"):
        op.gaps.append(
            Achado(
                "mensagem_dfe",
                "atencao",
                "Benefício fiscal sem mensagem/dado adicional",
                "A legislação do benefício exige informação complementar no documento (ex.: número do processo, 'ICMS diferido')?",
            )
        )

    if op.tem("cbene") and not op.tem("benef_vigencia"):
        op.gaps.append(
            Achado(
                "benef_vigencia",
                "bloqueio",
                "cBenef sem data de início de vigência no catálogo (Tabela 52)",
                "Desde quando este código de benefício está válido? A regra de ajuste de lançamento usa a data de início",
            )
        )

    ini, fim = data_valida(op.get("vigencia_inicio")), data_valida(op.get("vigencia_fim"))
    if op.get("vigencia_inicio") and ini is None:
        op.gaps.append(Achado("vigencia_inicio", "bloqueio", "Vigência inicial inválida", "Usar AAAA-MM-DD"))
    if ini and fim and fim < ini:
        op.gaps.append(Achado("vigencia_fim", "bloqueio", "Vigência final anterior à inicial", "Revisar as datas"))
    if ini and ini >= OBRIGATORIEDATE_CBENEF_SP and op.get("uf_origem").upper() == "SP" and cst in CST_ICMS_COM_BENEFICIO and not op.tem("cbene"):
        op.gaps.append(
            Achado(
                "cbene",
                "bloqueio",
                "Vigência posterior a 06/04/2026 em SP sem cBenef",
                "Para NF-e paulistas com benefício, o cBenef é obrigatório a partir de 06/04/2026",
            )
        )

    if op.tem("evidencias") is False:
        op.gaps.append(
            Achado(
                "evidencias",
                "bloqueio",
                "Nenhuma evidência de aceite definida",
                "Quais evidências fecham a operação? (XML autorizado, simulador, livro fiscal, consulta CJ3/F2D)",
            )
        )

    prioridade = {"bloqueio": 0, "atencao": 1}
    unicas: dict[str, Achado] = {}
    for g in op.gaps:
        atual = unicas.get(g.campo)
        if atual is None or prioridade[g.nivel] < prioridade[atual.nivel]:
            unicas[g.campo] = g
    op.gaps = sorted(unicas.values(), key=lambda g: (prioridade[g.nivel], g.campo))
    return op


# ----------------------------------------------------------------------------- render


def tabela_dados(op: Operacao) -> list[str]:
    linhas = ["| Bloco | Campo | Valor informado |", "| --- | --- | --- |"]
    atual = None
    for campo in CAMPOS:
        valor = op.get(campo.nome)
        if not valor:
            continue
        if campo.bloco != atual:
            atual = campo.bloco
        linhas.append(f"| {campo.bloco} | `{campo.nome}` ({campo.rotulo}) | {valor} |")
    return linhas


def checklist(op: Operacao, fontes: list[dict[str, str]]) -> list[str]:
    modo = op.get("modo_calculo").lower()
    out: list[str] = ["## O que é preciso criar no Configurador de Tributos", ""]
    passos: list[tuple[str, list[str], list[tuple[str, ...]]]] = []

    passos.append(
        (
            "1. Confirmar o cenário de cálculo (TES x FISA170 x híbrido)",
            [
                f"- Motor declarado: `{modo or 'não informado'}`.",
                "- Validar quais impostos desta operação o FISA170 passa a calcular e quais campos continuam na TES.",
                "- Confirmar versão/atualização do dicionário e do motor de cálculo antes de cadastrar regra.",
            ],
            (("campos", "tes"), ("campos", "descontinu"), ("campos", "permanecem"), ("tes", "permanecer"), ("dicion", "motor")),
        )
    )
    passos.append(
        (
            "2. Cadastrar tributos e tabelas auxiliares",
            [
                "- Garantir que ICMS, IPI, PIS, COFINS, IBSEST e CBSFED existem e estão ativos no cadastro de tributos.",
                "- Importar/atualizar a tabela cClassTrib do IBS/CBS.",
                "- Manter os códigos de benefício na rotina de catálogo exigida pelo FISA170 (em SP, a Tabela 52 via FISA156).",
            ],
            (("carga", "automatica"), ("importar", "cclasstrib"), ("ajuste", "lancamento", "configurador")),
        )
    )
    passos.append(
        (
            "3. Perfis (produto, participante, origem x destino, operação)",
            [
                f"- Perfil de operação a partir do CFOP `{op.get('cfop_saida') or '?'}` e do documento `{op.get('documento') or '?'}`.",
                f"- Recorte de produtos: {op.get('produtos_aplicavel') or 'não informado'}.",
                f"- Recorte de participantes: {op.get('participantes_aplicavel') or 'não informado'}.",
                "- Usar o facilitador de cadastro para popular produto/participante e evitar perfil órfão.",
            ],
            (("facilitador",), ("perfil",), ("boas", "praticas", "perfis")),
        )
    )
    regras = []
    if op.tem("regra_base"):
        regras.append(f"- Base de cálculo: `{op.get('regra_base')}`.")
    if op.tem("regra_aliquota"):
        regras.append(f"- Alíquota: `{op.get('regra_aliquota')}`.")
    if op.tem("regra_ncm"):
        regras.append(f"- Regra por NCM: `{op.get('regra_ncm')}` (verificar se vale para todas as UFs).")
    if op.tem("icms_st_cst"):
        regras.append(f"- ICMS-ST: base `{op.get('icms_st_base')}` e alíquota `{op.get('icms_st_aliquota')}`.")
    if op.tem("reflete_em") and op.get("reflete_em").lower() not in {"nenhum", "nao"}:
        regras.append(f"- Reflexo/majoração entre tributos: `{op.get('reflete_em')}` (definir a ordem de cálculo).")
    if not regras:
        regras.append("- Definir regra de base e de alíquota para cada tributo que o FISA170 vai calcular.")
    passos.append(
        (
            "4. Regras de cálculo (base, alíquota, NCM, reflexo)",
            regras,
            (("regra", "calculo", "garantir"), ("regra", "por", "ncm"), ("influencia",), ("majorac",)),
        )
    )

    escrita = [
        f"- Incidência: `{op.get('incidencia') or 'não informada'}`; livro fiscal: `{op.get('livro_fiscal') or 'não informado'}`.",
        (
            f"- CST ICMS: origem `{op.get('icms_origem') or '?'}` + situação `{op.get('icms_cst') or '?'}`"
            f" (CST de 3 dígitos do XML: `{(op.get('icms_origem') or '?') + (op.get('icms_cst') or '?')}`);"
            f" CST IPI `{op.get('ipi_cst') or '?'}`; PIS/COFINS `{op.get('pis_cst') or '?'}` / `{op.get('cofins_cst') or '?'}`."
        ),
        f"- IBS/CBS: CST `{op.get('ibs_cst') or '?'}` + cClassTrib `{op.get('cclasstrib') or '?'}`.",
    ]
    if op.tem("diferimento_pct"):
        escrita.append(f"- Percentual de diferimento/suspensão na escrita: `{op.get('diferimento_pct')}`.")
    if op.tem("incidencia_parcela_reduzida"):
        escrita.append(f"- Parcela reduzida: `{op.get('incidencia_parcela_reduzida')}`.")
    if op.tem("codigo_ajuste"):
        escrita.append(f"- Código de ajuste/registro SPED: `{op.get('codigo_ajuste')}` / `{op.get('registros_sped')}`.")
    passos.append(
        (
            "5. Regra de escrituração (define livro, CST e apuração)",
            escrita,
            (("incidencia", "escrituracao"), ("escrituracao",), ("lançamento", "cat")),
        )
    )

    beneficio = []
    if op.tem("cbene"):
        beneficio += [
            f"- Criação da regra de ajuste de lançamento com código `{op.get('cbene')}` (tabela de benefícios), vigência `{op.get('benef_vigencia') or 'a confirmar'}` e a regra tributária correspondente.",
            f"- Texto do documento: {op.get('benef_descricao') or 'confirmar a descrição exigida pela SEFAZ'}.",
        ]
    if op.tem("mensagem_dfe"):
        beneficio.append(f"- Mensagem/cadastro de mensagens: `{op.get('mensagem_dfe')}`.")
    if not beneficio:
        beneficio.append("- Sem benefício fiscal declarado; confirmar se a operação realmente não exige cBenef.")
    passos.append(
        (
            "6. Benefício fiscal, cBenef e mensagens",
            beneficio,
            (("ajuste", "lancamento", "configurador"), ("mensagem", "documento", "fiscal"), ("dados", "adicionais")),
        )
    )

    if op.tem("tes"):
        passos.append(
            (
                "7. TES e amarração com o módulo de origem",
                [
                    f"- TES `{op.get('tes')}` no módulo `{op.get('mod_protheus') or 'não informado'}`.",
                    f"- Campos ativos na TES: {op.get('tes_campos_ativeis') or 'a confirmar'}",
                    "- Confirmar TES inteligente x regra do FISA170 e o que persiste em C5_RECISS/A1_RECISS quando for serviço.",
                ],
                (("tes", "inteligente"), ("reciss",), ("menu", "configurador")),
            )
        )

    aceite = [
        "- Simular a operação no simulador do FISA170 e comparar com o cálculo atual (legado).",
        "- Emitir nota em homologação e conferir as tags do XML: ICMS, IPI, PIS/COFINS e o grupo de IBS/CBS (CST + cClassTrib).",
        "- Conferir gravação em CJ3 (escrituração por item), F2D (tributos genéricos), SFT/SF3 e o código de regra no documento (F2B_REGRA).",
        "- Validar livro fiscal, apuração do período e contabilização dos tributos.",
        "- Submeter a regra ao mecanismo de aprovação e registrar a vigência.",
    ]
    if op.get("ibs_cst") in {"410", "500"}:
        aceite.append(
            "- Validar a geração do grupo de IBS/CBS no XML: quando o tributo não é calculado, o grupo zerado provoca rejeição (ver o parâmetro que controla a geração do grupo no XML)."
        )
    passos.append(
        (
            "8. Validação, aprovação e publish",
            aceite,
            (("simulador", "operacao"), ("simulador", "comparativo"), ("tabelas", "fazem", "parte"), ("relacionamento", "sd1"), ("aprovac", "regra")),
        )
    )

    for titulo, itens, chaves in passos:
        out.append(f"### {titulo}")
        out.extend(itens)
        out.append("")
        out.append("**Fontes TOTVS:**")
        for grupo in chaves:
            out.append(fontechave(fontes, *grupo))
        out.append("")
    return out


def ficha(op: Operacao, fontes: list[dict[str, str]]) -> str:
    cod = op.get("cod_operacao") or "SEM-CODIGO"
    bloqueios = [g for g in op.gaps if g.nivel == "bloqueio"]
    atencao = [g for g in op.gaps if g.nivel == "atencao"]

    linhas = [
        f"# Ficha {cod} — {op.get('nome_operacao') or 'sem descrição'}",
        "",
        f"> Gerada por `scripts/gerar_pacote_fisa170.py`. Editar apenas a matriz em `docs/fisa170/modelos/matriz-operacoes.csv`.",
        "",
        "## Diagnóstico do levantamento",
        "",
        f"- Status: `{op.get('status') or 'não informado'}` · dono: {op.get('responsavel') or 'não informado'}",
        f"- **Bloqueios**: {len(bloqueios)} · **Pontos de atenção**: {len(atencao)}",
        "",
        "### Bloqueios (a regra não deve ser cadastrada sem isso)",
        "",
    ]
    if bloqueios:
        for g in bloqueios:
            linhas.append(f"- [ ] `{g.campo}` — {g.problema}. **Perguntar:** {g.pergunta}")
    else:
        linhas.append("- Nenhum. Dados mínimos completos.")
    linhas += ["", "### Pontos de atenção", ""]
    if atencao:
        for g in atencao:
            linhas.append(f"- [ ] `{g.campo}` — {g.problema}. **Perguntar:** {g.pergunta}")
    else:
        linhas.append("- Nenhum.")
    if op.alertas:
        linhas += ["", "### Riscos identificados automaticamente", ""]
        linhas += [f"- {a}" for a in op.alertas]
    if op.tem("duvidas_abertas"):
        linhas += ["", "### Dúvidas abertas pelo cliente", "", f"- {op.get('duvidas_abertas')}", ""]
    linhas += tabela_dados(op)
    linhas.append("")
    linhas += checklist(op, fontes)
    return "\n".join(linhas).rstrip() + "\n"


def resumo(ops: list[Operacao]) -> str:
    linhas = [
        "# Resumo do levantamento — FISA170",
        "",
        f"Gerado em {date.today().isoformat()} a partir de `docs/fisa170/modelos/matriz-operacoes.csv`.",
        "",
        "| Operação | Descrição | CFOP | CST ICMS | PIS/COF | IBS/CBS | cBenef | TES | Bloqueios | Atenções |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for op in ops:
        celulas = [
            op.get("cod_operacao") or "-",
            (op.get("nome_operacao") or "-")[:48],
            op.get("cfop_saida") or "-",
            op.get("icms_cst") or "-",
            f"{op.get('pis_cst') or '-'}/{op.get('cofins_cst') or '-'}",
            f"{op.get('ibs_cst') or '-'}/{op.get('cclasstrib') or '-'}",
            op.get("cbene") or "-",
            op.get("tes") or "-",
            str(len([g for g in op.gaps if g.nivel == "bloqueio"])),
            str(len([g for g in op.gaps if g.nivel == "atencao"])),
        ]
        linhas.append("| " + " | ".join(celulas) + " |")
    total_b = sum(len([g for g in op.gaps if g.nivel == "bloqueio"]) for op in ops)
    total_a = sum(len([g for g in op.gaps if g.nivel == "atencao"]) for op in ops)
    linhas += [
        "",
        f"**Total:** {len(ops)} operações · {total_b} bloqueios · {total_a} pontos de atenção.",
        "",
        "Cada operação tem uma ficha `ficha-<código>.md` com o checklist de construção no FISA170.",
        "",
    ]
    return "\n".join(linhas)


def lacunas(ops: list[Operacao]) -> str:
    linhas = [
        "# Lacunas do levantamento (roteiro de perguntas)",
        "",
        "Ordem sugerida: resolver todos os bloqueios por operação antes de abrir o cadastro no FISA170.",
        "",
    ]
    for op in ops:
        if not op.gaps:
            linhas.append(f"## {op.get('cod_operacao')} — completo")
            linhas.append("")
            continue
        linhas.append(f"## {op.get('cod_operacao')} — {op.get('nome_operacao')}")
        linhas.append("")
        for nivel in ("bloqueio", "atencao"):
            itens = [g for g in op.gaps if g.nivel == nivel]
            if not itens:
                continue
            linhas.append(f"**{'Bloqueios' if nivel == 'bloqueio' else 'Pontos de atenção'}**")
            linhas.append("")
            for g in itens:
                linhas.append(f"- `{g.campo}`: {g.problema} → **{g.pergunta}**")
            linhas.append("")
    return "\n".join(linhas).rstrip() + "\n"


# ----------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera o pacote de levantamento para o FISA170")
    parser.add_argument("--matriz", type=Path, default=MATRIZ_PADRAO, help="CSV da matriz de operações (separador ';')")
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO, help="Diretório de saída")
    parser.add_argument("--init-csv", action="store_true", help="Escreve o cabeçalho e os exemplos na matriz (--matriz)")
    parser.add_argument("--check", action="store_true", help="Sai com código 1 se houver bloqueio")
    args = parser.parse_args(argv)

    if args.init_csv:
        escrever_csv(args.matriz)
        print(f"Matriz criada em {args.matriz} com {len(CAMPOS)} colunas e {len(EXEMPLOS)} exemplos.")
        return 0

    fontes = carregar_fontes()
    linhas = ler_matriz(args.matriz)
    ops = [analisar(linha) for linha in linhas if any((v or "").strip() for v in linha.values())]
    if not ops:
        print("Nenhuma operação na matriz.", file=sys.stderr)
        return 1

    args.saida.mkdir(parents=True, exist_ok=True)
    (args.saida / "00-resumo.md").write_text(resumo(ops), encoding="utf-8")
    (args.saida / "01-lacunas.md").write_text(lacunas(ops), encoding="utf-8")
    (args.saida / "fontes.md").write_text(render_fontes(fontes), encoding="utf-8")
    for op in ops:
        cod = (op.get("cod_operacao") or "sem-codigo").lower().replace(" ", "-")
        (args.saida / f"ficha-{cod}.md").write_text(ficha(op, fontes), encoding="utf-8")

    bloqueios = sum(len([g for g in op.gaps if g.nivel == "bloqueio"]) for op in ops)
    atencao = sum(len([g for g in op.gaps if g.nivel == "atencao"]) for op in ops)
    print(
        f"{len(ops)} operações · {len(fontes)} links de fonte TOTVS · {bloqueios} bloqueios · {atencao} atenções -> {args.saida}"
    )
    return 1 if args.check and bloqueios else 0


if __name__ == "__main__":
    raise SystemExit(main())
