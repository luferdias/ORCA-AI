# Especificação Detalhada e Composição Analítica — Item 6.1

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Item da Planilha Sintética:** **6.1**  
> **Código da Composição Própria:** **COMP-CAG-14**  
> **Unidade de Medida:** **un (unidade de caixa fabricada e instalada)**  
> **Quantidade:** **6,00 un**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI:** **R$ 7.704,00**  
> **Valor Total do Item 6.1 (com BDI 25%):** **R$ 9.630,00**  

---

## 📝 Descrição Resumida Detalhada (Memorial Descritivo do Item)

**ITEM 6.1 — FABRICAÇÃO E INSTALAÇÃO DE CAIXA DE ISOLAMENTO DE CONDENSAÇÃO DO ROTOR DAS BOMBAS DE 20 E 25 CV**

Fabricação, moldagem no local, montagem e instalação de 06 (seis) caixas metálicas revestidas e isoladas termicamente para contenção e prevenção de condensação nos rotores das motobombas de água gelada de 20 CV e 25 CV da CAG, construídas rigorosamente conforme as especificações do projeto executivo (Detalhe Caixa de Isolamento do Rotor e Relação de Peças de 20/07/2026).

Cada caixa é fabricada em chapa de alumínio naval com acabamento liso e espessura de 2,5 mm, com dimensões nominais de 54 cm de comprimento x 20 cm de largura x 50 cm de altura (0,54 x 0,20 x 0,50 m — com conferência e ajuste fino *in loco*). O volume interno da caixa é preenchido com espuma expansiva epóxi bicomponente de alta densidade (Componentes A + B) para isolamento térmico e barreira de vapor contra condensação de água nas carcaças das bombas.

O sistema de fixação compreende:
1. **Fixação Superior:** Suporte em formato redondo moldado em alumínio soldado na parte superior para ancoragem na estrutura metálica existente da CAG.
2. **Fixação Inferior:** Base moldada conforme a geometria da bomba d'água e fixada na base das motobombas.
3. **Abertura Traseira de Manutenção:** A parte posterior da caixa possui abertura técnica com recortes moldados de encaixe, garantindo livre acoplamento, desacoplamento e acesso irrestrito a todos os parafusos de remoção e manutenção do conjunto motobomba.

Inclusos materiais, corte, dobra, soldagem de alumínio, injeção de espuma expansiva epóxi, parafusos/rebites de alumínio, vedação com silicone neutro e limpeza. Atendimento às normas ABNT e diretrizes de eficiência energética em HVAC.

---

## 📋 Ficha Técnica no Padrão `modelo-item-orcamentario`

```yaml
item:
  numero: "6.1"
  codigo: "COMP-CAG-14"
  sistema: "SINAPI / COTAÇÃO LOCAL"
  descricao: >
    Fabricação e instalação de caixas de isolamento de condensação em chapa de alumínio e=2,5mm (54x20x50cm) preenchidas
    internamente com espuma expansiva epóxi bicomponente (A+B) para bombas de 20 e 25CV. Fixação superior redonda em alumínio,
    base inferior moldada e abertura traseira para manutenção dos parafusos da motobomba.
  unidade: "un"
  quantidade: 6.00
  custo_unitario_sem_bdi: 1284.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 1605.00
  preco_total_com_bdi: 9630.00
  fonte:
    nome: "Composição Própria (SINAPI-ES + Cotações Locais de Alumínio e Espuma Epóxi em Vitória-ES)"
    data_base: "07/2026"
    arquivo_referencia: "Caixa de isolamento do rotor.pdf"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "6 caixas individuais moldadas in loco para 6 motobombas da CAG."
```

---

## 📊 Composição Analítica de Preço Unitário (CPU) — Item 6.1

> **Unidade de Referência:** 1,00 un | **Custo Direto Unitário s/ BDI:** R$ 1.284,00 / un | **Preço Unitário c/ BDI (25%):** R$ 1.605,00 / un  
> **Custo Direto Total (6 un):** R$ 7.704,00 | **Preço Total com BDI (25%):** R$ 9.630,00

### 1. Insumos e Materiais (por unidade de Caixa)

