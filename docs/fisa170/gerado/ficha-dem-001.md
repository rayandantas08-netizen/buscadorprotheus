# Ficha DEM-001 — Remessa de mercadoria para demonstração (SP)

> Gerada por `scripts/gerar_pacote_fisa170.py`. Editar apenas a matriz em `docs/fisa170/modelos/matriz-operacoes.csv`.

## Diagnóstico do levantamento

- Status: `levantada` · dono: a definir
- **Bloqueios**: 5 · **Pontos de atenção**: 1

### Bloqueios (a regra não deve ser cadastrada sem isso)

- [ ] `cfop_retorno` — Operação de remessa/devolução sem CFOP de retorno mapeado. **Perguntar:** Qual o CFOP de retorno e em quantos dias o retorno precisa ocorrer? O retorno usa o mesmo cBenef?
- [ ] `perfil_operacao` — Modo `hibrido` exige `Perfil tributário de operação` antes de a regra funcionar no documento. **Perguntar:** F23/F26 - chave CFOP + tipo de documento
- [ ] `regra_aliquota` — Modo `hibrido` exige `Regra de alíquota (F28)` antes de a regra funcionar no documento. **Perguntar:** ex.: I:ALIQ_NCM
- [ ] `regra_base` — Modo `hibrido` exige `Regra de base de cálculo (F27)` antes de a regra funcionar no documento. **Perguntar:** ex.: O:VAL_MERCADORIA
- [ ] `regra_tributaria` — Modo `hibrido` exige `Regra tributária do documento fiscal (F2B)` antes de a regra funcionar no documento. **Perguntar:** código numérico da regra, ex.: 000403

### Pontos de atenção

- [ ] `mensagem_dfe` — Benefício fiscal sem mensagem/dado adicional. **Perguntar:** A legislação do benefício exige informação complementar no documento (ex.: número do processo, 'ICMS diferido')?

### Riscos identificados automaticamente

- `410999` é o código residual de não incidência. Use apenas se nenhum código específico descrever a operação; a escolha errada distorce a apuração.

### Dúvidas abertas pelo cliente

- CFOP de retorno (5913); tratamento da transmissão da propriedade; cBenef do retorno; IBS/CBS é suspensão (550) ou não incidência (410)?

