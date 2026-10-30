# Especificação Detalhada e Composição Analítica — Grupo 5.0 (Itens 5.1 a 5.6)

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Grupo de Serviços:** **5.0 — ESTRUTURA DE SUSTENTAÇÃO DOS MÓDULOS DO CHILLER, COMPRESSORES E TANQUES**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI (Grupo 5.0):** **R$ 74.775,96**  
> **Valor Total do Grupo 5.0 (com BDI 25%):** **R$ 93.469,95**  

---

## 📝 Memorial Descritivo Detalhado — Grupo 5.0

### **ITEM 5.1 — NOVOS SUPORTES DO COMPRESSOR E TANQUE SOBRE O PISO (COMP-CAG-08)**
Fabricação, fornecimento e instalação de 32 (trinta e dois) suportes de apoio de piso para o compressor e tanque de líquido (Detalhes 02 e 06). Cada suporte é constituído por 01 coluna em perfil laminado tipo "I" de 4" x 2" em aço carbono (h=0,20 m), soldada continuamente sobre 01 base em chapa de aço carbono de 3/8" (0,20 x 0,20 m) com furação de 5/8", ancorada na laje através de 04 parafusos de ancoragem / parabolts de 1/2". Entre a base metálica e o piso acabado é instalada 01 manta antivibratória de borracha/neoprene de 3 cm de espessura (0,20 x 0,20 m) para amaciamento e isolamento de vibrações.

### **ITEM 5.2 — NOVOS SUPORTES DE SUSTENTAÇÃO DOS MÓDULOS DO CHILLER (COMP-CAG-09)**
Fabricação e montagem de 24 (vinte e quatro) colunas metálicas de sustentação elevada dos módulos do Chiller (Detalhe 01 e Relação 20/07/2026). Cada módulo compreende 01 coluna de perfil laminado tipo "I" de 4" x 2" (L=2,00 m), soldada a 01 base em chapa de aço carbono 3/8" (0,20 x 0,20 m) com 4 furos para parabolt de 1/2", 02 chapas metálicas de reforço lateral 3/16" (0,10 x 0,10 m) soldadas, 576 furos totais nos perfis, parafusos M16 com porcas e 2 arruelas lisas por parafuso, e 01 manta antivibratória de borracha de 3 cm (0,20 x 0,20 m).

### **ITEM 5.3 — REFORMA DOS SUPORTES EXISTENTES DO TANQUE DE CONDENSAÇÃO (COMP-CAG-10)**
Readequação e reforma de 16 (dezesseis) bases de colunas "I" existentes para o tanque de condensação (Detalhe 03). Compreende o corte, preparação da superfície, soldagem de 16 cantoneiras em aço carbono de abas iguais (1.3/4" x 6,35 mm x 12 cm de comprimento) com furação para acoplamento, fornecimento de 64 parafusos parabolt de 1/2" para fixação na laje, 16 mantas antivibratórias de borracha de 3 cm (0,20 x 0,20 m) e parafusos M16 com porca e arruelas.

### **ITEM 5.4 — SUBSTITUIÇÃO DE LONGARINAS DAS SERPENTINAS E TRAVAMENTO FRONTAL (COMP-CAG-11)**
Substituição das longarinas de sustentação das serpentinas e travamentos frontais meio e inferior (Detalhe 04). Compreende o fornecimento e montagem de 16 unidades de perfil laminado tipo "U" de 4" (101 x 40 x 4,8 mm x 2,35 m de comprimento, totalizando 37,60 m de perfil U ~ 780,00 kg de aço), 32 cantoneiras em aço carbono (1.3/4" x 6,35 mm x 30 cm) soldadas ao perfil U para suporte da base da serpentina, parafusos M16 x 30 mm, porcas e arruelas.

### **ITEM 5.5 — SUBSTITUIÇÃO DE LONGARINAS DE TRAVAMENTO LATERAL INFERIOR (COMP-CAG-12)**
Substituição das longarinas de travamento lateral inferior dos módulos (Detalhe 05). Compreende o fornecimento e montagem de 08 unidades de perfil laminado tipo "U" de 4" (101 x 40 x 4,8 mm x 2,29 m de comprimento, totalizando 18,32 m de perfil U ~ 380,00 kg de aço), furação no perfil de 4", parafusos M16 x 30 mm, porcas e arruelas M16.

