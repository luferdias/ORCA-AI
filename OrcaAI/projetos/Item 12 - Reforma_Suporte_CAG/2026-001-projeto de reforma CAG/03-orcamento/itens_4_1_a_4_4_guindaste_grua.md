# Especificação Detalhada e Composição Analítica — Grupo 4.0 (Itens 4.1 a 4.4)

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Grupo de Serviços:** **4.0 — REFORMA E ADEQUAÇÃO DO GUINDASTE (GRUA) DA CAG**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI (Grupo 4.0):** **R$ 7.499,70**  
> **Valor Total do Grupo 4.0 (com BDI 25%):** **R$ 9.375,13**  

---

## 📝 Memorial Descritivo Detalhado — Grupo 4.0

### **ITEM 4.1 — GUINDASTE DE MANUTENÇÃO DA CAG (GRUA), FORNECIMENTO E INSTALAÇÃO (COMP-CAG-04)**
Fornecimento, adaptação e instalação completa do guindaste mecânico de manutenção (grua) da Central de Água Gelada (CAG), construído conforme Detalhe 04 / Projeto do Guindaste e Relação de Peças de 20/07/2026.
* **Prolongamento do Braço:** Extensão de 2,00 metros utilizando viga em perfil laminado tipo "I" de 100 mm (4" x 2" de alma) em aço carbono ASTM A36, soldada continuamente à estrutura metálica existente.
* **Sistema de Tracionamento e Cabos:** Fornecimento e passagem de novo cabo de aço galvanizado antiderrapante especial para içamento pesado com alma de aço, alças de tração reforçadas, manilhas e regulador de tensão (esticador industrial tracionador).
* **Caixa de Contrapeso:** Fabricação de caixa estanque em chapa de aço carbono de 4,75 mm com dimensões de 500 mm de largura x 700 mm de comprimento x 300 mm de altura (0,50 x 0,70 x 0,30 m), preenchida com concreto aditivado C20, resultando em massa total aproximada de 280 kg, posicionada para manter livre movimentação ao longo do braço de alavanca.
* **Base de Fixação e Tubo Vertical:** Base quadrada de ancoragem em chapa de aço carbono de 400 x 400 mm com espessura de 5/8" (15,875 mm), fixada à estrutura por chumbadores de expansão, e tubo externo de apoio em aço carbono de diâmetro nominal 8" com folga ajustada.

### **ITEM 4.2 — APLICAÇÃO DE 3 FLANGES EM AÇO CARBONO H=30MM EM TUBO DN 8" (COMP-CAG-05)**
Fabricação, usinagem e aplicação de 03 (três) flanges circulares em aço carbono com altura de 30 mm (H=30mm) e diâmetro compatível com tubo de 8" (203,2 mm). O conjunto compreende 02 (duas) flanges fixas soldadas continuamente em toda a circunferência do tubo externo (uma na extremidade superior e uma na extremidade inferior) e 01 (uma) flange solta intermediária posicionada entre as flanges fixas, garantindo alinhamento axial rigoroso e folga máxima de rotação entre tubos de 1,0 cm.

### **ITEM 4.3 — SUBSTITUIÇÃO DE TUBO GUIA INTERNO EM AÇO CARBONO DN 8" L=5,0M (COMP-CAG-06)**
Remoção do tubo danificado existente e substituição por novo tubo guia interno estrutural em aço carbono de diâmetro nominal 8" (203,2 mm), comprimento total de 5,00 metros. O serviço inclui corte térmico de precisão, tamponamento/fechamento hermético das extremidades superior e inferior com chapa de aço soldada, posicionamento plumbado e soldagem elétrica contínua da extremidade inferior à base metálica fixa existente.

### **ITEM 4.4 — INSTALAÇÃO DE ORIFÍCIO PARA LUBRIFICAÇÃO COM NIPLE E TAMPÃO 1/2" (COMP-CAG-07)**
Execução de furo de precisão de diâmetro 1/2" (12,7 mm) com inclinação de 45 graus no tubo de aço carbono da grua, rosqueamento e soldagem de 01 (um) niple em aço carbono de 1/2" equipado com tampão roscado de 1/2" de fechamento, posicionado estrategicamente para inserção de graxa e lubrificação periódica do conjunto rotativo.

---

## 📋 Fichas Técnicas no Padrão `modelo-item-orcamentario`

