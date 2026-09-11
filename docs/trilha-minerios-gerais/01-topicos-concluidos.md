# Tópicos concluídos — revisão e reforço de treinamento

> Itens já implantados no cliente. A trilha serve para revisar a parametrização feita, padronizar o discurso do treinamento e registrar evidências de validação.

Projeto: **Minérios Gerais — implantação e treinamento do Fiscal Protheus 12**  ·  Gerado em 2026-09-11  ·  Base local com 2382 links.

## 1. Cadastros fiscais: produtos, fornecedores e clientes

**Status:** `concluido`  ·  **Fontes na base:** 109 candidatas, 12 selecionadas.

Base de tudo: SB1 (produto), SA1 (cliente) e SA2 (fornecedor) carregam os atributos que alimentam TES, Configurador de Tributos, livros fiscais e SPED (registros 0150, 0200 e 0205).

**Rotinas e objetos técnicos**

- `MATA010 / Cadastro de Produtos (SB1)`
- `MATA030 / Cadastro de Clientes (SA1)`
- `MATA020 / Cadastro de Fornecedores (SA2)`
- `FISA164 — Perfil tributário de participantes`
- `FISA166 — Perfil tributário de produtos`
- `Atualização de Dicionário da Classificação Tributária (cClassTrib)`

**Como implantar**

1. Conferir nos produtos: tipo (B1_TIPO), NCM, CEST, unidade de medida, origem da mercadoria, alíquotas de ICMS/IPI/PIS/COFINS e, quando usado o Configurador de Tributos, a classificação tributária (cClassTrib) e o cBenef.
2. Conferir nos participantes: inscrição estadual (validação de IE), indicador de contribuinte, município/UF, regime de tributação e os campos de retenção (A1_RECPIS/A1_RECCOFI, A2_RECPIS/A2_RECCOFI/A2_RECCSLL, A2_RECISS).
3. Vincular os perfis tributários (FISA164/FISA166) aos participantes e produtos que exigem tratamento diferenciado.
4. Definir quem mantém cada atributo após o go-live (governança de cadastro) e como será feita a carga/atualização em massa.

**Como treinar**

- Mostrar onde cada campo fiscal do cadastro impacta: TES, cálculo do imposto, livro fiscal (SF3/SFT) e SPED.
- Exercitar a inclusão de um produto novo completo e a validação do alerta de IE inválida no cliente/fornecedor.
- Treinar a rotina de atualização da classificação tributária e o conceito de pacote do Configurador de Tributos.

**Como validar (evidência de entrega)**

- Amostra de produtos e participantes escriturados corretamente no registro 0200/0150 do SPED Fiscal.
- Sem helps de IE, NCM ou classificação tributária na emissão de notas de teste.

**Fontes no índice local**

*Para implantar / parametrizar*

