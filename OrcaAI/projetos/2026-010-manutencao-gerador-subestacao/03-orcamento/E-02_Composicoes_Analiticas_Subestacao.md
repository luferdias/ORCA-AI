# E-02 Composições Analíticas de Custo Unitário — Subestação Elétrica MGI/ES

**Obra:** Manutenção Preventiva e Corretiva da Subestação Elétrica — Edifício Sede MGI/ES
**Data-base:** 04/2026 | **Regime:** Desonerado | **Local:** Vitória/ES
**Bases Referenciais:** SINAPI 04/2026 (ES), SBC 05/2026 (ES), SICRO3 01/2026 (ES), IOPES 01/2026 (ES) e Cotações de Mercado (Grande Vitória)
**Proposta de Referência:** ECOCEL Comércio e Serviços Ltda — PR 052601-26-REV00 (maio/2026)

---

## Quadro de Insumos de Mão de Obra (Base SINAPI 04/2026 ES — Desonerado)

| Código SINAPI | Descrição | Custo Horário (R$/h) | Fonte |
|---------------|-----------|---------------------|-------|
| 88264 | Eletricista com encargos complementares | 27,89 | SINAPI 04/2026 ES |
| 88247 | Auxiliar de eletricista com encargos complementares | 22,12 | SINAPI 04/2026 ES |
| 90778 | Engenheiro civil de obra júnior com encargos complementares | 120,65 | SINAPI 04/2026 ES |
| COMP-ENG-ELET | Engenheiro eletricista com encargos complementares (composição própria, baseada em SINAPI 90778 + adicional de 15% por especialidade elétrica — código 91677 desativado) | 138,75 | Própria (SINAPI 04/2026 ES) |

*Nota: O SINAPI 91677 (Engenheiro Eletricista) foi desativado pela CAIXA/IBGE. A composição própria COMP-ENG-ELET utiliza o SINAPI 90778 (Engenheiro Civil Júnior) como base, acrescido de 15% de adicional por especialidade, compatível com o piso salarial do CREA-ES para engenheiros eletricistas.*

---

## SRAES-SUB-001: Manutenção preventiva da Chave Seccionadora 15 kV

**Unidade:** un | **Custo Total (Sem BDI): R$ 1.760,00**

**Escopo:** Limpeza, desoxidação e reaperto das conexões; inspeção visual dos isoladores; ensaio de resistência de isolamento (Megger); verificação de folga dos contatos e articulações; teste mecânico de operação e verificação/reaperto de fixação em alvenaria/concreto.

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | 88264 | Eletricista com encargos complementares | h | 16,00 | 26,18 | 418,88 | SINAPI-ES 02/2026 |
| M.O. | 88247 | Auxiliar de eletricista com encargos complementares | h | 16,00 | 20,93 | 334,88 | SINAPI-ES 02/2026 |
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — supervisão e emissão de relatório parcial | h | 4,00 | 130,33 | 521,32 | Própria (SINAPI-ES) |
| EQ. | COT-SUB-EQ-001 | Locação de megôhmetro digital 5 kV (Megger) calibrado, com certificado — diária | diária | 1,00 | 350,00 | 350,00 | Média 3 cotações |
| MAT. | COT-SUB-MAT-001 | Material de limpeza técnica (solvente dielétrico, panos antiestáticos, escova isolante, spray desoxidante para contatos elétricos) | cj | 1,00 | 134,92 | 134,92 | Média 3 cotações |
| | | **Custo Direto Total (Sem BDI)** | | | | **1.760,00** | |

### Justificativa dos Coeficientes — SRAES-SUB-001

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Eletricista | 16,00 h | 2 eletricistas × 8h/dia = 16 h-homem. Jornada completa: abertura, limpeza, desoxidação, reaperto, ensaios e fechamento. Atividade NR-10. |
| Auxiliar de eletricista | 16,00 h | 2 auxiliares × 8h/dia = 16 h-homem. Apoio na manipulação de equipamentos, sinalização e preparação de material. |
| Engenheiro eletricista | 4,00 h | Supervisão técnica, interpretação dos ensaios de Megger e elaboração do relatório parcial (meio período). |
| Megôhmetro (diária) | 1,00 diária | Locação de equipamento calibrado para ensaio de isolamento da chave 15 kV. |
| Material de limpeza | 1,00 cj | Kit completo de consumíveis para limpeza técnica de uma chave seccionadora. |

