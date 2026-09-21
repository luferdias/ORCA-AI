# COMPOSIÇÃO DE CUSTOS UNITÁRIOS PRÓPRIA (CPU)
## CÓDIGO: SRAES-CP-[NUMERO]
### DESCRIÇÃO DO SERVIÇO: [DESCRICAO_DETALHADA_DO_SERVICO]
### UNIDADE: [UNIDADE_MEDIDA] | DATA-BASE: [MES/ANO] | REGIME: NÃO DESONERADO

---

## 1. DETALHAMENTO ANALÍTICO DA COMPOSIÇÃO

### 1.1 Mão de Obra com Encargos Sociais
| Código / CBO | Função / Categoria Profissional | Fonte | Unidade | Coeficiente (H) | Salário Horário (R$) | Custo Total (R$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 88316 | Servente com Encargos Complementares | SINAPI-ES | H | [COEF_1] | R$ [VALOR_1] | R$ [TOT_1] |
| 88309 | Pedreiro com Encargos Complementares | SINAPI-ES | H | [COEF_2] | R$ [VALOR_2] | R$ [TOT_2] |
| **Subtotal Mão de Obra (A)** | | | | | | **R$ [SUBTOT_MO]** |

### 1.2 Materiais e Insumos
| Código Insumo | Descrição do Material / Insumo | Fonte | Unidade | Coeficiente | Preço Unitário (R$) | Custo Total (R$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SRAES-INS-001 | [Descricao Insumo Mercado 1] | Pesq. Mercado | UN | [COEF_MAT_1] | R$ [VALOR_MAT_1] | R$ [TOT_MAT_1] |
| SRAES-INS-002 | [Descricao Insumo Mercado 2] | Pesq. Mercado | KG | [COEF_MAT_2] | R$ [VALOR_MAT_2] | R$ [TOT_MAT_2] |
| **Subtotal Materiais (B)** | | | | | | **R$ [SUBTOT_MAT]** |

### 1.3 Equipamentos e Ferramental
| Código Insumo | Descrição do Equipamento | Fonte | Unidade | Coeficiente | Preço Unitário (R$) | Custo Total (R$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| [COD_EQ] | [Descricao Equipamento] | SINAPI-ES | CHP | [COEF_EQ] | R$ [VALOR_EQ] | R$ [TOT_EQ] |
| **Subtotal Equipamentos (C)** | | | | | | **R$ [SUBTOT_EQ]** |

---

## 2. RESUMO DE CUSTO E FORMAÇÃO DE PREÇO

$$\text{Custo Direto Total (CD)} = A + B + C = \text{R\$ } [\text{VALOR\_CD}]$$

$$\text{BDI Aplicado (25,00\%)} = \text{CD} \times 0{,}2500 = \text{R\$ } [\text{VALOR\_BDI}]$$

$$\textbf{PREÇO UNITÁRIO FINAL COM BDI} = \textbf{R\$ } [\textbf{PRECO\_FINAL\_UNIT}]$$

---

## 3. JUSTIFICATIVA TÉCNICA DA COMPOSIÇÃO PRÓPRIA
Declara-se que a presente composição unitária foi desenvolvida em razão da ausência de serviço idêntico ou similar nos cadernos técnicos do SINAPI-ES e da Tabela IOPES-ES, tendo sido empregados insumos homologados e pesquisa de mercado conforme a IN SEGES/ME nº 65/2021.
