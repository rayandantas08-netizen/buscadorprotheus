# Crawl TDN Fiscal — notas de execução

A página raiz oficial é `https://tdn.totvs.com/display/public/PROT/Fiscal+-+Protheus+12`, com ID Confluence `270093968`.

A API pública de filhos diretos permitiu recuperar 14 páginas de primeiro nível: Pontos de Entrada, Menu do Módulo, Conceitos, Configurações, Integrações, Expedição Contínua, Funções, Localizaciones, Especificação de Requisitos, TOTVS News Fiscal, Banco de Conhecimento, FAQ, SmartView e Ciclo de Vida (SIGAFIS).

A consulta direta via `curl` retorna HTTP 403 do Cloudflare, mas o endpoint público do Confluence pode ser lido pelo extrator web. A página raiz e alguns endpoints grandes são retornados parcialmente; por isso os scripts locais usam parser por regex como fallback para preservar registros completos antes do corte.

Na primeira rodada foram confirmados 275 páginas-filhas em respostas `child/page`, incluindo 223 Pontos de Entrada e 38 páginas de Localizaciones. A resposta expandida com três níveis recuperou 354 registros de página em seu prefixo válido. Ainda é necessário consultar recursivamente as categorias com descendentes para completar a árvore.

Principais IDs de primeiro nível:

| Categoria | Page ID |
| --- | ---: |
| Pontos de Entrada - Fiscal - P12 | 513414990 |
| Menu do Módulo - Fiscal - P12 | 514445940 |
| Conceitos - Fiscal - P12 | 514454190 |
| Configurações - Fiscal - P12 | 514456601 |
| Integrações - Fiscal - P12 | 514719960 |
| Expedição Contínua - Fiscal - P12 | 527848707 |
| Funções - Fiscal - P12 | 539527253 |
| Localizaciones - Fiscal - P12 | 570367508 |
| Especificação de Requisitos | 594429492 |
| TOTVS News Fiscal | 628627108 |
| Banco de Conhecimento - Fiscal - P12 | 654284086 |
| FAQ - Fiscal - P12 | 663304266 |
| SmartView - Fiscal | 759937508 |
| Ciclo de Vida (SIGAFIS) | 841682134 |

Scripts criados até aqui:

| Arquivo | Finalidade |
| --- | --- |
| `scripts/extract_tdn_links.py` | Extrai e normaliza links de Markdown do TDN |
| `scripts/parse_tdn_api_children.py` | Consolida respostas `child/page` em páginas e relações |
| `scripts/parse_tdn_expanded_tree.py` | Processa árvores expandidas e recupera prefixos truncados |

## Novas ramificações confirmadas

As seguintes categorias também foram confirmadas como páginas-pai ou agrupadoras com sublinks:

| Página-pai | Page ID | Filhos confirmados |
| --- | ---: | --- |
| Menu do Módulo - Fiscal - P12 | 514445940 | Atualizações, Consultas, Miscelânea, Outras Ações, Relatórios |
| Configurações - Fiscal - P12 | 514456601 | Cadastros e Parâmetros, Funções Disponíveis, Fundos e Contribuições, ICMS, ICMS-ST, Importação, INSS, IPI, IRRF, ISS, PIS/COFINS, Rotinas Automáticas e Outras Configurações |
| Integrações - Fiscal - P12 | 514719960 | INTFAC e TaxOpJson |
| Expedição Contínua - Fiscal - P12 | 527848707 | Atualização de Dicionário Classificação Tributária, Pacotes Classificação Tributária, Pacotes de Atualização e Pacotes de Atualização - Dicionário |
| Funções - Fiscal - P12 | 539527253 | Aplicativo SIRETPER, MaAvalTes, MaFisIni, MaFisIniLoad, MaFisRef e MaFisRet |
| Especificação de Requisitos | 594429492 | Desenvolvimento Participativo, Legislações, Projetos Squad´s Fiscais e RETAIL - Backoffice |
| TOTVS News Fiscal | 628627108 | Artigo sobre exclusão do ICMS da base PIS/COFINS e alerta de Inscrição Estadual |
| Banco de Conhecimento - Fiscal - P12 | 654284086 | BC - Configurações, BC - FAQ'S, BC - Menu - Livros Fiscais e BC - Pontos de Entrada |
| FAQ - Fiscal - P12 | 663304266 | FAQ de Apurações, Arquivos Magnéticos, Documentos Fiscais, EFD Contribuições e Relatórios, entre outras FAQs específicas |
| SmartView - Fiscal | 759937508 | Fiscal - Localizaciones |
| Ciclo de Vida (SIGAFIS) | 841682134 | Rotinas descontinuadas em 2024, rotinas descontinuadas em 12/2026 e TES com cenários de IBS/CBS |
| Miscelânea - Fiscal - P12 | 270923448 | Acertos Fiscais, Apurações, Arquivos Magnéticos e TIT |
| Relatórios - Fiscal - P12 | 270923451 | Certificado de Retención FISA015, Listagem de Conferência, Livros Oficiais e Relatórios Outros Países |
| Movimentos - Fiscal - P12 | 654106548 | COMPEXP, MATA910, NFCom e PRNFCRPRES |

