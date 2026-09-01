# Caso concreto — remessa para demonstração com suspensão em SP

Linha `DEM-001` da matriz. Serve de referência para as outras operações porque reúne os sete campos que
o fiscal sempre entrega e expõe exatamente onde eles não bastam.

| Dado informado | Leitura |
| --- | --- |
| CFOP 5.912 / 6.912 | Remessa de mercadoria ou bem para **demonstração** (interna / interestadual) |
| CST ICMS 50 | Saída com **lançamento suspenso** — sem destaque de ICMS. Na tabela de CST de ICMS, 50 = suspensão e 51 = diferimento |
| CST IPI 53 | **Saída não tributada** de IPI |
| CST PIS/COFINS 49 | **Outras operações de saída** (não é "operação não tributada") |
| IBS/CBS 410 → 410999 | Imunidade e não incidência, código residual para **operação não onerosa** |
| cBenef SP053190 | Suspensão – saída de mercadoria remetida para demonstração, inclusive com destino a consumidor ou usuário final, até o momento em que ocorrer a transmissão de sua propriedade |
| TES 704 | Gatilho da operação no módulo de origem |

> As descrições de CFOP, cBenef, CST de IPI/PIS/COFINS e cClassTrib foram conferidas em fontes oficiais e
> na tabela cBenef da SEFAZ-SP em 2026-09-01. **Não** são informação do TDN: revalide antes de configurar,
> principalmente o código do retorno e o enquadramento de IBS/CBS.

Atenção ao vocabulário: o par `410 / 410999` foi anotado como "operação não tributada", mas na tabela
oficial o `410` é **imunidade e não incidência** e o `410999` é o **residual** de operações não onerosas sem
previsão de tributação. Remessa para demonstração é operação não onerosa, então o enquadramento em 410 faz
sentido; se o entendimento do fiscal for de *suspensão*, o grupo correto é o `550` e o código muda — é a
pergunta que está na seção 3. Padronize a descrição na planilha do cliente: regra cadastrada com rótulo
errado depois vira discussão sobre o que foi combinado.

## 1. A operação não é uma, é um ciclo

| # | Movimento | CFOP de saída do remetente | CFOP de entrada do destinatário | Status na matriz |
| --- | --- | --- | --- | --- |
| 1 | Envio para demonstração | 5.912 (SP→SP) / 6.912 (SP→fora) | 1.912 / 2.912 | levantado (DEM-001, DEM-002) |
| 2 | Retorno da mercadoria | 5.913 / 6.913 | 1.913 / 2.913 | **faltando** |
| 3 | Transmissão da propriedade (venda ao portador/representante) | a definir (tipicamente CFOP de venda) | idem | **faltando** |
| 4 | Retorno simbólico após a venda | a definir | idem | **faltando** |

Se a linha 1 sai com o imposto suspenso, as linhas 2 a 4 têm de ser configuradas juntas: é a saída da
demonstração que fecha (ou não) o imposto. Levantar só o envio deixa o cliente com a nota de retorno sem
regra — o sintoma clássico é o retorno sair tributando de novo.

## 2. Padrão de configuração equivalente publicado pela TOTVS

O artigo "Cross Segmento - TOTVS Backoffice (Linha Protheus) - FIS Como configurar o ICMS diferido 100% e
gerar cBenef para SP?" (`centraldeatendimento.totvs.com/hc/pt-br/articles/38777174413463`) descreve o mesmo
formato de solução — imposto não destacado + cBenef paulista. A sequência usada lá, que serve de esqueleto:

1. **Cadastro de produto**: origem informada (ex.: `Origem = 0`).
2. **TES**: CFOP definido na TES (no artigo, 5101; aqui, 5912/6912 na TES 704).
3. **ID dos tributos** que entram no cálculo do documento (ICMS; no nosso caso também IPI, PIS, COFINS e os
   códigos de IBS/CBS se o configurador for calcular).
4. **Regra por NCM** quando a alíquota depende de NCM e UF (no artigo: NCM `39232910`, SP→SP, 18%).
5. **Regra de base de cálculo**: `O:VAL_MERCADORIA`.
6. **Regra de alíquota**: `I:ALIQ_NCM`.
7. **Regra de escrituração**: Incidência = `Outros`, `Diferimento = 100`, `CST = 51` — para o nosso caso,
   suspensão, o CST informado é `50`; confirme na tela da sua release o campo/código que expressa a
   suspensão e se ela precisa de percentual.
8. **Regra de cálculo do documento fiscal**: código da regra tributária (no artigo, `000403`).
9. **Regra de ajuste de lançamento**: código do benefício na **tabela 52** (`SP053600` no artigo;
   `SP053190` aqui), com **data de início** e a mesma regra tributária do item 8.
10. **Mensagem** no documento fiscal, quando exigida.

