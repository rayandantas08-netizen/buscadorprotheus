export type KnowledgeRecord = {
  id: number;
  title: string;
  url: string;
  module: string;
  moduleCode: string;
  source: string;
  linkType: string;
  kind: "article" | "section";
  searchText: string;
};

export function tokenize(value: string) {
  return value
    .toLocaleLowerCase("pt-BR")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .split(/[^a-z0-9_]+/)
    .filter(token => token.length > 1);
}

/**
 * Normaliza o texto comparado com a mesma regra do `tokenize`.
 *
 * Sem isso, um token sem acento ("apuracao") nunca casava com o título acentuado
 * ("Apuração de ICMS") e a consulta devolvia quase nada.
 */
export function normalizeText(value: string) {
  return value
    .toLocaleLowerCase("pt-BR")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

/**
 * Palavras que aparecem em quase todos os títulos fiscais ("de", "do", "os"...).
 * Continuam valendo ponto, mas valem pouco: sem isso um título genérico cheio de
 * preposições ultrapassa o artigo que realmente responde à pergunta.
 */
const STOPWORDS = new Set([
  "ao",
  "aos",
  "as",
  "com",
  "como",
  "da",
  "das",
  "de",
  "do",
  "dos",
  "e",
  "em",
  "essa",
  "esse",
  "esta",
  "este",
  "isso",
  "na",
  "nas",
  "no",
  "nos",
  "os",
  "ou",
  "para",
  "pela",
  "pelo",
  "por",
  "qual",
  "quais",
  "que",
  "sao",
  "se",
  "sem",
  "ser",
  "um",
  "uma",
  "umas",
  "uns",
]);

const STOPWORD_TITLE_POINTS = 1;
const STOPWORD_SEARCH_POINTS = 1;
const TOKEN_TITLE_POINTS = 6;
const TOKEN_SEARCH_POINTS = 2;
const PAIR_POINTS = 5;
const TRIPLE_POINTS = 9;
/** Peso da forma flexionada ("tributos" x "tributo"): vale menos que a palavra exata. */
const VARIANT_WEIGHT = 2 / 3;

function hasContentWord(tokens: string[]) {
  return tokens.some(token => !STOPWORDS.has(token));
}

/** Bônus para expressões da consulta que aparecem inteiras, e na mesma ordem, no título. */
function phraseBonus(title: string, tokens: string[]) {
  let bonus = 0;
  for (const size of [3, 2]) {
    for (let start = 0; start + size <= tokens.length; start += 1) {
      const phrase = tokens.slice(start, start + size);
      if (!hasContentWord(phrase)) continue;
      if (title.includes(phrase.join(" ")))
        bonus += size === 3 ? TRIPLE_POINTS : PAIR_POINTS;
    }
  }
  return bonus;
}

/**
 * Formas aceitas para um token: a palavra digitada e a flexão de plural/singular.
 * A documentação mistura "tributo" e "tributos", "imposto" e "impostos"; sem isso a
 * consulta no plural não encontrava o artigo escrito no singular.
 */
function tokenVariants(token: string): { value: string; weight: number }[] {
  if (token.endsWith("s") && token.length > 4) {
    return [
      { value: token, weight: 1 },
      { value: token.slice(0, -1), weight: VARIANT_WEIGHT },
    ];
  }
  if (token.length > 3) {
    return [
      { value: token, weight: 1 },
      { value: `${token}s`, weight: VARIANT_WEIGHT },
    ];
  }
  return [{ value: token, weight: 1 }];
}

function scoreRecord(record: KnowledgeRecord, query: string) {
  const normalizedQuery = normalizeText(query).trim();
  const title = normalizeText(record.title);
  const searchText = normalizeText(record.searchText);
  const tokens = tokenize(query);
  let score = 0;

  if (normalizedQuery.length > 1) {
    if (title.includes(normalizedQuery)) score += 20;
    if (searchText.includes(normalizedQuery)) score += 8;
  }

  for (const token of tokens) {
    const stopword = STOPWORDS.has(token);
    const titlePoints = stopword ? STOPWORD_TITLE_POINTS : TOKEN_TITLE_POINTS;
    const searchPoints = stopword
      ? STOPWORD_SEARCH_POINTS
      : TOKEN_SEARCH_POINTS;
    const variants = stopword
      ? [{ value: token, weight: 1 }]
      : tokenVariants(token);

    for (const variant of variants) {
      if (title.includes(variant.value)) {
        score += titlePoints * variant.weight;
        break;
      }
      if (searchText.includes(variant.value)) {
        score += searchPoints * variant.weight;
        break;
      }
    }
  }

  return score + phraseBonus(title, tokens);
}

export function searchRecords(
  records: KnowledgeRecord[],
  query: string,
  module: string,
  source = "all",
  limit = 40
) {
  const byModule =
    module === "all"
      ? records
      : records.filter(record => record.module === module);
  const base =
    source === "all"
      ? byModule
      : byModule.filter(record => record.source === source);
  if (!query.trim()) return base.slice(0, limit);

  return base
    .map(record => ({ record, score: scoreRecord(record, query) }))
    .filter(({ score }) => score > 0)
    .sort(
      (a, b) =>
        b.score - a.score ||
        a.record.title.localeCompare(b.record.title, "pt-BR")
    )
    .slice(0, limit)
    .map(({ record }) => record);
}