| Bloco | Campo | Valor informado |
| --- | --- | --- |
| 1. Identificação | `cod_operacao` (Código da operação) | DEM-001 |
| 1. Identificação | `nome_operacao` (Descrição para o negócio) | Remessa de mercadoria para demonstração (SP) |
| 1. Identificação | `grupo_operacao` (Grupo da operação) | demonstracao |
| 1. Identificação | `sentido` (Sentido) | saida |
| 1. Identificação | `ambito` (Abrangência) | interna |
| 1. Identificação | `uf_origem` (UF do estabelecimento emitente) | SP |
| 1. Identificação | `uf_destino` (UF do destinatário/remetente) | SP |
| 1. Identificação | `documento` (Documento fiscal) | NF-e |
| 1. Identificação | `finalidade` (Finalidade do documento) | simbolica |
| 1. Identificação | `mod_protheus` (Módulo/gatilho no Protheus) | faturamento |
| 1. Identificação | `vigencia_inicio` (Vigência - início) | 2026-01-01 |
| 1. Identificação | `base_legal` (Fundamento legal do tratamento) | Suspensão na saída para demonstração - confirmar artigo do RICMS/SP e Ajuste SINIEF aplicável |
| 1. Identificação | `responsavel` (Dono da informação no cliente) | a definir |
| 1. Identificação | `status` (Status do atendimento) | levantada |
| 2. Aplicação | `produtos_aplicavel` (Recorte de produtos) | todos |
| 2. Aplicação | `origem_mercadoria` (Origem da mercadoria no produto (B1_ORIGEM)) | 0 |
| 2. Aplicação | `participantes_aplicavel` (Recorte de participantes) | clientes contribuintes e não contribuintes |
| 2. Aplicação | `destinatario_contribuinte` (Destinatário é contribuinte de ICMS?) | indiferente |
| 2. Aplicação | `finalidade_item` (Finalidade/destino do item) | demonstração |
| 3. ICMS | `cfop_saida` (CFOP de saída) | 5912 |
| 3. ICMS | `icms_origem` (CST ICMS - origem (1º dígito)) | 5 |
| 3. ICMS | `icms_cst` (CST ICMS - situação (2º/3º dígitos)) | 50 |
| 3. ICMS | `icms_credito` (A operação gera crédito de ICMS na entrada?) | nao |
| 4. IPI | `ipi_cst` (CST IPI) | 53 |
| 5. PIS/COFINS | `pis_cst` (CST PIS) | 49 |
| 5. PIS/COFINS | `cofins_cst` (CST COFINS) | 49 |
| 5. PIS/COFINS | `pis_cofins_regime` (Regime PIS/COFINS) | confirmar (cumulativo/não cumulativo) |
| 5. PIS/COFINS | `pis_cofins_credito` (Gera crédito de PIS/COFINS?) | nao |
| 6. IBS/CBS (Reforma) | `ibs_cst` (CST IBS/CBS) | 410 |
| 6. IBS/CBS (Reforma) | `cclasstrib` (cClassTrib) | 410999 |
| 7. Benefício fiscal | `tipo_beneficio` (Natureza do benefício) | suspensao |
| 7. Benefício fiscal | `cbene` (cBenef da saída) | SP053190 |
| 7. Benefício fiscal | `benef_descricao` (Descrição do benefício para o documento) | Suspensão - Saída de mercadoria remetida para demonstração, inclusive com destino a consumidor ou usuário final, até o momento em que ocorrer a transmissão de sua propriedade |
| 7. Benefício fiscal | `benef_vigencia` (Vigência do benefício na Tabela 52) | 2026-01-01 |
| 9. No Protheus | `tes` (TES (SF1)) | 704 |
| 9. No Protheus | `modo_calculo` (Motor de cálculo) | hibrido |
| 9. No Protheus | `tes_campos_ativeis` (Campos que permanecem na TES) | CFOP, cálculo de ICMS/PIS/COFINS e flag de IBS/CBS zerado - validar contra a lista de campos remanescentes |
| 10. Escrita e DFe | `livro_fiscal` (Coluna no livro fiscal) | Outros |
| 10. Escrita e DFe | `incidencia` (Incidência na Regra de Escrituração (CJ2)) | Outros |
| 10. Escrita e DFe | `diferimento_pct` (% de diferimento/suspensão na escrita) | suspensão integral - sem débito de ICMS |
| 10. Escrita e DFe | `registros_sped` (Registros SPED exigidos) | C100/C170 (confirmar C190/C195 para o ajuste) |
| 10. Escrita e DFe | `codigo_ajuste` (Código de ajuste/ CAT) | confirmar se a SEFAZ-SP exige ajuste específico para a suspensão |
| 10. Escrita e DFe | `reflete_em` (Reflexo entre tributos) | nenhum |
| 10. Escrita e DFe | `contabilizacao` (Contabilização dos tributos genéricos) | sem efeito no resultado (imposto não debitado) |
| 11. Governança | `aprovacao_regra` (Regra passa por aprovação?) | sim |
| 11. Governança | `evidencias` (Evidências de aceite) | pendiente |
| 11. Governança | `duvidas_abertas` (Dúvidas abertas) | CFOP de retorno (5913); tratamento da transmissão da propriedade; cBenef do retorno; IBS/CBS é suspensão (550) ou não incidência (410)? |
| 11. Governança | `observacoes` (Observações do consultor) | Operação sem deslocamento tributário: não gera débito de ICMS, mas precisa escrever corretamente no livro e no DFe. |

## O que é preciso criar no Configurador de Tributos

### 1. Confirmar o cenário de cálculo (TES x FISA170 x híbrido)
- Motor declarado: `hibrido`.
- Validar quais impostos desta operação o FISA170 passa a calcular e quais campos continuam na TES.
- Confirmar versão/atualização do dicionário e do motor de cálculo antes de cadastrar regra.

