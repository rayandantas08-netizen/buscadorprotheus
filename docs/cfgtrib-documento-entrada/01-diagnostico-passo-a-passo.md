# Roteiro de diagnóstico — Documento de Entrada sem os impostos do FISA170

Siga na ordem: cada passo elimina uma causa e o passo 1 decide onde procurar depois.

Legenda das fontes:

- **[LIDO]** — artigo aberto e lido nesta sessão (2026-09-15).
- **[ÍNDICE]** — título e URL obtidos na busca dos domínios oficiais; o corpo não foi aberto.
- **[TERCEIROS]** — resumo de consultoria/parceiro, não é documentação TOTVS; usar como pista.

---

## Passo 1 — Confirmar se a nota calculou pelo Configurador ou pela TES

1. Abra o Documento de Entrada e vá na **aba Impostos** (é aí que o cálculo do FISA170 aparece na
   entrada; no pedido de venda seria a Planilha Financeira). **[LIDO]**
2. Olhe **código** e **descrição** do imposto:
   - código `ICM` com descrição `ICMS` → cálculo pelo **legado (TES)**;
   - outro código/descrição (os que você definiu no Configurador) → cálculo pelo **Configurador**.
     **[LIDO]**
3. Confirme pelas tabelas: com o Configurador é gerado um identificador de tributo em
   `SD1.D1_IDTRIB`, `SD2.D2_IDTRIB` e `SFT.FT_IDTRIB`. `SF3`, `SF1`, `SF2`, `SC5` e `SC6` **não**
   guardam esse ID. **[LIDO]**
   - `D1_IDTRIB` vazio no item da entrada = o Configurador não entrou no cálculo daquele item.
   - O ID liga a `F2D.F2D_IDREL`; `F2D_TRIB` traz a sigla do tributo e `F2D_VALOR` o valor, e a
     regra aplicada fica em `F2B` (`F2B_REGRA`). **[ÍNDICE]**
4. Alternativa sem abrir tabela: aba **"Tributos Genéricos - por item"** do documento, onde o campo
   **Sigla** indica o código da Regra de Cálculo - Documentos Fiscais aplicada. **[ÍNDICE]**

Fontes:
[Como confirmar se os impostos estão sendo gerados pelo Configurador de Tributos ou TES?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35357410638231-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-confirmar-se-os-impostos-est%C3%A3o-sendo-gerados-pelo-Configurador-de-Tributos-ou-TES)
· [Como identificar impostos do Configurador de Tributos nas Notas Fiscais?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/37535417591319-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-Como-identificar-impostos-do-Configurador-de-Tributos-nas-Notas-Fiscais)
· [Relacionamento entre tabelas SD1/SD2, SFT, CJ3 e F2D](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38741160434199-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Relacionamento-entre-tabelas-SD1-SD2-SFT-CJ3-e-F2D-no-Configurador-de-Tributos)

---

## Passo 2 — Validar a Regra de Cálculo - Documentos Fiscais

- **Status** da regra: `1 - Aprovado` aplica o cálculo; `2 - Em Teste` mostra o tributo **apenas no
  Simulador** e não afeta a nota real. **[LIDO]**
- **Vigência**: a data do documento precisa estar dentro da vigência da regra; se a data do
  documento for anterior à data inicial, a regra não é aplicada. **[TERCEIROS]**
  Onde informar: [FISA170 - Onde informar a data de vigência da regra criada no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33964900963223-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Onde-informar-a-data-de-vig%C3%AAncia-da-regra-criada-no-Configurador-de-Tributos) **[ÍNDICE]**
  e [Mecanismo de aprovação de Regras de Cálculo (campo Status)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35344118632215-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Mecanismo-de-aprova%C3%A7%C3%A3o-de-Regras-de-C%C3%A1lculo-campo-Status-no-Configurador-de-Tributos) **[ÍNDICE]**

Fonte:
[Como garantir o cálculo correto do tributo na nota fiscal utilizando a Regra de Cálculo no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35041323516183-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-garantir-o-c%C3%A1lculo-correto-do-tributo-na-nota-fiscal-utilizando-a-Regra-de-C%C3%A1lculo-no-Configurador-de-Tributos)

---

## Passo 3 — Conferir o enquadramento dos quatro perfis (causa mais comum)

A regra só vale se a nota se enquadrar nos perfis amarrados nela. Se não enquadrar, o sistema
recorre aos cadastros tradicionais. **[LIDO]**