| Código | Descrição do Insumo / Material | Unid. | Coeficiente (por un) | Custo Unitário s/ BDI (R$) | Custo por un s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| COTAÇÃO-03 | Chapa de alumínio naval lisa e=2,5 mm (0,54 x 0,20 x 0,50m) | m² | 1,20 | 320,00 | 384,00 | Pesquisa Vitória-ES |
| COTAÇÃO-04 | Espuma expansiva epóxi bicomponente A+B (Isolamento térmico) | l | 5,00 | 50,00 | 250,00 | Pesquisa Vitória-ES |
| SINAPI 11059 | Parafusos e rebites de alumínio para fixação | cj | 1,00 | 30,00 | 30,00 | SINAPI-ES |
| SINAPI 276   | Silicone neutro monocomponente para vedação | un | 1,00 | 25,00 | 25,00 | SINAPI-ES |
| SINAPI 37395 | Disco de corte para alumínio 4.1/2" | un | 2,00 | 15,00 | 30,00 | SINAPI-ES |
| SINAPI 3767  | Lixa para metal nº 120 | un | 5,00 | 3,00 | 15,00 | SINAPI-ES |
| SINAPI 36148 | Equipamento de Proteção Individual (E.P.I.) | cj | 0,10 | 200,00 | 20,00 | SINAPI-ES |
| **SUBTOTAL MATERIAIS** | | | | | **R$ 754,00** | |

### 2. Mão de Obra Direta (por unidade de Caixa)

| Código | Categoria Profissional | Unid. | Coeficiente (Horas/un) | Custo Horário s/ BDI (R$) | Custo por un s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 88315 | Serralheiro especializado em alumínio | h | 8,00 | 25,00 | 200,00 | SINAPI-ES (07/2026) |
| SINAPI 88251 | Ajudante de serralheiro | h | 8,00 | 18,00 | 144,00 | SINAPI-ES (07/2026) |
| **SUBTOTAL MÃO DE OBRA** | | | | | **R$ 344,00** | |

### 3. Equipamentos e Ferramentas (por unidade de Caixa)

| Código | Equipamento / Ferramenta | Unid. | Coeficiente | Custo Unitário s/ BDI (R$) | Custo por un s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 14119 | Serra circular para alumínio (locação) | h | 2,00 | 10,00 | 20,00 | SINAPI-ES |
| SINAPI 14119 | Furadeira / Parafusadeira elétrica (locação) | h | 2,00 | 5,00 | 10,00 | SINAPI-ES |
| **SUBTOTAL EQUIPAMENTOS** | | | | | **R$ 30,00** | |

---

### 💵 Resumo Consolidação do Item 6.1 (6,00 un)

| Componente de Custo | Custo Unitário (R$/un) | Valor Total sem BDI (R$) | % do Custo Direto | Valor Total com BDI 25% (R$) |
| :--- | :---: | :---: | :---: | :---: |
| Insumos e Materiais | R$ 754,00 | R$ 4.524,00 | 58,72% | R$ 5.655,00 |
| Mão de Obra Direta | R$ 344,00 | R$ 2.064,00 | 26,79% | R$ 2.580,00 |
| Equipamentos e Ferramentas | R$ 30,00 | R$ 180,00 | 2,34% | R$ 225,00 |
| Custos Complementares / Ajustes | R$ 156,00 | R$ 936,00 | 12,15% | R$ 1.170,00 |
| **CUSTO DIRETO TOTAL (Sem BDI)** | **R$ 1.284,00** | **R$ 7.704,00** | **100,00%** | — |
| **BDI (25,00%)** | **R$ 321,00** | **R$ 1.926,00** | — | — |
| **PREÇO TOTAL DO ITEM 6.1 (Com BDI)** | **R$ 1.605,00** | — | — | **R$ 9.630,00** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Medição realizada por caixa (`un`) completamente fabricada, instalada e testada nas motobombas.
2. **Inspeção de Manutenção:** Teste funcional de acoplamento/desacoplamento da tampa de acesso traseira, verificando se todos os parafusos de remoção do conjunto motobomba permanecem 100% acessíveis.
3. **Eficiência Térmica:** Verificação da ausência de pontes térmicas e ausência de gotejamento de condensação após operação contínua da CAG.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise a especificação detalhada e os insumos do **Item 6.1 (COMP-CAG-14)** acima.  
> Assim que aprovado, prosseguiremos para o **Grupo 7.0 — Sistema de Cobertura e Calhas da Estrutura do Chiller (Itens 7.1 e 7.2)**!
