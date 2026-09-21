# Especificação Técnica do Sistema OrcaAI
## MGI / SRA-ES - Engenharia de Custos e Orçamentação Pública

---

## 1. Objetivo do Sistema
O **OrcaAI** é um sistema projetado para automatizar e auditar o ciclo de vida completo de orçamentação de obras e serviços de engenharia no âmbito da Administração Pública Federal, atendendo com rigor técnico e legal às diretrizes do **Ministério da Gestão e da Inovação em Serviços Públicos (MGI / SRA-ES)** e dos órgãos de controle (**TCU / CGU**).

---

## 2. Bases Legais e Normativas Aplicáveis

```
+---------------------------------------------------------------------------------------+
| LEGISLAÇÃO E NORMAS APLICÁVEIS                                                        |
+---------------------------------------------------------------------------------------+
| • Lei Federal nº 14.133/2021 (Nova Lei de Licitações e Contratos Administrativos)     |
| • Decreto Federal nº 7.983/2013 (Regras de elaboração de orçamento de obras e serviços)|
| • Instrução Normativa SEGES/ME nº 65/2021 (Procedimento de pesquisa de preços)        |
| • Acórdão TCU nº 2.622/2013 - Plenário (Parâmetros e fórmulas de cálculo de BDI)      |
| • Acórdão TCU nº 2.371/2020 - Plenário (BDI diferenciado para fornecimento)           |
| • Portaria MS nº 3.523/1998 e RE nº 09 ANVISA (Normas de Climatização / PMOC)         |
| • ABNT NBR 16690, NBR 16274, NBR 5410 (Instalações Elétricas e Fotovoltaicas)        |
| • Diretrizes do CREA-ES e CAU-ES para Emissão de ART/RRT                             |
+---------------------------------------------------------------------------------------+
```

---

## 3. Diretrizes Paramétricas Fixas (MGI/SRA-ES)

### 3.1 Localidade e Praça de Preços
- **Local de Execução**: Edifício Sede e Anexo do MGI/SRA-ES em Vitória/ES.
- **Bases Oficiais Prioritárias**:
  1. **SINAPI-ES** (Caixa / IBGE) - Base oficial P0 para construção civil.
  2. **IOPES-ES** (DER-ES) - Base estadual P1 para itens de edificações no ES.
  3. **SICRO3-ES** (DNIT) - Base para infraestrutura viária e pavimentação.
  4. **ORSE-SE** (CEHOP) - Base de fallback consagrada pelo TCU para saneamento/especiais.
  5. **Bases Regionais Sudeste**: SUDECAP-MG, SETOP-MG, EMOP-RJ, SIURB-SP.

### 3.2 Parametrização do BDI (Bonificações e Despesas Indiretas)
- **Serviços de Engenharia e Manutenção Predial**: **BDI Fixo de 25,00%** (calibrado para a alíquota de ISS de Vitória e despesas indiretas do órgão).
- **Fornecimento Puro de Materiais/Equipamentos Relevantes**: **BDI Diferenciado Reduzido de 14,02%** (faixa média do Acórdão TCU 2.622/2013: 11,10% a 18,45%).

### 3.3 Regras de Codificação Própria
Quando uma composição de custos não constar em nenhuma base oficial homologada, o OrcaAI deve estruturar uma Composição Própria com código exclusivo:
- Serviços: `SRAES-CP-001`, `SRAES-CP-002`, ...
- Insumos de Mercado: `SRAES-INS-001`, `SRAES-INS-002`, ...
- É terminantemente proibido o uso de códigos genéricos ou arbitrários sem a chancela `SRAES-`.

### 3.4 Linha de Produção de CPUs Próprias e Planejamento Integrado
- **Agente 7 (EspecialistaEspecificacao)**: Elabora a Descrição Canônica Padronizada no modelo SINAPI/EMOP a partir da demanda sumarizada.
- **Agente 5 (MineradorBasesOficiais)**: Localiza e extrai em alta velocidade os códigos oficiais e preços vigentes de insumos no SINAPI-ES e IOPES.
- **Agente 6 (CompositorCustosUnitarios)**: Constrói a Ficha Analítica de CPU (`SRAES-CP-XXX`) com produtividades calibradas.
- **Agente 8 (EngenheiroPlanejamentoEConomico)**: Incorpora a CPU no `.xlsx`, aplica o BDI do TCU (25% ou 14,02%), estabelece as redes PERT/CPM e gera o cronograma de Gantt e Curva S dinâmicos.
- **Agente 9 (AuditorConformidade)**: Valida a conformidade legal dos guardrails (G-01 a G-10) antes da emissão do dossiê.
- **Agente 10 (EspecialistaInstrucaoProcessualSEI)**: Elabora as respostas técnicas a pareceres da AGU/CJU, despachos SEI, notas técnicas e termos de justificativas da Lei 14.133/2021.

---

## 4. Peças Técnicas Obrigatórias do Dossiê OrcaAI

Para cada contratação, o OrcaAI gera o conjunto de 7 peças técnicas coordenadas:

1. **Planilha Orçamentária Analítica** (`.xlsx` e `.pdf`): Decomposição com item, código, fonte, descrição, unidade, quantidade, custo unitário sem BDI, BDI (%) e preço unitário com BDI.
2. **Planilha de Composições de Custos Unitários (CPUs)**: Detalhamento analítico de insumos (materiais, mão de obra com encargos sociais e equipamentos).
3. **Demonstrativo Analítico de BDI**: Memória de cálculo com a fórmula do TCU e justificativa técnica da taxa aplicada.
4. **Cronograma Físico-Financeiro**: Distribuição mensal dos serviços em valor financeiro (R$), percentual (%) e rede PERT/CPM.
5. **Caderno de Especificações Técnicas e Memorial Descritivo** (`.docx` / `.pdf`): Detalhamento dos materiais, normas ABNT e critérios de medição e pagamento.
6. **Mapa de Cotações e Relatório de Pesquisa de Mercado**: 3 cotações válidas, cálculo de mediana e descarte motivado de valores anômalos.
7. **Dossiê de Instrução Processual SEI / Governança Jurídica**: Termo de Justificativas Técnicas Relevantes (TJTR), Justificativa do Regime de Preço Global, Declaração do Decreto nº 9.507/2018 e Notas Técnicas de resposta a pareceres da AGU/CGU.