```yaml
# ITEM 4.1
item:
  numero: "4.1"
  codigo: "COMP-CAG-04"
  sistema: "SINAPI / COTAÇÃO LOCAL"
  descricao: >
    Guindaste de manutenção da CAG (Grua): prolongamento do braço em perfil I 100mm (2,00m), novo cabo de aço,
    tracionador, caixa de contrapeso em aço com concreto C20 (~280 kg, 500x700x300mm), base 400x400x15,875mm e tubos 8".
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 4269.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 5336.25
  preco_total_com_bdi: 5336.25
  fonte: {nome: "Composição Própria", data_base: "07/2026", arquivo_referencia: "guindaste da CAG.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Equipamento para movimentação de cargas pesadas na CAG."

# ITEM 4.2
item:
  numero: "4.2"
  codigo: "COMP-CAG-05"
  sistema: "SINAPI-ES"
  descricao: >
    Aplicação de 3 flanges em aço carbono H=30mm soldadas em tubo de aço carbono DN 8" (203,2mm),
    sendo 2 flanges fixas e 1 flange solta intermediária com folga máxima de 1cm.
  unidade: "un"
  quantidade: 3.00
  custo_unitario_sem_bdi: 320.20
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 400.25
  preco_total_com_bdi: 1200.75
  fonte: {nome: "SINAPI-ES", data_base: "07/2026", arquivo_referencia: "detalhe da movimentação do guindaste CAG.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Folga de rotação ajustada em no máximo 1cm."

# ITEM 4.3
item:
  numero: "4.3"
  codigo: "COMP-CAG-06"
  sistema: "SINAPI-ES"
  descricao: >
    Substituição de tubo guia interno em aço carbono DN 8" L=5,0m para grua, com tamponamento de extremidades e solda à base.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 2209.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 2761.25
  preco_total_com_bdi: 2761.25
  fonte: {nome: "SINAPI-ES", data_base: "07/2026", arquivo_referencia: "detalhe da movimentação do guindaste CAG.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Substituição completa do tubo de 5 metros."

# ITEM 4.4
item:
  numero: "4.4"
  codigo: "COMP-CAG-07"
  sistema: "SINAPI-ES"
  descricao: >
    Instalação de orifício para lubrificação com niple e tampão de 1/2" soldado (inclinação 45°) em tubo de 8".
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 61.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 76.88
  preco_total_com_bdi: 76.88
  fonte: {nome: "SINAPI-ES", data_base: "07/2026", arquivo_referencia: "detalhe da movimentação do guindaste CAG.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Com tampão roscado de 1/2\"."
```

---

## 📊 Tabela Consolidada de Composição — Grupo 4.0

| Item | Código | Descrição | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | Total s/ BDI (R$) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **4.1** | COMP-CAG-04 | Guindaste de manutenção (grua), braço I 100mm, contrapeso 280kg | un | 1,00 | 4.269,00 | 4.269,00 | 5.336,25 | 5.336,25 |
| **4.2** | COMP-CAG-05 | Aplicação de 3 flanges em aço carbono H=30mm soldadas em tubo DN 8" | un | 3,00 | 320,20 | 960,60 | 400,25 | 1.200,75 |
| **4.3** | COMP-CAG-06 | Substituição de tubo guia interno em aço carbono DN 8" L=5,0m | un | 1,00 | 2.209,00 | 2.209,00 | 2.761,25 | 2.761,25 |
| **4.4** | COMP-CAG-07 | Orifício de lubrificação com niple e tampão 1/2" em tubo da grua | un | 1,00 | 61,50 | 61,50 | 76,88 | 76,88 |
| **TOTAL**| | **SUBTOTAL DO GRUPO 4.0** | | | | **R$ 7.499,70** | | **R$ 9.375,13** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Mediçoes individuais por unidade (`un`) após montagem, fixação das flanges e tamponamento do tubo guia.
2. **Teste de Carga e Giro:** Teste de rotação 360° sem engasgos sob carga nominal de teste e verificação de rotação das flanges com folga máxima de 1 cm.
3. **Estanqueidade e Lubrificação:** Injeção de graxa no niple 1/2" para comprovar preenchimento correto da junta rotativa.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise as especificações e composições dos **Itens 4.1 a 4.4 (Grupo 4.0)** acima.  
> Assim que aprovado, prosseguiremos para o **Grupo 5.0 — Estrutura de Sustentação dos Módulos do Chiller, Compressores e Tanques (Itens 5.1 a 5.6)**!
