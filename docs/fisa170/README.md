# Levantamento de necessidades fiscais para o Configurador de Tributos (FISA170)

Pacote de levantamento usado para transformar "o que o cliente faz hoje" em material suficiente para
**cadastrar regras no Configurador de Tributos** sem retrabalho.

O ponto de partida é a lista de campos que o fiscal costuma entregar (CFOP, CST ICMS, CST IPI,
CST PIS/COFINS, ClassTrib de IBS/CBS, cBenef e TES). Essa lista descreve **o resultado na nota**, mas o
FISA170 não é alimentado com o resultado: ele é alimentado com **perfil + regra de cálculo + regra de
escrituração + ajuste de lançamento + vigência**. Este pacote cobre essa diferença.

## Conteúdo

| Arquivo | Para que serve |
| --- | --- |
| `01-metodo-de-levantamento.md` | Como enumerar **todas** as operações do cliente e conduzir a coleta. |
| `02-matriz-de-informacoes.md` | O que cada dado informado decide no FISA170 e o que ainda falta perguntar. |
| `03-caso-demonstracao-sp.md` | Caso concreto: CFOP 5.912/6.912, CST ICMS 50, IPI 53, PIS/COFINS 49, ClassTrib 410/410999, cBenef SP053190, TES 704. |
| `04-checklist-validacao.md` | Teste, homologação, evidências e riscos. |
| `modelos/matriz-operacoes.csv` | Matriz de coleta: uma linha por operação, 91 colunas organizadas em 11 blocos. |
| `gerado/ciclos-operacoes-fisa170.xlsx` | Planilha Excel com **18 ciclos de operação** (64 movimentos) no formato da tabela "a operação não é uma, é um ciclo": CFOP de saída × CFOP de entrada, CST, cBenef, TES e status na matriz. |
| `gerado/` | Saída do gerador: resumo, lacunas, fichas por operação e mapa de fontes TOTVS. |

## Fluxo de trabalho

```bash
# 1. criar/reatualizar a matriz de coleta (cabeçalho + linhas de exemplo)
python3 scripts/gerar_pacote_fisa170.py --init-csv

# 2. preencher docs/fisa170/modelos/matriz-operacoes.csv (uma linha por operação)
#    separador ';' para abrir direto no Excel

# 3. gerar fichas, resumo, lacunas e mapa de fontes
python3 scripts/gerar_pacote_fisa170.py

# 4. travar o cadastro de regra enquanto houver bloqueio (útil em CI e no gate de kickoff)
python3 scripts/gerar_pacote_fisa170.py --check
```

O gerador só conhece links que já existem nos índices versionados em `data/indices/`, então toda fonte
citada nas fichas é um link real do TDN ou da Central de Atendimento TOTVS. Para buscar mais material,
use o próprio Buscador Protheus (`pnpm dev`) com termos como `FISA170`, `CFOP`, `cClassTrib`, `diferido`.

## Regra de ouro do levantamento

Uma operação só está **levantada** quando a linha da matriz responde às cinco perguntas abaixo:

1. **Quando** a regra deve valer? (CFOP, UF, participantes, produtos, vigência)
2. **O que** o FISA170 deve calcular? (base, alíquota, reflexo, quem calcula: TES ou configurador)
3. **O que** deve ser escrito? (coluna do livro, CST, incidência, ajuste SPED, apuração)
4. **O que** vai no documento fiscal? (tags, cBenef, mensagem, dados adicionais)
5. **Como** provamos que está certo? (simulador, XML, CJ3/F2D, livro, apuração, aprovação)

Os sete campos que o fiscal entrega costumam responder apenas as perguntas 3 e 4 de forma parcial.