**Fontes TOTVS:**
- [CFGTRIB - Campos da TES](https://tdn.totvs.com/pages/viewpage.action?pageId=943126076)
- [CFGTRIB - Campos do cadastro de Tipos de Entrada e Saída descontinuados em favor do Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=906853167)
- [CFGTRIB - Campos que Permanecem no TES ( 🚧documentação em construção )](https://tdn.totvs.com/pages/viewpage.action?pageId=928965724)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - A TES Inteligente irá permanecer com a implantação do Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35554255260439-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-A-TES-Inteligente-ir%C3%A1-permanecer-com-a-implanta%C3%A7%C3%A3o-do-Configurador-de-Tributos)
- [Cross Segmentos - Backoffice Protheus - FIS - Escrita Fiscal - Dicionário desatualizado, favor verificar atualizações do motor de cálculo fiscal](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36699322874263-Cross-Segmentos-Backoffice-Protheus-FIS-Escrita-Fiscal-Dicion%C3%A1rio-desatualizado-favor-verificar-atualiza%C3%A7%C3%B5es-do-motor-de-c%C3%A1lculo-fiscal)

### 2. Cadastrar tributos e tabelas auxiliares
- Garantir que ICMS, IPI, PIS, COFINS, IBSEST e CBSFED existem e estão ativos no cadastro de tributos.
- Importar/atualizar a tabela cClassTrib do IBS/CBS.
- Manter os códigos de benefício na rotina de catálogo exigida pelo FISA170 (em SP, a Tabela 52 via FISA156).

**Fontes TOTVS:**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como realizar carga automática dos Tributos CBS e IBS no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/33147484988823-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-realizar-carga-autom%C3%A1tica-dos-Tributos-CBS-e-IBS-no-Configurador-de-Tributos)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Como importar a tabela cClassTrib-IBS/CBS no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34662420522391-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Como-importar-a-tabela-cClassTrib-IBS-CBS-no-Configurador-de-Tributos)
- [CFGTRIB - Ajustes de Lançamento no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=822223872)

### 3. Perfis (produto, participante, origem x destino, operação)
- Perfil de operação a partir do CFOP `5912` e do documento `NF-e`.
- Recorte de produtos: todos.
- Recorte de participantes: clientes contribuintes e não contribuintes.
- Usar o facilitador de cadastro para popular produto/participante e evitar perfil órfão.

**Fontes TOTVS:**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Como utilizar o Facilitador de cadastro no perfil de produtos e participante no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34824467940247-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-utilizar-o-Facilitador-de-cadastro-no-perfil-de-produtos-e-participante-no-Configurador-de-Tributos)
- [CFGTRIB - Perfil de Operação - Política do Tributo para Documentos que possuem vínculos com o Documentos de Origem](https://tdn.totvs.com/pages/viewpage.action?pageId=1070065237)
- [CFGTRIB - Boas Práticas - Guia de Utilização do Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=825324804)

### 4. Regras de cálculo (base, alíquota, NCM, reflexo)
- Definir regra de base e de alíquota para cada tributo que o FISA170 vai calcular.

**Fontes TOTVS:**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - Como garantir o cálculo correto do tributo na nota fiscal utilizando a Regra de Cálculo no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35041323516183-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-garantir-o-c%C3%A1lculo-correto-do-tributo-na-nota-fiscal-utilizando-a-Regra-de-C%C3%A1lculo-no-Configurador-de-Tributos)
- [CFGTRIB - Regras por NCM](https://tdn.totvs.com/pages/viewpage.action?pageId=942052690)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Como configurar as regras dos impostos quando um imposto influencia o cálculo de outro?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/26438476614935-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-configurar-as-regras-dos-impostos-quando-um-imposto-influencia-o-c%C3%A1lculo-de-outro)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - Quantas majorações posso incluir em outro tributo no Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/34371268913303-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-Quantas-majora%C3%A7%C3%B5es-posso-incluir-em-outro-tributo-no-Configurador-de-Tributos)

### 5. Regra de escrituração (define livro, CST e apuração)
- Incidência: `Outros`; livro fiscal: `Outros`.
- CST ICMS: origem `5` + situação `50` (CST de 3 dígitos do XML: `550`); CST IPI `53`; PIS/COFINS `49` / `49`.
- IBS/CBS: CST `410` + cClassTrib `410999`.
- Percentual de diferimento/suspensão na escrita: `suspensão integral - sem débito de ICMS`.
- Código de ajuste/registro SPED: `confirmar se a SEFAZ-SP exige ajuste específico para a suspensão` / `C100/C170 (confirmar C190/C195 para o ajuste)`.

**Fontes TOTVS:**
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Tratativa do Campo Incidência da Regra de Escrituração sobre operação de redução](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35360344325527-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Tratativa-do-Campo-Incid%C3%AAncia-da-Regra-de-Escritura%C3%A7%C3%A3o-sobre-opera%C3%A7%C3%A3o-de-redu%C3%A7%C3%A3o)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Compartilhamento de Tabelas de Perfis, Regras de Cálculo e Regra de Escrituração](https://centraldeatendimento.totvs.com/hc/pt-br/articles/36181199260183-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Compartilhamento-de-Tabelas-de-Perfis-Regras-de-C%C3%A1lculo-e-Regra-de-Escritura%C3%A7%C3%A3o)
- [CFGTRIB - Lançamento CAT 66/2018](https://tdn.totvs.com/pages/viewpage.action?pageId=822223908)

### 6. Benefício fiscal, cBenef e mensagens
- Criação da regra de ajuste de lançamento com código `SP053190` (tabela de benefícios), vigência `2026-01-01` e a regra tributária correspondente.
- Texto do documento: Suspensão - Saída de mercadoria remetida para demonstração, inclusive com destino a consumidor ou usuário final, até o momento em que ocorrer a transmissão de sua propriedade.

**Fontes TOTVS:**
- [CFGTRIB - Ajustes de Lançamento no Configurador de Tributos](https://tdn.totvs.com/pages/viewpage.action?pageId=822223872)
- [CFGTRIB - Cadastro de Mensagens no Documento Fiscal](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Cadastro+de+Mensagens+no+Documento+Fiscal)
- [CFGTRIB - Dados Adicionais](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Dados+Adicionais)

### 7. TES e amarração com o módulo de origem
- TES `704` no módulo `faturamento`.
- Campos ativos na TES: CFOP, cálculo de ICMS/PIS/COFINS e flag de IBS/CBS zerado - validar contra a lista de campos remanescentes
- Confirmar TES inteligente x regra do FISA170 e o que persiste em C5_RECISS/A1_RECISS quando for serviço.

**Fontes TOTVS:**
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - A TES Inteligente irá permanecer com a implantação do Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35554255260439-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-A-TES-Inteligente-ir%C3%A1-permanecer-com-a-implanta%C3%A7%C3%A3o-do-Configurador-de-Tributos)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – Com a utilização do Configurador de Tributos, os campos C5_RECISS e A1_RECISS são utilizados?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35033655429399-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Com-a-utiliza%C3%A7%C3%A3o-do-Configurador-de-Tributos-os-campos-C5-RECISS-e-A1-RECISS-s%C3%A3o-utilizados)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS – FISA170 - Como incluir o Configurador de Tributos no menu?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35445470588823-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Como-incluir-o-Configurador-de-Tributos-no-menu)