### **ITEM 5.6 — VIGAS I W150 DE REFORÇO NA SUSTENTAÇÃO DE SERPENTINAS DO CHILLER (COMP-CAG-13)**
Fornecimento e montagem de vigas de aço ASTM A36 tipo I W150 x 22,5 (6" x 4"), peso linear de 22,5 kg/m, comprimento total de 40,00 metros (massa total de 900,00 kg). Inclui cortes, furações, soldas MIG/MAG, parafusos de alta resistência ASTM A325 5/8" x 2", porcas, arruelas, aplicação de primer epóxi anticorrosivo (1 demão, 25 μm) e pintura de acabamento em esmalte sintético (2 demãos, 50 μm cada). Atendimento à norma ABNT NBR 8800.

---

## 📋 Fichas Técnicas no Padrão `modelo-item-orcamentario`

```yaml
# ITEM 5.1
item:
  numero: "5.1"
  codigo: "COMP-CAG-08"
  sistema: "SINAPI / RELAÇÃO 20.07.2026"
  descricao: >
    Novos suportes do compressor e tanque sobre piso (32 colunas viga I 4"x2", chapas 3/8", 128 parabolts 1/2", mantas 3cm).
  unidade: "un"
  quantidade: 32.00
  custo_unitario_sem_bdi: 345.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 431.88
  preco_total_com_bdi: 13820.00
  fonte: {nome: "Relação 20.07.2026", data_base: "07/2026", arquivo_referencia: "detalhes 01 02 04 06.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "32 colunas h=0,20m com mantas antivibratórias."

# ITEM 5.2
item:
  numero: "5.2"
  codigo: "COMP-CAG-09"
  sistema: "SINAPI / RELAÇÃO 20.07.2026"
  descricao: >
    Novos suportes dos módulos do Chiller (24 colunas viga I 4"x2" h=2m, chapas 3/8", 48 chapas 3/16", 96 parabolts 1/2", mantas 3cm).
  unidade: "un"
  quantidade: 24.00
  custo_unitario_sem_bdi: 649.69
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 812.11
  preco_total_com_bdi: 19490.70
  fonte: {nome: "Relação 20.07.2026", data_base: "07/2026", arquivo_referencia: "detalhes 01 02 04 06.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "24 colunas h=2,00m completas."

# ITEM 5.3
item:
  numero: "5.3"
  codigo: "COMP-CAG-10"
  sistema: "SINAPI / RELAÇÃO 20.07.2026"
  descricao: >
    Reforma dos suportes existentes do tanque de condensação (16 readequações, cantoneiras 1.3/4", 64 parabolts 1/2", mantas 3cm).
  unidade: "un"
  quantidade: 16.00
  custo_unitario_sem_bdi: 285.40
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 356.75
  preco_total_com_bdi: 5708.00
  fonte: {nome: "Relação 20.07.2026", data_base: "07/2026", arquivo_referencia: "detalhes 03 e 05.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "16 readequações com cantoneiras e fixação."

# ITEM 5.4
item:
  numero: "5.4"
  codigo: "COMP-CAG-11"
  sistema: "SINAPI / RELAÇÃO 20.07.2026"
  descricao: >
    Substituição de longarinas das serpentinas e travamento frontal (16 perfis U 4" L=2,35m, 32 cantoneiras 1.3/4"x30cm, parafusos M16).
  unidade: "kg"
  quantidade: 780.00
  custo_unitario_sem_bdi: 21.80
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 27.25
  preco_total_com_bdi: 21255.00
  fonte: {nome: "Relação 20.07.2026", data_base: "07/2026", arquivo_referencia: "detalhes 01 02 04 06.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "37,6m de perfil U 4\" + cantoneiras."

# ITEM 5.5
item:
  numero: "5.5"
  codigo: "COMP-CAG-12"
  sistema: "SINAPI / RELAÇÃO 20.07.2026"
  descricao: >
    Substituição de longarinas de travamento lateral inferior (8 perfis U 4" L=2,29m, parafusos M16).
  unidade: "kg"
  quantidade: 380.00
  custo_unitario_sem_bdi: 21.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 26.88
  preco_total_com_bdi: 10212.50
  fonte: {nome: "Relação 20.07.2026", data_base: "07/2026", arquivo_referencia: "detalhes 03 e 05.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "18,32m de perfil U 4\" de travamento."

# ITEM 5.6
item:
  numero: "5.6"
  codigo: "COMP-CAG-13"
  sistema: "SINAPI-ES"
  descricao: >
    Vigas I de aço ASTM A36 W150 x 22,5 (6" x 4") para sustentação de serpentinas (40m total, pintura epóxi/esmalte).
  unidade: "kg"
  quantidade: 900.00
  custo_unitario_sem_bdi: 20.43
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 25.54
  preco_total_com_bdi: 22983.75
  fonte: {nome: "SINAPI-ES", data_base: "07/2026", arquivo_referencia: "Modernização da CAG - rev 1.xlsx"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "40 metros lineares de perfil I W150."
```

