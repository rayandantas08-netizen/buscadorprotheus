import { describe, expect, it } from "vitest";
import knowledge from "@/../public/knowledge.json";
import { searchRecords, type KnowledgeRecord } from "./search";

const records = knowledge.records as unknown as KnowledgeRecord[];

/** Fontes oficiais que explicam por que o Documento de Entrada fica sem os impostos do FISA170. */
const FONTES_DO_SINTOMA = [
  "35357410638231", // FISA170 - impostos gerados pelo Configurador de Tributos ou pela TES?
  "37535417591319", // SIGAEST - como identificar impostos do Configurador nas notas fiscais
  "35041323516183", // FISA170 - critérios para a Regra de Cálculo ser aplicada
  "825324831", // CFGTRIB - Cadastro de Perfis - Boas Práticas
  "887731155", // CFGTRIB - Cadastro de Regras de Cálculo - Boas Práticas
  "35446019140119", // SIGAFIN - impostos no financeiro a partir do documento de entrada
  "754953443", // CFGTRIB - Cálculo de ICMS ST (exemplo de documento de entrada)
  "38741160434199", // Relacionamento entre SD1/SD2, SFT, CJ3 e F2D
];

describe("índice local para documento de entrada sem os impostos do Configurador de Tributos", () => {
  it("carrega as fontes oficiais do roteiro de diagnóstico", () => {
    for (const id of FONTES_DO_SINTOMA) {
      expect(
        records.some(record => record.url.includes(id)),
        `link ausente do índice: ${id}`
      ).toBe(true);
    }
  });

  it("mantém o total declarado coerente com o índice regenerado", () => {
    expect(knowledge.total).toBe(records.length);
    expect(knowledge.total).toBeGreaterThanOrEqual(2391);
  });

  it("devolve o artigo de identificação dos tributos como primeiro resultado da frase do usuário", () => {
    const resultado = searchRecords(
      records,
      "documento de entrada não está trazendo os impostos do configurador de tributos",
      "all"
    );

    expect(resultado[0]?.url).toContain("37535417591319");
    const top10 = resultado
      .slice(0, 10)
      .map(record => record.url)
      .join(" ");
    expect(top10).toContain("825324831"); // boas práticas de perfis: onde a regra deixa de enquadrar
    const urls = resultado.map(record => record.url).join(" ");
    expect(urls).toContain("35357410638231"); // Configurador x TES
    expect(urls).toContain("35446019140119"); // impostos no financeiro a partir da entrada
  });

  it("acha o mesmo roteiro digitando sem acento", () => {
    const urls = searchRecords(
      records,
      "documento de entrada impostos configurador de tributos",
      "all"
    )
      .map(record => record.url)
      .join(" ");
    expect(urls).toContain("37535417591319");
    expect(urls).toContain("35357410638231");
  });
});