Passo crítico, confirmado no artigo: *"o código precisa estar na rotina FISA156"* — o cBenef não nasce da
regra de cálculo, nasce do catálogo de benefícios. Se o `SP053190` não estiver na tabela 52 da base, a
regra de ajuste de lançamento não resolve e o XML sai sem o campo.

## 3. O que ainda não fecha nesta operação

| Lacuna | Pergunta para o cliente | Onde trava |
| --- | --- | --- |
| CFOP de retorno e prazo | Qual o CFOP de retorno e em quantos dias o retorno deve ocorrer para manter a suspensão? | Perfil de operação + regra de escrituração da entrada |
| cBenef do retorno | O retorno usa `SP053190` ou código próprio do catálogo? | Regra de ajuste de lançamento da TES de retorno |
| Transmissão da propriedade | Quando a mercadoria é vendida ao portador, qual CFOP/CST e qual cBenef? | Nova operação na matriz |
| IBS/CBS: 410 ou 550 | A demonstração é tratada como operação não onerosa (410/410999) ou como suspensão (grupo 550)? | Regra de escrituração IBS/CBS + geração do grupo no XML |
| Fundamento legal | Qual artigo do RICMS/SP e qual ajuste/convênio sustenta a suspensão? (A SEFAZ pode exigir a menção no documento) | Mensagem/dados adicionais |
| Regime do cliente | Emitente é Lucro Presumido/Real (CST) ou Simples Nacional (CSOSN)? | Todo o bloco de ICMS muda de dicionário |
| Interestadual | O benefício paulista vale para a saída 6.912? Qual cBenef? | Linha DEM-002 da matriz |
| Modo de cálculo | ICMS/PIS/COFINS continuam na TES 704 ou migram para o FISA170? | Define quantos objetos criar |

## 4. Riscos conhecidos que atingem esta configuração

- **cBenef obrigatório em SP desde 06/04/2026** (Portaria SRE nº 70/2025): nota paulista com benefício sem
  o campo tende a ser rejeitada. A tabela oficial de códigos está no portal da SEFAZ-SP
  (`portal.fazenda.sp.gov.br/servicos/nfe/Paginas/cBenef.aspx`).
- **Grupo de IBS/CBS zerado**: para CST 410 o XML esperado traz só `CST` + `cClassTrib`. Relatos na própria
  página do artigo da Central (dez/2025) descrevem rejeição por geração de base/alíquota zeradas e, no
  outro sentido, rejeição 1119 por ausência de `IBSCBSTot`. A orientação registrada nos comentários é
  ajustar o parâmetro que controla a geração do grupo no XML (MV_CSTGXML, ver TDN
  `pages/viewpage.action?pageId=1011566715`) para que o CST 410 não gere o grupo. **Valide no ambiente do
  cliente** — é configuração, não regra de negócio.
- **`410999` é residual**: usar o código residual quando existe código específico distorce a apuração e é
  apontado em fiscalização. Documente a justificativa da escolha no cadastro da regra.
- **Regra de escrituração com incidência em branco**: a parcela reduzida vai parar na coluna
  "Outros" por padrão, o que muda o resultado do livro sem mudar o cálculo.
- **Tabelas de escrita vazias**: CJ3/F2D em branco com imposto "certo" no documento é sintoma de regra de
  escrituração desalinhada da regra de cálculo (ver artigos "Tabelas CJ3 e F2D em branco, o que validar?" e
  "Como gerar CJ3 para nota fiscal de devolução?").
- **Mesmo CFOP, fins diferentes**: se a TES 704 for usada tanto para demonstração quanto para outra saída,
  a seleção por perfil precisa separar os casos (artigo "FISA170 - Como fazer uma Venda com o mesmo CFOP
  para fins diferentes no Configurador de Tributos?").

## 5. Plano de aceite desta operação

| # | Caso | O que conferir |
| --- | --- | --- |
| 1 | SP → SP, destinatário contribuinte | XML sem débito de ICMS, `cBenef = SP053190`, IPI 53, PIS/COFINS 49, grupo IBS/CBS com 410/410999; livro na coluna escolhida; CJ3/F2D gravados |
| 2 | SP → SP, destinatário não contribuinte | mesma saída; validar mensagem exigida e o campo de identidade do destinatário |
| 3 | SP → outro estado (6.912) | cBenef aplicável? DIFAL/ST indevidos? CST 410 mantido? |
| 4 | Retorno da demonstração | CFOP de retorno, sem cobrança indevida, escrita de entrada correta |
| 5 | Transmissão da propriedade (venda) | destaque do imposto, referência à nota de remessa, cBenef que fecha o ciclo |
| 6 | Cancelamento/devolução após prazo | comportamento do ajuste e efeito na apuração |

Para cada caso: simulador do FISA170 antes da emissão, depois XML + livro + apuração. Evidências vão no
campo `evidencias` da matriz, que é o que fecha a linha.
