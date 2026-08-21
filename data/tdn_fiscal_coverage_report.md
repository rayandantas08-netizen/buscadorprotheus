# Relatório de Cobertura do Crawl — Fiscal Protheus 12

**Projeto:** Buscador Protheus  
**Fonte principal:** [Fiscal — Protheus 12 no TDN](https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12)  
**Data da consolidação:** 21 de agosto de 2026  
**Responsável:** Manus AI

## Resumo executivo

Foi consolidado um inventário local de **576 páginas únicas** relacionadas ao módulo Fiscal do Protheus 12, com **410 relações pai–filho** identificadas nas respostas oficiais do TDN. O inventário foi normalizado, deduplicado por ID/URL e exportado para o arquivo `data/indices/tdn_fiscal_recursive.txt`; em seguida, foi incorporado ao `client/public/knowledge.json` usado pelo buscador estático.

A base geral passou de 1.929 para **2.494 links únicos**, sendo **857 links provenientes do TDN** e **1.637 da Central de Atendimento TOTVS**. Os testes automatizados, a checagem TypeScript e o build de produção foram executados com sucesso.

> **Nota de transparência:** o inventário representa as páginas oficiais recuperadas e confirmadas durante esta rodada. O TDN utiliza CAPTCHA e algumas respostas REST são truncadas ou limitadas por paginação; portanto, não é tecnicamente correto afirmar que todos os descendentes existentes no portal foram comprovados de forma exaustiva.

## Método de coleta

A coleta usou a página raiz do Fiscal e endpoints oficiais de filhos do Confluence no formato `/rest/api/content/{pageId}/child/page?limit=500`. Quando a renderização normal da página foi bloqueada por CAPTCHA, a resposta estruturada disponibilizada pelo próprio endpoint foi preservada localmente para posterior processamento.

As respostas foram combinadas com os inventários parciais já existentes no projeto. O script `scripts/merge_tdn_fiscal_inventory.py` remove duplicidades por ID, normaliza os URLs para `pages/viewpage.action?pageId=...` e mantém o URL canônico da raiz fornecida pelo usuário. O script `scripts/export_tdn_fiscal_index.py` gera o arquivo de entrada consumido pelo gerador da base.

## Estatísticas consolidadas

| Indicador | Resultado |
|---|---:|
| Páginas únicas do inventário Fiscal | 576 |
| Relações pai–filho identificadas | 410 |
| Respostas `child/page` processadas localmente | 25 |
| Links totais no `knowledge.json` | 2.494 |
| Links TDN no `knowledge.json` | 857 |
| Links Central TOTVS no `knowledge.json` | 1.637 |
| Testes Vitest | 9 aprovados |
| Checagem TypeScript | Aprovada |
| Build Vite de produção | Aprovado |

## Ramificações recuperadas

A coleta inclui a raiz Fiscal e ramificações de menu, conceitos, configurações, integrações, funções, localizações, especificação de requisitos, TOTVS News, Banco de Conhecimento, FAQ, SmartView, Ciclo de Vida, Apurações, Arquivos Magnéticos, Acertos Fiscais, Fundos e Contribuições, além de grupos tributários como ICMS, ICMS-ST, ISS, PIS/COFINS/CSLL, IPI, IRRF, INSS e Importação.

Também foram incluídos artigos técnicos de parametrização, cálculos estaduais, retenções, créditos, desonerações, DIFAL, substituição tributária, relatórios, documentos eletrônicos e funções auxiliares localizadas no inventário expandido do Fiscal.

## Arquivos gerados e modificados

| Arquivo | Finalidade |
|---|---|
| `data/tdn_fiscal_inventory.json` | Inventário estruturado com páginas e relações pai–filho |
| `data/indices/tdn_fiscal_recursive.txt` | Índice textual compatível com `build_knowledge.py` |
| `scripts/merge_tdn_fiscal_inventory.py` | Consolidação e deduplicação das respostas do TDN |
| `scripts/export_tdn_fiscal_index.py` | Exportação do JSON para o índice textual |
| `client/public/knowledge.json` | Base estática consumida pelo navegador |
| `client/src/lib/knowledge.test.ts` | Teste de integridade do índice Fiscal |
| `data/tdn_fiscal_coverage_report.md` | Este relatório de auditoria |

## Validação automatizada

O teste específico verifica que o conjunto Fiscal contém pelo menos 500 registros, contém a raiz canônica, não possui URLs duplicados, inclui exemplos de artigos de apuração e ICMS-ST e mantém consistente o total declarado no JSON. A suíte completa terminou com **9 testes aprovados**; a checagem TypeScript e o build de produção também foram concluídos sem erros.

## Limitações conhecidas

O endpoint de descendentes completo do Confluence não forneceu uma resposta integral utilizável nesta rodada. Além disso, o portal bloqueou algumas navegações com CAPTCHA e há respostas que exigem paginação adicional. Por esse motivo, o número de 576 deve ser interpretado como **inventário confirmado nesta rodada**, e não como uma garantia matemática de que nenhuma página adicional exista no TDN.

Para ampliar a cobertura em uma próxima rodada, será necessário continuar a partir das páginas-pai ainda não consultadas individualmente, respeitando o CAPTCHA e a paginação do TDN. O buscador, entretanto, já está preparado para receber novos arquivos de índice sem backend ou custo de servidor.

## Referências

[1]: https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12 "Fiscal — Protheus 12 — TDN TOTVS"
[2]: https://tdn.totvs.com/rest/api/content/270093968/child/page?limit=500 "API REST do conteúdo Fiscal — filhos diretos"
[3]: https://tdn.totvs.com/rest/api/content/270093968/descendant/page?limit=500 "API REST do conteúdo Fiscal — descendentes"
