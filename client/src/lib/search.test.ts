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
    searchText: "como configurar o parâmetro mv_atvevt na nfs-e nacional sigafat faturamento",
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
];

describe("busca local do Buscador Protheus", () => {
  it("normaliza acentos e separa tokens técnicos", () => {
    expect(tokenize("Configuração MV_ATVEVT")).toEqual(["configuracao", "mv_atvevt"]);
  });

  it("prioriza o título que contém o termo exato", () => {
    const result = searchRecords(records, "MV_ATVEVT", "all");
    expect(result[0]?.id).toBe(1);
  });

  it("aplica o filtro do módulo antes do ranking", () => {
    const result = searchRecords(records, "TES", "Escrituração e Relatórios Fiscal");
    expect(result).toHaveLength(1);
    expect(result[0]?.moduleCode).toBe("SIGAFIS");
  });

  it("filtra por origem depois do módulo", () => {
    const result = searchRecords(records, "", "all", "TDN");
    expect(result).toHaveLength(1);
    expect(result[0]?.id).toBe(1);
  });

  it("retorna os primeiros registros quando a consulta está vazia", () => {
    expect(searchRecords(records, "", "all")).toHaveLength(2);
  });

  it("recalcula os resultados para cada valor digitado", () => {
    expect(searchRecords(records, "MV", "all")[0]?.id).toBe(1);
    expect(searchRecords(records, "MATA", "all")[0]?.id).toBe(2);
  });
});

