import { describe, expect, it } from "vitest";
import inventory from "@/../../data/tdn_protheus12_inventory.json";

describe("inventário da árvore Protheus 12 no TDN", () => {
  it("mantém uma coleção reproduzível de URLs únicas e informa o estado de cobertura", () => {
    const urls = inventory.pages.map(page => page.url);

    expect(inventory.total).toBeGreaterThanOrEqual(250);
    expect(inventory.total).toBe(inventory.pages.length);
    expect(new Set(urls).size).toBe(urls.length);
    expect(urls).toContain("https://tdn.totvs.com/display/PROT/Protheus++12");
    expect(inventory.coverage_status).toContain("not proven");
  });
});
