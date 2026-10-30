# Especificação Detalhada e Composição Analítica — Item 2.1

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Item da Planilha Sintética:** **2.1**  
> **Código da Composição Própria:** **COMP-CAG-02**  
> **Unidade de Medida:** **kg (quilograma de aço instalado)**  
> **Quantidade:** **450,00 kg**  
> **Taxa de BDI:** **25,00%**  

---

## 📝 Descrição Resumida Detalhada (Memorial Descritivo do Item)

**ITEM 2.1 — FORNECIMENTO E MONTAGEM DE ESTRUTURA METÁLICA PARA SUPORTE DO CARRINHO E TRILHOS NA CAG**

Fornecimento, fabricação, transporte e montagem de estrutura metálica aérea/terrestre para suporte e guia do carrinho de movimentação de cargas na Central de Água Gelada (CAG), constituída rigorosamente conforme as especificações do projeto executivo (Detalhes da Estrutura/Guindaste e Relação de Peças de 20/07/2026).

A estrutura de suporte é composta por vigas em perfil laminado tipo "I" de aço carbono de 3" (8 vigas de 1,73 m de comprimento e 2 longarinas de 10,20 m de comprimento), travadas inferiormente e interligadas. Sobre a mesa superior dos perfis "I" é soldado continuamente o trilho de rolamento em barra redonda maciça de aço carbono de 3/4" (19,05 mm de diâmetro), totalizando 12,00 metros de trilhos direcionais.

O conjunto inclui guias de alinhamento lateral e travamento em barra chata de aço carbono de 1" x 1/8" (25,4 mm x 3,18 mm), batentes de fim de curso em chapa/barra chata reforçada, placas de apoio e chumbadores de expansão/parabolts de 1/2" para ancoragem estrutural nas vigas/lajes de concreto da CAG.

Toda a estrutura metálica receberá preparação de superfície por jateamento/limpeza mecânica rigorosa e pintura de proteção anticorrosiva especial com tinta alcatrão de hulha bicomponente (Coal Tar Epóxi, similar à marca Internacional), aplicada em 2 demãos com espessura de filme seco de no mínimo 100 μm. A medição será realizada pelo peso teórico efetivo dos perfis, barras, trilhos e elementos de conexão instalados (450,00 kg). Atendimento integral às normas ABNT NBR 8800 e NBR 14762.

---

## 📋 Ficha Técnica no Padrão `modelo-item-orcamentario`

```yaml
item:
  numero: "2.1"
  codigo: "COMP-CAG-02"
  sistema: "SINAPI-ES"
  descricao: >
    Fornecimento e montagem de estrutura metálica para suporte de carrinho de movimentação de cargas em CAG,
    constituída por vigas perfil I de 3" (8x1,73m e 2x10,20m), trilho em barra redonda maciça de 3/4" (12m total),
    guias e batentes em barra chata 1" x 1/8", elementos de fixação e pintura anticorrosiva de alcatrão de hulha bicomponente.
  unidade: "kg"
  quantidade: 450.00
  custo_unitario_sem_bdi: 17.47
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 21.84
  preco_total_com_bdi: 9826.87
  fonte:
    nome: "Composição Própria baseada em SINAPI-ES (43082, 43148, 43059, 95241, 102494, 88315)"
    data_base: "07/2026"
    arquivo_referencia: "guindaste da CAG.pdf"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Massa calculada para 450 kg de aço efetivamente instalado com tratamento anticorrosivo."
```

---

## 📊 Composição Analítica de Preço Unitário (CPU) — Item 2.1

> **Unidade de Referência:** 1,00 kg | **Custo Direto Unitário s/ BDI:** R$ 17,47 / kg | **Preço Unitário c/ BDI (25%):** R$ 21,84 / kg  
> **Custo Direto Total (450 kg):** R$ 7.861,50 | **Preço Total com BDI (25%):** R$ 9.826,87

### 1. Insumos e Materiais (por kg de Aço Estrutural)

