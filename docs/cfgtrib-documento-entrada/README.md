# Documento de Entrada sem os impostos do Configurador de Tributos (FISA170)

Pacote de diagnóstico para o sintoma: **o Documento de Entrada (MATA103, pré-nota MATA140 e
classificação) não traz os impostos calculados pelo Configurador de Tributos (FISA170)** — a aba
"Impostos" fica só com os impostos legados, ou o tributo genérico simplesmente não aparece.

Levantamento feito em 2026-09-15 a partir de duas varreduras:

1. **Base local do repositório** — os 2.391 links versionados em `data/indices/` (TDN e Central de
   Atendimento TOTVS), pesquisados com o mesmo ranking da aplicação (`client/src/lib/search.ts`).
2. **Busca nos domínios oficiais** — `tdn.totvs.com` e `centraldeatendimento.totvs.com`, para os
   artigos que ainda não estavam indexados. Nove links novos entraram na base
   (`data/indices/Indice_Cfgtrib_Documento_Entrada.txt`).

> **Não existe** artigo oficial com o título exato "documento de entrada não calcula os impostos do
> Configurador de Tributos". O que existe é o conjunto abaixo: um artigo que ensina a confirmar a
> origem do cálculo, um que lista os critérios de enquadramento da regra e os guias de perfis. Este
> roteiro costura os três na ordem em que se deve verificar.

| Arquivo                           | Conteúdo                                                                                |
| --------------------------------- | --------------------------------------------------------------------------------------- |
| `01-diagnostico-passo-a-passo.md` | Roteiro de verificação na ordem do sintoma, com campos, tabelas e a fonte de cada item. |
| `02-fontes.md`                    | Os 51 links do pacote, agrupados por etapa, com o status de verificação de cada um.     |

## Resposta curta

Com o Configurador de Tributos ativo, ele é sempre a **primeira** fonte de cálculo: o sistema só
volta para TES/cadastros legados quando a nota **não se enquadra** nos quatro perfis de validação —
Perfil de Produto, Perfil de Participante, Perfil de Operação e Perfil de Origem/Destino
([Central de Atendimento TOTVS, artigo 35357410638231](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35357410638231-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-confirmar-se-os-impostos-est%C3%A3o-sendo-gerados-pelo-Configurador-de-Tributos-ou-TES)).

Portanto, "documento de entrada sem os impostos do Configurador" quase sempre é **enquadramento**,
não cálculo: a regra existe, mas um dos quatro perfis não casou com os dados da nota (CFOP de
saída em vez de entrada, participante cadastrado como cliente em vez de fornecedor, produto fora do
perfil, UF de origem/destino fora do perfil), ou a regra está **Em Teste**/fora da vigência.

## Como procurar isso no Buscador Protheus

Digite a frase inteira na busca:

```
documento de entrada não está trazendo os impostos do configurador de tributos
```

O primeiro resultado é _SIGAEST — Como identificar impostos do Configurador de Tributos nas Notas
Fiscais?_; nas dez primeiras posições também entra _CFGTRIB — Cadastro de Perfis … Boas Práticas_
(verificado em `client/src/lib/cfgtrib-documento-entrada.test.ts`).
