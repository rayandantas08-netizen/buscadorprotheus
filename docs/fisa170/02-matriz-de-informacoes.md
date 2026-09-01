# Matriz de informações — do dado do cliente ao objeto do FISA170

## 1. O que os sete campos que você já recebe realmente determinam

| Dado do cliente | O que ele decide | Onde isso vira cadastro no FISA170 | O que ainda falta para criar a regra |
| --- | --- | --- | --- |
| **CFOP 5.912 / 6.912** | Natureza da operação e o dígito de abrangência (5 interna, 6 interestadual). É a chave de seleção, não o cálculo. | Perfil tributário de operação (F23) e de tipo de operação (F26), cruzando CFOP + tipo de documento; o CFOP continua no cadastro de TES (SF1) | Lista dos CFOPs do mesmo ciclo (retorno, transmissão, ajuste); quais documentos usam o mesmo CFOP com fins diferentes; se a TES de entrada tem CFOP próprio |
| **CST ICMS 50** | Situação tributária de saída (origem + situação). Indica que o imposto não é destacado agora. | Regra de escrituração de ICMS (CJ0/CJ1/CJ2): CST, incidência e percentual de suspensão/diferimento → alimenta SFT/SF3 | Coluna do livro; se há crédito na entrada correspondente; se é suspensão ou diferimento (na tabela de CST de ICMS, 50 costuma ser suspensão e 51 diferimento — confirme a nomenclatura da UF); fundamento legal |
| **CST IPI 53** | Saída não tributada de IPI: sem débito e, em regra, sem crédito. | Regra de escrituração de IPI + cadastro de tributo (F2E); alíquota não deve gerar valor | O produto é de contribuinte do IPI? NCM e EX aplicáveis; se existe IPI "por dentro" em alguma hipótese da mesma TES |
| **CST PIS/COFINS 49** | "Outras operações de saída": fora das hipóteses 01 a 12. | Regra de escrituração de PIS/COFINS; confirmar se o tributo entra desligado para não gerar valor indevido | Regime (cumulativo/não cumulativo), base, se gera crédito, se a mesma TES serve para entrada (CST 49 é de saída) |
| **ClassTrib 410 / 410999** | Enquadramento de IBS/CBS. 410 = imunidade e não incidência; 410999 = código residual de operações não onerosas sem previsão de tributação. | Regra de escrituração de IBSEST/CBSFED + tabela cClassTrib importada; o CST também interfere no que é gerado no XML | Se a operação é mesmo não incidência (410) ou suspensão (550); se o grupo de IBS/CBS deve ser suprimido no XML quando não há cálculo; indicador de operação (IndOp) |
| **cBenef SP053190** | Qual benefício fiscal de ICMS está sendo declarado no item. | O código precisa existir no catálogo exigido (em SP, a Tabela 52 mantida na rotina FISA156) e ser ligado por uma **regra de ajuste de lançamento** (CJ9/CJA) com data de início e regra tributária (F2B) | Descrição que vai no documento; código do retorno/transmissão; vigência; se a SEFAZ exige mensagem ou dado adicional junto |
| **TES 704** | Gatilho no módulo de origem e o que ainda é decidido fora do FISA170. No modo híbrido, a TES continua mandando em CFOP e em flags de cálculo. | SF1 + vínculo com a regra do documento (F2B_REGRA) | Quais campos da TES seguem ativos e quais foram descontinuados; TES correspondente na entrada; se a TES é compartilhada entre filiais |

Leitura da tabela: a coluna do meio é o "produto" que você tem de criar. O que está na última coluna é o
motivo pelo qual a regra volta antes de funcionar.

## 2. Os quatro campos que faltam na lista de sempre

Sem estes, qualquer cadastro no FISA170 é chute. Eles não aparecem na nota, mas decidem a regra:

1. **`modo_calculo`** — a operação é calculada pela TES, pelo FISA170 ou de forma híbrida? É o que define
   quantos objetos criar. Em modo híbrido típico, ICMS/PIS/COFINS ficam na TES e IBS/CBS no configurador.
2. **`incidencia` + `livro_fiscal`** — a regra de escrituração tem de saber em qual coluna registrar
   (Tributado/Isento/Outros). Tem a mesma tratativa do campo Livro Fiscal da TES; em branco, a parcela
   reduzida cai por padrão em "Outros".
3. **`vigencia_inicio`** — regra sem vigência definida não é auditável e conflita com a data do catálogo de
   benefício.
4. **`evidencias`** — o que fecha o aceite (simulador, XML, livro, CJ3/F2D). Sem isso, "configurado" vira
   "homologado" por decisão de quem falou mais alto.

## 3. Blocos da matriz de coleta

| Bloco | Colunas | Quem preenche | Por que existe |
| --- | --- | --- | --- |
| 1. Identificação | 15 | cliente | Define a chave da regra e o recorte temporal |
| 2. Aplicação | 8 | cliente | Recorte de produto/participante — é o perfil, não o tributo, que direciona a regra |
| 3. ICMS | 15 | cliente | CFOP, CST, base, ST, FCP/DIFAL, crédito |
| 4. IPI | 4 | cliente | CST, alíquota, classe de enquadramento |
| 5. PIS/COFINS | 6 | cliente | CST, alíquota, regime, crédito |
| 6. IBS/CBS (Reforma) | 6 | cliente | CST + cClassTrib coerentes, crédito presumido, indicadores |
| 7. Benefício fiscal | 5 | cliente | cBenef, tipo, descrição, vigência no catálogo |
| 8. Retenções | 5 | cliente | Serviços, ISS, majorações e fundos |
| 9. No Protheus | 11 | consultor | TES, motor de cálculo e todos os objetos a criar |
| 10. Escrita e DFe | 13 | consultor | Escrituração, SPED, reflexo, apuração, contabilização |
| 11. Governança | 5 | os dois | Aprovação, compartilhamento, evidências, dúvidas abertas |