| Perfil                       | O que conferir na nota de entrada                                                                                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Perfil de Operação**       | O **CFOP** tem que ser o da TES usada no item (`F4_CF`) e precisa ser CFOP de **entrada**. **Tipo de Operação**: se não houver especificação, deve ficar `TODOS`. **Código de Serviço**: quando o produto tem `B1_CODISS`, o código precisa constar no perfil junto com o CFOP. **[LIDO]** |
| **Perfil de Participante**   | Para entrada o participante é **fornecedor**: o perfil tem `Tipo 1 - Fornecedor (SA2)`. Perfil montado como `2 - Cliente (SA1)` nunca casa com a nota de entrada. O participante/loja do documento é comparado com os participantes do perfil amarrado em `F2B_PERFPA`. **[ÍNDICE]**       |
| **Perfil de Produto**        | Todos os produtos que devem ter o tributo precisam estar no perfil (por código, NCM, tipo, destinação ou tributação). O enquadramento considera a origem informada **na linha do item** na inclusão do Documento Fiscal — Pedido de Venda ou Documento de Entrada. **[ÍNDICE]**            |
| **Perfil de Origem/Destino** | Os estados da operação. A carga inicial cria Operação interna, Todas as UFs, Saídas Interestaduais e **Entradas Interestaduais** a partir do `MV_ESTADO` da filial. **[ÍNDICE]**                                                                                                           |