Esses resultados foram obtidos a partir dos endpoints oficiais `https://tdn.totvs.com/rest/api/content/{pageId}/child/page?limit=500`, preservando os IDs para gerar URLs estáveis `https://tdn.totvs.com/pages/viewpage.action?pageId={pageId}`.

## Registro de execução — 2026-08-21

Foram salvas localmente as respostas oficiais de `child/page` para Menu (`514445940`) e Conceitos (`514454190`). O Menu possui cinco filhos diretos: Atualizações, Consultas, Miscelânea, Outras Ações e Relatórios. Conceitos retornou lista vazia de filhos diretos.

A API também confirmou e salvou localmente:

- Integrações (`514719960`): `INTFAC` (`600144076`) e `TaxOpJson` (`1008231251`).
- Expedição Contínua (`527848707`): atualização de dicionário (`784782300`), pacotes de classificação tributária (`784782255`), pacotes de atualização (`525823851`) e pacotes de atualização de dicionário (`527848712`).

Foram salvas localmente as respostas de Funções (`539527253`), com seis páginas-filhas (SIRETPER, MaAvalTes, MaFisIni, MaFisIniLoad, MaFisRef e MaFisRet), e de Localizaciones (`570367508`), com dezenas de artigos regionais da Argentina, Equador, Colômbia, México, Peru e outros países.

As respostas de Especificação de Requisitos (`594429492`) e TOTVS News Fiscal (`628627108`) foram salvas. A primeira possui quatro filhos (Desenvolvimento Participativo, Legislações, Projetos Squad´s Fiscais e RETAIL - Backoffice); a segunda possui dois artigos, incluindo a operacionalização da exclusão do ICMS da base de PIS/Cofins e o alerta sobre Inscrição Estadual.

Foram salvas as respostas de Banco de Conhecimento (`654284086`) e FAQ (`663304266`). O Banco de Conhecimento possui quatro categorias; o FAQ possui sete categorias principais, incluindo Apurações, Arquivos Magnéticos, Configurador de Tributos/TES legado, Documentos Fiscais, EFD Contribuições e Relatórios.

SmartView Fiscal (`759937508`) possui o filho `Fiscal - Localizaciones` (`789996435`). Ciclo de Vida (`841682134`) possui três filhos: rotinas descontinuadas em 2024, rotinas que serão descontinuadas em 12/2026 e cenários de composição do ICMS com IBS e CBS. As respostas foram salvas localmente.

A página Apurações (`627111872`) retornou 11 filhos diretos: APUI​​CM (`270894388`), APUIPI (`270093976`), APUISS (`654295834`), APUISSBLB (`500292737`), APURESST (`525806853`), APURSN (`642621812`), EF​​DCON (`212896468`), MGRESST (`698288943`), RSRESST (`698294461`), SCRESST (`484701377`) e SPRESST (`698292557`). A resposta foi salva em `/home/ubuntu/upload/tdn.totvs.com_rest_api_content_627111872_child_page_limit_500.md`.

A ramificação Cadastros e Parâmetros (`653144946`) revelou, entre outros, páginas específicas de parâmetros ICMS, ICMS-ST, ISS, PIS-COFINS-CSLL e diversos artigos TES. Fundos e Contribuições (`653143238`) possui BRFUNDOS/FUNRURAL, FUST/FUNTTEL e FCP. As duas respostas foram salvas em `/home/ubuntu/upload/` para consolidação automática.

As páginas Configurações ICMS (`653143266`) e ICMS-ST (`653143971`) foram salvas. Elas retornaram grupos extensos de artigos de cálculo, crédito presumido, DIFAL, desoneração, ICMS-ST, IVA ajustado e regimes estaduais.

Importação (`653147856`) revelou PISCOFIMP (`701692033`); INSS (`654102732`) revelou a página de configurações de retenção (`697252452`). As respostas foram salvas localmente.

IPI (`653145507`) retornou quatro artigos, entre eles crédito destacado/não destacado, complemento de IPI e IPI na Zona Franca de Manaus. IRRF (`653143855`) retornou quatro artigos sobre dedução simplificada, gross up, retenção para pessoa física/jurídica e tabela progressiva. As respostas foram salvas localmente.
