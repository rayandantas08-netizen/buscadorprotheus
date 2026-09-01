# Checklist de validação, governança e riscos

Este é o documento que sustenta o "pronto" de cada operação. Os links citados aqui existem no índice local
(`data/indices/Indice_Configurador_Tributos.txt`); para abrir o artigo, busque pelo título no Buscador
Protheus ou em `gerado/fontes.md`.

## 1. Pré-cadastro (evita regra que não pega)

- [ ] Versão do Protheus suporta os recursos usados (artigo "FISA170 - Os recursos do Configurador de
      Tributos estão disponíveis em quais versões do Protheus?").
- [ ] Dicionário e motor de cálculo atualizados ("Escrita Fiscal - Dicionário desatualizado, favor verificar
      atualizações do motor de cálculo fiscal").
- [ ] Tabelas do configurador identificadas na base ("FISA170 - Quais tabelas fazem parte do Configurador de
      Tributos?" e "Relacionamento entre tabelas SD1/SD2, SFT, CJ3 e F2D").
- [ ] Tabela cClassTrib importada na versão exigida pela Nota Técnica vigente; tributos IBS/CBS carregados
      ("Como importar a tabela cClassTrib-IBS/CBS no Configurador de Tributos?", "Como realizar carga
      automática dos Tributos CBS e IBS?").
- [ ] Códigos de benefício cadastrados no catálogo exigido pelo ajuste de lançamento (Tabela 52 / FISA156)
      com data de início.
- [ ] Decisão registrada: TES, FISA170 ou híbrido — e quais campos da TES permanecem ativos
      ("CFGTRIB - Campos que Permanecem no TES", "Campos do cadastro de TES descontinuados",
      "FISA170 - Como confirmar se os impostos estão sendo gerados pelo Configurador de Tributos ou TES?").

## 2. Durante o cadastro

- [ ] Perfis criados na menor granularidade útil; produto e participante populados pelo facilitador
      ("FISA170 - Como utilizar o Facilitador de cadastro no perfil de produtos e participante?").
- [ ] Perfil de origem × destino definido antes do perfil de operação, para não criar regra que nunca é
      alcançada.
- [ ] Regra de base e de alíquota separadas por tributo; regra por NCM cobrindo todas as UFs quando a
      alíquota varia ("Como configurar a Regra de NCM para todos os estados?").
- [ ] Ordem de cálculo e reflexos conferidos quando um tributo entra na base de outro
      ("...quando um imposto influencia o cálculo de outro?", "Quantas majorações posso incluir em outro
      tributo?").
- [ ] Arredondamento e redução de alíquota conferidos nos campos específicos
      ("Campo Config Arred (F2B_RND)", "Campo Redução de Alíquota (F28_REDALI)").
- [ ] Regra de escrituração com incidência, CST e percentual de suspensão/diferimento explícitos — nunca por
      omissão ("Tratativa do Campo Incidência da Regra de Escrituração").
- [ ] Operações com documento de origem vinculado revisadas na política do tributo
      ("CFGTRIB - Perfil de Operação - Política do Tributo para Documentos que possuem vínculos com o
      Documento de Origem").
- [ ] Mensagens e dados adicionais cadastrados quando a legislação exigir texto no documento.
- [ ] Vigência preenchida e aprovada ("Onde informar a data de vigência da regra", "Mecanismo de aprovação de
      Regras de Cálculo (campo Status)").
- [ ] Compartilhamento entre filiais decidido e testado ("Compartilhamento de Tabelas de Perfis, Regras de
      Cálculo e Regra de Escrituração", "Como compartilhar as regras dos perfis entre filiais no FISA170?").

## 3. Teste funcional (por operação)

Ordem que reduz retrabalho: simulador → pedido/entrada → faturamento → XML → livro → apuração → contabilidade.

- [ ] Simulador de operação com o resultado esperado, incluindo as variantes de UF e de participante
      ("CFGTRIB - Simulador de Operação", "Simulador Comparativo").
- [ ] Cálculo comparado com o método anterior (legado x configurador) para a mesma nota.
- [ ] XML conferido campo a campo: CST/CSOSN, cBenef, grupo de IBS/CBS (CST + cClassTrib), mensagens,
      dados adicionais, indicadores de operação.
- [ ] Gravação em CJ3 (escrituração por item), F2D (tributos genéricos) e no código de regra do documento
      (F2B_REGRA); tabela CJ3/F2D vazia é falha de escrita, não de cálculo
      ("SIGAFIS - Tabelas CJ3 e F2D em branco, o que validar?").
- [ ] Livro fiscal com valores nas colunas certas (tributado/isento/outros) e base conferida.
- [ ] Apuração do período sem diferença não explicada; crédito/estorno conforme decidido.
- [ ] Nota de retorno/devolução/complemento testada na mesma rodada (nunca só a de saída).
- [ ] Cancelamento, rejeição e uso do DFe de ajuste testados quando a operação tiver prazo legal.

## 4. Riscos do projeto e mitigação

| Risco | Sintoma | Mitigação |
| --- | --- | --- |
| Levantar por CFOP em vez de por diferença tributária | matriz com 200 linhas e regras duplicadas | corte do método: uma linha por combinação que muda cálculo ou escrita |
| CBenef tratado como campo livre | rejeição na SEFAZ, benefício não reconhecido | catálogo (tabela 52) primeiro, regra de ajuste depois, com vigência |
| cClassTrib escolhido "no olho" | apuração distorcida, uso de código residual | registro do artigo da LC 214/2025 na matriz + revisão fiscal antes de configurar |
| Modo híbrido sem mapa do que fica na TES | diferença entre simulador e XML | campo `tes_campos_ativeis` obrigatório no validador |
| Regra criada fora do mecanismo de aprovação | mudança não autorizada em produção | campo `aprovacao_regra` + status conferido no aceite |
| Só testar a saída | retorno e transmissão sem regra | bloco "ciclo da operação" na matriz (`cfop_retorno`, `cfop_entrada`) |
| Versão/base incompatível | função não existe, error log em FISA170 | checklist de pré-cadastro; artigos de versão e de dicionário |
| Ausência de evidência | discussão sem fim sobre o que foi aceito | campo `evidencias` preenchido antes de fechar a linha |

## 5. Estrutura de uma boa linha de matriz (o mínimo viável)

Para uma operação de venda simples, o mínimo é: código, descrição, sentido, abrangência, UF de origem,
documento, finalidade, módulo de origem, vigência, CFOP, origem + CST de ICMS, CST de IPI, CST de PIS e
COFINS, CST e cClassTrib de IBS/CBS, natureza do benefício, TES, modo de cálculo, coluna do livro,
incidência, aprovação e evidências.

Para uma operação com benefício (o caso deste pacote), acrescente: fundamento legal, cBenef e sua vigência
no catálogo, código do retorno, texto exigido no documento e os CFOPs do ciclo completo.