Fontes:
[CFGTRIB - Cadastro de Perfis do Configurador de Tributos - Boas Práticas](https://tdn.totvs.com/pages/viewpage.action?pageId=825324831)
· [CFGTRIB - Configurador de Tributos (Perfil de Participante / F2B_PERFPA)](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Configurador+de+Tributos)
· [CFGTRIB - Cadastro de Regras de Cálculo no Configurador de Tributos - Boas Práticas](https://tdn.totvs.com/pages/viewpage.action?pageId=887731155)
· [CFGTRIB - Regras por NCM](https://tdn.totvs.com/pages/viewpage.action?pageId=942052690)

---

## Passo 4 — Base de cálculo, alíquota e escrituração

- Se o operando escolhido na **Regra de Base de Cálculo** não existir no documento, o tributo não é
  calculado; o mesmo vale para a **Regra de Alíquota**. Quando a alíquota vem de **URF** e não há
  valor para o período da nota, a alíquota vai a zero e o tributo não sai. **[TERCEIROS]**
  Referência oficial: [CFGTRIB - Cálculos no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=676039354) **[ÍNDICE]**
- Sem **regra de escrituração** amarrada na Regra de Cálculo, o sistema usa Livro Fiscal, CST e
  aplicação do valor no total da nota que estiverem na **TES** usada no documento. **[ÍNDICE]**
  Referência: [Guia para adequações à Reforma Tributária](https://tdn.totvs.com/pages/releaseview.action?pageId=928942962)
- Campos da TES que decidiam imposto foram **descontinuados** em favor do Configurador — confira o
  que ainda vale: [Campos da TES descontinuados](https://tdn.totvs.com/pages/viewpage.action?pageId=906853167)
  e [Campos que permanecem no TES](https://tdn.totvs.com/pages/viewpage.action?pageId=928965724). **[ÍNDICE]**

---

## Passo 5 — Verificar tabelas e compartilhamento

- `F2D` (Tributos Genéricos Calculados) precisa estar **exclusiva**: o vínculo é por documento
  fiscal. `F2B` (regras) pode ser compartilhada. **[ÍNDICE]**
- `CJ3_IDTGEN` grava o mesmo ID do cálculo e amarra documento → livro fiscal → tributo. **[ÍNDICE]**
- Se `CJ3` e `F2D` ficaram em branco, siga o checklist oficial:
  [Tabelas CJ3 e F2D em branco, o que validar?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/42532771513111-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-SIGAFIS-Tabelas-CJ3-e-F2D-em-branco-o-que-validar) **[ÍNDICE]**

Fontes:
[Quais tabelas fazem parte do Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35314721022103-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Quais-tabelas-fazem-parte-do-Configurador-de-Tributos)
· [Impostos configurados no Configurador de Tributos não estão sendo integrados no TAF (F2D exclusiva)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360050200014-Cross-Segmentos-Backoffice-Protheus-FIS-Arq-Magn%C3%A9ticos-Impostos-Configurados-na-Rotina-de-Configurador-de-Tributos-n%C3%A3o-Est%C3%A3o-Sendo-Integrados-no-TAF)

---

## Passo 6 — Imposto retido, título financeiro e total da nota

- Para o imposto do documento de entrada **gerar título no financeiro**, é preciso existir uma
  **Regra Financeira** cadastrada e **amarrada à Regra de Cálculo** (Regra Fiscal → Regra de Cálculo
  do Documento Fiscal → alterar → vincular a Regra Financeira). Fornecedor e Natureza devem ser
  criados **sem** parametrização de imposto: tudo fica na Regra Financeira. **[ÍNDICE]**
  [FISA170 - Como gerar os impostos no financeiro através do documento de entrada?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35446019140119-Cross-Segmentos-Backoffice-Linha-Protheus-SIGAFIN-FISA170-Como-gerar-os-impostos-no-financeiro-atrav%C3%A9s-do-documento-de-entrada)
- IRRF originado de Documento de Entrada (MATA103) depende de parametrizar as Regras Fiscais
  (FISA170); a regra financeira isolada só cobre títulos avulsos. **[ÍNDICE]**
  [Lei 15.270/2025 - FISA170 - Reforma do Imposto de Renda 2026](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38643317434135-Cross-Segmentos-Backoffice-Linha-Protheus-SIGAFIN-Lei-15-270-2025-FISA170-Reforma-do-Imposto-de-Renda-2026-no-configurador-de-tributos)
- Por tributo na entrada: [ICMS próprio](https://centraldeatendimento.totvs.com/hc/pt-br/articles/23397761395223-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-ICMS-pr%C3%B3prio-em-opera%C3%A7%C3%B5es-de-entrada-e-sa%C3%ADda)
  · [ISS](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33675439757335-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-ISS-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda)
  · [PIS/COFINS/CSLL retenção](https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271950709399-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-PIS-COFINS-CSLL-reten%C3%A7%C3%A3o-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda)
  · [INSS](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33702907793175-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-INSS-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda)
  · [IPI revenda x consumo na entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/41483144616599-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-o-IPI-para-revenda-e-consumo-na-entrada-da-nota-fiscal) **[ÍNDICE]**

---

## Passo 7 — Se a nota veio por pré-nota, classificação ou ponto de entrada

- Na classificação de pré-nota, os itens podem não herdar a configuração: existe procedimento para
  **replicar a TES Inteligente para os itens** na classificação do documento de entrada. **[ÍNDICE]**
  [Replicar TES Inteligente para os itens na classificação do documento de entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360056639953--CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Replicar-TES-Inteligente-para-os-itens-na-classifica%C3%A7%C3%A3o-do-documento-de-entrada)
- Impostos editados/validados manualmente na entrada passam pelos pontos de entrada
  [MAVLDIMP](https://tdn.totvs.com/pages/viewpage.action?pageId=656048427) e
  [MFISIMP](https://tdn.totvs.com/pages/viewpage.action?pageId=655864588): se houver customização
  neles, ela pode sobrescrever o que o Configurador calculou. **[ÍNDICE]**
- Lançamento manual de imposto na inclusão: [Inclusão manual de impostos na inclusão do documento de entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360052837513-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Inclus%C3%A3o-manual-de-impostos-na-inclus%C3%A3o-do-documento-de-entrada) **[ÍNDICE]**

---

## Passo 8 — Testar a regra antes de culpar o cálculo

- [Simulador de Operação](https://tdn.totvs.com/pages/viewpage.action?pageId=877863294) — testa a
  regra com os dados de uma operação sem lançar documento. **[ÍNDICE]**
- [Simulador Comparativo](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34881724308119-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Simulador-Comparativo) —
  compara o resultado do Configurador com o legado. **[ÍNDICE]**
- [Central de Diagnóstico: Reforma Tributária - Configurações Mínimas](https://tdn.totvs.com/pages/viewpage.action?pageId=1027814147) —
  rotina que aponta as configurações mínimas ausentes. **[ÍNDICE]**
- Regra em `2 - Em Teste` aparece **só** no simulador (passo 2). **[LIDO]**

---

## Passo 9 — Quando o problema é outro (error.log, dicionário, CST)

- `argument #0 error, expected A->U, function asize` ao gerar nota com impostos do Configurador:
  [artigo 35148267248279](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35148267248279-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Erro-argument-0-error-expected-A-U-function-asize-on-TOTVS-PROTHEUS-BACKOFFICE-FISCAL-ao-gerar-nota-com-impostos-calculados-pelo-Configurador-de-Tributos) **[ÍNDICE]**
- CST de devolução não consta nos impostos calculados pelo Configurador:
  [artigo 35068259496599](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35068259496599-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-N%C3%A3o-consta-o-CST-de-devolu%C3%A7%C3%A3o-dos-impostos-calculados-pelo-Configurador-de-Tributos) **[ÍNDICE]**
- Dicionário desatualizado / motor de cálculo fiscal:
  [artigo 36699322874263](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36699322874263-Cross-Segmentos-Backoffice-Protheus-FIS-Escrita-Fiscal-Dicion%C3%A1rio-desatualizado-favor-verificar-atualiza%C3%A7%C3%B5es-do-motor-de-c%C3%A1lculo-fiscal) **[ÍNDICE]**
- Documentos já emitidos sem o cálculo via Configurador:
  [FAQ - LC 224/25](https://tdn.totvs.com/pages/viewpage.action?pageId=1070068057) **[ÍNDICE]**
- Alíquotas com asteriscos no MATA103:
  [artigo 360019859292](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360019859292-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Al%C3%ADquotas-com-asteriscos-no-documento-de-entrada-MATA103) **[ÍNDICE]**

---

## Requisitos de versão

- O Configurador de Tributos exige release **12.1.23** ou superior; os artigos oficiais de FISA170
  citam ambiente "a partir da versão 12.1.2210". **[TERCEIROS]** / **[LIDO]**
