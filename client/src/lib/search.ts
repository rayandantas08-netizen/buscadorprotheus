export type KnowledgeRecord = {
  id: number;
  title: string;
  url: string;
  module: string;
  moduleCode: string;
  source: string;
  kind: "article" | "section";
  searchText: string;
};

export function tokenize(value: string) {
  return value
    .toLocaleLowerCase("pt-BR")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .split(/[^a-z0-9_]+/)
    .filter((token) => token.length > 1);
}

function scoreRecord(record: KnowledgeRecord, query: string) {
  const normalizedQuery = query.toLocaleLowerCase("pt-BR");
  const title = record.title.toLocaleLowerCase("pt-BR");
  const searchText = record.searchText.toLocaleLowerCase("pt-BR");
  const tokens = tokenize(query);
  let score = 0;

  if (title.includes(normalizedQuery)) score += 20;
  if (searchText.includes(normalizedQuery)) score += 8;
  for (const token of tokens) {
    if (title.includes(token)) score += 6;
    else if (searchText.includes(token)) score += 2;
  }
  return score;
}

export function searchRecords(records: KnowledgeRecord[], query: string, module: string, limit = 40) {
  const base = module === "all" ? records : records.filter((record) => record.module === module);
  if (!query.trim()) return base.slice(0, limit);

  return base
    .map((record) => ({ record, score: scoreRecord(record, query) }))
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score || a.record.title.localeCompare(b.record.title, "pt-BR"))
    .slice(0, limit)
    .map(({ record }) => record);
}

