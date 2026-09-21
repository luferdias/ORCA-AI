# Especificação Detalhada e Composição Analítica — Item 3.1

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Item da Planilha Sintética:** **3.1**  
> **Código da Composição Própria:** **COMP-CAG-03**  
> **Unidade de Medida:** **m² (metro quadrado de passarela montada)**  
> **Quantidade:** **2,00 m²**  
> **Taxa de BDI:** **25,00%**  

---

## 📝 Descrição Resumida Detalhada (Memorial Descritivo do Item)

**ITEM 3.1 — FORNECIMENTO E MONTAGEM DE PASSARELA METÁLICA PARA ACESSO E MANUTENÇÃO NA CAG**

Fornecimento, fabricação, transporte e montagem de passarela metálica elevada para acesso, inspeção e manutenção dos equipamentos na Central de Água Gelada (CAG), promovendo um prolongamento de 2,00 metros em relação à estrutura existente, construída rigorosamente conforme as especificações do projeto executivo e Relação de Peças de 20/07/2026.

A estrutura de suporte da passarela é composta por vigas de sustentação em perfil laminado tipo "I" de aço carbono de 4" (1 coluna perfil I 4" de 2,85 m, 3 perfis I 4" de 0,80 m e 2 perfis I 4" de 1,50 m), perfeitamente niveladas e soldadas. O piso possui sistema duplo de revestimento: sub-base estrutural em chapa lisa de aço carbono de 4 mm e piso superior antiderrapante em chapa xadrez de alumínio de 2 mm de espessura com bordas rebatidas/dobradas de acabamento.

O conjunto inclui guarda-corpo de proteção coletiva em tubos de aço galvanizado de 1" com altura mínima de 1,10 m (dimensões 1,05 x 1,10 m, 3 vãos), rodapé metálico de proteção com altura de 15 cm nas bordas livres e 01 (uma) escada metálica de acesso com 1,30 m de comprimento e degraus de 20 cm.

Toda a estrutura metálica receberá tratamento de superfície contra corrosão e pintura protetora anticorrosiva com tinta alcatrão de hulha bicomponente (Coal Tar Epóxi), com espessura de filme seco de 100 μm. A medição será por metro quadrado (`m²`) de passarela efetivamente instalada (2,00 m²). Atendimento às normas ABNT NBR 8800, NBR 14762 e NR-12.

---

## 📋 Ficha Técnica no Padrão `modelo-item-orcamentario`

```yaml
item:
  numero: "3.1"
  codigo: "COMP-CAG-03"
  sistema: "SINAPI / EMOP"
  descricao: >
    Fornecimento e montagem de passarela metálica para acesso e manutenção na CAG, com prolongamento de 2m.
    Estrutura em vigas perfil I 4", revestimento em chapa lisa 4mm + chapa xadrez de alumínio 2mm antiderrapante,
    guarda-corpo em tubo galvanizado h=1,10m, rodapé 15cm, escada de acesso e pintura alcatrão de hulha.
  unidade: "m²"
  quantidade: 2.00
  custo_unitario_sem_bdi: 1433.30
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 1791.62
  preco_total_com_bdi: 3583.25
  fonte:
    nome: "Composição Própria (SINAPI-ES + EMOP 050104 + Cotações)"
    data_base: "07/2026"
    arquivo_referencia: "Relação de peças para restauração da CAG .20.07. 2026.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Garante trânsito seguro da equipe de manutenção conforme NR-12."
```

---

## 📊 Composição Analítica de Preço Unitário (CPU) — Item 3.1

> **Unidade de Referência:** 1,00 m² | **Custo Direto Unitário s/ BDI:** R$ 1.433,30 / m² | **Preço Unitário c/ BDI (25%):** R$ 1.791,62 / m²  
> **Custo Direto Total (2,00 m²):** R$ 2.866,60 | **Preço Total com BDI (25%):** R$ 3.583,25

### 1. Insumos e Materiais (por m² de Passarela)

