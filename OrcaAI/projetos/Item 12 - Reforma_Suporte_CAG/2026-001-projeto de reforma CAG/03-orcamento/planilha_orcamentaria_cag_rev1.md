# Planilha Orçamentária Detalhada — Reforma e Modernização da CAG

> **Orçamento Público de Engenharia Civil**  
> **Órgão Contratante:** Ministério da Gestão e da Inovação em Serviços Públicos — Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Objeto:** Reformas e melhorias nas instalações da Central de Água Gelada (CAG), incluindo a construção de um carrinho para movimentação dos equipamentos da CAG e reforma do guindaste da CAG no Prédio Sede do MGI/ES.  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Data de Referência (Rev. 1):** 23/08/2024  
> **Taxa de BDI:** 25,00%  

---

## 💰 Resumo Consolidado do Orçamento

| Indicador Orçamentário | Valor (R$) | % |
| :--- | :---: | :---: |
| **Custo Direto Total (Subtotal sem BDI)** | **R$ 76.771,74** | 80,00% |
| **Bonificação e Despesas Indiretas (BDI 25%)** | **R$ 19.192,93** | 20,00% |
| **VALOR TOTAL GERAL DO ORÇAMENTO (com BDI)** | **R$ 95.964,67** | **100,00%** |

---

## 📊 Planilha Orçamentária Sintética

| Item | Código | Descrição Resumida | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | BDI (%) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.0** | | **CARRINHO DE MOVIMENTAÇÃO DE CARGA** | | | | | | |
| 1.1 | COMP-CAG-01 | Fabricação e montagem de carrinho para movimentação de carga | un | 1,00 | 5.458,50 | 25,00% | 6.823,13 | 6.823,13 |
| **2.0** | | **ESTRUTURA DE SUPORTE DO CARRINHO** | | | | | | |
| 2.1 | COMP-CAG-02 | Estrutura metálica de suporte com trilho em barra 3/4" e pintura alcatrão | kg | 450,00 | 17,47 | 25,00% | 21,84 | 9.826,88 |
| **3.0** | | **PASSARELA METÁLICA PARA CAG** | | | | | | |
| 3.1 | COMP-CAG-03 | Passarela metálica de acesso/manutenção com prolongamento de 2m | m² | 2,00 | 1.433,30 | 25,00% | 1.791,63 | 3.583,25 |
| **4.0** | | **GUINDASTE (GRUA) PARA CAG** | | | | | | |
| 4.1 | COMP-CAG-04 | Guindaste de manutenção (grua), prolongamento, contrapeso 280kg | un | 1,00 | 4.269,00 | 25,00% | 5.336,25 | 5.336,25 |
| 4.2 | COMP-CAG-05 | Aplicação de flange em aço carbono H=30mm soldado em tubo DN 8" | un | 3,00 | 320,20 | 25,00% | 400,25 | 1.200,75 |
| 4.3 | COMP-CAG-06 | Substituição de tubo guia interno em aço carbono DN 8" L=5m | un | 1,00 | 2.209,00 | 25,00% | 2.761,25 | 2.761,25 |
| 4.4 | COMP-CAG-07 | Instalação de orifício para lubrificação com niple e tampão 1/2" | un | 1,00 | 61,50 | 25,00% | 76,88 | 76,88 |
| **5.0** | | **REFORÇO E SUPORTES PARA COMPRESSOR, TANQUE E SERPENTINA DO CHILLER** | | | | | | |
| 5.1 | COMP-CAG-08 | Suporte de sustentação para compressor e tanque de líquido (viga I 4"x2") | un | 16,00 | 649,69 | 25,00% | 812,11 | 12.993,83 |
| 5.2 | COMP-CAG-09 | Suporte de sustentação para serpentina do chiller (viga I 4"x2") | un | 24,00 | 649,69 | 25,00% | 812,11 | 19.490,75 |
| 5.3 | COMP-CAG-10 | Vigas I para reforço na sustentação de serpentinas (W150x22,5 - 40m) | kg | 900,00 | 20,43 | 25,00% | 25,54 | 22.988,48 |
| **6.0** | | **CAIXA DE ISOLAMENTO DAS BOMBAS** | | | | | | |
| 6.1 | COMP-CAG-11 | Caixa de isolamento de condensação em alumínio para bombas (20/25CV) | un | 6,00 | 1.284,00 | 25,00% | 1.605,00 | 9.630,00 |
| **7.0** | | **REMOÇÃO E REINSTALAÇÃO DO TELHADO METÁLICO** | | | | | | |
| 7.1 | SINAPI 88323 | Remoção e reinstalação de telhado metálico com reaproveitamento | m² | 20,00 | 21,45 | 25,00% | 26,81 | 536,25 |
| **8.0** | | **LIMPEZA GERAL E DESTINAÇÃO DE RESÍDUOS** | | | | | | |
| 8.1 | SINAPI 88316 | Limpeza geral de obra com remoção de entulho e destinação (PMV) | m² | 120,00 | 4,78 | 25,00% | 5,98 | 717,00 |
| **TOTAL** | | | | | **76.771,74** | **25,00%** | | **95.964,67** |

