import { describe, expect, it } from "vitest";
import { searchRecords, tokenize, type KnowledgeRecord } from "./search";

const records: KnowledgeRecord[] = [
  {
    id: 1,
    title: "Como configurar o parâmetro MV_ATVEVT na NFS-e Nacional",
    url: "https://tdn.totvs.com/pages/viewpage.action?pageId=1065231996",
    module: "Faturamento",
    moduleCode: "SIGAFAT",
    source: "TDN",
    linkType: "TDN — Página",
    kind: "article",
    searchText:
      "como configurar o parâmetro mv_atvevt na nfs-e nacional sigafat faturamento",
  },
  {
    id: 2,
    title: "Pontos de Entrada TES MATA080",
    url: "https://centraldeatendimento.totvs.com/hc/pt-br/articles/4404850575767",
    module: "Escrituração e Relatórios Fiscal",
    moduleCode: "SIGAFIS",
    source: "Central de Atendimento TOTVS",
    linkType: "Central TOTVS — Artigo",
    kind: "article",
    searchText: "pontos de entrada tes mata080 sigafis escrituração fiscal",
  },
  {
    id: 3,
    title: "APUICM - Apuração de ICMS - MATA953",
    url: "https://tdn.totvs.com/pages/viewpage.action?pageId=514512000",
    module: "Fiscal - Protheus 12",
    moduleCode: "SIGAFIS",
    source: "TDN",
    linkType: "TDN — Página",
    kind: "article",
    searchText: "apuicm apuração de icms mata953 fiscal protheus 12",
  },
  {
    id: 4,
    title: "Imposto de Renda retido na nota fiscal de saída",
    url: "https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271222087959",
    module: "Configurador de Tributos",
    moduleCode: "FISA",
    source: "Central de Atendimento TOTVS",
    linkType: "Central TOTVS — Artigo",
    kind: "article",
    searchText:
      "imposto de renda retido na nota fiscal de saída fisa configurador de tributos",
  },
  {
    id: 5,
    title:
      "Documento de Entrada MATA103 sem os impostos do Configurador de Tributos",
    url: "https://centraldeatendimento.totvs.com/hc/pt-br/articles/35357410638231",
    module: "Configurador de Tributos",
    moduleCode: "FISA",
    source: "Central de Atendimento TOTVS",
    linkType: "Central TOTVS — Artigo",
    kind: "article",
    searchText:
      "documento de entrada mata103 sem os impostos do configurador de tributos fisa",
  },
  {
    id: 6,
    title: "Entrada de dados e configuração de tributos",
    url: "https://tdn.totvs.com/pages/viewpage.action?pageId=676039354",
    module: "Configurador de Tributos",
    moduleCode: "FISA",
    source: "TDN",
    linkType: "TDN — Página",
    kind: "article",
    searchText:
      "entrada de dados e configuração de tributos fisa configurador de tributos",
  },
];

describe("busca local do Buscador Protheus", () => {
  it("normaliza acentos e separa tokens técnicos", () => {
    expect(tokenize("Configuração MV_ATVEVT")).toEqual([
      "configuracao",
      "mv_atvevt",
    ]);
  });

  it("prioriza o título que contém o termo exato", () => {
    const result = searchRecords(records, "MV_ATVEVT", "all");
    expect(result[0]?.id).toBe(1);
  });

  it("aplica o filtro do módulo antes do ranking", () => {
    const result = searchRecords(
      records,
      "TES",
      "Escrituração e Relatórios Fiscal"
    );
    expect(result).toHaveLength(1);
    expect(result[0]?.moduleCode).toBe("SIGAFIS");
  });

  it("filtra por origem depois do módulo", () => {
    const result = searchRecords(records, "", "all", "TDN");
    expect(result.map(record => record.id)).toEqual([1, 3, 6]);
    expect(result[0]?.id).toBe(1);
  });

  it("retorna os primeiros registros quando a consulta está vazia", () => {
    expect(searchRecords(records, "", "all")).toHaveLength(records.length);
  });

  it("recalcula os resultados para cada valor digitado", () => {
    expect(searchRecords(records, "MV", "all")[0]?.id).toBe(1);
    expect(
      searchRecords(records, "MATA", "all")
        .map(record => record.id)
        .sort()
    ).toEqual([2, 3, 5]);
  });

  it("casa a consulta acentuada com o título acentuado", () => {
    // Antes o token sem acento ("apuracao") nunca casava com "Apuração" e a busca voltava vazia.
    expect(searchRecords(records, "apuração", "all")[0]?.id).toBe(3);
    expect(searchRecords(records, "apuracao", "all")[0]?.id).toBe(3);
  });

  it("casa o plural da consulta com o singular do título", () => {
    const ids = searchRecords(records, "impostos", "all").map(
      record => record.id
    );
    expect(ids).toContain(5); // "impostos" no título
    expect(ids).toContain(4); // "Imposto" no título
  });

  it("prioriza o título que traz a expressão completa em vez das preposições", () => {
    const result = searchRecords(
      records,
      "documento de entrada impostos do configurador de tributos",
      "all"
    );
    expect(result[0]?.id).toBe(5);
    expect(result.map(record => record.id)).toContain(6);
  });
});
