import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import Home from "./Home";

const knowledge = {
  total: 2,
  modules: ["Escrituração e Relatórios Fiscal", "Faturamento"],
  linkTypes: ["Central TOTVS — Artigo", "TDN — Página"],
  records: [
    {
      id: 1,
      title: "Configuração do parâmetro MV_ATVEVT na NFS-e Nacional",
      url: "https://tdn.totvs.com/pages/viewpage.action?pageId=1065231996",
      module: "Faturamento",
      moduleCode: "SIGAFAT",
      source: "TDN",
      linkType: "TDN — Página",
      kind: "article",
      searchText: "configuração do parâmetro mv_atvevt na nfs-e nacional faturamento sigafat",
    },
    {
      id: 2,
      title: "Cross Segmentos — EFD Contribuições",
      url: "https://centraldeatendimento.totvs.com/hc/pt-br/articles/360048560713",
      module: "Escrituração e Relatórios Fiscal",
      moduleCode: "SIGAFIS",
      source: "Central de Atendimento TOTVS",
      linkType: "Central TOTVS — Artigo",
      kind: "article",
      searchText: "cross segmentos efd contribuições escrituração fiscal sigafis",
    },
  ],
};

describe("Home — busca live e filtro por módulo", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => knowledge,
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("atualiza os resultados ao digitar e mantém o filtro de módulo", async () => {
    const user = userEvent.setup();
    render(<Home />);

    await waitFor(() => expect(screen.getByText(/Cross Segmentos/)).not.toBeNull());

    const input = screen.getByPlaceholderText(/rejeição E0390/i);
    await user.type(input, "MV_ATVEVT");

    expect(screen.getByText(/Configuração do parâmetro MV_ATVEVT/)).not.toBeNull();
    expect(screen.queryByText(/Cross Segmentos/)).toBeNull();

    const moduleFilter = screen.getByRole("combobox", { name: "Filtrar por módulo" });
    await user.selectOptions(moduleFilter, "Escrituração e Relatórios Fiscal");
    expect(screen.getByText(/Nenhum link correspondeu/)).not.toBeNull();

    await user.selectOptions(moduleFilter, "all");
    const sourceFilter = screen.getByRole("combobox", { name: "Filtrar por origem" });
    await user.selectOptions(sourceFilter, "Central de Atendimento TOTVS");
    expect(screen.getByText(/Nenhum link correspondeu/)).not.toBeNull();

    await user.clear(input);
    await user.type(input, "EFD");
    expect(screen.getByText(/Cross Segmentos/)).not.toBeNull();
    expect(screen.queryByText(/Configuração do parâmetro MV_ATVEVT/)).toBeNull();
  });
});

