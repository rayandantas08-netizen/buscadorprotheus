export type TrilhaIntent = "implantar" | "treinar" | "customizar" | "suportar";

export type TrilhaLink = {
  id: number;
  title: string;
  label: string;
  url: string;
  module: string;
  moduleCode: string;
  source: string;
  linkType: string;
  intent: TrilhaIntent;
};

export type TrilhaTopico = {
  id: string;
  grupo: string;
  titulo: string;
  status: string;
  entrega?: string;
  resumo: string;
  rotinas: string[];
  implantar: string[];
  treinar: string[];
  validar: string[];
  observacoes: string[];
  totalCandidatos: number;
  links: TrilhaLink[];
};

export type TrilhaGrupo = {
  id: string;
  titulo: string;
  status: string;
  descricao: string;
};

export type TrilhaPayload = {
  version: number;
  generatedAt: string;
  projeto: string;
  descricao: string;
  totalLinksBase: number;
  grupos: TrilhaGrupo[];
  intencoes: Array<{ id: TrilhaIntent; titulo: string }>;
  topicos: TrilhaTopico[];
};

export const INTENT_ORDER: TrilhaIntent[] = ["implantar", "treinar", "customizar", "suportar"];

export const INTENT_LABEL: Record<TrilhaIntent, string> = {
  implantar: "Para implantar",
  treinar: "Para treinar",
  customizar: "Ponto de entrada",
  suportar: "Suporte / FAQ",
};

/** Valida o JSON estático: a mesma chamada de fetch do site pode retornar outra base em testes. */
export function isTrilhaPayload(value: unknown): value is TrilhaPayload {
  if (!value || typeof value !== "object") return false;
  const candidate = value as Partial<TrilhaPayload>;
  return (
    Array.isArray(candidate.grupos) &&
    Array.isArray(candidate.topicos) &&
    candidate.topicos.every((topico) => typeof topico?.titulo === "string" && Array.isArray(topico?.links))
  );
}

export function topicosDoGrupo(payload: TrilhaPayload, grupoId: string) {
  return payload.topicos.filter((topico) => topico.grupo === grupoId);
}

export function linksPorIntencao(links: TrilhaLink[]) {
  const grupos = new Map<TrilhaIntent, TrilhaLink[]>();
  for (const intent of INTENT_ORDER) grupos.set(intent, []);
  for (const link of links) {
    const chave: TrilhaIntent = INTENT_ORDER.includes(link.intent) ? link.intent : "implantar";
    grupos.get(chave)?.push(link);
  }
  return grupos;
}

export type FiltroStatus = "todos" | "pendente" | "concluido" | "apoio";

export function filtrarTopicos(payload: TrilhaPayload, status: FiltroStatus, busca: string) {
  const termo = busca.trim().toLocaleLowerCase("pt-BR");
  return payload.topicos.filter((topico) => {
    if (status !== "todos" && topico.status !== status) return false;
    if (!termo) return true;
    const alvo = [topico.titulo, topico.resumo, ...topico.rotinas, ...topico.links.map((link) => link.label)]
      .join(" ")
      .toLocaleLowerCase("pt-BR");
    return alvo.includes(termo);
  });
}

export function resumoTrilha(payload: TrilhaPayload) {
  const pendentes = payload.topicos.filter((topico) => topico.status === "pendente");
  const concluidos = payload.topicos.filter((topico) => topico.status === "concluido");
  const links = payload.topicos.reduce((total, topico) => total + topico.links.length, 0);
  const unicos = new Set(payload.topicos.flatMap((topico) => topico.links.map((link) => link.url))).size;
  return {
    totalTopicos: payload.topicos.length,
    pendentes: pendentes.length,
    concluidos: concluidos.length,
    links,
    linksUnicos: unicos,
  };
}