- [[CFGTRIB] - FISA164 - Cadastro de perfil tributário de participantes](https://tdn.totvs.com/pages/viewpage.action?pageId=788607214) — Fiscal - Protheus 12 (TDN)
- [[CFGTRIB] - FISA166 - Cadastro de perfil tributário de produtos](https://tdn.totvs.com/pages/viewpage.action?pageId=788614355) — Fiscal - Protheus 12 (TDN)
- [Atualização de Dicionário Classificação Tributária - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=784782300) — Fiscal - Protheus 12 (TDN)
- [Cadastros - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=606084833) — Fiscal - Protheus 12 (TDN)
- [CLASSTRIB- Classificação Tributária by Systax](https://tdn.totvs.com/pages/viewpage.action?pageId=727362166) — Referências gerais TDN (TDN)
- [Configurações - Cadastros e Parâmetros - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=653144946) — Fiscal - Protheus 12 (TDN)
- [Faturamento - Cadastros > Cross Segmentos - Backoffice Protheus - SIGAFAT - Manutenção no Cadastro NCM (Clientes que não utilizam o módulo SIGAEIC)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/10545950391703-Cross-Segmentos-Backoffice-Protheus-SIGAFAT-Manuten%C3%A7%C3%A3o-no-Cadastro-NCM-Clientes-que-n%C3%A3o-utilizam-o-m%C3%B3dulo-SIGAEIC) — Faturamento (Central TOTVS)
- [Materiais - Compras > Cross Segmentos - TOTVS Backoffice (Linha Protheus) - SIGACOM - Facilitador do Cadastro de Fornecedores](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33660892155671-Cross-Segmentos-TOTVS-Backoffice-Linha-Protheus-SIGACOM-Facilitador-do-Cadastro-de-Fornecedores) — Compras (Central TOTVS)
- [Faturamento - Cadastros > Cross Segmentos - TOTVS Backoffice (Linha Protheus) - SIGAFAT (Faturamento) - Configurar campos que não aparecem no facilitador de cadastro de clientes](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4414663139863-Cross-Segmentos-TOTVS-Backoffice-Linha-Protheus-SIGAFAT-Faturamento-Configurar-campos-que-n%C3%A3o-aparecem-no-facilitador-de-cadastro-de-clientes) — Faturamento (Central TOTVS)
- [Faturamento - Cadastros > Cross Segmentos - TOTVS Backoffice (Linha Protheus) - SIGAFAT - Facilitador do Cadastro de Clientes](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4403166262167-Cross-Segmentos-TOTVS-Backoffice-Linha-Protheus-SIGAFAT-Facilitador-do-Cadastro-de-Clientes) — Faturamento (Central TOTVS)

*Suporte, FAQ e resolução de erros*

- [Como resolver alerta ao informar Inscrição Estadual no Cadastro de Cliente/Fornecedor?](https://tdn.totvs.com/pages/viewpage.action?pageId=706135215) — Fiscal - Protheus 12 (TDN)
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Alerta ao informar Inscrição Estadual de MG no cadastro de Cliente/Fornecedor](https://centraldeatendimento.totvs.com/hc/pt-br/articles/8442235970839-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Alerta-ao-informar-Inscri%C3%A7%C3%A3o-Estadual-de-MG-no-cadastro-de-Cliente-Fornecedor) — Escrituração e Relatórios Fiscal (Central TOTVS)

---

## 2. TES: entrada e saída

**Status:** `concluido`  ·  **Fontes na base:** 75 candidatas, 12 selecionadas.

Tipo de Entrada e Saída (SF4) define CFOP, atualização de estoque/financeiro, cálculo e escrituração de cada imposto. É o ponto que mais gera retrabalho quando fica mal configurado.

**Rotinas e objetos técnicos**

- `MATA080 — Cadastro de TES (SF4)`
- `TES Inteligente / Réplica de TES`
- `Pontos de entrada da TES (MATA080)`

**Como implantar**

1. Para cada cenário de operação (compra, venda, devolução, remessa, retorno, transferência, uso/consumo, ativo imobilizado, industrialização em terceiros) definir TES de entrada e de saída.
2. Conferir campo a campo: CFOP, calcula ICMS/IPI/PIS/COFINS/ISS, livro fiscal de cada imposto, material de consumo, credita ICMS, atualiza estoque, gera duplicata, poder de terceiros (F4_PODER3) e agrega valor (F4_AGREG).
3. Definir a convivência entre TES legado e Configurador de Tributos (híbrido) e quais campos passam a ser decididos pelo FISA170.
4. Documentar a matriz CFOP x TES x CST/CSOSN x classificação tributária usada no projeto.

**Como treinar**

- Explicar a leitura da TES em conjunto com o cadastro do produto e do participante (o imposto sai da combinação dos três).
- Exercitar a cópia de TES e a montagem de uma TES nova para um cenário inexistente.
- Mostrar os helps mais comuns (A900CPO, validações de CFOP) e como diagnosticá-los.

**Como validar (evidência de entrega)**

- Notas de teste de entrada e saída gravando SF3/SFT com CFOP, base e imposto coerentes.
- Matriz de operações do projeto coberta por TES homologadas.

**Fontes no índice local**

*Para implantar / parametrizar*

- [MATA080 - Rotina automática para cadastro de TES](https://tdn.totvs.com/pages/viewpage.action?pageId=706121236) — Fiscal - Protheus 12 (TDN)
- [TES - Base de ICMS sobre o valor produto com desconto condicional](https://tdn.totvs.com/pages/viewpage.action?pageId=706119416) — Fiscal - Protheus 12 (TDN)
- [TES - Calcular Diferencial de Alíquota sem Reduzir a Base de Cálculo](https://tdn.totvs.com/pages/viewpage.action?pageId=705462168) — Fiscal - Protheus 12 (TDN)
- [TES - Campo Agrega Valor F4_AGREG](https://tdn.totvs.com/pages/viewpage.action?pageId=705461928) — Fiscal - Protheus 12 (TDN)
- [TES - Cenários de composição do ICMS com IBS e CBS](https://tdn.totvs.com/pages/viewpage.action?pageId=1076455560) — Fiscal - Protheus 12 (TDN)
- [TES - Comportamento campo F4_DESCOND sobre a Base do ISS quando existir desconto](https://tdn.totvs.com/pages/viewpage.action?pageId=706119992) — Fiscal - Protheus 12 (TDN)
- [TES - Configuração de TES para Uso/Consumo (CFOP 1556)](https://tdn.totvs.com/pages/viewpage.action?pageId=706118700) — Fiscal - Protheus 12 (TDN)
- [TES - Configuração para ICMS Dispensado](https://tdn.totvs.com/pages/viewpage.action?pageId=706118422) — Fiscal - Protheus 12 (TDN)
- [TES - Cópia de TES - MATA080](https://tdn.totvs.com/pages/viewpage.action?pageId=705461414) — Fiscal - Protheus 12 (TDN)
- [TES - Situação Trib. do ICMS F4_SITTRIB](https://tdn.totvs.com/pages/viewpage.action?pageId=706120657) — Fiscal - Protheus 12 (TDN)

*Pontos de entrada e customizações (ADVPL)*

- [Escrita Fiscal - CFOP > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Pontos de Entrada TES (MATA080)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4404850575767-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Pontos-de-Entrada-TES-MATA080) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [PE - MT089TES - Seleção do TES](https://tdn.totvs.com/pages/viewpage.action?pageId=658234488) — Fiscal - Protheus 12 (TDN)

---

## 3. Configuração de tributos (impostos legados) e Configurador de Tributos

**Status:** `concluido`  ·  **Fontes na base:** 220 candidatas, 12 selecionadas.

Duas camadas convivem: os impostos legados (TES, exceção fiscal, alíquotas em cadastro) e o Configurador de Tributos (FISA170), que passa a ser obrigatório para novas legislações e para IBS/CBS.

**Rotinas e objetos técnicos**

- `FISA170 — Configurador de Tributos`
- `FISA080 — UF x UF (FECP e interestadual)`
- `SF7 — Exceção Fiscal`
- `TaxOpJson / Operando — recepção de tributos cadastrados`

**Como implantar**

1. Mapear o escopo: quais tributos e operações ficam no Configurador e quais permanecem no legado.
2. Cadastrar regras de tributação (operadores, vigências, cBenef, ClassTrib) por UF e por cenário de operação.
3. Configurar exceções fiscais (SF7) para MVA/pauta/redução de base por produto ou NCM.
4. Definir rotina de atualização dos pacotes de classificação tributária e quem aprova cada alteração.

**Como treinar**

- Usar os webinars e treinamentos oficiais do Configurador de Tributos como material base da capacitação.
- Exercitar a criação de uma regra completa (tributo, vigência, entidade, produto) e a leitura do resultado na nota.
- Mostrar a diferença prática entre calcular pela TES e calcular pelo FISA170 no mesmo documento.

**Como validar (evidência de entrega)**

- Comparativo de cálculo legado x Configurador nos cenários críticos (DIFAL, ST, benefício fiscal).
- Notas de teste autorizadas com as tags de IBS/CBS corretas quando aplicável.

**Observações do projeto**

- A partir de 03/08/2026 o IBS/CBS é obrigatório: revisar se o escopo do projeto já prevê o cenário híbrido (legado + Configurador).

**Fontes no índice local**

*Para implantar / parametrizar*

- [CFGTRIB - Adequação do Configurador de Tributos aos Códigos de Classificação Tributária do IBS, CBS e IS](https://tdn.totvs.com/pages/viewpage.action?pageId=962623217) — Configurador de Tributos (TDN)
- [Escrita Fiscal - Reforma Tributária - CBS e IBS > Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como calcular IBS/CBS cClasstrib 000001 na venda Hibrida ?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36147453667095-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-calcular-IBS-CBS-cClasstrib-000001-na-venda-Hibrida) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Reforma Tributária - CBS e IBS > Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como calcular IBS/CBS cClasstrib 515001 Diferimento 100% forma Hibrida?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36628367724567-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-calcular-IBS-CBS-cClasstrib-515001-Diferimento-100-forma-Hibrida) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Reforma Tributária - CBS e IBS > Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como configurar IBS/CBS no cClasstrib 550001 de forma Hibrida?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36447138801175-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-IBS-CBS-no-cClasstrib-550001-de-forma-Hibrida) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - TOTVS Gestão Fiscal - FIS - Como calcular Suframa de forma Hibrida com cBenef ?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/40300010845975-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-TOTVS-Gest%C3%A3o-Fiscal-FIS-Como-calcular-Suframa-de-forma-Hibrida-com-cBenef) — Configurador de Tributos (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - TOTVS Gestão Fiscal - FIS - Como fazer a devolução de compra com IBS/CBS forma Hibrida?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38656780729623-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-TOTVS-Gest%C3%A3o-Fiscal-FIS-Como-fazer-a-devolu%C3%A7%C3%A3o-de-compra-com-IBS-CBS-forma-Hibrida) — Configurador de Tributos (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - TOTVS Gestão Fiscal - FIS Como fazer devolução de Saidas com calculo IBS/CBS forma Hibrida ?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38604180935447-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-TOTVS-Gest%C3%A3o-Fiscal-FIS-Como-fazer-devolu%C3%A7%C3%A3o-de-Saidas-com-calculo-IBS-CBS-forma-Hibrida) — Configurador de Tributos (Central TOTVS)
- [Escrita Fiscal - Reforma Tributária - CBS e IBS > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como configurar o cClasstrib 410 para operações Isentas no fisa170 forma Hibrida?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36312155068823-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-o-cClasstrib-410-para-opera%C3%A7%C3%B5es-Isentas-no-fisa170-forma-Hibrida) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Reforma Tributária - CBS e IBS > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como importar a tabela cClassTrib-IBS/CBS no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34662420522391-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-importar-a-tabela-cClassTrib-IBS-CBS-no-Configurador-de-Tributos) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escopo de atendimento do Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=863302293) — Fiscal - Protheus 12 (TDN)
- [🧭 Central de Conteúdo | Reforma Tributária e Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=945408020) — Referências gerais TDN (TDN)

*Suporte, FAQ e resolução de erros*

- [FAQ - Boas praticas na utilização híbrida da ferramenta Configurador de Tributos e Tes (Legado)](https://tdn.totvs.com/pages/viewpage.action?pageId=1018568875) — Fiscal - Protheus 12 (TDN)

---

## 4. Diferencial de alíquota (DIFAL)

**Status:** `concluido`  ·  **Fontes na base:** 115 candidatas, 12 selecionadas.

DIFAL de aquisição (uso/consumo e ativo imobilizado) e DIFAL EC 87/2015 para não contribuinte, com ou sem base dupla, FECP e GNRE.

**Rotinas e objetos técnicos**

- `ICMSDIFAL — Cálculo e apuração de DIFAL (EC 87/2015)`
- `SEICMS — Base dupla de ICMS diferencial de alíquota`
- `IEDIFAL — Cadastro de IE para diferencial de alíquota`
- `MV_ESTICM / FISA080 — alíquotas internas por UF`

**Como implantar**

1. Definir a matriz de DIFAL por operação: entrada de uso/consumo, entrada para ativo imobilizado, saída para não contribuinte (EC 87) e saída interestadual com FECP.
2. Configurar base simples x base dupla (conv. 52/91), redução de base e reflexos no Configurador de Tributos.
3. Configurar a geração de guia (GNRE/DIFAL) e o título financeiro correspondente, incluindo a natureza do título.
4. Cadastrar as IE de DIFAL quando houver recolhimento por operação em outra UF.

**Como treinar**

- Exercitar uma compra interestadual de uso/consumo com e sem base dupla e conferir o valor na nota e no livro fiscal.
- Mostrar onde o DIFAL aparece na apuração, na guia e no financeiro.
- Discutir os erros mais comuns: alíquota interna desatualizada, FECP não configurado, cliente contribuinte marcado errado.

**Como validar (evidência de entrega)**

- Notas de teste com DIFAL calculado e destacado conforme a UF de destino.
- Guias e títulos gerados com natureza e vencimento corretos.

**Fontes no índice local**

*Para implantar / parametrizar*

- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como calcular o Difal ec/87 base dupla no fisa170 com IBS/CBS ?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/39473914475159-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-calcular-o-Difal-ec-87-base-dupla-no-fisa170-com-IBS-CBS) — Referências gerais Central TOTVS (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como Configurar Difal da EC/87 com Base dupla no fisa170?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/14193357628823-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-Configurar-Difal-da-EC-87-com-Base-dupla-no-fisa170) — Referências gerais Central TOTVS (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como configurar Diferencial de alíquotas base dupla sem deduzir o ICMS próprio no FISA170?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/31231115455127-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-Diferencial-de-al%C3%ADquotas-base-dupla-sem-deduzir-o-ICMS-pr%C3%B3prio-no-FISA170) — Referências gerais Central TOTVS (Central TOTVS)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Como configurar o DIFAL EC/87 com FECP no FISA170 base simples?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33254267433751-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Como-configurar-o-DIFAL-EC-87-com-FECP-no-FISA170-base-simples) — Referências gerais Central TOTVS (Central TOTVS)
- [ICMS - Cálculo do DIFAL Aquisição de Mercadoria](https://tdn.totvs.com/pages/viewpage.action?pageId=567740017) — Fiscal - Protheus 12 (TDN)
- [ICMSDIFAL - Cálculo e Apuração de DIFAL conforme Emenda Constitucional 87/2015](https://tdn.totvs.com/pages/viewpage.action?pageId=699815598) — Fiscal - Protheus 12 (TDN)
- [ICMSST Base dupla de ICMS-ST recolhida por diferencial de alíquota](https://tdn.totvs.com/pages/viewpage.action?pageId=517127259) — Fiscal - Protheus 12 (TDN)
- [IEDIFAL - Cadastro de Inscrição Estadual para Diferencial de Alíquota](https://tdn.totvs.com/pages/viewpage.action?pageId=695190614) — Fiscal - Protheus 12 (TDN)
- [Escrita Fiscal - Impostos - ICMS - ICMS ST > MP - FIS - Como Configurar uma Saída de Difal ICMS ST para Contribuinte com Base Dupla ?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360023833311-MP-FIS-Como-Configurar-uma-Sa%C3%ADda-de-Difal-ICMS-ST-para-Contribuinte-com-Base-Dupla) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [SEICMS - Cálculo de Base Dupla de ICMS Diferencial de Alíquota](https://tdn.totvs.com/pages/viewpage.action?pageId=699818895) — Fiscal - Protheus 12 (TDN)

*Para treinar (conceito, guia e material oficial)*

- [MV_UNIFST - Geração de guia de ICMS ST e FECP (GNRE) unificada](https://tdn.totvs.com/pages/viewpage.action?pageId=1104710810) — Fiscal - Protheus 12 (TDN)

*Suporte, FAQ e resolução de erros*

- [FAQ - Como funciona o campo GNRE DIFAL F2_GNRDIF?](https://tdn.totvs.com/pages/viewpage.action?pageId=733199209) — Fiscal - Protheus 12 (TDN)

---

## 5. Apuração de impostos

**Status:** `concluido`  ·  **Fontes na base:** 94 candidatas, 14 selecionadas.

Apurações de ICMS, IPI, ISS, PIS/COFINS e ST: fechamento do período, geração de guias e títulos, contabilização e conferência contra os livros fiscais.

**Rotinas e objetos técnicos**

- `MATA953 — Apuração de ICMS (APUICM)`
- `Apuração de IPI (APUIPI) e MATR943 — Registro de apuração do IPI`
- `APUISS — Apuração de ISS`
- `APURESST / FISA302 — Ressarcimento ou complemento de ICMS-ST`
- `FISA001 — Apuração EFD Contribuições`
- `MATA930 — Reprocessamento dos livros fiscais`

**Como implantar**

1. Definir a ordem de fechamento: livros fiscais -> acertos -> apuração -> guias/títulos -> contabilização -> SPED.
2. Configurar regime de apuração, períodos, filiais centralizadoras e parâmetros de cada imposto.
3. Cadastrar os lançamentos padrão (LANPAD) para contabilização das apurações.
4. Configurar geração de guias e títulos (naturezas, códigos de recolhimento, datas de vencimento por UF).

**Como treinar**

- Executar uma apuração completa em ambiente de treino e conferir os valores contra MATR930/MATRAPR.
- Mostrar reprocessamento, estorno e bloqueio de reprocessamento (PROCAPUR).
- Explicar a leitura das abas de outros créditos/outros débitos e como justificar cada ajuste.

**Como validar (evidência de entrega)**

- Apuração do período fechada sem divergência entre livro, apuração e contabilidade.
- Guias e títulos gerados e conferidos pelo cliente.

**Fontes no índice local**

*Para implantar / parametrizar*

- [APUICM - Apuração de ICMS - MATA953 - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=270894388) — Fiscal - Protheus 12 (TDN)
- [APUIPI - Apuração de IPI - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=270093976) — Fiscal - Protheus 12 (TDN)
- [APUISS - Apuração de ISS](https://tdn.totvs.com/pages/viewpage.action?pageId=654295834) — Fiscal - Protheus 12 (TDN)
- [APUISSBLB - Apuração de ISS - EFD ICMS/IPI - Bloco B](https://tdn.totvs.com/pages/viewpage.action?pageId=500292737) — Fiscal - Protheus 12 (TDN)
- [Apurações - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=627111872) — Fiscal - Protheus 12 (TDN)
- [Escrita Fiscal - Impostos - ICMS - Apuração > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS- Coluna código de lançamento não é exibida na apuração de ICMS(MATA953)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360024706793-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Coluna-c%C3%B3digo-de-lan%C3%A7amento-n%C3%A3o-%C3%A9-exibida-na-apura%C3%A7%C3%A3o-de-ICMS-MATA953) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Impostos - ICMS - Apuração > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS- Como gerar o relatório Registro de Apuração do ICMS P9 (MATR940) de forma anual](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360027673011-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-gerar-o-relat%C3%B3rio-Registro-de-Apura%C3%A7%C3%A3o-do-ICMS-P9-MATR940-de-forma-anual) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Impostos - ICMS - Apuração > MP - FIS - MATA953 - Conferência dos códigos de ajuste na apuração de ICMS](https://centraldeatendimento.totvs.com/hc/pt-br/articles/1500012793801-MP-FIS-MATA953-Confer%C3%AAncia-dos-c%C3%B3digos-de-ajuste-na-apura%C3%A7%C3%A3o-de-ICMS) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Novas Apurações](https://tdn.totvs.com/pages/viewpage.action?pageId=991865200) — Fiscal - Protheus 12 (TDN)
- [RESUMEF3 - Apuração do ICMS, ISS e IPI através de Multi-Thread](https://tdn.totvs.com/pages/viewpage.action?pageId=706120371) — Fiscal - Protheus 12 (TDN)

*Para treinar (conceito, guia e material oficial)*

- [Escrita Fiscal - Impostos - ICMS - ICMS ST > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Conceito da pergunta "Imprime Crédito ST" na Apuração de ICMS (MATA953)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360020388031-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Conceito-da-pergunta-Imprime-Cr%C3%A9dito-ST-na-Apura%C3%A7%C3%A3o-de-ICMS-MATA953) — Escrituração e Relatórios Fiscal (Central TOTVS)

*Pontos de entrada e customizações (ADVPL)*

- [PE - CPAPUICMS - Atualiza campos de Títulos a Pagar na Apuração de ICMS](https://tdn.totvs.com/pages/viewpage.action?pageId=655875804) — Fiscal - Protheus 12 (TDN)
- [PE-MATR941 - Registro de apuração do ICMS](https://tdn.totvs.com/pages/viewpage.action?pageId=793212524) — Fiscal - Protheus 12 (TDN)

*Suporte, FAQ e resolução de erros*

- [Escrita Fiscal - Impostos - ICMS - Apuração > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS- Código de lançamento inválido ao inserir código de ajuste na Apuração do ICMS (MATA953)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360018836892-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-C%C3%B3digo-de-lan%C3%A7amento-inv%C3%A1lido-ao-inserir-c%C3%B3digo-de-ajuste-na-Apura%C3%A7%C3%A3o-do-ICMS-MATA953) — Escrituração e Relatórios Fiscal (Central TOTVS)

---

## 6. Impostos retidos (PCC, IRRF, INSS, ISS)

**Status:** `concluido`  ·  **Fontes na base:** 38 candidatas, 16 selecionadas.

Retenções na entrada e na saída, geração de títulos de imposto, cumulatividade do PCC e obrigações acessórias (DIRF/DCTFWeb).

**Rotinas e objetos técnicos**

- `PARÂMETROS - PIS-COFINS-CSLL / ISS / IRRF / INSS`
- `MV_BX10925, MV_VCPCCP, MV_VL13137, MV_PISNAT/MV_COFINS/MV_CSLL`
- `Configurador de Tributos — Regras Financeiras (FISA170)`
- `FINA378/FINA381 — Aglutinação de títulos de PIS/COFINS/CSLL`

**Como implantar**

1. Definir o momento da retenção (na emissão ou na baixa do título) por imposto e por tipo de operação.
2. Configurar naturezas financeiras de imposto, valores mínimos de retenção e cumulatividade do PCC.
3. Configurar as regras financeiras no Configurador de Tributos: vigência, tipo de entidade, fator gerador e "data base para vencimento do imposto".
4. Ajustar cadastros de clientes/fornecedores (rec. PIS/COFINS/CSLL/ISS, órgão público, MEI, autônomo).

**Como treinar**

- Exercitar uma nota de entrada de serviço com retenção de PCC e IRRF e acompanhar o título gerado no financeiro.
- Mostrar a diferença entre retenção na emissão e na baixa, e o efeito na cumulatividade.
- Revisar o roteiro oficial de cálculo e apuração de PIS/COFINS/CSLL com o time.

**Como validar (evidência de entrega)**

- Títulos de imposto com natureza, valor e data de vencimento conferidos pelo cliente.
- DIRF/DCTFWeb alimentados corretamente a partir das retenções.

**Observações do projeto**

- PENDÊNCIA REPORTADA: PCC gerando data de vencimento incorreta. Tratar como item de revisão de parametrização: a data de vencimento do PCC depende do momento da retenção (MV_BX10925), da data considerada para cumulatividade (MV_VCPCCP: 1=Emissão, 2=Venc. Real, 3=Dt. Contábil), do valor mínimo (MV_VL13137 = R$ 10,00) e, no Configurador de Tributos, da "Data base p/ vencto. do imposto (Emissão)" e da "Data Cumulat" da regra financeira. Pela Lei 13.137/15 o vencimento é no segundo decêndio do mês subsequente ao fato gerador.
- Se a aglutinação de títulos estiver em uso, verificar se é FINA378 (aglutina por data de EMISSÃO) ou FINA381 (por data de VENCIMENTO).

**Fontes no índice local**

*Para implantar / parametrizar*

- [Configurações - INSS - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=654102732) — Fiscal - Protheus 12 (TDN)
- [Configurações - IRRF - Fiscal - P12](https://tdn.totvs.com/pages/viewpage.action?pageId=653143855) — Fiscal - Protheus 12 (TDN)
- [Financeiro - Cadastros > Cross Segmentos - Backoffice Linha Protheus - SIGAFIN - Natureza utilizada nos titulos de retenção de impostos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/39270216649495-Cross-Segmentos-Backoffice-Linha-Protheus-SIGAFIN-Natureza-utilizada-nos-titulos-de-reten%C3%A7%C3%A3o-de-impostos) — Financeiro (Central TOTVS)
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como habilitar a opção Modalidade de retenção do PIS, COFINS e CSLL localizado na aba Duplicatas na rotina MATA103 - Documento de Entrada?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4409524481047-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-habilitar-a-op%C3%A7%C3%A3o-Modalidade-de-reten%C3%A7%C3%A3o-do-PIS-COFINS-e-CSLL-localizado-na-aba-Duplicatas-na-rotina-MATA103-Documento-de-Entrada) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [Escrita Fiscal - Impostos - Cálculos > CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Cumulatividade do INSS](https://centraldeatendimento.totvs.com/hc/pt-br/articles/4411045344919-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Cumulatividade-do-INSS) — Escrituração e Relatórios Fiscal (Central TOTVS)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 – Como calcular PIS/COFINS/CSLL retenção utilizando o Configurador de Tributos para notas de entrada e saída.](https://centraldeatendimento.totvs.com/hc/pt-br/articles/28271950709399-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-calcular-PIS-COFINS-CSLL-reten%C3%A7%C3%A3o-utilizando-o-Configurador-de-Tributos-para-notas-de-entrada-e-sa%C3%ADda) — Configurador de Tributos (Central TOTVS)
- [Impostos Retidos (trilha fiscal) - Configurador de Tributos - Regras Financeiras (data base para vencimento do imposto e cumulatividade)](https://tdn.totvs.com/display/public/PROT/Configurador+de+Tributos+-+Regras+Financeiras) — Trilha Fiscal — Complementos (TDN) · complemento da trilha
- [Impostos Retidos (trilha fiscal) - MP - FIS - Cumulatividade PIS, COFINS e CSLL (Lei 13.137/15 e vencimento no 2º decêndio)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360053516414-MP-FIS-Cumulatividade-Pis-Cofins-e-CSLL) — Trilha Fiscal — Complementos (Central TOTVS) · complemento da trilha
- [Impostos Retidos (trilha fiscal) - MP - FIS - Retenção de PIS, COFINS e CSLL (MV_BX10925, MV_VCPCCP, MV_VL13137, MV_PISNAT)](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360056887693-MP-FIS-Reten%C3%A7%C3%A3o-de-PIS-COFINS-e-CSLL) — Trilha Fiscal — Complementos (Central TOTVS) · complemento da trilha
- [Impostos Retidos (trilha fiscal) - Roteiro Proc. Cálc. Retenção e Ap. PIS/Cofins/CSLL (SIGAFAT)](https://tdn.totvs.com/pages/releaseview.action?pageId=312163918) — Faturamento (TDN) · complemento da trilha
- [Impostos Retidos (trilha fiscal) - SIGAFIN - FINA378 - É possível aglutinar títulos dos impostos PIS/COFINS/CSLL pela data de vencimento?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/360022030252-Cross-Segmento-Backoffice-Linha-Protheus-SIGAFIN-FINA378-%C3%89-poss%C3%ADvel-aglutinar-t%C3%ADtulos-dos-impostos-PIS-COFINS-CSLL-pela-data-de-vencimento) — Financeiro (Central TOTVS) · complemento da trilha
- [INSS - Configurações para Retenção de INSS](https://tdn.totvs.com/pages/viewpage.action?pageId=697252452) — Fiscal - Protheus 12 (TDN)
- [IRRF - Retenção de Imposto de Renda Pessoa Jurídica ou Física](https://tdn.totvs.com/pages/viewpage.action?pageId=531009057) — Fiscal - Protheus 12 (TDN)
- [PARÂMETROS - PIS-COFINS-CSLL - Como configurar os parâmetros para Operações Fiscais](https://tdn.totvs.com/pages/viewpage.action?pageId=701693213) — Fiscal - Protheus 12 (TDN)
- [PCORGPUB - Retenção Diferenciada de PIS e COFINS para Órgão Público](https://tdn.totvs.com/pages/viewpage.action?pageId=697251410) — Fiscal - Protheus 12 (TDN)

*Pontos de entrada e customizações (ADVPL)*

- [PE - VLCODRET - Valida código de retenção dos impostos da DIRF](https://tdn.totvs.com/pages/viewpage.action?pageId=655865917) — Fiscal - Protheus 12 (TDN)

---
