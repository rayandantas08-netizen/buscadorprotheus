# Fontes do pacote — documento de entrada sem os impostos do FISA170

Levantamento de 2026-09-15. Todos os links abaixo existem na base local do repositório
(`client/public/knowledge.json`, 2.391 registros) e foram obtidos nos domínios oficiais
`tdn.totvs.com` e `centraldeatendimento.totvs.com`. O mesmo conteúdo, em formato de índice, está em
`data/indices/Indice_Cfgtrib_Documento_Entrada.txt`.

Status de verificação:

- **LIDO** — artigo aberto e lido nesta sessão; as afirmações do roteiro saem do texto dele.
- **ÍNDICE** — título e URL obtidos na busca dos domínios oficiais; o corpo não foi aberto.
- **NOVO** — não estava na base do repositório antes deste levantamento.

## 1. Diagnóstico: o documento calculou pelo Configurador ou pela TES?

Comece por aqui: estes artigos ensinam a provar **de onde** veio o imposto do documento e a rastrear o cálculo nas tabelas.

- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - Como confirmar se os impostos estão sendo gerados pelo Configurador de Tributos ou TES?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35357410638231-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-confirmar-se-os-impostos-est%C3%A3o-sendo-gerados-pelo-Configurador-de-Tributos-ou-TES) — **LIDO**
- [Cross Segmento - Backoffice (Linha Protheus) - SIGAEST - Como identificar impostos do Configurador de Tributos nas Notas Fiscais?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/37535417591319-Cross-Segmento-Backoffice-Linha-Protheus-SIGAEST-Como-identificar-impostos-do-Configurador-de-Tributos-nas-Notas-Fiscais) — **ÍNDICE · NOVO**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – Não consta o CST de devolução dos impostos calculados pelo Configurador de Tributos.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35068259496599-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-N%C3%A3o-consta-o-CST-de-devolu%C3%A7%C3%A3o-dos-impostos-calculados-pelo-Configurador-de-Tributos) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Erro argument #0 error, expected A->U, function asize on TOTVS.PROTHEUS.BACKOFFICE.FISCAL ao gerar nota com impostos calculados pelo Configurador de Tributos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35148267248279-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Erro-argument-0-error-expected-A-U-function-asize-on-TOTVS-PROTHEUS-BACKOFFICE-FISCAL-ao-gerar-nota-com-impostos-calculados-pelo-Configurador-de-Tributos) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Relacionamento entre tabelas SD1/SD2, SFT, CJ3 e F2D no Configurador de Tributos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38741160434199-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Relacionamento-entre-tabelas-SD1-SD2-SFT-CJ3-e-F2D-no-Configurador-de-Tributos) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - SIGAFIS - Tabelas CJ3 e F2D em branco, o que validar?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/42532771513111-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-SIGAFIS-Tabelas-CJ3-e-F2D-em-branco-o-que-validar) — **ÍNDICE**
- [Cross Segmentos - Backoffice Protheus - FIS - Arq. Magnéticos - Impostos Configurados na Rotina de Configurador de Tributos não Estão Sendo Integrados no TAF](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360050200014-Cross-Segmentos-Backoffice-Protheus-FIS-Arq-Magn%C3%A9ticos-Impostos-Configurados-na-Rotina-de-Configurador-de-Tributos-n%C3%A3o-Est%C3%A3o-Sendo-Integrados-no-TAF) — **ÍNDICE · NOVO**
- [Cross Segmento - Backoffice Linha Protheus - SIGACTB - Contabilização com Base na Sigla do Tributo](https://centraldeatendimento.totvs.com/hc/pt-br/articles/37100272710039-Cross-Segmento-Backoffice-Linha-Protheus-SIGACTB-Contabiliza%C3%A7%C3%A3o-com-Base-na-Sigla-do-Tributo) — **ÍNDICE · NOVO**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Como contabilizar os tributos genéricos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/23400899238295-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-contabilizar-os-tributos-gen%C3%A9ricos) — **ÍNDICE**
- [FAQ - LC 224/25 - Como devem ser tratados os documentos fiscais que foram emitidos sem o cálculo via Configurador de Tributos?](https://tdn.totvs.com/pages/viewpage.action?pageId=1070068057) — **ÍNDICE**

## 2. Por que a regra de cálculo não foi aplicada (perfis, status, vigência, base e alíquota)

Se o imposto não veio do Configurador, a causa quase sempre está nesta etapa: status da regra, vigência e enquadramento dos quatro perfis.

- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - Como garantir o cálculo correto do tributo na nota fiscal utilizando a Regra de Cálculo no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35041323516183-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-garantir-o-c%C3%A1lculo-correto-do-tributo-na-nota-fiscal-utilizando-a-Regra-de-C%C3%A1lculo-no-Configurador-de-Tributos) — **LIDO**
- [CFGTRIB - Cadastro de Perfis do Configurador de Tributos - Boas Práticas](https://tdn.totvs.com/pages/viewpage.action?pageId=825324831) — **ÍNDICE · NOVO**
- [CFGTRIB - Cadastro de Regras de Cálculo no Configurador de Tributos - Boas Práticas](https://tdn.totvs.com/pages/viewpage.action?pageId=887731155) — **ÍNDICE · NOVO**
- [CFGTRIB - Cadastro de Regras de Cálculo no Configurador de Tributos - Boas Práticas](https://tdn.totvs.com/pages/viewpage.action?pageId=825324804) — **ÍNDICE**
- [CFGTRIB - Cálculos no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=676039354) — **ÍNDICE**
- [CFGTRIB - Guia Prático Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=966220651) — **ÍNDICE**
- [How To - Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=985663880) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Onde informar a data de vigência da regra criada no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33964900963223-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Onde-informar-a-data-de-vig%C3%AAncia-da-regra-criada-no-Configurador-de-Tributos) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Mecanismo de aprovação de Regras de Cálculo (campo Status) no Configurador de Tributos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35344118632215-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Mecanismo-de-aprova%C3%A7%C3%A3o-de-Regras-de-C%C3%A1lculo-campo-Status-no-Configurador-de-Tributos) — **ÍNDICE**
- [CFGTRIB - Mecanismo de aprovação de regra](https://tdn.totvs.com/pages/viewpage.action?pageId=942068847) — **ÍNDICE**
- [Central de Diagnóstico: Reforma Tributária - Configurações Mínimas](https://tdn.totvs.com/pages/viewpage.action?pageId=1027814147) — **ÍNDICE**
- [CFGTRIB - Configurador de Tributos](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Configurador+de+Tributos) — **ÍNDICE**
- [CFGTRIB - Perguntas e Respostas - Configurador de Tributos](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Perguntas+e+Respostas+-+Configurador+de+Tributos) — **ÍNDICE**
- [CFGTRIB - Campos do cadastro de Tipos de Entrada e Saída descontinuados em favor do Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=906853167) — **ÍNDICE**
- [CFGTRIB - Campos da TES](https://tdn.totvs.com/pages/viewpage.action?pageId=943126076) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Quais tabelas fazem parte do Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35314721022103-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Quais-tabelas-fazem-parte-do-Configurador-de-Tributos) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Compartilhamento de Tabelas de Perfis, Regras de Cálculo e Regra de Escrituração](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36181199260183-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Compartilhamento-de-Tabelas-de-Perfis-Regras-de-C%C3%A1lculo-e-Regra-de-Escritura%C3%A7%C3%A3o) — **ÍNDICE**

## 3. Testar a regra antes de lançar o documento (simuladores e exemplos de entrada)

Como validar a regra sem lançar documento — e exemplos completos de operação de entrada.

- [CFGTRIB - Simulador de Operação](https://tdn.totvs.com/pages/viewpage.action?pageId=877863294) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Simulador de Operações](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34881620535831-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Simulador-de-Opera%C3%A7%C3%B5es) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Simulador Comparativo](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34881724308119-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Simulador-Comparativo) — **ÍNDICE**
- [CFGTRIB - Cálculo de ICMS ST](https://tdn.totvs.com/pages/viewpage.action?pageId=754953443) — **ÍNDICE · NOVO**
- [CFGTRIB - ICMS Próprio - Cálculos no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=899211646) — **ÍNDICE**
- [CFGTRIB - ICMS-ST - Cálculos no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=899211761) — **ÍNDICE**

## 4. Documento de Entrada (MATA103, pré-nota/classificação) e impostos por tributo

Documentação específica do Documento de Entrada (MATA103), pré-nota/classificação, impostos por tributo e integração com o financeiro.

- [MATA103 - Documentos Fiscais de Entrada](https://tdn.totvs.com/pages/viewpage.action?pageId=702350726) — **ÍNDICE**
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS- Replicar TES Inteligente para os itens na classificação do documento de entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360056639953--CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Replicar-TES-Inteligente-para-os-itens-na-classifica%C3%A7%C3%A3o-do-documento-de-entrada) — **ÍNDICE**
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Inclusão manual de impostos na inclusão do documento de entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360052837513-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Inclus%C3%A3o-manual-de-impostos-na-inclus%C3%A3o-do-documento-de-entrada) — **ÍNDICE**
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Alíquotas com asteriscos no documento de entrada (MATA103).](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360019859292-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Al%C3%ADquotas-com-asteriscos-no-documento-de-entrada-MATA103) — **ÍNDICE**
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como habilitar a opção Modalidade de retenção do PIS, COFINS e CSLL localizado na aba Duplicatas na rotina MATA103 - Documento de Entrada?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4409524481047-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-habilitar-a-op%C3%A7%C3%A3o-Modalidade-de-reten%C3%A7%C3%A3o-do-PIS-COFINS-e-CSLL-localizado-na-aba-Duplicatas-na-rotina-MATA103-Documento-de-Entrada) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como configurar o IPI para revenda e consumo na entrada da nota fiscal?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/41483144616599-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-o-IPI-para-revenda-e-consumo-na-entrada-da-nota-fiscal) — **ÍNDICE**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Como calcular o ICMS próprio em operações de entrada e saída?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/23397761395223-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-ICMS-pr%C3%B3prio-em-opera%C3%A7%C3%B5es-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular o ISS utilizando o Configurador de Tributos para notas de entrada e saída?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33675439757335-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-ISS-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular PIS/COFINS/CSLL retenção utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271950709399-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-PIS-COFINS-CSLL-reten%C3%A7%C3%A3o-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular o INSS utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33702907793175-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-o-INSS-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular PIS-COFINS Apuração utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/28273192090135-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-PIS-COFINS-Apura%C3%A7%C3%A3o-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular IRRF utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271222087959-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-IRRF-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular FUNRURAL utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33723976776471-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-FUNRURAL-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — **ÍNDICE**
- [Cross Segmentos - Backoffice Linha Protheus - SIGAFIN - FISA170 - Como gerar os impostos no financeiro através do documento de entrada?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35446019140119-Cross-Segmentos-Backoffice-Linha-Protheus-SIGAFIN-FISA170-Como-gerar-os-impostos-no-financeiro-atrav%C3%A9s-do-documento-de-entrada) — **ÍNDICE · NOVO**
- [Cross Segmentos - Backoffice Linha Protheus - SIGAFIN - Lei 15.270/2025 - FISA170 - Reforma do Imposto de Renda 2026 no configurador de tributos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38643317434135-Cross-Segmentos-Backoffice-Linha-Protheus-SIGAFIN-Lei-15-270-2025-FISA170-Reforma-do-Imposto-de-Renda-2026-no-configurador-de-tributos) — **ÍNDICE · NOVO**
- [Guia para adequações à Reforma Tributária - Escritórios de Advocacia](https://tdn.totvs.com/pages/releaseview.action?pageId=928942962) — **ÍNDICE · NOVO**
- [Cross Segmento - TOTVS Backoffice Linha Protheus - SIGAEIC - Apresentar valores do PIS e Cofins ao Classificar o Documento de Entrada](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360028714292-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-SIGAEIC-Apresentar-valores-do-PIS-e-Cofins-ao-Classificar-o-Documento-de-Entrada) — **ÍNDICE**
- [PE - MAVLDIMP - Edição dos Impostos do documento de entrada](https://tdn.totvs.com/pages/viewpage.action?pageId=656048427) — **ÍNDICE**
- [PE - MFISIMP - Valida a inclusão de Impostos manuais do Documento de Entrada](https://tdn.totvs.com/pages/viewpage.action?pageId=655864588) — **ÍNDICE**

## Fora da base local (fontes de terceiros)

Não são documentação TOTVS e **não** entram no índice do repositório. Foram usadas apenas para
os pontos marcados como **[TERCEIROS]** no roteiro (vigência da regra, URF sem valor no período,
operando de base/alíquota ausente no documento e release mínima 12.1.23):

- [Configurador de Tributos — Mastersiga Consultoria](https://mastersiga.tomticket.com/kb/livros-fiscais/configurador-de-tributos)
- [Configurador de Tributos do Protheus — ERP Serv](https://erpserv.com.br/configurador-de-tributos-do-protheus-saiba-tudo-sobre-essa-ferramenta/)
- [FAQ Configurador de Tributos — FB Solutions](https://www.fbsolutions.com.br/erp-totvs-protheus/configurador-de-tributos/faq-configurador-tributos-protheus/)
