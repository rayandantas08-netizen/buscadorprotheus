# Método de levantamento — operações para o FISA170

## 1. Enumerar as operações (antes de perguntar qualquer CST)

O erro mais caro é pedir "a lista de operações" sem critério: o cliente entrega uma lista de TES ou uma
lista de CFOP e a contagem não fecha com a realidade. Monte o inventário cruzando quatro fontes:

| Fonte no Protheus | O que extrair | Cuidado |
| --- | --- | --- |
| Cadastro de TES | TES ativas por filial, CFOP associado, flags de cálculo | TES sem uso há 12 meses ainda vira regra no FISA170 se você não filtrar |
| Cadastro de CFOP | Natureza, se permite crédito, se é de serviço | Muitos CFOPs são usados por um único cliente/fornecedor específico |
| Documentos emitidos/recebidos (12 meses) | Frequência por CFOP × UF de destino × NCM × tipo de participante | É isso que diz o que é operação relevante |
| XMLs autorizados | O que realmente saiu no `<det>` (CST, cBenef,ClassTrib, mensagem) | A nota é a verdade; o cadastro do cliente nem sempre é |

Regras de corte para não explodir a matriz:

- Uma linha por **combinação que muda o cálculo ou a escrita**. Se dois clientes diferentes usam o mesmo
  CFOP, o mesmo CST, o mesmo cBenef e a mesma escrita, é uma linha só com `participantes_aplicavel = todos`.
- Separe **sempre** entrada de saída e interna de interestadual: o FISA170 resolve por perfil de operação
  e por perfil origem × destino, então a chave muda.
- Operação de ciclo (remessa → retorno, consignação, beneficiamento, demonstração) ocupa **duas linhas**:
  a de saída e a de retorno. Ver `03-caso-demonstracao-sp.md`.
- Mesmo CFOP para fins diferentes não é a mesma operação: ver o artigo da Central
  "FISA170 - Como fazer uma Venda com o mesmo CFOP para fins diferentes no Configurador de Tributos?"
  (indexado em `data/indices/Indice_Configurador_Tributos.txt`).

Entregável da etapa: `modelos/matriz-operacoes.csv` com uma linha por operação, mesmo com campos vazios.

## 2. Coleta com o cliente (roteiro por bloco)

A matriz tem 11 blocos. Os blocos 1, 3, 5, 6 e 7 são de responsabilidade do **cliente**; os blocos 9, 10
e 11 são preenchidos pelo **consultor** durante a construção. Coletar tudo em uma reunião única não
funciona — o roteiro abaixo é o que costuma fechar em duas conversas.

**Conversa 1 — negócio e documento (45 min)**

1. O que dispara a emissão? (pedido, faturamento, MATA103, estoque, serviços, PDV)
2. Quem é o destinatário? contribuinte ou não, dentro ou fora do estado, regime (normal/Simples).
3. O produto? NCM, CEST, origem da mercadoria, se é revenda/próprio uso/ativo/demonstração.
4. Tem benefício fiscal? Qual o fundamento legal e o que a SEFAZ manda escrever no documento?
5. Existe retorno/devolução/complemento dessa operação? Em quanto tempo?
6. O que muda em 2026? (cBenef obrigatório em SP, IBS/CBS no XML)

**Conversa 2 — escrita, apuração e exceções (45 min)**

1. Onde isso cai no livro fiscal? (tributado / isento / outros / fora do livro)
2. Gera crédito? De quanto? Em qual apuração (ICMS, IPI, PIS/COFINS, subapuração)?
3. Algum imposto entra na base de outro? (reflexo, majoração, "desconto do ICMS da base do PIS/COFINS")
4. Precisa de registro de ajuste no SPED? Qual código?
5. Tem contabilização de tributo genérico?
6. Quem aprova a regra e com qual vigência?

## 3. Validação do levantamento

```bash
python3 scripts/gerar_pacote_fisa170.py --check
```

O validador bloqueia quando falta dado indispensável e aponta incoerência de código (CFOP × UF,
cClassTrib × CST de IBS/CBS, benefício sem cBenef em SP, redução de base sem incidência da parcela
reduzida, ST sem base/alíquota, cBenef sem vigência). A lista completa de checagens está em
`02-matriz-de-informacoes.md`, seção "Regras de coerência".

O arquivo `gerado/01-lacunas.md` é o roteiro de follow-up: cada lacuna já sai com a pergunta pronta.

## 4. Ordem de construção no FISA170

Seguir a ordem evita retrabalho, porque cada camada depende da anterior:

1. **Tributos e tabelas auxiliares** — cadastro de tributos, URF, tabela cClassTrib, catálogo de
   benefícios (em SP, a Tabela 52 usada pelo ajuste de lançamento).
2. **Perfis** — participante, produto (e produto × origem), origem × destino, operação (CFOP + documento).
3. **Regras de cálculo** — base e alíquota por tributo; regra por NCM quando a alíquota depende de NCM/UF;
   reflexos e majorações.
4. **Regra de escrituração** — CST, incidência (inclusive da parcela reduzida), percentual de
   diferimento/suspensão; é o que alimenta SFT/SF3 e, por consequência, livro e apuração.
5. **Regra de ajuste de lançamento** — vincula o código de benefício (cBenef) à regra tributária e à
   vigência.
6. **Mensagens e dados adicionais** do documento fiscal.
7. **TES** — o que continua ativo (CFOP e o que ainda é decidido por ela) e o que foi descontinuado.
8. **Simulador de operação / comparativo** — compara com o cálculo legado antes de tocar em produção.
9. **Aprovação da regra e compartilhamento** (se a regra vale para várias filiais).

As fichas geradas (`gerado/ficha-*.md`) já trazem exatamente essa sequência, com os links do TDN e da
Central de Atendimento no passo correspondente.

## 5. Critério de aceite por operação

Uma operação está fechada quando, para cada uma das cinco perguntas do `README.md`, existe resposta na
matriz **e** existe evidência anexada:

- [ ] simulador do FISA170 com o resultado esperado;
- [ ] XML de homologação com as tags conferidas (ICMS, IPI, PIS/COFINS, grupo de IBS/CBS, cBenef, mensagem);
- [ ] livro fiscal com a coluna e o valor corretos;
- [ ] gravação conferida em CJ3 (escrituração por item) e F2D (tributos genéricos), com o código de
      regra do documento gravado (F2B_REGRA);
- [ ] apuração do período sem diferença não explicada;
- [ ] regra aprovada com vigência registrada.

Sem as seis caixas marcadas, a operação volta para `gerado/01-lacunas.md`.
