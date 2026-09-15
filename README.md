# Buscador Protheus

O **Buscador Protheus** é uma aplicação estática para consulta técnica da documentação TOTVS Protheus. O projeto foi desenhado para funcionar no GitHub Pages, sem backend, sem banco de dados, sem servidor próprio e sem chave de IA embutida.

## O que a aplicação faz

A interface carrega um índice JSON local com **2.391 links deduplicados** do TDN e da Central de Atendimento TOTVS, incluindo artigos e seções/subseções mapeadas. A busca acontece inteiramente no navegador e considera títulos, URLs, códigos de módulo e termos técnicos. Os resultados exibem o título, a origem, o módulo e o link clicável para a documentação original.

Além da busca, a aplicação tem a aba **Trilha de treinamento**: um dossiê de implantação e capacitação do escopo fiscal (projeto Minérios Gerais) com 18 tópicos, cada um com o que implantar, o que treinar, como validar e as fontes oficiais selecionadas automaticamente a partir do próprio índice local.

A aplicação também oferece uma camada opcional de análise com OpenAI ou Google Gemini. Nesse modo, o usuário escolhe o provedor, informa a própria chave e envia a pergunta junto com os resultados encontrados diretamente ao provedor escolhido. A chave não está no repositório e não passa por servidor intermediário do projeto.

> A busca local é gratuita. O uso de OpenAI ou Gemini depende da conta, da chave e da política de cobrança do próprio provedor escolhido pelo usuário.

## Estrutura principal

| Caminho                                             | Finalidade                                                                                      |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `client/src/pages/Home.tsx`                         | Interface, alternância Busca/Trilha, filtros e chamadas opcionais às APIs de IA.                |
| `client/src/components/TrilhaPanel.tsx`             | Aba **Trilha de treinamento**: grupos da agenda, tópicos expansíveis e links por intenção.      |
| `client/src/lib/trilhas.ts`                         | Tipos, validação e filtros (status/busca) da trilha consumida pelo navegador.                   |
| `client/public/knowledge.json`                      | Base estática de links consumida pelo navegador.                                                |
| `client/public/trilhas.json`                        | Trilha de implantação e treinamento gerada a partir da base estática.                           |
| `docs/trilha-minerios-gerais/`                      | Dossiê em Markdown da trilha (agendas 09/09 e 11/09, treinamento e cobertura).                  |
| `scripts/build_knowledge.py`                        | Regeneração da base JSON a partir dos índices `.txt` versionados em `data/indices/`.            |
| `scripts/gerar_trilha_treinamento.py`               | Seleção dos links por tópico e geração de `trilhas.json` + dossiê Markdown.                     |
| `data/indices/Indice_Trilha_Complementos.txt`       | Complementos oficiais (TDN/Central) usados para cobrir lacunas da trilha.                       |
| `data/indices/Indice_Cfgtrib_Documento_Entrada.txt` | 52 links curados do sintoma "Documento de Entrada sem os impostos do Configurador de Tributos". |
| `docs/cfgtrib-documento-entrada/`                   | Roteiro de diagnóstico desse sintoma, com a fonte de cada verificação.                          |
| `.github/workflows/deploy-pages.yml`                | Build e publicação automática no GitHub Pages.                                                  |
| `vite.config.ts`                                    | Configuração do caminho-base para preview local e subdiretório do GitHub Pages.                 |

## Regenerar a base de conhecimento

Os arquivos de origem estão versionados em `data/indices/` e incluem os índices por módulo, subseções e acumuladores históricos. Para reconstruir a base depois de atualizar esses arquivos, execute:

```bash
python3 scripts/build_knowledge.py
```

O resultado será gravado em `client/public/knowledge.json`. O gerador remove URLs duplicadas (mantendo o melhor título encontrado para cada URL), corrige URLs concatenadas dos índices acumulados, identifica a origem pelo domínio e organiza os registros por módulo quando o código SIGA aparece no título ou na URL.

## Trilha de implantação e treinamento

A trilha responde, por tópico do escopo fiscal, **como implantar**, **como treinar**, **como validar** e **quais fontes oficiais consultar**. Os tópicos seguem a agenda do cliente Minérios Gerais:

- **Já validados** (revisão e reforço de treinamento): cadastros fiscais, TES de entrada/saída, configuração de tributos legados + Configurador de Tributos, DIFAL, apuração de impostos e impostos retidos (com a observação do PCC com data de vencimento incorreta).
- **Agenda 09/09**: EFD-ICMS/IPI, EFD Contribuições, Registro de Apuração de ICMS-P9, CIAP, Bloco K e registro de inventário (Bloco H/MATR460).
- **Agenda 11/09**: validação das rotinas fiscais (NF manual e acertos), TAF/Extrator Fiscal/EFD-REINF, revisão das parametrizações conforme o escopo, quebra de estoque e exportação.
- **Apoio transversal**: materiais oficiais de treinamento (webinars do FISA170, eventos tira-dúvidas, Banco de Conhecimento, guias e dashboards).

Cada link é classificado por intenção — implantar/parametrizar, treinar, ponto de entrada (ADVPL) e suporte/FAQ — e a seleção aplica limites por intenção, cotas por família de documento (por exemplo, no máximo 5 pontos de entrada por tópico) e remoção de duplicatas por título normalizado.