---

## 📄 Detalhamento dos Itens no Padrão `modelo-item-orcamentario`

```yaml
# ==============================================================================
# ITEM 1.1 - CARRINHO DE MOVIMENTAÇÃO DE CARGA
# ==============================================================================
item:
  numero: "1.1"
  codigo: "COMP-CAG-01"
  sistema: "SINAPI / EMOP / COTAÇÃO LOCAL"
  descricao: >
    Fabricação e montagem de carrinho para movimentação de carga em Central de Água Gelada (CAG),
    estrutura metálica em vigas perfil "I" de 3" com soldas contínuas, piso em chapa xadrez de alumínio
    antiderrapante de 3mm, deslocamento sobre trilhos de barra redonda maciça de 3/4", roldanas de 2 1/2"
    com rolamentos duplos na parte inferior, dois freios com sistema de alavanca e trava, pintura protetora
    com alcatrão de hulha bicomponente, similar à marca Internacional.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 5458.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 6823.13
  preco_total_com_bdi: 6823.13
  fonte:
    nome: "Composição Própria baseada em SINAPI (43082, 98510, 100772, 88315, 88316) + EMOP (050104) + Cotações"
    data_base: "02/2014 & Cotações Locais (Vitória-ES)"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Capacidade e resistência testadas conforme especificações de segurança da CAG."
```

```yaml
# ==============================================================================
# ITEM 2.1 - ESTRUTURA DE SUPORTE DO CARRINHO
# ==============================================================================
item:
  numero: "2.1"
  codigo: "COMP-CAG-02"
  sistema: "SINAPI-ES"
  descricao: >
    Fornecimento e montagem de estrutura metálica para suporte de carrinho de movimentação de cargas em CAG,
    constituída por vigas perfil "I" de 3", com trilho em barra redonda maciça de 3/4" soldada sobre o perfil,
    incluindo travamento inferior e guias laterais em barra chata de aço carbono 1" x 1/8", batentes e elementos
    de fixação. Tratamento anticorrosivo com pintura de alcatrão de hulha bicomponente.
  unidade: "kg"
  quantidade: 450.00
  custo_unitario_sem_bdi: 17.47
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 21.84
  preco_total_com_bdi: 9826.88
  fonte:
    nome: "SINAPI (43082, 43148, 43059, 95241, 102494, 88315)"
    data_base: "02/2014 & Atualizações SINAPI"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Massa calculada com base no peso teórico dos perfis e componentes de aço efetivamente instalados."
```

```yaml
# ==============================================================================
# ITEM 3.1 - PASSARELA METÁLICA PARA CAG
# ==============================================================================
item:
  numero: "3.1"
  codigo: "COMP-CAG-03"
  sistema: "SINAPI / EMOP"
  descricao: >
    Fornecimento e montagem de passarela metálica para acesso e manutenção na CAG, com prolongamento de 2m
    em relação à estrutura existente. Vigas de perfil "I" de 3", revestida com chapa xadrez de alumínio 3mm.
    Inclui guarda-corpo em tubo galvanizado (H=1,10m), rodapé metálico de 15cm, escada de acesso de 1,30m
    e pintura anticorrosiva com alcatrão de hulha.
  unidade: "m²"
  quantidade: 2.00
  custo_unitario_sem_bdi: 1433.30
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 1791.63
  preco_total_com_bdi: 3583.25
  fonte:
    nome: "SINAPI / EMOP + Composição Própria"
    data_base: "02/2014 & Cotações Locais"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Atende aos requisitos de durabilidade e segurança de trabalho em altura."
```

```yaml
# ==============================================================================
# ITEM 4.1 - GUINDASTE (GRUA) PARA CAG
# ==============================================================================
item:
  numero: "4.1"
  codigo: "COMP-CAG-04"
  sistema: "SINAPI / COTAÇÃO LOCAL"
  descricao: >
    Guindaste de manutenção da CAG (Grua), fornecimento e instalação. Prolongamento do trilho em 2,00m (perfil I 100mm),
    substituição do cabo de aço, caixa de contrapeso em aço carbono com concreto C20 (~280 kg), base 400x400x15,875mm,
    tubos de aço carbono 8", niple e tampão de 1/2" para lubrificação e flanges H=30cm.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 4269.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 5336.25
  preco_total_com_bdi: 5336.25
  fonte:
    nome: "Composição Própria com Cotações de Insumos e Mão de Obra SINAPI"
    data_base: "02/2014 & Cotações Locais (Vitória-ES)"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Equipamento essencial para movimentação segura de peças pesadas da CAG."
```

