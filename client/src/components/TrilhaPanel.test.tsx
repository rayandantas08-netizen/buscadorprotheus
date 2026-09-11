import React from "react";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import TrilhaPanel from "./TrilhaPanel";
import type { TrilhaPayload } from "@/lib/trilhas";

const trilha: TrilhaPayload = {
  version: 1,
  generatedAt: "2026-09-11",
  projeto: "Minérios Gerais — implantação e treinamento do Fiscal Protheus 12",
  descricao: "Trilha de testes.",
  totalLinksBase: 2382,
  grupos: [
    { id: "agenda", titulo: "Agenda 09/09", status: "pendente", descricao: "Tópicos da agenda." },
    { id: "apoio", titulo: "Materiais de apoio", status: "apoio", descricao: "Treinamento oficial." },
  ],
  intencoes: [
    { id: "implantar", titulo: "Para implantar / parametrizar" },
    { id: "treinar", titulo: "Para treinar" },
    { id: "customizar", titulo: "Pontos de entrada" },
    { id: "suportar", titulo: "Suporte / FAQ" },
  ],
  topicos: [
    {
      id: "bloco-k",
      grupo: "agenda",
      titulo: "Bloco K — controle da produção e do estoque",
      status: "pendente",
      entrega: "09/09",
      resumo: "Geração do Bloco K no SPED Fiscal.",
      rotinas: ["SPEDFISCAL", "MATA910"],
      implantar: ["Ativar MV_BLKTP00 e revisar as fontes do Bloco K."],
      treinar: ["Explicar K200/K220/K235 com exemplos de produção."],
      validar: ["Conferir o K200 no validador do SPED."],
      observacoes: ["Mineração: incluir perdas e refugo como procedimento de perda."],
      totalCandidatos: 14,
      links: [
        {
          id: 1,
          title: "Bloco K: Informações Gerais sobre o Bloco",
          label: "Bloco K: Informações Gerais sobre o Bloco",
          url: "https://tdn.totvs.com/pages/releaseview.action?pageId=259560649",
          module: "Fiscal - Protheus 12",
          moduleCode: "SIGAFIS",
          source: "TDN",
          linkType: "TDN — Release",
          intent: "implantar",
        },
        {
          id: 2,
          title: "SUP.PROTHEUS - Eventos Tira Dúvidas",
          label: "SUP.PROTHEUS - Eventos Tira Dúvidas",
          url: "https://tdn.totvs.com/pages/releaseview.action?pageId=550307175",
          module: "Fiscal - Protheus 12",
          moduleCode: "SIGAFIS",
          source: "TDN",
          linkType: "TDN — Release",
          intent: "treinar",
        },
      ],
    },
    {
      id: "treinamento-oficial",
      grupo: "apoio",
      titulo: "Materiais oficiais de treinamento e referência",
      status: "apoio",
      resumo: "Banco de conhecimento, webinars e guias.",
      rotinas: ["FISA170"],
      implantar: ["Usar o Banco de Conhecimento como referência."],
      treinar: ["Agendar os webinars do Configurador de Tributos."],
      validar: ["Registrar a presença da equipe nos treinamentos."],
      observacoes: [],
      totalCandidatos: 47,
      links: [
        {
          id: 3,
          title: "Conceitos - Fiscal - P12",
          label: "Conceitos - Fiscal - P12",
          url: "https://tdn.totvs.com/pages/viewpage.action?pageId=514454190",
          module: "Fiscal - Protheus 12",
          moduleCode: "SIGAFIS",
          source: "TDN",
          linkType: "TDN — Página",
          intent: "treinar",
        },
      ],
    },
  ],
};

describe("TrilhaPanel", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => trilha }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("lista os tópicos, abre o detalhe e filtra por status e busca", async () => {
    const user = userEvent.setup();
    render(<TrilhaPanel />);

    await waitFor(() => expect(screen.getByText(/Minérios Gerais/)).not.toBeNull());

    // tópico pendente já nasce aberto
    expect(screen.getByText("Bloco K: Informações Gerais sobre o Bloco")).not.toBeNull();
    expect(screen.getByText(/Ativar MV_BLKTP00/)).not.toBeNull();
    expect(screen.getByText(/Mineração: incluir perdas e refugo/)).not.toBeNull();

    // filtro por status
    await user.click(screen.getByRole("button", { name: /Já validados/i }));
    expect(screen.queryByText(/Bloco K — controle da produção/)).toBeNull();
    expect(screen.getByText(/Nenhum tópico corresponde ao filtro atual/)).not.toBeNull();

    await user.click(screen.getByRole("button", { name: /Todos os tópicos/i }));

    // busca por rotina
    await user.type(screen.getByLabelText(/Filtrar tópicos da trilha/i), "FISA170");
    expect(screen.getByText(/Materiais oficiais de treinamento/)).not.toBeNull();
    expect(screen.queryByText(/Bloco K — controle da produção/)).toBeNull();

    await user.clear(screen.getByLabelText(/Filtrar tópicos da trilha/i));

    // colapsar e reabrir um tópico
    const botao = screen.getByRole("button", { name: /Bloco K — controle da produção/ });
    await user.click(botao);
    expect(screen.queryByText(/Ativar MV_BLKTP00/)).toBeNull();
    await user.click(botao);
    const card = screen.getByText(/Bloco K — controle da produção/).closest("article")!;
    expect(within(card).getByText("SUP.PROTHEUS - Eventos Tira Dúvidas")).not.toBeNull();
    expect(within(card).getAllByRole("link").length).toBe(2);
  });

  it("mostra erro amigável quando o JSON não é uma trilha válida", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ total: 0, records: [] }) }));
    render(<TrilhaPanel />);
    await waitFor(() =>
      expect(screen.getByText(/formato inesperado/i)).not.toBeNull(),
    );
  });
});
