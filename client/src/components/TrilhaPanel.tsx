import React, { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BadgeCheck,
  Boxes,
  ChevronDown,
  CircleDashed,
  CircleHelp,
  ClipboardCheck,
  ExternalLink,
  GraduationCap,
  Info,
  Link2,
  Loader2,
  Route,
  Search,
  Wrench,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import {
  INTENT_LABEL,
  INTENT_ORDER,
  type FiltroStatus,
  type TrilhaLink,
  type TrilhaPayload,
  type TrilhaTopico,
  filtrarTopicos,
  isTrilhaPayload,
  linksPorIntencao,
  resumoTrilha,
} from "@/lib/trilhas";

const FILTROS: Array<{ id: FiltroStatus; label: string; icon: typeof Route }> = [
  { id: "todos", label: "Todos os tópicos", icon: Boxes },
  { id: "pendente", label: "Na agenda", icon: CircleDashed },
  { id: "concluido", label: "Já validados", icon: BadgeCheck },
  { id: "apoio", label: "Apoio / treinamento", icon: GraduationCap },
];

const INTENT_ICON = {
  implantar: Wrench,
  treinar: GraduationCap,
  customizar: Route,
  suportar: Info,
} as const;

const STATUS_BADGE: Record<string, string> = {
  concluido: "border-emerald-300/25 bg-emerald-300/10 text-emerald-100",
  pendente: "border-amber-300/25 bg-amber-300/10 text-amber-100",
  apoio: "border-cyan-300/25 bg-cyan-300/10 text-cyan-100",
};

const STATUS_LABEL: Record<string, string> = {
  concluido: "Já validado no cliente",
  pendente: "Na agenda",
  apoio: "Apoio",
};

function LinkLinha({ link }: { link: TrilhaLink }) {
  return (
    <li>
      <a
        href={link.url}
        target="_blank"
        rel="noreferrer"
        className="group flex items-start gap-2.5 rounded-xl border border-white/10 bg-[#071018] px-3 py-2.5 transition hover:border-cyan-300/40 hover:bg-[#0d1c29]"
      >
        <Link2 size={14} className="mt-0.5 shrink-0 text-slate-500 group-hover:text-cyan-200" />
        <span className="min-w-0 flex-1">
          <span className="block truncate text-xs leading-5 text-slate-200 group-hover:text-cyan-100" title={link.title}>
            {link.label}
          </span>
          <span className="mt-0.5 block truncate font-mono text-[10px] uppercase tracking-wide text-slate-500">
            {link.moduleCode} · {link.source} · {link.linkType}
          </span>
        </span>
        <ExternalLink size={13} className="mt-0.5 shrink-0 text-slate-600 group-hover:text-cyan-200" />
      </a>
    </li>
  );
}

function PassoLista({ titulo, itens, icone: Icone, cor }: { titulo: string; itens: string[]; icone: typeof Wrench; cor: string }) {
  if (itens.length === 0) return null;
  return (
    <div className="rounded-xl border border-white/10 bg-[#071018] p-4">
      <p className={cn("flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em]", cor)}>
        <Icone size={14} />
        {titulo}
      </p>
      <ol className="mt-3 space-y-2.5 text-xs leading-5 text-slate-300">
        {itens.map((item, index) => (
          <li key={item} className="flex gap-2.5">
            <span className="mt-0.5 shrink-0 rounded-md border border-white/10 bg-[#0b1722] px-1.5 font-mono text-[10px] text-cyan-200/80">
              {String(index + 1).padStart(2, "0")}
            </span>
            <span>{item}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

function TopicoCard({
  topico,
  titulosIntencao,
  aberto,
  onToggle,
}: {
  topico: TrilhaTopico;
  titulosIntencao: Record<string, string>;
  aberto: boolean;
  onToggle: () => void;
}) {
  const grupos = linksPorIntencao(topico.links);

  return (
    <article className="overflow-hidden rounded-2xl border border-white/10 bg-[#0b1722] transition hover:border-cyan-300/25">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={aberto}
        className="flex w-full cursor-pointer items-start gap-4 px-5 py-4 text-left"
      >
        <span className="min-w-0 flex-1">
          <span className="block text-sm font-semibold leading-6 text-white">{topico.titulo}</span>
          <span className="mt-1 block text-xs leading-5 text-slate-400">{topico.resumo}</span>
        </span>
        <span className="flex shrink-0 items-center gap-2">
          <Badge className={cn("rounded-full border font-mono text-[10px] hover:bg-transparent", STATUS_BADGE[topico.status])}>
            {STATUS_LABEL[topico.status] ?? topico.status}
            {topico.entrega ? ` · ${topico.entrega}` : ""}
          </Badge>
          <Badge variant="outline" className="rounded-full border-white/10 font-mono text-[10px] text-slate-400">
            {topico.links.length} links
          </Badge>
          <ChevronDown size={16} className={cn("text-slate-500 transition", aberto && "rotate-180 text-cyan-200")} />
        </span>
      </button>

      {aberto && (
        <div className="border-t border-white/10 px-5 py-5">
          {topico.rotinas.length > 0 && (
            <div className="mb-4 flex flex-wrap items-center gap-1.5">
              <span className="mr-1 font-mono text-[10px] uppercase tracking-[0.18em] text-slate-500">Rotinas</span>
              {topico.rotinas.map((rotina) => (
                <span
                  key={rotina}
                  className="rounded-md border border-cyan-300/20 bg-cyan-300/5 px-2 py-0.5 font-mono text-[10px] text-cyan-100"
                >
                  {rotina}
                </span>
              ))}
            </div>
          )}

          <div className="grid gap-3 lg:grid-cols-3">
            <PassoLista titulo="Como implantar" itens={topico.implantar} icone={Wrench} cor="text-cyan-200" />
            <PassoLista titulo="Como treinar" itens={topico.treinar} icone={GraduationCap} cor="text-emerald-200" />
            <PassoLista titulo="Como validar" itens={topico.validar} icone={ClipboardCheck} cor="text-violet-200" />
          </div>

          {topico.observacoes.length > 0 && (
            <div className="mt-3 space-y-2">
              {topico.observacoes.map((observacao) => (
                <p
                  key={observacao}
                  className="flex gap-2.5 rounded-xl border border-amber-300/20 bg-amber-300/5 px-3.5 py-2.5 text-xs leading-5 text-amber-100"
                >
                  <AlertTriangle size={14} className="mt-0.5 shrink-0 text-amber-200" />
                  {observacao}
                </p>
              ))}
            </div>
          )}

          <Separator className="my-5 bg-white/10" />

          <div className="grid gap-5 xl:grid-cols-2">
            {INTENT_ORDER.map((intent) => {
              const links = grupos.get(intent) ?? [];
              if (links.length === 0) return null;
              const Icone = INTENT_ICON[intent];
              return (
                <div key={intent}>
                  <p className="mb-2.5 flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-slate-400">
                    <Icone size={14} className="text-cyan-200" />
                    {titulosIntencao[intent] ?? INTENT_LABEL[intent]}
                    <span className="rounded-md border border-white/10 bg-[#071018] px-1.5 text-[10px] text-slate-500">
                      {links.length}
                    </span>
                  </p>
                  <ul className="space-y-2">
                    {links.map((link) => (
                      <LinkLinha key={link.id} link={link} />
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          <p className="mt-4 font-mono text-[10px] uppercase tracking-wide text-slate-600">
            {topico.totalCandidatos} páginas candidatas na base · {topico.links.length} selecionadas para este tópico
          </p>
        </div>
      )}
    </article>
  );
}

export default function TrilhaPanel() {
  const [payload, setPayload] = useState<TrilhaPayload | null>(null);
  const [loadError, setLoadError] = useState("");
  const [filtro, setFiltro] = useState<FiltroStatus>("todos");
  const [busca, setBusca] = useState("");
  const [abertos, setAbertos] = useState<string[]>([]);

  useEffect(() => {
    const url = `${import.meta.env.BASE_URL}trilhas.json`;
    fetch(url)
      .then((response) => {
        if (!response.ok) throw new Error(`Falha ao carregar a trilha (${response.status}).`);
        return response.json() as Promise<unknown>;
      })
      .then((data) => {
        if (!isTrilhaPayload(data)) {
          setLoadError("O arquivo trilhas.json está em um formato inesperado.");
          return;
        }
        setPayload(data);
        setAbertos(data.topicos.filter((topico) => topico.status === "pendente").slice(0, 1).map((topico) => topico.id));
      })
      .catch((error: Error) => setLoadError(error.message));
  }, []);

  const resumo = payload ? resumoTrilha(payload) : null;
  const topicos = useMemo(() => (payload ? filtrarTopicos(payload, filtro, busca) : []), [payload, filtro, busca]);
  const titulosIntencao = useMemo(() => {
    const mapa: Record<string, string> = {};
    for (const intencao of payload?.intencoes ?? []) mapa[intencao.id] = intencao.titulo;
    return mapa;
  }, [payload]);

  const alternar = (id: string) =>
    setAbertos((atual) => (atual.includes(id) ? atual.filter((item) => item !== id) : [...atual, id]));

  return (
    <main className="mx-auto max-w-[1500px] px-5 py-8 lg:px-10 lg:py-11">
      <div className="relative overflow-hidden rounded-3xl border border-cyan-300/15 bg-[radial-gradient(circle_at_15%_0%,rgba(34,211,238,0.14),transparent_38%),linear-gradient(135deg,#0b1823,#0a121b)] px-6 py-8 shadow-2xl shadow-black/20 sm:px-10 sm:py-10">
        <div className="absolute -left-16 -top-20 size-56 rounded-full border border-cyan-300/10" />
        <div className="relative max-w-3xl">
          <Badge className="mb-4 border-cyan-300/20 bg-cyan-300/10 font-mono text-cyan-100 hover:bg-cyan-300/10">
            TRILHA DE IMPLANTAÇÃO E TREINAMENTO
          </Badge>
          <h2 className="text-2xl font-semibold leading-tight tracking-tight text-white sm:text-4xl">
            {payload?.projeto ?? "Trilha de treinamento fiscal"}
          </h2>
          <p className="mt-4 text-sm leading-7 text-slate-300">{payload?.descricao ?? "Carregando a trilha local..."}</p>
        </div>
      </div>

      {resumo && (
        <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
          {[
            { label: "tópicos mapeados", valor: resumo.totalTopicos, icone: Boxes, cor: "text-cyan-200" },
            { label: "na agenda (a implantar)", valor: resumo.pendentes, icone: CircleDashed, cor: "text-amber-200" },
            { label: "já validados no cliente", valor: resumo.concluidos, icone: BadgeCheck, cor: "text-emerald-300" },
            { label: "links oficiais selecionados", valor: `${resumo.links} (${resumo.linksUnicos} únicos)`, icone: Link2, cor: "text-violet-200" },
          ].map((item) => (
            <div key={item.label} className="rounded-2xl border border-white/10 bg-[#0b1722] p-4">
              <item.icone size={17} className={item.cor} />
              <p className="mt-2 text-xl font-semibold text-white">{item.valor}</p>
              <p className="text-[11px] leading-4 text-slate-500">{item.label}</p>
            </div>
          ))}
        </div>
      )}

      <div className="mt-5 flex flex-col gap-3 rounded-2xl border border-white/10 bg-[#0b1722] p-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap items-center gap-2">
          {FILTROS.map((item) => (
            <Button
              key={item.id}
              size="sm"
              variant="outline"
              onClick={() => setFiltro(item.id)}
              className={cn(
                "h-9 gap-2 rounded-full border-white/10 bg-transparent text-xs",
                filtro === item.id
                  ? "border-cyan-300/40 bg-cyan-300/10 text-cyan-100 hover:bg-cyan-300/15 hover:text-cyan-50"
                  : "text-slate-300 hover:bg-white/5 hover:text-white",
              )}
            >
              <item.icon size={14} />
              {item.label}
            </Button>
          ))}
        </div>
        <div className="relative min-w-0 lg:w-[360px]">
          <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-cyan-200/60" size={16} />
          <input
            value={busca}
            onChange={(event) => setBusca(event.target.value)}
            placeholder="Filtrar tópico, rotina ou link (ex: Bloco K, MATA910, TAF)"
            aria-label="Filtrar tópicos da trilha"
            className="h-10 w-full rounded-lg border border-white/10 bg-[#071018] pl-9 pr-3 text-sm text-slate-200 outline-none placeholder:text-slate-500 focus:border-cyan-300/50"
          />
        </div>
      </div>

      {loadError && (
        <div className="mt-5 rounded-xl border border-rose-300/20 bg-rose-400/10 p-4 text-sm text-rose-100">{loadError}</div>
      )}
      {!payload && !loadError && (
        <div className="mt-5 flex items-center gap-3 rounded-2xl border border-white/10 bg-[#0b1722] p-6 text-sm text-slate-300">
          <Loader2 className="animate-spin text-cyan-200" size={18} /> Carregando a trilha local...
        </div>
      )}
      {payload && topicos.length === 0 && (
        <div className="mt-5 rounded-2xl border border-dashed border-white/15 bg-[#0b1722] p-8 text-center">
          <CircleHelp className="mx-auto text-slate-500" size={28} />
          <p className="mt-3 text-sm text-slate-300">Nenhum tópico corresponde ao filtro atual.</p>
          <p className="mt-1 text-xs text-slate-500">Limpe a busca ou selecione “Todos os tópicos”.</p>
        </div>
      )}

      <div className="mt-7 space-y-8">
        {payload?.grupos.map((grupo) => {
          const topicosGrupo = topicos.filter((topico) => topico.grupo === grupo.id);
          if (topicosGrupo.length === 0) return null;
          return (
            <section key={grupo.id}>
              <div className="flex flex-wrap items-center gap-2.5">
                <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-cyan-200/70">Grupo</p>
                <h3 className="text-lg font-semibold text-white">{grupo.titulo}</h3>
                <Badge className={cn("rounded-full border font-mono text-[10px] hover:bg-transparent", STATUS_BADGE[grupo.status])}>
                  {STATUS_LABEL[grupo.status] ?? grupo.status}
                </Badge>
              </div>
              <p className="mt-1.5 max-w-4xl text-xs leading-5 text-slate-400">{grupo.descricao}</p>
              <div className="mt-4 space-y-3">
                {topicosGrupo.map((topico) => (
                  <TopicoCard
                    key={topico.id}
                    topico={topico}
                    titulosIntencao={titulosIntencao}
                    aberto={abertos.includes(topico.id)}
                    onToggle={() => alternar(topico.id)}
                  />
                ))}
              </div>
            </section>
          );
        })}
      </div>

      {payload && (
        <p className="mt-9 border-t border-white/10 pt-5 text-center font-mono text-[10px] uppercase tracking-wide text-slate-600">
          Seleção automática sobre {payload.totalLinksBase} páginas oficiais (TDN e Central de Atendimento TOTVS) ·
          gerada em {new Date(payload.generatedAt).toLocaleDateString("pt-BR")}
        </p>
      )}
    </main>
  );
}
