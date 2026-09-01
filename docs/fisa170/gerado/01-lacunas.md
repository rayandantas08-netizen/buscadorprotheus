# Lacunas do levantamento (roteiro de perguntas)

Ordem sugerida: resolver todos os bloqueios por operação antes de abrir o cadastro no FISA170.

## DEM-001 — Remessa de mercadoria para demonstração (SP)

**Bloqueios**

- `cfop_retorno`: Operação de remessa/devolução sem CFOP de retorno mapeado → **Qual o CFOP de retorno e em quantos dias o retorno precisa ocorrer? O retorno usa o mesmo cBenef?**
- `perfil_operacao`: Modo `hibrido` exige `Perfil tributário de operação` antes de a regra funcionar no documento → **F23/F26 - chave CFOP + tipo de documento**
- `regra_aliquota`: Modo `hibrido` exige `Regra de alíquota (F28)` antes de a regra funcionar no documento → **ex.: I:ALIQ_NCM**
- `regra_base`: Modo `hibrido` exige `Regra de base de cálculo (F27)` antes de a regra funcionar no documento → **ex.: O:VAL_MERCADORIA**
- `regra_tributaria`: Modo `hibrido` exige `Regra tributária do documento fiscal (F2B)` antes de a regra funcionar no documento → **código numérico da regra, ex.: 000403**

**Pontos de atenção**

- `mensagem_dfe`: Benefício fiscal sem mensagem/dado adicional → **A legislação do benefício exige informação complementar no documento (ex.: número do processo, 'ICMS diferido')?**

## DEM-002 — Remessa de mercadoria para demonstração (interestadual a partir de SP)

**Bloqueios**

- `cbene`: CST ICMS 50 indica benefício e SP exige o cBenef na NF-e → **Qual código da Tabela cBenef da SEFAZ-SP corresponde exatamente a esta operação?**
- `cfop_retorno`: Operação de remessa/devolução sem CFOP de retorno mapeado → **Qual o CFOP de retorno e em quantos dias o retorno precisa ocorrer? O retorno usa o mesmo cBenef?**
- `perfil_operacao`: Modo `hibrido` exige `Perfil tributário de operação` antes de a regra funcionar no documento → **F23/F26 - chave CFOP + tipo de documento**
- `regra_aliquota`: Modo `hibrido` exige `Regra de alíquota (F28)` antes de a regra funcionar no documento → **ex.: I:ALIQ_NCM**
- `regra_base`: Modo `hibrido` exige `Regra de base de cálculo (F27)` antes de a regra funcionar no documento → **ex.: O:VAL_MERCADORIA**
- `regra_tributaria`: Modo `hibrido` exige `Regra tributária do documento fiscal (F2B)` antes de a regra funcionar no documento → **código numérico da regra, ex.: 000403**

**Pontos de atenção**

- `base_legal`: Benefício informado sem fundamento legal → **Qual artigo/convênio sustenta a suspensão ou o diferimento? (vira regra de ajuste de lançamento e mensagem no documento)**
- `tes_campos_ativeis`: Modo híbrido sem definição do que ainda é decidido pela TES → **Quais campos da TES continuam ativos para esta operação? (ver lista de campos remanescentes/descontinuados no TDN)**
