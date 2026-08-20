import React, { useEffect, useMemo, useState } from "react";
import {
  BookOpen,
  ChevronDown,
  CircleHelp,
  ExternalLink,
  FileText,
  Filter,
  Github,
  KeyRound,
  Layers3,
  Library,
  Link2,
  Loader2,
  MessageSquareText,
  Search,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { searchRecords, type KnowledgeRecord } from "@/lib/search";

const STORAGE_KEY = "buscadorprotheus.ai-settings";

type Provider = "openai" | "gemini";

type KnowledgePayload = {
  total: number;
  modules: string[];
  records: KnowledgeRecord[];
};

type AiSettings = {
  provider: Provider;
  key: string;
  remember: boolean;
};

const DEFAULT_SETTINGS: AiSettings = { provider: "openai", key: "", remember: false };

function readStoredSettings(): AiSettings {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (!saved) return DEFAULT_SETTINGS;
    const parsed = JSON.parse(saved) as Partial<AiSettings>;
    return {
      provider: parsed.provider === "gemini" ? "gemini" : "openai",
      key: parsed.remember ? parsed.key ?? "" : "",
      remember: parsed.remember === true,
    };
  } catch {
    return DEFAULT_SETTINGS;
  }
}

function buildSourcesPrompt(records: KnowledgeRecord[]) {
  return records
    .slice(0, 20)
    .map((record, index) => `${index + 1}. [${record.moduleCode}] ${record.title}\nFonte: ${record.url}`)
    .join("\n\n");
}

async function askOpenAi(key: string, question: string, records: KnowledgeRecord[]) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      temperature: 0.1,
      messages: [
        {
          role: "system",
          content:
            "Você é um consultor técnico de TOTVS Protheus. Responda em português do Brasil, seja objetivo e não invente procedimentos. Use somente as fontes fornecidas, indique quando a evidência não for suficiente e preserve os links no texto.",
        },
        {
          role: "user",
          content: `Pergunta do usuário:\n${question}\n\nFontes locais encontradas:\n${buildSourcesPrompt(records)}`,
        },
      ],
    }),
  });
  const data = (await response.json()) as { choices?: Array<{ message?: { content?: string } }>; error?: { message?: string } };
  if (!response.ok) throw new Error(data.error?.message || "A API OpenAI recusou a solicitação.");
  return data.choices?.[0]?.message?.content || "A API não retornou uma resposta textual.";
}