| Código | Descrição do Insumo / Material | Unid. | Coeficiente (por m²) | Custo Unitário s/ BDI (R$) | Custo por m² s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 44210 | Perfil de aço laminado "I" 4" (15,4 kg/m) — Estrutura | kg | 30,00 | 9,51 | 285,30 | SINAPI-ES |
| SINAPI 43057 | Chapa de aço carbono lisa e=4,0 mm — Sub-base estrutural | kg | 31,40 | 8,40 | 263,76 | SINAPI-ES |
| EMOP 050104 | Chapa xadrez de alumínio 2,0 mm antiderrapante — Piso | m² | 1,25 | 380,00 | 475,00 | EMOP / Cotação |
| SINAPI 43102 | Tubo de aço galvanizado 1" (para guarda-corpo) | m | 3,50 | 22,40 | 78,40 | SINAPI-ES |
| SINAPI 95241 | Eletrodo revestido E7018 3,25 mm para solda elétrica | kg | 1,50 | 37,92 | 56,88 | SINAPI-ES |
| SINAPI 100772| Tinta epóxi alcatrão de hulha bicomponente (Coal Tar) | m² | 3,00 | 52,41 | 157,23 | SINAPI-ES |
| **SUBTOTAL MATERIAIS** | | | | | **R$ 1.316,57** | |

### 2. Mão de Obra Direta (por m² de Passarela)

| Código | Categoria Profissional | Unid. | Coeficiente (Horas/m²) | Custo Horário s/ BDI (R$) | Custo por m² s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 88315 | Serralheiro com encargos complementares | h | 2,50 | 24,39 | 60,98 | SINAPI-ES (07/2026) |
| SINAPI 88316 | Ajudante de serralheiro com encargos complementares | h | 2,50 | 18,26 | 45,65 | SINAPI-ES (07/2026) |
| **SUBTOTAL MÃO DE OBRA** | | | | | **R$ 106,63** | |

### 3. Equipamentos e Ferramentas (por m² de Passarela)

| Código | Equipamento / Ferramenta | Unid. | Coeficiente | Custo Unitário s/ BDI (R$) | Custo por m² s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 14120 | Máquina de solda elétrica 400A (locação) | h prod | 0,40 | 15,20 | 6,08 | SINAPI-ES |
| SINAPI 14119 | Lixadeira / Esmerilhadeira elétrica (locação) | h prod | 0,67 | 5,97 | 4,02 | SINAPI-ES |
| **SUBTOTAL EQUIPAMENTOS** | | | | | **R$ 10,10** | |

---

### 💵 Resumo Consolidação do Item 3.1 (2,00 m²)

| Componente de Custo | Custo Unitário (R$/m²) | Valor Total sem BDI (R$) | % do Custo Direto | Valor Total com BDI 25% (R$) |
| :--- | :---: | :---: | :---: | :---: |
| Insumos e Materiais | R$ 1.316,57 | R$ 2.633,14 | 91,86% | R$ 3.291,43 |
| Mão de Obra Direta | R$ 106,63 | R$ 213,26 | 7,44% | R$ 266,58 |
| Equipamentos e Ferramentas | R$ 10,10 | R$ 20,20 | 0,70% | R$ 25,25 |
| **CUSTO DIRETO TOTAL (Sem BDI)** | **R$ 1.433,30** | **R$ 2.866,60** | **100,00%** | — |
| **BDI (25,00%)** | **R$ 358,32** | **R$ 716,65** | — | — |
| **PREÇO TOTAL DO ITEM 3.1 (Com BDI)** | **R$ 1.791,62** | — | — | **R$ 3.583,25** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Medição realizada por metro quadrado (`m²`) de passarela completamente montada, instalada e pintada.
2. **Segurança e Rigidez:** Verificação da estabilidade estrutural sob carga distribuída de no mínimo 300 kg/m² e resistência do guarda-corpo a esforço horizontal de 100 kgf/m conforme NR-12.
3. **Pintura e Acabamento:** Inspeção da espessura do filme seco da pintura epóxi alcatrão de hulha (mínimo 100 μm) e ausência de rebarbas.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise a especificação detalhada e os insumos do **Item 3.1 (COMP-CAG-03)** acima.  
> Assim que aprovado, prosseguiremos para os **Itens do Grupo 4.0 — Reforma e Adequação do Guindaste (Grua)**!