```yaml
# ==============================================================================
# ITEM 4.2 - FLANGE EM AÇO CARBONO H=30MM
# ==============================================================================
item:
  numero: "4.2"
  codigo: "COMP-CAG-05"
  sistema: "SINAPI-ES"
  descricao: >
    Aplicação de flange em aço carbono H=30mm, soldado em tubo de aço carbono DN 8" (203,2 mm).
    Inclui preparação da superfície, posicionamento, soldagem contínua em toda circunferência com eletrodo revestido,
    garantindo fixação e folga máxima de 1 cm entre tubos.
  unidade: "un"
  quantidade: 3.00
  custo_unitario_sem_bdi: 320.20
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 400.25
  preco_total_com_bdi: 1200.75
  fonte:
    nome: "SINAPI + Cotações Locais"
    data_base: "02/2014"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Folga ajustada para movimentação da grua."
```

```yaml
# ==============================================================================
# ITEM 4.3 - SUBSTITUIÇÃO DE TUBO GUIA INTERNO DN 8"
# ==============================================================================
item:
  numero: "4.3"
  codigo: "COMP-CAG-06"
  sistema: "SINAPI-ES"
  descricao: >
    Substituição de tubo guia interno em aço carbono DN 8" (203,2 mm), L=5,0m para grua de manutenção.
    Corte, preparação das extremidades, tamponamento, soldagem contínua da extremidade inferior à base fixa,
    remoção do tubo antigo e limpeza.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 2209.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 2761.25
  preco_total_com_bdi: 2761.25
  fonte:
    nome: "Composição Própria baseada em SINAPI"
    data_base: "02/2014"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Base livre superior para rotação da grua."
```

```yaml
# ==============================================================================
# ITEM 4.4 - ORIFÍCIO PARA LUBRIFICAÇÃO EM ESTRUTURA METÁLICA
# ==============================================================================
item:
  numero: "4.4"
  codigo: "COMP-CAG-07"
  sistema: "SINAPI-ES"
  descricao: >
    Instalação de orifício para lubrificação em estrutura metálica de grua. Furo 1/2" com inclinação de 45°
    em tubo de aço carbono, niple de 1/2" com tampão soldado para manutenção.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 61.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 76.88
  preco_total_com_bdi: 76.88
  fonte:
    nome: "Composição Própria baseada em SINAPI"
    data_base: "02/2014"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Acesso facilitado para engraxamento periódico."
```

```yaml
# ==============================================================================
# ITEM 5.1 - SUPORTE DE SUSTENTAÇÃO PARA COMPRESSOR E TANQUE DE LÍQUIDO
# ==============================================================================
item:
  numero: "5.1"
  codigo: "COMP-CAG-08"
  sistema: "SINAPI-ES"
  descricao: >
    Execução de suporte de sustentação para compressor e tanque de líquido. Viga perfil "I" 4" x 2",
    base em chapa 3/8" (0,20x0,20m), 04 parafusos de ancoragem 1/2", manta de neoprene e=10mm para amortecimento.
    Conforme ABNT NBR 8800 e NBR 14762. AF_01/2024.
  unidade: "un"
  quantidade: 16.00
  custo_unitario_sem_bdi: 649.69
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 812.11
  preco_total_com_bdi: 12993.83
  fonte:
    nome: "SINAPI (44210, 43057, 4322, 343, 37395, 7307, 7311, 88315, 88251, 88310, 14120, 14119) + Neoprene Cotação"
    data_base: "01/2024 & SINAPI-ES"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Isolamento antivibratório exigido para proteção da laje."
```

```yaml
# ==============================================================================
# ITEM 5.2 - SUPORTE DE SUSTENTAÇÃO PARA SERPENTINA DO CHILLER
# ==============================================================================
item:
  numero: "5.2"
  codigo: "COMP-CAG-09"
  sistema: "SINAPI-ES"
  descricao: >
    Execução de suporte de sustentação para serpentina do chiller. Viga perfil "I" 4" x 2",
    base em chapa 3/8" (0,20x0,20m), 04 parafusos de ancoragem 1/2", neoprene e=10mm para amortecimento.
    Conforme ABNT NBR 8800 e NBR 14762. AF_01/2024.
  unidade: "un"
  quantidade: 24.00
  custo_unitario_sem_bdi: 649.69
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 812.11
  preco_total_com_bdi: 19490.75
  fonte:
    nome: "SINAPI + Cotação Neoprene"
    data_base: "01/2024 & SINAPI-ES"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Redistribuição de carga para suporte das serpentinas."
```