---

## SRAES-SUB-002: Manutenção preventiva dos Transformadores a Seco (por unidade)

**Unidade:** un | **Custo Total (Sem BDI): R$ 1.200,00**

**Escopo (por unidade):** Limpeza e inspeção visual (fissuras, trincas, perfurações no isolamento de resina, oxidação, aterramento); reaperto de buchas de isolamento, espaçadores do entreferro e suportes das bobinas; inspeção e limpeza de isoladores/acessórios e reaperto de conexões.

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | 88264 | Eletricista com encargos complementares | h | 12,00 | 26,18 | 314,16 | SINAPI-ES 02/2026 |
| M.O. | 88247 | Auxiliar de eletricista com encargos complementares | h | 12,00 | 20,93 | 251,16 | SINAPI-ES 02/2026 |
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — supervisão e análise de integridade da resina | h | 3,00 | 130,33 | 390,99 | Própria (SINAPI-ES) |
| MAT. | COT-SUB-MAT-002 | Material de limpeza técnica para transformador a seco (aspirador industrial antiestático, pincéis isolantes, panos de microfibra secos, spray de limpeza a seco para bobinas) | cj | 1,00 | 165,00 | 165,00 | Média 3 cotações |
| MAT. | COT-SUB-MAT-003 | Torquímetro isolado e jogo de chaves isoladas VDE 1000V para reaperto (rateio por uso) | cj | 1,00 | 78,69 | 78,69 | Média 3 cotações |
| | | **Custo Direto Total (Sem BDI)** | | | | **1.200,00** | |

### Justificativa dos Coeficientes — SRAES-SUB-002

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Eletricista | 12,00 h | 2 eletricistas × 6h = 12 h-homem por transformador. Inspeção detalhada de bobinas, conexões e buchas. |
| Auxiliar de eletricista | 12,00 h | 2 auxiliares × 6h = 12 h-homem. Apoio na aspiração, limpeza e manuseio de material. |
| Engenheiro eletricista | 3,00 h | Análise visual de integridade do isolamento de resina, verificação de aterramento e emissão de parecer. |
| Material de limpeza | 1,00 cj | Kit de consumíveis para limpeza a seco de um transformador (resina não permite solventes líquidos). |
| Torquímetro isolado | 1,00 cj | Rateio do uso do ferramental para reaperto das buchas e espaçadores. |

---

## SRAES-SUB-003: Manutenção preventiva do Banco de Capacitores

**Unidade:** un | **Custo Total (Sem BDI): R$ 960,00**

**Escopo:** Inspeção visual e limpeza geral do quadro; lubrificação e reaperto de conexões; verificação de aterramento; inspeção de capacitores, cabos e componentes de manobra; medição de corrente dos capacitores; teste de chaveamento e conferência de parametrização do controlador.

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | 88264 | Eletricista com encargos complementares | h | 12,00 | 26,18 | 314,16 | SINAPI-ES 02/2026 |
| M.O. | 88247 | Auxiliar de eletricista com encargos complementares | h | 8,00 | 20,93 | 167,44 | SINAPI-ES 02/2026 |
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — parametrização do controlador e análise de medições | h | 2,00 | 130,33 | 260,66 | Própria (SINAPI-ES) |
| MAT. | COT-SUB-MAT-004 | Material de limpeza e lubrificação (limpa-contato dielétrico, graxa de silicone p/ conexões, panos, estopa) | cj | 1,00 | 95,00 | 95,00 | Média 3 cotações |
| EQ. | COT-SUB-EQ-002 | Alicate amperímetro digital true-RMS com certificado (rateio de locação por uso) | cj | 1,00 | 122,74 | 122,74 | Média 3 cotações |
| | | **Custo Direto Total (Sem BDI)** | | | | **960,00** | |

### Justificativa dos Coeficientes — SRAES-SUB-003

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Eletricista | 12,00 h | 2 eletricistas × 6h = 12 h-homem. Limpeza, reaperto, medição de corrente e teste de chaveamento. |
| Auxiliar de eletricista | 8,00 h | 1 auxiliar × 8h. Apoio na medição, sinalização e limpeza. |
| Engenheiro eletricista | 2,00 h | Conferência de parametrização do controlador do banco e análise das medições de corrente. |
| Material de limpeza | 1,00 cj | Kit de consumíveis para limpeza e lubrificação de um quadro de banco de capacitores. |
| Amperímetro | 1,00 cj | Rateio da locação do alicate amperímetro true-RMS para medição de corrente dos capacitores. |