async function askGemini(key: string, question: string, records: KnowledgeRecord[]) {
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${encodeURIComponent(key)}`;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      generationConfig: { temperature: 0.1 },
      systemInstruction: {
        parts: [{ text: "Você é um consultor técnico de TOTVS Protheus. Responda em português do Brasil, não invente procedimentos e use somente as fontes fornecidas." }],
      },
      contents: [{ role: "user", parts: [{ text: `Pergunta:\n${question}\n\nFontes locais:\n${buildSourcesPrompt(records)}` }] }],
    }),
  });
  const data = (await response.json()) as { candidates?: Array<{ content?: { parts?: Array<{ text?: string }> } }>; error?: { message?: string } };
  if (!response.ok) throw new Error(data.error?.message || "A API Gemini recusou a solicitação.");
  return data.candidates?.[0]?.content?.parts?.map((part) => part.text || "").join("\n") || "A API não retornou uma resposta textual.";
}

export default function Home() {
  const [knowledge, setKnowledge] = useState<KnowledgePayload | null>(null);
  const [loadError, setLoadError] = useState("");
  const [query, setQuery] = useState("");
  const [selectedModule, setSelectedModule] = useState("all");
  const [settings, setSettings] = useState<AiSettings>(readStoredSettings);
  const [showAiPanel, setShowAiPanel] = useState(false);
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiError, setAiError] = useState("");
  const [isAsking, setIsAsking] = useState(false);

  useEffect(() => {
    const url = `${import.meta.env.BASE_URL}knowledge.json`;
    fetch(url)
      .then((response) => {
        if (!response.ok) throw new Error(`Falha ao carregar a base local (${response.status}).`);
        return response.json() as Promise<KnowledgePayload>;
      })
      .then(setKnowledge)
      .catch((error: Error) => setLoadError(error.message));
  }, []);

  useEffect(() => {
    if (!settings.remember) {
      window.localStorage.removeItem(STORAGE_KEY);
      return;
    }
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  }, [settings]);

  const modules = useMemo(() => {
    if (!knowledge) return [];
    return [...knowledge.modules].sort((a, b) => a.localeCompare(b, "pt-BR"));
  }, [knowledge]);

  const results = useMemo(
    () => searchRecords(knowledge?.records ?? [], query, selectedModule),
    [knowledge, selectedModule, query],
  );

  const moduleCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const record of knowledge?.records ?? []) counts.set(record.module, (counts.get(record.module) ?? 0) + 1);
    return counts;
  }, [knowledge]);

  const handleSearch = () => {
    setAiAnswer("");
    setAiError("");
  };

  const handleClear = () => {
    setQuery("");
    setSelectedModule("all");
    setAiAnswer("");
    setAiError("");
  };

  const handleAiAnswer = async () => {
    if (!query.trim()) {
      setAiError("Faça uma pergunta ou execute uma busca antes de solicitar uma análise.");
      return;
    }
    if (!settings.key.trim()) {
      setAiError("Informe sua chave de API no painel de IA. A chave não é enviada para este site.");
      setShowAiPanel(true);
      return;
    }

    setIsAsking(true);
    setAiAnswer("");
    setAiError("");
    try {
      const answer = settings.provider === "openai"
        ? await askOpenAi(settings.key.trim(), query.trim(), results)
        : await askGemini(settings.key.trim(), query.trim(), results);
      setAiAnswer(answer);
    } catch (error) {
      setAiError(error instanceof Error ? error.message : "Não foi possível consultar o provedor de IA.");
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#071018] text-slate-100 selection:bg-cyan-400/30">
      <header className="border-b border-white/10 bg-[#071018]/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1500px] items-center justify-between gap-5 px-5 py-4 lg:px-10">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-xl border border-cyan-300/30 bg-cyan-300/10 text-cyan-200 shadow-[0_0_30px_rgba(34,211,238,0.12)]">
              <TerminalSquare size={22} />
            </div>
            <div>
              <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-cyan-200/70">Base técnica local</p>
              <h1 className="text-lg font-semibold tracking-tight text-white">Buscador Protheus</h1>
            </div>
          </div>
          <div className="hidden items-center gap-2 text-xs text-slate-400 sm:flex">
            <ShieldCheck size={15} className="text-emerald-300" />
            <span>100% no navegador</span>
            <span className="text-slate-600">•</span>
            <span>sem servidor intermediário</span>
          </div>
          <a className="inline-flex items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-300 transition hover:border-cyan-300/40 hover:text-cyan-100" href="https://github.com" target="_blank" rel="noreferrer">
            <Github size={15} /> GitHub Pages
          </a>
        </div>
      </header>

      <main className="mx-auto grid max-w-[1500px] gap-7 px-5 py-8 lg:grid-cols-[minmax(0,1fr)_350px] lg:px-10 lg:py-11">
        <section className="min-w-0">
          <div className="relative overflow-hidden rounded-3xl border border-cyan-300/15 bg-[radial-gradient(circle_at_80%_0%,rgba(34,211,238,0.14),transparent_35%),linear-gradient(135deg,#0b1823,#0a121b)] px-6 py-8 shadow-2xl shadow-black/20 sm:px-10 sm:py-11">
            <div className="absolute -right-20 -top-24 size-64 rounded-full border border-cyan-300/10" />
            <div className="absolute -right-8 -top-12 size-40 rounded-full border border-cyan-300/10" />
            <div className="relative max-w-3xl">
              <Badge className="mb-5 border-cyan-300/20 bg-cyan-300/10 font-mono text-cyan-100 hover:bg-cyan-300/10">SIGA • TDN • CENTRAL TOTVS</Badge>
              <h2 className="max-w-3xl text-3xl font-semibold leading-tight tracking-tight text-white sm:text-5xl">Encontre respostas técnicas no ecossistema Protheus.</h2>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-300 sm:text-base">Pesquise por rotina, parâmetro, help, módulo ou problema. O site consulta uma base local de links e mostra as fontes originais sem depender de backend.</p>
              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <div className="relative min-w-0 flex-1">
                  <Search className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-cyan-200/60" size={19} />
                  <Input
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    onKeyDown={(event) => { if (event.key === "Enter") handleSearch(); }}
                    placeholder="Ex.: rejeição E0390, MV_ATVEVT, MATA461..."
                    aria-label="Pergunta ou termo técnico"
                    className="h-14 border-white/10 bg-[#061019]/80 pl-12 pr-10 text-base text-white placeholder:text-slate-500 focus-visible:ring-cyan-300/50"
                  />
                  {query && <button aria-label="Limpar pergunta" onClick={() => setQuery("")} className="absolute right-3 top-1/2 -translate-y-1/2 rounded-md p-1 text-slate-500 hover:text-white"><X size={17} /></button>}
                </div>
                <Button onClick={handleSearch} className="h-14 bg-cyan-300 px-6 font-semibold text-slate-950 hover:bg-cyan-200"><Search size={18} /> Buscar</Button>
              </div>
              <div className="mt-4 flex flex-wrap items-center gap-2 text-xs text-slate-400">
                <span className="font-mono text-cyan-200/80">Dica:</span>
                <button onClick={() => { setQuery("MV_ATVEVT"); }} className="rounded-full border border-white/10 px-3 py-1.5 transition hover:border-cyan-300/40 hover:text-cyan-100">MV_ATVEVT</button>
                <button onClick={() => { setQuery("NFS-e Nacional"); }} className="rounded-full border border-white/10 px-3 py-1.5 transition hover:border-cyan-300/40 hover:text-cyan-100">NFS-e Nacional</button>
                <button onClick={() => { setQuery("MATA410"); }} className="rounded-full border border-white/10 px-3 py-1.5 transition hover:border-cyan-300/40 hover:text-cyan-100">MATA410</button>
              </div>
            </div>
          </div>

          <div className="mt-7 flex flex-col gap-3 rounded-2xl border border-white/10 bg-[#0b1722] p-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-3 text-sm text-slate-300"><Filter size={17} className="text-cyan-200" /><span>Refinar resultados por módulo</span></div>
            <div className="flex gap-2">
              <select value={selectedModule} onChange={(event) => setSelectedModule(event.target.value)} aria-label="Filtrar por módulo" className="h-10 min-w-0 flex-1 rounded-lg border border-white/10 bg-[#071018] px-3 text-sm text-slate-200 outline-none focus:border-cyan-300/50 sm:min-w-[280px]">
                <option value="all">Todos os módulos</option>
                {modules.map((module) => <option key={module} value={module}>{module} ({moduleCounts.get(module) ?? 0})</option>)}
              </select>
              <Button variant="outline" onClick={handleClear} className="h-10 border-white/10 bg-transparent text-slate-300 hover:bg-white/5 hover:text-white">Limpar</Button>
            </div>
          </div>

          <div className="mt-7 flex items-end justify-between gap-4">
            <div>
              <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-cyan-200/70">Fontes encontradas</p>
              <h3 className="mt-1 text-xl font-semibold text-white">{query.trim() ? `Resultados para “${query.trim()}”` : "Comece por uma consulta"}</h3>
            </div>
            <span className="whitespace-nowrap text-xs text-slate-500">{knowledge ? `${results.length} exibidos` : "carregando base..."}</span>
          </div>

          {loadError && <div className="mt-4 rounded-xl border border-rose-300/20 bg-rose-400/10 p-4 text-sm text-rose-100">{loadError}</div>}
          {!knowledge && !loadError && <div className="mt-5 flex items-center gap-3 rounded-2xl border border-white/10 bg-[#0b1722] p-6 text-sm text-slate-300"><Loader2 className="animate-spin text-cyan-200" size={18} /> Carregando o índice local...</div>}
          {knowledge && results.length === 0 && <div className="mt-5 rounded-2xl border border-dashed border-white/15 bg-[#0b1722] p-8 text-center"><CircleHelp className="mx-auto text-slate-500" size={28} /><p className="mt-3 text-sm text-slate-300">Nenhum link correspondeu aos filtros atuais.</p><p className="mt-1 text-xs text-slate-500">Tente termos menores, como “TES”, “NFSE”, “MATA”, “help” ou o nome de um parâmetro.</p></div>}

          <div className="mt-5 space-y-3">
            {results.map((record) => (
              <article key={record.id} className="group rounded-2xl border border-white/10 bg-[#0b1722] p-5 transition hover:-translate-y-0.5 hover:border-cyan-300/30 hover:bg-[#0d1c29]">
                <div className="flex flex-wrap items-center gap-2 text-[11px] font-mono uppercase tracking-wide text-slate-500"><Badge variant="outline" className="border-cyan-300/20 bg-cyan-300/5 text-cyan-100">{record.moduleCode}</Badge><span>{record.kind === "section" ? "Seção" : "Artigo"}</span><span>{record.source}</span></div>
                <h4 className="mt-3 text-base font-medium leading-6 text-slate-100 group-hover:text-cyan-100">{record.title}</h4>
                <a href={record.url} target="_blank" rel="noreferrer" className="mt-3 flex items-start gap-2 break-all text-xs leading-5 text-slate-500 transition hover:text-cyan-200"><Link2 size={14} className="mt-0.5 shrink-0" />{record.url}<ExternalLink size={13} className="mt-0.5 shrink-0 opacity-60" /></a>
              </article>
            ))}
          </div>
        </section>

        <aside className="space-y-5">
          <Card className="border-white/10 bg-[#0b1722] text-slate-100 shadow-xl shadow-black/10">
            <CardHeader><div className="flex items-center justify-between"><div className="flex size-10 items-center justify-center rounded-xl bg-violet-300/10 text-violet-200"><Sparkles size={19} /></div><Badge className="border-amber-300/20 bg-amber-300/10 text-amber-100 hover:bg-amber-300/10">Opcional</Badge></div><CardTitle className="mt-4 text-lg text-white">Analisar com sua IA</CardTitle><CardDescription className="leading-6 text-slate-400">Envie a pergunta e os links encontrados diretamente do navegador para OpenAI ou Gemini.</CardDescription></CardHeader>
            <CardContent><Button onClick={() => setShowAiPanel((value) => !value)} variant="outline" className="w-full border-white/10 bg-transparent text-slate-200 hover:bg-white/5 hover:text-white">{showAiPanel ? "Ocultar configuração" : "Configurar provedor"}<ChevronDown size={16} className={showAiPanel ? "rotate-180 transition" : "transition"} /></Button>
              {showAiPanel && <div className="mt-5 space-y-4 border-t border-white/10 pt-5"><div><Label htmlFor="provider" className="text-xs text-slate-300">Provedor</Label><select id="provider" value={settings.provider} onChange={(event) => setSettings((current) => ({ ...current, provider: event.target.value as Provider }))} className="mt-2 h-10 w-full rounded-lg border border-white/10 bg-[#071018] px-3 text-sm text-slate-200 outline-none focus:border-violet-300/50"><option value="openai">OpenAI · gpt-4o-mini</option><option value="gemini">Google Gemini · 2.0 Flash</option></select></div><div><Label htmlFor="api-key" className="text-xs text-slate-300">Sua chave de API</Label><div className="relative mt-2"><KeyRound size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" /><Input id="api-key" type="password" value={settings.key} onChange={(event) => setSettings((current) => ({ ...current, key: event.target.value, remember: current.remember }))} placeholder={settings.provider === "openai" ? "sk-..." : "AIza..."} className="border-white/10 bg-[#071018] pl-9 text-slate-100" /></div></div><label className="flex items-center gap-2 text-xs text-slate-400"><input type="checkbox" checked={settings.remember} onChange={(event) => setSettings((current) => ({ ...current, remember: event.target.checked }))} className="accent-violet-300" /> Lembrar somente neste navegador</label><p className="text-[11px] leading-5 text-slate-500">A chave fica no estado da página ou no localStorage se você marcar a opção. Nunca há chave embutida no código e nenhuma chamada passa por servidor intermediário.</p><Button onClick={handleAiAnswer} disabled={isAsking} className="w-full bg-violet-300 text-slate-950 hover:bg-violet-200">{isAsking ? <Loader2 className="animate-spin" size={16} /> : <MessageSquareText size={16} />} {isAsking ? "Analisando..." : "Gerar análise"}</Button></div>}
              {aiError && <p className="mt-4 rounded-lg border border-rose-300/20 bg-rose-400/10 p-3 text-xs leading-5 text-rose-100">{aiError}</p>}
            </CardContent>
          </Card>

          {aiAnswer && <Card className="border-violet-300/20 bg-[#111326] text-slate-100"><CardHeader><div className="flex items-center gap-2 text-violet-200"><Sparkles size={16} /><CardTitle className="text-base text-white">Análise gerada</CardTitle></div><CardDescription className="text-xs text-slate-500">Resposta produzida pelo provedor escolhido usando as fontes exibidas.</CardDescription></CardHeader><CardContent><div className="whitespace-pre-wrap text-sm leading-6 text-slate-300">{aiAnswer}</div></CardContent></Card>}

          <Card className="border-white/10 bg-[#0b1722] text-slate-100"><CardHeader><div className="flex items-center gap-2 text-cyan-200"><Library size={17} /><CardTitle className="text-base text-white">Índice local</CardTitle></div></CardHeader><CardContent className="space-y-4"><div className="grid grid-cols-2 gap-3"><div className="rounded-xl border border-white/10 bg-[#071018] p-3"><FileText size={16} className="text-cyan-200" /><p className="mt-2 text-xl font-semibold text-white">{knowledge?.total ?? "—"}</p><p className="text-[11px] text-slate-500">links indexados</p></div><div className="rounded-xl border border-white/10 bg-[#071018] p-3"><Layers3 size={16} className="text-emerald-300" /><p className="mt-2 text-xl font-semibold text-white">{modules.length || "—"}</p><p className="text-[11px] text-slate-500">módulos</p></div></div><Separator className="bg-white/10" /><p className="text-xs leading-5 text-slate-400">A base é carregada como JSON estático e a busca usa títulos, URLs, códigos SIGA e texto dos índices. As fontes permanecem nos domínios oficiais da TOTVS.</p><div className="flex items-center gap-2 text-xs text-emerald-200"><ShieldCheck size={15} /> Nenhum dado de busca é enviado automaticamente.</div></CardContent></Card>

          <div className="rounded-2xl border border-white/10 bg-[#09131d] p-5"><div className="flex items-center gap-2 text-cyan-200"><BookOpen size={16} /><p className="text-sm font-medium text-white">Como consultar</p></div><ol className="mt-3 space-y-3 text-xs leading-5 text-slate-400"><li><span className="mr-2 font-mono text-cyan-200">01</span>Digite uma rotina, parâmetro, help ou mensagem de rejeição.</li><li><span className="mr-2 font-mono text-cyan-200">02</span>Filtre pelo módulo e abra a fonte oficial mais relevante.</li><li><span className="mr-2 font-mono text-cyan-200">03</span>Se desejar, forneça sua própria chave para obter uma síntese contextual.</li></ol></div>
        </aside>
      </main>

      <footer className="mx-auto flex max-w-[1500px] flex-col gap-2 border-t border-white/10 px-5 py-7 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-10"><span>Buscador Protheus · índice estático para consulta técnica</span><span className="flex items-center gap-2"><ShieldCheck size={13} /> A chave de IA, quando usada, permanece sob controle do usuário</span></footer>
    </div>
  );
}

