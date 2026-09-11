import { describe, expect, it } from "vitest";
import trilhas from "@/../public/trilhas.json";
import {
  INTENT_ORDER,
  filtrarTopicos,
  isTrilhaPayload,
  linksPorIntencao,
  resumoTrilha,
  topicosDoGrupo,
  type TrilhaPayload,
} from "./trilhas";

const payload = trilhas as unknown as TrilhaPayload;

const TOPICOS_DA_AGENDA = [
  "efd-icms-ipi",
  "efd-contribuicoes",
  "apuracao-icms-p9",
  "ciap",
  "bloco-k",
  "registro-inventario",
  "rotinas-fiscais",
  "taf-extrator-reinf",
  "revisao-parametrizacoes",
  "quebra-estoque",
  "exportacao",
];

describe("trilha de treinamento gerada a partir do índice local", () => {
  it("cobre todos os tópicos pedidos na agenda de Minérios Gerais", () => {
    expect(isTrilhaPayload(payload)).toBe(true);
    const ids = payload.topicos.map((topico) => topico.id);
    for (const esperado of TOPICOS_DA_AGENDA) expect(ids).toContain(esperado);
    expect(payload.topicos.every((topico) => topico.links.length >= 8)).toBe(true);
    expect(payload.topicos.every((topico) => topico.implantar.length > 0)).toBe(true);
  });

  it("não repete links, não usa título 'URL' e aponta só para domínios oficiais", () => {
    for (const topico of payload.topicos) {
      const urls = topico.links.map((link) => link.url);
      expect(new Set(urls).size).toBe(urls.length);
      for (const link of topico.links) {
        expect(link.label.trim().length).toBeGreaterThan(4);
        expect(link.label).not.toBe("URL");
        expect(link.url).not.toContain("totvs.comhttps://");
        expect(link.url).toMatch(/^https:\/\/(tdn|centraldeatendimento)\.totvs\.com\//);
        expect(INTENT_ORDER).toContain(link.intent);
      }
    }
  });

  it("traz o conteúdo específico de Minas Gerais no P9 e a documentação oficial no Bloco K", () => {
    const p9 = payload.topicos.find((topico) => topico.id === "apuracao-icms-p9");
    expect(
      p9?.links.some((link) => /Minas Gerais|P9AUTOTEXT\.MG|SINTEGRA-MG|MGREDICM|MGIVAAJUS|MGLEITE/i.test(link.title)),
    ).toBe(true);

    const blocoK = payload.topicos.find((topico) => topico.id === "bloco-k");
    expect(blocoK?.links.some((link) => /Bloco K/i.test(link.title))).toBe(true);
    expect(blocoK?.links.length).toBeGreaterThanOrEqual(10);

    const inventario = payload.topicos.find((topico) => topico.id === "registro-inventario");
    expect(inventario?.links.some((link) => /MATR460|Bloco H|Invent/i.test(link.title))).toBe(true);

    const taf = payload.topicos.find((topico) => topico.id === "taf-extrator-reinf");
    expect(taf?.links.some((link) => /REINF/i.test(link.title))).toBe(true);
    expect(taf?.links.some((link) => /Extrator/i.test(link.title))).toBe(true);
  });

  it("agrupa os links por intenção e mantém o resumo consistente", () => {
    const grupos = linksPorIntencao(payload.topicos[0].links);
    expect([...grupos.keys()]).toEqual(INTENT_ORDER);
    const total = [...grupos.values()].reduce((soma, links) => soma + links.length, 0);
    expect(total).toBe(payload.topicos[0].links.length);

    const resumo = resumoTrilha(payload);
    expect(resumo.totalTopicos).toBe(payload.topicos.length);
    expect(resumo.pendentes + resumo.concluidos).toBeLessThanOrEqual(resumo.totalTopicos);
    expect(resumo.links).toBe(payload.topicos.reduce((soma, topico) => soma + topico.links.length, 0));
    expect(resumo.linksUnicos).toBeLessThanOrEqual(resumo.links);
    expect(resumo.linksUnicos).toBeGreaterThan(100);
  });

  it("filtra por status, por busca e separa os tópicos por grupo da agenda", () => {
    const pendentes = filtrarTopicos(payload, "pendente", "");
    expect(pendentes.length).toBeGreaterThan(0);
    expect(pendentes.every((topico) => topico.status === "pendente")).toBe(true);

    expect(filtrarTopicos(payload, "todos", "bloco k").some((topico) => topico.id === "bloco-k")).toBe(true);
    expect(filtrarTopicos(payload, "todos", "MATA910").some((topico) => topico.id === "rotinas-fiscais")).toBe(true);
    expect(filtrarTopicos(payload, "todos", "zzz-termo-inexistente")).toHaveLength(0);

    expect(topicosDoGrupo(payload, "agenda-11-09").length).toBeGreaterThan(0);
    expect(payload.grupos.every((grupo) => topicosDoGrupo(payload, grupo.id).length > 0)).toBe(true);
  });
});