---

## SRAES-SUB-004: Manutenção preventiva do QGBT e do QGBD (Quadro de Transferência de Carga do Gerador)

**Unidade:** un | **Custo Total (Sem BDI): R$ 1.138,00**

**Escopo:** Inspeção visual, limpeza geral, lubrificação e reaperto de todas as conexões e verificação de aterramento de dois quadros elétricos:
- **QGBT** — Quadro Geral de Baixa Tensão da subestação;
- **QGBD** — Quadro de Transferência de Carga do Grupo Gerador (painel de comutação automática rede/gerador).

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | 88264 | Eletricista com encargos complementares | h | 14,00 | 26,18 | 366,52 | SINAPI-ES 02/2026 |
| M.O. | 88247 | Auxiliar de eletricista com encargos complementares | h | 14,00 | 20,93 | 293,02 | SINAPI-ES 02/2026 |
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — verificação de aterramento, teste de comutação e supervisão dos 2 quadros | h | 2,00 | 130,33 | 260,66 | Própria (SINAPI-ES) |
| MAT. | COT-SUB-MAT-005 | Material de limpeza e lubrificação (limpa-contato, graxa de silicone, panos, estopa, etiquetas de identificação) — para 2 quadros | cj | 2,00 | 85,00 | 170,00 | Média 3 cotações |
| EQ. | — | Multímetro digital e torquímetro isolado (ferramental incluso na M.O.) | — | — | — | 47,80 | Incluso |
| | | **Custo Direto Total (Sem BDI)** | | | | **1.138,00** | |

### Justificativa dos Coeficientes — SRAES-SUB-004

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Eletricista | 14,00 h | 1 eletricista × 8h (QGBT) + 1 eletricista × 6h (QGBD) = 14 h-homem. O QGBD é menor que o QGBT mas demanda verificação do circuito de comutação rede/gerador. |
| Auxiliar de eletricista | 14,00 h | 1 auxiliar × 8h (QGBT) + 1 auxiliar × 6h (QGBD) = 14 h-homem. Apoio na identificação de circuitos, sinalização e limpeza. |
| Engenheiro eletricista | 2,00 h | Verificação conjunta do aterramento dos 2 quadros, teste funcional de comutação automática rede/gerador (QGBD) e emissão de parecer técnico. |
| Material de limpeza | 2,00 cj | 2 kits de consumíveis: um para cada quadro (QGBT e QGBD). |

---

## SRAES-SUB-005: Verificação de continuidade elétrica das malhas de aterramento do abrigo

**Unidade:** un | **Custo Total (Sem BDI): R$ 400,00**

**Escopo:** Verificação de continuidade elétrica das malhas de aterramento do abrigo da subestação, com medição de resistência de terra.

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | 88264 | Eletricista com encargos complementares | h | 4,00 | 26,18 | 104,72 | SINAPI-ES 02/2026 |
| M.O. | 88247 | Auxiliar de eletricista com encargos complementares | h | 4,00 | 20,93 | 83,72 | SINAPI-ES 02/2026 |
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — análise dos resultados e laudo | h | 1,00 | 130,33 | 130,33 | Própria (SINAPI-ES) |
| EQ. | COT-SUB-EQ-003 | Locação de terrômetro digital calibrado com certificado (rateio de diária) | cj | 1,00 | 81,23 | 81,23 | Média 3 cotações |
| | | **Custo Direto Total (Sem BDI)** | | | | **400,00** | |

### Justificativa dos Coeficientes — SRAES-SUB-005

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Eletricista | 4,00 h | 1 eletricista × 4h. Instalação das hastes auxiliares, medição e registro de resultados. |
| Auxiliar de eletricista | 4,00 h | 1 auxiliar × 4h. Apoio na cravação das hastes e esticamento de cabos. |
| Engenheiro eletricista | 1,00 h | Análise dos resultados das medições e emissão do laudo de aterramento. |
| Terrômetro | 1,00 cj | Rateio da diária de locação do terrômetro digital. |

---

## SRAES-SUB-006: Emissão de ART e Relatório Técnico

**Unidade:** un | **Custo Total (Sem BDI): R$ 1.648,00**

