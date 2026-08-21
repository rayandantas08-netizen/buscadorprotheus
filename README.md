# Buscador Protheus

O **Buscador Protheus** é uma aplicação estática para consulta técnica da documentação TOTVS Protheus. O projeto foi desenhado para funcionar no GitHub Pages, sem backend, sem banco de dados, sem servidor próprio e sem chave de IA embutida.

## O que a aplicação faz

A interface carrega um índice JSON local com **1.929 links deduplicados** do TDN e da Central de Atendimento TOTVS, incluindo artigos e seções/subseções mapeadas. A busca acontece inteiramente no navegador e considera títulos, URLs, códigos de módulo e termos técnicos. Os resultados exibem o título, a origem, o módulo e o link clicável para a documentação original.

A aplicação também oferece uma camada opcional de análise com OpenAI ou Google Gemini. Nesse modo, o usuário escolhe o provedor, informa a própria chave e envia a pergunta junto com os resultados encontrados diretamente ao provedor escolhido. A chave não está no repositório e não passa por servidor intermediário do projeto.

> A busca local é gratuita. O uso de OpenAI ou Gemini depende da conta, da chave e da política de cobrança do próprio provedor escolhido pelo usuário.

## Estrutura principal

| Caminho | Finalidade |
| --- | --- |
| `client/src/pages/Home.tsx` | Interface, busca local, filtros e chamadas opcionais às APIs de IA. |
| `client/public/knowledge.json` | Base estática de links consumida pelo navegador. |
| `scripts/build_knowledge.py` | Regeneração da base JSON a partir dos índices `.txt` versionados em `data/indices/`. |
| `.github/workflows/deploy-pages.yml` | Build e publicação automática no GitHub Pages. |
| `vite.config.ts` | Configuração do caminho-base para preview local e subdiretório do GitHub Pages. |

## Regenerar a base de conhecimento

Os arquivos de origem estão versionados em `data/indices/` e incluem os índices por módulo, subseções e acumuladores históricos. Para reconstruir a base depois de atualizar esses arquivos, execute:

```bash
python3 scripts/build_knowledge.py
```

O resultado será gravado em `client/public/knowledge.json`. O gerador remove URLs duplicadas, identifica a origem pelo domínio e organiza os registros por módulo quando o código SIGA aparece no título ou na URL.

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

## Limitações deliberadas

A aplicação pesquisa os títulos e URLs disponíveis no índice; ela não baixa automaticamente o conteúdo completo de cada artigo. Isso mantém o projeto gratuito, rápido e compatível com hospedagem puramente estática. Para obter uma resposta da IA, os links relevantes encontrados são enviados como contexto, e o usuário deve abrir a fonte oficial para confirmar a versão, o pacote e os detalhes de implantação.