```yaml
# ==============================================================================
# ITEM 5.3 - VIGAS I DE REFORÇO DE SUSTENTAÇÃO DE SERPENTINAS (W150 x 22,5)
# ==============================================================================
item:
  numero: "5.3"
  codigo: "COMP-CAG-10"
  sistema: "SINAPI-ES"
  descricao: >
    Fornecimento e montagem de vigas I em aço ASTM A36 tipo I W150 x 22,5 (6" x 4") para reforço de sustentação de serpentinas.
    Comprimento total 40m. Soldas MIG/MAG, primer epóxi e pintura esmalte sintético (2 demãos). Parafusos A325 5/8" x 2".
    Conforme ABNT NBR 8800. AF_01/2024.
  unidade: "kg"
  quantidade: 900.00
  custo_unitario_sem_bdi: 20.43
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 25.54
  preco_total_com_bdi: 22988.48
  fonte:
    nome: "SINAPI (44210, 4330, 4375, 39997, 343, 37395, 7307, 7311, 88278, 88316, 88310, 14120, 14119)"
    data_base: "01/2024 & SINAPI-ES"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Maior item orçamentário da obra (Curva ABC Item A - 23,95% do total)."
```

```yaml
# ==============================================================================
# ITEM 6.1 - CAIXA DE ISOLAMENTO PARA BOMBAS DE 20 E 25CV
# ==============================================================================
item:
  numero: "6.1"
  codigo: "COMP-CAG-11"
  sistema: "SINAPI / COTAÇÃO LOCAL"
  descricao: >
    Fabricação e instalação de caixa de isolamento para bombas de 20 e 25CV em chapa de alumínio e=2,5mm (54x20x50cm).
    Preenchimento com espuma expansiva bicomponente (A+B). Abertura traseira mantendo acesso a parafusos de manutenção.
  unidade: "un"
  quantidade: 6.00
  custo_unitario_sem_bdi: 1284.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 1605.00
  preco_total_com_bdi: 9630.00
  fonte:
    nome: "SINAPI (11059, 276, 37395, 3767, 88315, 88251, 14119, 36148) + Cotações (Espuma e Alumínio)"
    data_base: "02/2014 & Cotações Locais"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Proteção térmica/acústica e controle de condensação do rotor das motobombas."
```

```yaml
# ==============================================================================
# ITEM 7.1 - REMOÇÃO E REINSTALAÇÃO DE TELHADO METÁLICO
# ==============================================================================
item:
  numero: "7.1"
  codigo: "SINAPI 88323"
  sistema: "SINAPI-ES"
  descricao: >
    Remoção e reinstalação de telhado metálico com reaproveitamento. Desmontagem de telhas metálicas, armazenamento,
    remontagem da estrutura e cobertura. Inclui andaime tubular, guincho elétrico e carga manual de entulho.
  unidade: "m²"
  quantidade: 20.00
  custo_unitario_sem_bdi: 21.45
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 26.81
  preco_total_com_bdi: 536.25
  fonte:
    nome: "SINAPI (88316, 88323, 88324, 10527, 10776, 98297, 36148, 72897)"
    data_base: "02/2014 & SINAPI-ES"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Serviço de abertura temporária da cobertura para içamento e instalação dos equipamentos."
```

```yaml
# ==============================================================================
# ITEM 8.1 - LIMPEZA GERAL E DESTINAÇÃO DE RESÍDUOS
# ==============================================================================
item:
  numero: "8.1"
  codigo: "SINAPI 88316"
  sistema: "SINAPI-ES"
  descricao: >
    Limpeza geral de obra com remoção de entulho, transporte e destinação final em aterro sanitário credenciado
    pela Prefeitura Municipal de Vitória (PMV), com pagamento da taxa ambiental de destinação final. AF_04/2019.
  unidade: "m²"
  quantidade: 120.00
  custo_unitario_sem_bdi: 4.78
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 5.98
  preco_total_com_bdi: 717.00
  fonte:
    nome: "SINAPI (88316, 90776, 38400, 38402, 38311, 5811, 36148) + Taxa PMV"
    data_base: "04/2019 & SINAPI-ES"
    arquivo_referencia: "Modernização da CAG - rev 1.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Comprovação obrigatória de destinação ambientalmente adequada de resíduos."
```

---

## 📌 Condições Técnicas e Observações Gerais
* **a)** Dúvidas técnicas deverão ser dirimidas junto ao responsável técnico, Engº. Luis Fernando Dias (Tel: 27 3211-5328).
* **b)** A contratada deverá apresentar cronograma de execução física que não interfira no funcionamento das demais atividades do Edifício Sede do MGI/ES.
* **c)** Não será permitida a subcontratação/terceirização total dos serviços contratados.
* **d)** O prazo máximo para entrega de todos os serviços concluídos é de **60 (sessenta) dias corridos**.
* **e)** A garantia formal de todos os serviços executados e materiais fornecidos será de **5 (cinco) anos**.
* **f)** As medições serão efetuadas a cada **45 dias corridos** após a emissão da Ordem de Serviço (OS).
