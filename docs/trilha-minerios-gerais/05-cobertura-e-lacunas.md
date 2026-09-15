# Cobertura da base e lacunas da trilha

Leitura gerada automaticamente: quantos links do índice local casam com cada tópico e quais tópicos precisaram de complemento externo (páginas oficiais localizadas em 2026-09-11 e versionadas em `data/indices/Indice_Trilha_Complementos.txt`).

| Tópico | Candidatos na base | Selecionados | Complementos usados | Situação |
| --- | --- | --- | --- | --- |
| Cadastros fiscais: produtos, fornecedores e clientes | 109 | 12 | 0 | ✅ cobertura própria |
| TES: entrada e saída | 75 | 12 | 0 | ✅ cobertura própria |
| Configuração de tributos (impostos legados) e Configurador de Tributos | 228 | 12 | 0 | ✅ cobertura própria |
| Diferencial de alíquota (DIFAL) | 116 | 12 | 0 | ✅ cobertura própria |
| Apuração de impostos | 94 | 14 | 0 | ✅ cobertura própria |
| Impostos retidos (PCC, IRRF, INSS, ISS) | 38 | 16 | 5 | ⚠️ dependente de complemento |
| Geração do EFD-ICMS/IPI (SPED Fiscal) | 97 | 16 | 0 | ✅ cobertura própria |
| Geração da EFD Contribuições (PIS/COFINS) | 104 | 16 | 2 | ✅ cobertura própria |
| Registro de Apuração de ICMS — P9 (outros créditos e débitos) | 80 | 14 | 0 | ✅ cobertura própria |
| CIAP — Controle de Crédito de ICMS do Ativo Permanente | 85 | 14 | 2 | ✅ cobertura própria |
| Bloco K — controle da produção e do estoque | 14 | 14 | 6 | ⚠️ dependente de complemento |
| Registro de inventário (Bloco H / MATR460) | 38 | 16 | 8 | ⚠️ dependente de complemento |
| Validação das rotinas fiscais — NF manual de entrada/saída e acertos fiscais | 162 | 16 | 1 | ✅ cobertura própria |
| TAF, Extrator Fiscal e EFD-REINF | 24 | 16 | 4 | ✅ cobertura própria |
| Revisão das parametrizações conforme o escopo do projeto | 270 | 16 | 0 | ✅ cobertura própria |
| Quebra de estoque (perdas, refugo e baixas) | 17 | 14 | 10 | ⚠️ dependente de complemento |
| Exportação | 31 | 12 | 5 | ⚠️ dependente de complemento |
| Materiais oficiais de treinamento e referência | 47 | 16 | 2 | ✅ cobertura própria |

## O que foi incorporado como complemento

Os 34 links de `data/indices/Indice_Trilha_Complementos.txt` cobrem as lacunas encontradas:

- **Bloco K** — só havia 1 ponto de entrada na base; entraram o guia geral do Bloco K no TDN, os artigos de K200 (tabelas, tipos de produto) e a seção Legais/Fiscais do Estoque.
- **Registro de inventário** — entraram o passo a passo do Bloco H, o processo de inventário do SIGAEST (MATA270/MATA271/MATA340), os relatórios de conferência (MATR460) e a página de eventos tira-dúvidas com material.
- **CIAP** — entraram a página oficial do CIAP (modelos A/B/C/D, MV_FSNCIAP) e o processo de configuração para gerar o SPED.
- **EFD Contribuições** — entraram o manual da apuração FISA001 e o artigo FISA001/FISA008 (substituição de MATA996/SPEDPISCOF).
- **TAF/Extrator/REINF** — entraram o guia do Extrator Fiscal (EXTFISXTAF), o suporte financeiro do REINF, a documentação de EFD-Reinf no TAF e os layouts de extração.
- **Impostos retidos / PCC** — entraram as Regras Financeiras do Configurador de Tributos (data base de vencimento e cumulatividade), os artigos de retenção e cumulatividade de PIS/COFINS/CSLL e a aglutinação FINA378/FINA381.
- **Quebra de estoque** — entraram a nota de débito de perda em estoque, o estorno de movimento de inventário e o MV_ESTNEG.
- **Exportação** — entraram a DU-E no SIGAEEC, a integração por mensagem única (EAI), a vinculação de notas para formação de lote (EECNF400) e os artigos de nota complementar/título de câmbio.
- **Rotinas fiscais** — entrou o artigo sobre emissão de nota fiscal de saída no Faturamento (pedido + liberação).
- **Revisão de parametrização** — entrou a documentação de adequação ao IBS/CBS obrigatório a partir de 03/08/2026.

## Lacunas que continuam abertas (ação sugerida)

- **Mineração**: não há na base conteúdo fiscal específico de mineração (CFEM, exportação de minério, Lei Kandir). Se o escopo incluir esses temas, é preciso abrir chamado/consultoria específica na TOTVS.
- **Bloco K em mineração**: confirmar se o beneficiamento do minério caracteriza industrialização para fins do Bloco K (IND_ATIV do registro 0000) — decisão de escopo, não de documentação.
- **Quebra de estoque**: o conceito fiscal de perda (estorno de crédito, CFOP 5.927) precisa ser homologado com a SEF/MG; a documentação da TOTVS cobre a mecânica, não a tese tributária.
- **PCC com vencimento incorreto**: item aberto no tópico de impostos retidos; a correção passa por MV_BX10925/MV_VCPCCP e pelas regras financeiras do Configurador de Tributos.
