# Trilha de implantação e treinamento — Fiscal Protheus 12

Projeto: **Minérios Gerais — implantação e treinamento do Fiscal Protheus 12**. Dossiê gerado por `scripts/gerar_trilha_treinamento.py` a partir do índice local (`client/public/knowledge.json`, 2382 links do TDN e da Central de Atendimento TOTVS). Nenhum link aqui é inventado: todos existem na base versionada do repositório.

## Como usar

1. Abra o arquivo da agenda correspondente e siga a ordem **Implantar → Treinar → Validar → Fontes**.
2. Cada fonte está classificada por intenção: implantar/parametrizar, treinar (guia, conceito, webinar), ponto de entrada (customização ADVPL) e suporte/FAQ.
3. No site estático, a aba **Trilha** carrega `client/public/trilhas.json` e mostra o mesmo conteúdo com links clicáveis.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `01-topicos-concluidos.md` | Cadastros fiscais, TES, configuração de tributos, DIFAL, apuração e impostos retidos (revisão + treinamento) |
| `02-agenda-09-09.md` | EFD ICMS/IPI, EFD Contribuições, Apuração de ICMS-P9, CIAP, Bloco K e registro de inventário |
| `03-agenda-11-09.md` | Rotinas fiscais (NF manual e acertos), TAF/Extrator/REINF, revisão de parametrizações, quebra de estoque e exportação |
| `04-treinamento-oficial.md` | Materiais oficiais de capacitação (webinars, eventos tira-dúvidas, guias e BC) |
| `05-cobertura-e-lacunas.md` | Quantos links a base tem por tópico e onde foi preciso complementar |
| `trilha.json` | Saída estruturada consumida pelo site (`client/public/trilhas.json`) |

## Regenerar

```bash
python3 scripts/build_knowledge.py            # atualiza o índice local
python3 scripts/gerar_trilha_treinamento.py   # regenera dossiê + trilhas.json
python3 scripts/gerar_trilha_treinamento.py --check  # falha se algum tópico ficar sem fonte
```

## Tópicos e cobertura

| # | Tópico | Grupo | Status | Links na base | Selecionados |
| --- | --- | --- | --- | --- | --- |
| 1 | Cadastros fiscais: produtos, fornecedores e clientes | Tópicos concluídos | concluido | 109 | 12 |
| 2 | TES: entrada e saída | Tópicos concluídos | concluido | 75 | 12 |
| 3 | Configuração de tributos (impostos legados) e Configurador de Tributos | Tópicos concluídos | concluido | 220 | 12 |
| 4 | Diferencial de alíquota (DIFAL) | Tópicos concluídos | concluido | 115 | 12 |
| 5 | Apuração de impostos | Tópicos concluídos | concluido | 94 | 14 |
| 6 | Impostos retidos (PCC, IRRF, INSS, ISS) | Tópicos concluídos | concluido | 38 | 16 |
| 7 | Geração do EFD-ICMS/IPI (SPED Fiscal) | Agenda 09/09 | pendente | 96 | 16 |
| 8 | Geração da EFD Contribuições (PIS/COFINS) | Agenda 09/09 | pendente | 104 | 16 |
| 9 | Registro de Apuração de ICMS — P9 (outros créditos e débitos) | Agenda 09/09 | pendente | 80 | 14 |
| 10 | CIAP — Controle de Crédito de ICMS do Ativo Permanente | Agenda 09/09 | pendente | 85 | 14 |
| 11 | Bloco K — controle da produção e do estoque | Agenda 09/09 | pendente | 14 | 14 |
| 12 | Registro de inventário (Bloco H / MATR460) | Agenda 09/09 | pendente | 38 | 16 |
| 13 | Validação das rotinas fiscais — NF manual de entrada/saída e acertos fiscais | Agenda 11/09 | pendente | 161 | 16 |
| 14 | TAF, Extrator Fiscal e EFD-REINF | Agenda 11/09 | pendente | 23 | 16 |
| 15 | Revisão das parametrizações conforme o escopo do projeto | Agenda 11/09 | pendente | 263 | 16 |
| 16 | Quebra de estoque (perdas, refugo e baixas) | Agenda 11/09 | pendente | 17 | 14 |
| 17 | Exportação | Agenda 11/09 | pendente | 31 | 12 |
| 18 | Materiais oficiais de treinamento e referência | Apoio transversal | apoio | 47 | 16 |