```bash
python3 scripts/build_knowledge.py                    # 1. reconstrói o índice local
python3 scripts/gerar_trilha_treinamento.py           # 2. regenera trilhas.json + dossiê
python3 scripts/gerar_trilha_treinamento.py --check   # 3. falha se algum tópico ficar sem fonte
```

Os artefatos são `client/public/trilhas.json` (consumido pela aba **Trilha**) e `docs/trilha-minerios-gerais/` (Markdown para levar à reunião). O arquivo `05-cobertura-e-lacunas.md` registra quantos candidatos a base tem por tópico, quais precisaram de complemento externo e as lacunas que continuam abertas (por exemplo, conteúdo fiscal específico de mineração/CFEM, que não existe na documentação oficial indexada).

## Executar localmente

Instale as dependências e inicie o preview do Vite:

```bash
pnpm install
pnpm dev
```

Para validar o build de produção estática:

```bash
pnpm build
```

O artefato final fica em `dist/public`.

## Publicar no GitHub Pages

O workflow em `.github/workflows/deploy-pages.yml` publica automaticamente quando há um push na branch `main`. No GitHub, abra **Settings → Pages**, selecione **GitHub Actions** como fonte e faça o primeiro push. O workflow instala o pnpm via npm depois do Node.js e ajusta `VITE_BASE_PATH` para que o arquivo `knowledge.json` funcione tanto na raiz quanto no subdiretório do projeto.

> O `package.json` **não** declara `packageManager`. O `actions/setup-node@v5` lê esse campo e tenta cachear o pnpm antes de o binário existir, o que derruba o job com `Unable to locate executable file: pnpm`. A versão usada no CI é a do `npm install --global pnpm@10.4.1` no workflow.

Se o repositório for `usuario/buscadorprotheus`, a URL normalmente terá o formato `https://usuario.github.io/buscadorprotheus/`. O endereço exato depende do nome da conta e das configurações do GitHub Pages.

## Uso da IA no navegador

Por padrão, a chave é mantida apenas no estado da página e desaparece ao recarregar. Se o usuário marcar a opção de lembrar, ela será armazenada no `localStorage` daquele navegador. Essa opção deve ser usada somente em computador pessoal. O projeto não coleta nem envia a chave para qualquer endpoint próprio.

As chamadas client-side utilizam os endpoints oficiais dos provedores. Alguns ambientes, extensões ou políticas do provedor podem bloquear requisições feitas diretamente do navegador por CORS; nesse caso, a busca local continuará funcionando normalmente, mas a análise de IA não estará disponível naquele ambiente.

## Pacote de levantamento para o Configurador de Tributos (FISA170)

O índice indexado não serve só para buscar artigo: ele é a base do material de levantamento de
necessidades do módulo Fiscal. Em `docs/fisa170/` está o pacote pronto para uso em projeto: método de
coleta, matriz de informações (o que cada dado do cliente decide no configurador), caso concreto de
remessa para demonstração com cBenef, checklist de validação e a matriz CSV de coleta.

```bash
python3 scripts/gerar_pacote_fisa170.py --init-csv   # cria/reatualiza a matriz de coleta
python3 scripts/gerar_pacote_fisa170.py             # gera resumo, lacunas, fichas e mapa de fontes
python3 scripts/gerar_pacote_fisa170.py --check      # falha se houver bloqueio de levantamento
```

As fontes citadas nas fichas são sempre links já versionados em `data/indices/`, o que mantém o pacote
ancorado na documentação oficial em vez de citar páginas soltas.

## Roteiro: Documento de Entrada sem os impostos do Configurador de Tributos

O sintoma "o documento de entrada não traz os impostos do Configurador de Tributos" não tem um
artigo oficial com esse título: o que existe são três documentos que precisam ser lidos juntos. Em
`docs/cfgtrib-documento-entrada/` está o roteiro na ordem de verificação (confirmar a origem do
cálculo, validar a regra, conferir o enquadramento dos quatro perfis, base/alíquota, tabelas,
financeiro, pré-nota e simuladores), cada passo com o link da fonte e o status da verificação.

```bash
python3 scripts/build_knowledge.py   # inclui o índice curado na base (2.391 links)
pnpm test                            # garante que a frase do usuário acha as fontes
```

A busca passou a normalizar acentos nos dois lados (antes "classificação tributária" devolvia 9
resultados; agora devolve 65) e a casar singular e plural ("impostos" x "Imposto"). Palavras vazias
("de", "do", "os") valem menos, e expressões inteiras no título ("documento de entrada",
"configurador de tributos") recebem bônus — é isso que coloca o artigo certo na primeira posição.

## Limitações deliberadas

A aplicação pesquisa os títulos e URLs disponíveis no índice; ela não baixa automaticamente o conteúdo completo de cada artigo. Isso mantém o projeto gratuito, rápido e compatível com hospedagem puramente estática. Para obter uma resposta da IA, os links relevantes encontrados são enviados como contexto, e o usuário deve abrir a fonte oficial para confirmar a versão, o pacote e os detalhes de implantação.
