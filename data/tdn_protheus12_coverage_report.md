# Relatório de Cobertura — Árvore Protheus 12 no TDN

**Fonte:** [Protheus 12 — TDN TOTVS](https://tdn.totvs.com/display/public/PROT/Protheus++12)  
**Data:** 21 de agosto de 2026

## Resultado

Foi gerado um inventário reproduzível da árvore de links TDN já capturada no projeto. O inventário contém **282 URLs únicas**, com título e URL oficial, e está disponível em `data/tdn_protheus12_inventory.json`. O mesmo conjunto foi exportado para `data/indices/tdn_protheus12_root.txt` e incorporado ao pipeline de geração do `knowledge.json`.

A deduplicação global manteve o total da base em **2.494 links**, porque os 282 URLs da árvore geral já estavam representados por outras fontes textuais do projeto, principalmente `tdn_tree_links.txt` e índices de módulos. A integração, portanto, não duplica registros; ela torna a origem da árvore Protheus 12 explícita e auditável.

| Indicador | Resultado |
|---|---:|
| URLs únicas no inventário da árvore capturada | 282 |
| Arquivo JSON reproduzível | `data/tdn_protheus12_inventory.json` |
| Índice textual integrado ao build | `data/indices/tdn_protheus12_root.txt` |
| Total final de links no buscador | 2.494 |
| Duplicidades introduzidas | 0 |

## Limitação de recursividade

A consulta direta da raiz e de seu endpoint REST de filhos retornou a mensagem de bloqueio “Please contact the site owner for access” durante esta rodada. A página raiz também foi previamente bloqueada por CAPTCHA. Por essa razão, o arquivo representa a **árvore de links capturada e verificável**, mas não comprova que todos os descendentes atualmente existentes no TDN tenham sido enumerados.

O inventário mantém essa situação explicitamente no campo `coverage_status`. Uma expansão futura deverá começar pelas páginas da árvore que ainda não tenham respostas `child/page` salvas, quando o TDN permitir acesso automatizado.

## Referências

[1]: https://tdn.totvs.com/display/public/PROT/Protheus++12 "Protheus 12 — TDN TOTVS"
[2]: https://tdn.totvs.com/rest/api/content/237387586/child/page?limit=500 "Endpoint oficial de filhos da página raiz Protheus 12"