### 8. Validação, aprovação e publish
- Simular a operação no simulador do FISA170 e comparar com o cálculo atual (legado).
- Emitir nota em homologação e conferir as tags do XML: ICMS, IPI, PIS/COFINS e o grupo de IBS/CBS (CST + cClassTrib).
- Conferir gravação em CJ3 (escrituração por item), F2D (tributos genéricos), SFT/SF3 e o código de regra no documento (F2B_REGRA).
- Validar livro fiscal, apuração do período e contabilização dos tributos.
- Submeter a regra ao mecanismo de aprovação e registrar a vigência.
- Validar a geração do grupo de IBS/CBS no XML: quando o tributo não é calculado, o grupo zerado provoca rejeição (ver o parâmetro que controla a geração do grupo no XML).

**Fontes TOTVS:**
- [CFGTRIB - Simulador de Operação](https://tdn.totvs.com/pages/viewpage.action?pageId=877863294)
- [CFGTRIB - Simulador Comparativo](https://tdn.totvs.com/display/PROT/CFGTRIB+-+Simulador+Comparativo)
- [Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS - FISA170 - Quais tabelas fazem parte do Configurador de Tributos?](https://centraldeatendimento.totvs.com/hc/pt-br/articles/35314721022103-Cross-Segmento-TOTVS-Backoffice-Linha-Protheus-FIS-FISA170-Quais-tabelas-fazem-parte-do-Configurador-de-Tributos)
- [CROSS Segmentos - TOTVS Backoffice Linha Protheus - FIS - Relacionamento entre tabelas SD1/SD2, SFT, CJ3 e F2D no Configurador de Tributos](https://centraldeatendimento.totvs.com/hc/pt-br/articles/38741160434199-CROSS-Segmentos-TOTVS-Backoffice-Linha-Protheus-FIS-Relacionamento-entre-tabelas-SD1-SD2-SFT-CJ3-e-F2D-no-Configurador-de-Tributos)
- [CFGTRIB - Mecanismo de aprovação de regra](https://tdn.totvs.com/pages/viewpage.action?pageId=942068847)