---

## 📊 Tabela Consolidada de Composição — Grupo 5.0

| Item | Código | Descrição | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | Total s/ BDI (R$) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **5.1** | COMP-CAG-08 | Novos suportes do compressor e tanque sobre piso (32 colunas I 4"x2", chapas 3/8", 128 parabolts 1/2", mantas 3cm) | un | 32,00 | 345,50 | 11.056,00 | 431,88 | 13.820,00 |
| **5.2** | COMP-CAG-09 | Novos suportes dos módulos do Chiller (24 colunas I 4"x2" h=2m, chapas 3/8", 48 chapas 3/16", 96 parabolts 1/2", mantas 3cm) | un | 24,00 | 649,69 | 15.592,56 | 812,11 | 19.490,70 |
| **5.3** | COMP-CAG-10 | Reforma dos suportes existentes do tanque de condensação (16 readequações, cantoneiras 1.3/4", 64 parabolts 1/2", mantas 3cm) | un | 16,00 | 285,40 | 4.566,40 | 356,75 | 5.708,00 |
| **5.4** | COMP-CAG-11 | Substituição de longarinas das serpentinas e travamento frontal (16 perfis U 4" L=2,35m, 32 cantoneiras 1.3/4"x30cm, parafusos M16) | kg | 780,00 | 21,80 | 17.004,00 | 27,25 | 21.255,00 |
| **5.5** | COMP-CAG-12 | Substituição de longarinas de travamento lateral inferior (8 perfis U 4" L=2,29m, parafusos M16) | kg | 380,00 | 21,50 | 8.170,00 | 26,88 | 10.212,50 |
| **5.6** | COMP-CAG-13 | Vigas I de aço ASTM A36 W150 x 22,5 (6" x 4") para sustentação de serpentinas (40m total, pintura epóxi/esmalte) | kg | 900,00 | 20,43 | 18.387,00 | 25,54 | 22.983,75 |
| **TOTAL**| | **SUBTOTAL DO GRUPO 5.0** | | | | **R$ 74.775,96** | | **R$ 93.469,95** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Mediçoes efetuadas por unidade (`un`) de coluna montada (Itens 5.1 a 5.3) e por quilograma (`kg`) de estrutura metálica fixada (Itens 5.4 a 5.6).
2. **Inspeção de Mantas Antivibratórias:** Verificação do correto assentamento das mantas de 3 cm sob todas as bases metálicas em contato com o piso.
3. **Alinhamento e Torque:** Verificação do torque de aperto nos parafusos parabolt de 1/2" e parafusos M16, com tolerância de aprumo das colunas de 1:500.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise as especificações e composições dos **Itens 5.1 a 5.6 (Grupo 5.0)** acima.  
> Assim que aprovado, prosseguiremos para o **Grupo 6.0 — Caixas de Isolamento Térmico das Bombas (Item 6.1)**!