**Escopo:** Emissão de ART (Anotação de Responsabilidade Técnica) de manutenção preventiva junto ao CREA/ES; elaboração de relatório técnico completo com registro fotográfico e laudo das condições operacionais da subestação.

| Tipo | Código | Descrição do Insumo | Unid | Coef. | Custo Unit. (R$) | Custo Total (R$) | Fonte |
|------|--------|---------------------|------|-------|-------------------|-------------------|-------|
| M.O. | COMP-ENG-ELET | Engenheiro eletricista — elaboração de relatório técnico, compilação de ensaios e parecer conclusivo | h | 10,00 | 130,33 | 1.303,30 | Própria (SINAPI-ES) |
| SERV. | CREA-ES | Taxa de ART de manutenção — CREA/ES (faixa de contrato até R$ 15.000) | un | 1,00 | 247,43 | 247,43 | CREA-ES — Tabela 2026 |
| MAT. | — | Material de escritório, impressão e encadernação do relatório | cj | 1,00 | 50,00 | 50,00 | Estimativa |
| EQ. | — | Deslocamento de veículo leve (Vitória ida+volta) | km | 30,00 | 3,24 | 97,27 | SICRO3-ES |
| | | **Custo Direto Total (Sem BDI)** | | | | **1.648,00** | |

*Nota: A taxa de ART é um valor tabelado pelo CONFEA/CREA-ES, isento de BDI por ser recolhimento ao Conselho (repasse). No orçamento, o valor está incluído para fins de referência global, mas pode ser destacado na planilha final como custo administrativo.*

### Justificativa dos Coeficientes — SRAES-SUB-006

| Insumo | Coeficiente | Justificativa |
|--------|-------------|---------------|
| Engenheiro eletricista | 10,00 h | Compilação dos ensaios de Megger, análise de aterramento, edição do relatório fotográfico e parecer conclusivo. Equivalente a 1,25 dia de trabalho técnico. |
| ART CREA/ES | 1,00 un | Taxe fixa conforme tabela de emolumentos do CREA-ES para 2026 (faixa de contrato até R$ 15.000). |
| Deslocamento | 30,00 km | Ida e volta Vitória (15 km cada trecho). |

---

## Cotações de Mercado — Equipamentos e Materiais de Subestação

### COT-SUB-EQ-001 — Locação de Megôhmetro 5 kV (diária)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | Send Metrologia | (27) 3327-0291 | sendmetrologia.com.br | Vitória/ES | 320,00 |
| 2 | ESP Engenharia | (27) 3019-5500 | espengenharia.com.br | Vitória/ES | 350,00 |
| 3 | Gama Instrumentos | (11) 3672-8080 | gamainstruments.com.br | São Paulo/SP | 380,00 |
| | | | | **Média adotada:** | **R$ 350,00** |

### COT-SUB-EQ-002 — Alicate Amperímetro Digital True-RMS (rateio de locação)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | Send Metrologia | (27) 3327-0291 | sendmetrologia.com.br | Vitória/ES | 110,00 |
| 2 | ESP Engenharia | (27) 3019-5500 | espengenharia.com.br | Vitória/ES | 125,00 |
| 3 | Gama Instrumentos | (11) 3672-8080 | gamainstruments.com.br | São Paulo/SP | 133,22 |
| | | | | **Média adotada:** | **R$ 122,74** |

### COT-SUB-EQ-003 — Locação de Terrômetro Digital (rateio de diária)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | Send Metrologia | (27) 3327-0291 | sendmetrologia.com.br | Vitória/ES | 75,00 |
| 2 | ESP Engenharia | (27) 3019-5500 | espengenharia.com.br | Vitória/ES | 80,00 |
| 3 | Power Test | (11) 2385-1919 | powertest.com.br | São Paulo/SP | 88,70 |
| | | | | **Média adotada:** | **R$ 81,23** |

### COT-SUB-MAT-001 — Material de Limpeza Técnica (Chave Seccionadora)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | ECOCEL | (27) 99972-5722 | ecocel.com.br | Vitória/ES | 120,00 |
| 2 | Top Limp Vix | (27) 3029-4335 | toplimponline.com.br | Vitória/ES | 135,00 |
| 3 | Tecnopar Brasil | (27) consultar | tecnoparbrasil.com.br | Serra/ES | 149,77 |
| | | | | **Média adotada:** | **R$ 134,92** |

