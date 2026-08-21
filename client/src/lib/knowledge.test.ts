import { describe, expect, it } from "vitest";
import knowledge from "@/../public/knowledge.json";

describe("índice estático do Fiscal - Protheus 12", () => {
  it("contém a raiz e uma coleção ampla de páginas TDN sem URLs duplicadas", () => {
    const fiscalRecords = knowledge.records.filter(
      record => record.module === "Fiscal - Protheus 12",
    );
    const fiscalUrls = fiscalRecords.map(record => record.url);

    expect(fiscalRecords.length).toBeGreaterThanOrEqual(500);
    expect(fiscalUrls).toContain(
      "https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12",
    );
    expect(new Set(fiscalUrls).size).toBe(fiscalUrls.length);
    expect(fiscalRecords.some(record => record.title.includes("APUICM"))).toBe(true);
    expect(fiscalRecords.some(record => record.title.includes("ICMS-ST"))).toBe(true);
  });

  it("mantém o total declarado consistente com o número de registros", () => {
    expect(knowledge.total).toBe(knowledge.records.length);
  });
});