Total: 91 colunas. Não é para preencher tudo: o validador só exige os campos obrigatórios e os
condicionais que as respostas anteriores tornaram obrigatórios.

## 4. Regras de coerência aplicadas pelo validador

O `scripts/gerar_pacote_fisa170.py` verifica, por linha:

- campos obrigatórios vazios → **bloqueio**;
- CFOP com 4 dígitos e primeiro dígito compatível com sentido + abrangência → incoerência é **bloqueio**;
- cClassTrib com 6 dígitos e os três primeiros iguais ao CST de IBS/CBS (ex.: 410 → 410xxx) → **bloqueio**;
- CST de ICMS que indica benefício (`20/30/40/41/50/51/53`) sem cBenef em SP → **bloqueio**; em outra UF →
  **atenção** ("confirme a exigência local");
- CST que não costuma carregar benefício (`00/02/06/10/60/70/90`) com cBenef preenchido → **atenção**;
- operação de remessa/retorno/consignação/beneficiamento/demonstração sem `cfop_retorno` → **bloqueio**;
- benefício sem fundamento legal, sem vigência no catálogo ou sem mensagem → **bloqueio/atenção**;
- redução de base sem `incidencia_parcela_reduzida` → **bloqueio**;
- ICMS-ST sem base ou sem alíquota interna do destino → **bloqueio**;
- CST IPI de saída não tributada (51–55) com alíquota maior que zero → **atenção**;
- PIS/COFINS com CST 49 e alíquota informada → **atenção** (ver desligamento automático do tributo);
- `cClassTrib` residual `410999` → **atenção** permanente (usar só quando não houver código específico);
- modo `hibrido`/`cfgtrib` sem perfil de operação, regra de base, de alíquota ou regra tributária →
  **bloqueio**; híbrido sem `tes_campos_ativeis` → **atenção**;
- vigência final anterior à inicial → **bloqueio**; vigência a partir de 06/04/2026 em SP com benefício e sem
  cBenef → **bloqueio**;
- `evidencias` vazio → **bloqueio**.

São heurísticas de levantamento, não substituto da análise tributária: o objetivo é chegar na reunião de
configuração sem pergunta óbvia pendente.

## 5. Mapa de campos → objeto do FISA170

| Se o cliente informou... | Você cria/ajusta | Consulta no índice local |
| --- | --- | --- |
| CFOP que muda o tipo de documento | Perfil de operação (F23) e de tipo de operação (F26) | "CFGTRIB - Configurador de Tributos", "Boas Práticas - Guia de Utilização" |
| Produto com NCM e alíquota variável | Regras por NCM (CIS/CIT/CIU) e regra de alíquota (F28) | "CFGTRIB - Regras por NCM", "FISA170 - Como configurar a Regra de NCM para todos os estados?" |
| Base de cálculo própria, "por dentro", dupla, MVA | Regra de base (F27) + cálculo do tributo | "CFGTRIB - Cálculos no Configurador de Tributos", "CFGTRIB - DIFAL e ICMS Complementar", "CFGTRIB - ICMS-ST - Cálculos" |
| Um imposto que afeta a base de outro | Reflexo e majoração entre tributos | "FISA170 - Como configurar as regras dos impostos quando um imposto influencia o cálculo de outro?", "Quantas majorações posso incluir em outro tributo" |
| CST, isenção, suspensão, redução | Regra de escrituração (CJ0/CJ1/CJ2) → SFT/SF3 | "CFGTRIB - Campos..." e "FISA170 - Tratativa do Campo Incidência da Regra de Escrituração" |
| cBenef | Regra de ajuste de lançamento (CJ9/CJA) + catálogo (Tabela 52 via FISA156) | "CFGTRIB - Ajustes de Lançamento no Configurador de Tributos", "FIS Como configurar o ICMS diferido 100% e gerar cBenef para SP?" |
| ClassTrib IBS/CBS | Importação da tabela cClassTrib + escrituração de IBSEST/CBSFED + ajuste do grupo no XML | "CFGTRIB - Adequação do Configurador de Tributos aos Códigos de Classificação Tributária do IBS, CBS e IS", "FISA170 - Como importar a tabela cClassTrib-IBS/CBS", "Como configurar o cClasstrib 410 ... forma Hibrida?" |
| Crédito, estorno, guia | Regra de apuração (F2G), títulos (F2F), código de receita (CJ4-CJ7) | "CFGTRIB - Cadastro e Apuração Código IPM", "FISA170 - Como usar a Sub Apuração junto com o configurador de tributos" |
| Texto obrigatório na nota | Cadastro de mensagens (CJ8) e dados adicionais | "CFGTRIB - Cadastro de Mensagens no Documento Fiscal", "CFGTRIB - Dados Adicionais" |
| Datas e filiais | Vigência, aprovação e compartilhamento de tabelas | "FISA170 - Onde informar a data de vigência da regra", "Mecanismo de aprovação de Regras de Cálculo", "Compartilhamento de Tabelas de Perfis..." |

## 6. Fontes de referência por bloco

O mapa completo, com todos os links agrupados por tema, é gerado em `gerado/fontes.md` a partir de
`data/indices/Indice_Configurador_Tributos.txt` e `data/indices/Indice_SIGAFIS_Fiscal.txt`.

Fatos de legislação (descrição de CFOP, tabela cBenef de SP, descrição de cClassTrib e exigência do campo)
não vêm do TDN: foram conferidos em fontes oficiais em 2026-09-01 e estão marcados como tal no caso
concreto — revalide no portal da SEFAZ do estado do cliente antes de configurar.