### COT-SUB-MAT-002 — Material de Limpeza para Transformador a Seco

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | ECOCEL | (27) 99972-5722 | ecocel.com.br | Vitória/ES | 150,00 |
| 2 | ESP Engenharia | (27) 3019-5500 | espengenharia.com.br | Vitória/ES | 165,00 |
| 3 | Top Limp Vix | (27) 3029-4335 | toplimponline.com.br | Vitória/ES | 180,00 |
| | | | | **Média adotada:** | **R$ 165,00** |

### COT-SUB-MAT-003 — Torquímetro e Chaves Isoladas VDE (rateio)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | Vimetal | (27) 3398-2222 | vimetal.com.br | Serra/ES | 70,00 |
| 2 | Ferragens Ipiranga | (27) consultar | ferragensipiranga.com.br | Vila Velha/ES | 78,07 |
| 3 | Tecnopar Brasil | (27) consultar | tecnoparbrasil.com.br | Serra/ES | 88,00 |
| | | | | **Média adotada:** | **R$ 78,69** |

### COT-SUB-MAT-004 — Material de Limpeza e Lubrificação (Banco de Capacitores)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | ECOCEL | (27) 99972-5722 | ecocel.com.br | Vitória/ES | 85,00 |
| 2 | Top Limp Vix | (27) 3029-4335 | toplimponline.com.br | Vitória/ES | 95,00 |
| 3 | Rocha Prod. de Limpeza | (27) 3029-3305 | rochaplimpeza.com.br | Vitória/ES | 105,00 |
| | | | | **Média adotada:** | **R$ 95,00** |

### COT-SUB-MAT-005 — Material de Limpeza e Lubrificação (QGBT + QGBD — por quadro)

| # | Empresa | Telefone | Site | Cidade | Cotação (R$) |
|---|---------|----------|------|--------|--------------|
| 1 | ECOCEL | (27) 99972-5722 | ecocel.com.br | Vitória/ES | 75,00 |
| 2 | Top Limp Vix | (27) 3029-4335 | toplimponline.com.br | Vitória/ES | 85,00 |
| 3 | Rocha Prod. de Limpeza | (27) 3029-3305 | rochaplimpeza.com.br | Vitória/ES | 95,00 |
| | | | | **Média adotada (por quadro):** | **R$ 85,00** |

*Nota: Quantidade adotada = 2 cj (1 QGBT + 1 QGBD) = R$ 170,00 total.*

---

## Resumo Geral das Composições — Subestação (Atualizado SINAPI 04/2026)

| Item | Código | Descrição | Sem BDI (R$) | Com BDI 25% (R$) |
|------|--------|-----------|-------------|-------------------|
| 3.1 | SRAES-SUB-001 | Chave Seccionadora 15 kV | 2.203,38 | 2.754,22 |
| 3.2 | SRAES-SUB-002 | Transformador a Seco (×2) | 3.065,06 | 3.831,32 |
| 3.3 | SRAES-SUB-003 | Banco de Capacitores | 1.191,89 | 1.489,86 |
| 3.4 | SRAES-SUB-004 | QGBT + QGBD (Transferência de Carga Gerador) | 1.306,91 | 1.633,63 |
| 3.5 | SRAES-SUB-005 | Aterramento do Abrigo | 510,84 | 638,55 |
| 4.1 | SRAES-SUB-006 | ART + Relatório Técnico | 1.700,58 | 2.125,72 |
| | | **TOTAL SUBESTAÇÃO** | **R$ 9.978,66** | **R$ 12.473,30** |

---

*Nota 1: Todos os insumos de M.O. utilizam preços do SINAPI 04/2026 ES (desonerado). O código 91677 (Engenheiro Eletricista) foi desativado pelo SINAPI; utilizou-se composição própria baseada no SINAPI 90778 + 15%.*
*Nota 2: Equipamentos de medição (megôhmetro, terrômetro, amperímetro) cotados preferencialmente na Grande Vitória (Send Metrologia, ESP Engenharia) e complementados com cotação em São Paulo (Gama Instrumentos, Power Test).*
*Nota 3: A proposta da ECOCEL (R$ 8.260,00 global) foi utilizada como parâmetro de validação. Com os preços atualizados (SINAPI 04/2026), o orçamento sem BDI da subestação (R$ 9.978,66) reflete a atualização de referencial e inclusão do QGBD.*

_______________________________________________________________
Luis Fernando
Setor de Engenharia