| Código | Descrição do Insumo / Material | Unid. | Coeficiente (por kg) | Custo Unitário s/ BDI (R$) | Custo por kg s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 43082 | Perfil de aço laminado "I" de 3" (8x1,73m + 2x10,20m) | kg | 0,7111 | 10,91 | 7,76 | SINAPI-ES |
| SINAPI 43148 | Barra de aço carbono redonda maciça 3/4" (trilhos) | kg | 0,1022 | 9,93 | 1,01 | SINAPI-ES |
| SINAPI 43059 | Barra chata de aço carbono 1" x 1/8" (guias/batentes) | kg | 0,0667 | 9,13 | 0,61 | SINAPI-ES |
| SINAPI 95241 | Eletrodo revestido E7018 3,25 mm para solda elétrica | kg | 0,0422 | 37,92 | 1,60 | SINAPI-ES |
| SINAPI 102494| Pintura protetora em alcatrão de hulha bicomponente | m² | 0,1333 | 14,61 | 1,95 | SINAPI-ES |
| SINAPI 4322  | Chumbador de expansão / Parabolt 1/2" x 4" | un | 0,0355 | 7,91 | 0,28 | SINAPI-ES |
| **SUBTOTAL MATERIAIS** | | | | | **R$ 13,22** | |

### 2. Mão de Obra Direta (por kg de Aço Estrutural)

| Código | Categoria Profissional | Unid. | Coeficiente (Horas/kg) | Custo Horário s/ BDI (R$) | Custo por kg s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 88315 | Serralheiro com encargos complementares | h | 0,0889 | 24,39 | 2,17 | SINAPI-ES (07/2026) |
| SINAPI 88316 | Ajudante de serralheiro com encargos complementares | h | 0,0889 | 18,26 | 1,62 | SINAPI-ES (07/2026) |
| **SUBTOTAL MÃO DE OBRA** | | | | | **R$ 3,79** | |

### 3. Equipamentos e Ferramentas (por kg de Aço Estrutural)

| Código | Equipamento / Ferramenta | Unid. | Coeficiente | Custo Unitário s/ BDI (R$) | Custo por kg s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 14120 | Máquina de solda elétrica 400A (locação) | h prod | 0,0178 | 15,20 | 0,27 | SINAPI-ES |
| SINAPI 14119 | Lixadeira / Esmerilhadeira elétrica (locação) | h prod | 0,0320 | 5,97 | 0,19 | SINAPI-ES |
| **SUBTOTAL EQUIPAMENTOS** | | | | | **R$ 0,46** | |

---

### 💵 Resumo Consolidação do Item 2.1 (450,00 kg)

| Componente de Custo | Custo Unitário (R$/kg) | Valor Total sem BDI (R$) | % do Custo Direto | Valor Total com BDI 25% (R$) |
| :--- | :---: | :---: | :---: | :---: |
| Insumos e Materiais | R$ 13,22 | R$ 5.949,00 | 75,67% | R$ 7.436,25 |
| Mão de Obra Direta | R$ 3,79 | R$ 1.705,50 | 21,69% | R$ 2.131,88 |
| Equipamentos e Ferramentas | R$ 0,46 | R$ 207,00 | 2,64% | R$ 258,75 |
| **CUSTO DIRETO TOTAL (Sem BDI)** | **R$ 17,47** | **R$ 7.861,50** | **100,00%** | — |
| **BDI (25,00%)** | **R$ 4,37** | **R$ 1.965,37** | — | — |
| **PREÇO TOTAL DO ITEM 2.1 (Com BDI)** | **R$ 21,84** | — | — | **R$ 9.826,87** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** A medição será realizada por quilograma (`kg`) de aço estrutural efetivamente instalado e fixado, com base no peso teórico dos perfis, barras e placas de ancoragem.
2. **Nivelamento e Alinhamento:** Verificação do nivelamento dos trilhos com tolerância máxima de 1 mm por metro linear para garantir o deslizamento sem travamentos.
3. **Inspeção de Solda e Ancoragem:** Ensaio visual e com líquido penetrante nas soldas contínuas dos trilhos e teste de arrancamento/torque nos parabolts.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise a especificação detalhada e os insumos do **Item 2.1 (COMP-CAG-02)** acima.  
> Assim que aprovado, prosseguiremos imediatamente para a construção do **Item 3.1 (Passarela Metálica de Acesso e Manutenção)**!
