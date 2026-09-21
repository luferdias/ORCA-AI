# Especificação Detalhada e Composição Analítica — Item 1.1

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Item da Planilha Sintética:** **1.1**  
> **Código da Composição Própria:** **COMP-CAG-01**  
> **Unidade de Medida:** **un (unidade)**  
> **Quantidade:** **1,00 un**  
> **Taxa de BDI:** **25,00%**  

---

## 📝 Descrição Resumida Detalhada (Memorial Descritivo do Item)

**ITEM 1.1 — FABRICAÇÃO E MONTAGEM DE CARRINHO PARA MOVIMENTAÇÃO DE CARGA EM CENTRAL DE ÁGUA GELADA (CAG)**

Fabricação, transporte e montagem no local de 01 (um) carrinho metálico reforçado para movimentação e manuseio de cargas pesadas nas instalações da Central de Água Gelada (CAG), construído rigorosamente conforme o projeto executivo (Detalhe 01/Projeto do Carrinho e Relação de Peças de 20/07/2026). 

A estrutura metálica principal é constituída por perfis laminados tipo "U" de aço carbono de 3" (101 x 40 x 4,8 mm), sendo 4 travessas de 0,80 m e 2 longarinas de 2,00 m, perfeitamente alinhadas e unidas por soldagem elétrica contínua com eletrodo revestido E7018. O piso do carrinho possui sistema duplo de forramento: camada inferior estrutural em chapa lisa de aço carbono de 4 mm de espessura (dimensões 1,00 x 2,00 m) assentada sobre a grelha de perfis U, e camada superior de acabamento em chapa xadrez antiderrapante de alumínio de 2 mm de espessura (dimensões 1,00 x 2,50 m) com bordas rebatidas/dobradas para proteção e estanqueidade.

O sistema de deslocamento do carrinho é composto por 04 (quatro) roldanas em aço usinado de diâmetro 2.1/2" equipadas com rolamentos duplos blindados de alta capacidade na parte inferior, projetadas para rodar sobre trilhos em tubo maciço de aço redondos de 3/4", e 02 (dois) sistemas de freio mecânico de ação direta acionados por alavanca com trava de segurança.

Todo o conjunto metálico receberá tratamento de superfície contra corrosão (limpeza mecânica e desengraxamento) e pintura protetora especial em alcatrão de hulha bicomponente (tipo Coal Tar Epóxi, similar à marca Internacional), aplicada em 2 demãos com espessura mínima de filme seco de 100 μm, resistente à umidade severa da CAG. Atendimento integral às normas ABNT NBR 8800 (Projeto de Estruturas de Aço) e NBR 14762.

---

## 📋 Ficha Técnica no Padrão `modelo-item-orcamentario`

```yaml
item:
  numero: "1.1"
  codigo: "COMP-CAG-01"
  sistema: "SINAPI / EMOP / COTAÇÃO LOCAL"
  descricao: >
    Fabricação e montagem de carrinho para movimentação de carga em Central de Água Gelada (CAG),
    constituído por estrutura metálica principal em perfis U de 3" (4x0,80m e 2x2,00m), piso em chapa
    lisa de aço 4mm revestido com chapa xadrez de alumínio 2mm antiderrapante (1,00x2,50m) com bordas dobradas;
    deslocamento sobre trilhos de aço maciço 3/4", 04 roldanas de 2.1/2" com rolamentos duplos, 02 freios tipo alavanca
    com trava mecânica, pintura anticorrosiva de alcatrão de hulha bicomponente.
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 5458.50
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 6823.12
  preco_total_com_bdi: 6823.12
  fonte:
    nome: "Composição Própria (SINAPI-ES + EMOP + Cotações Locais de Vitória-ES)"
    data_base: "07/2026"
    arquivo_referencia: "Relação de peças para restauração da CAG .20.07. 2026.xlsx"
  validacao:
    codigo_encontrado: true
    unidade_compativel: true
    descricao_compativel: true
  observacoes: "Equipamento dimensionado para suportar movimentação de componentes e bombas da CAG."
```

---

## 📊 Composição Analítica de Preço Unitário (CPU) — Item 1.1

> **Unidade de Referência:** 1,00 un | **Custo Direto Total (Sem BDI):** R$ 5.458,50 | **Preço Total com BDI (25%):** R$ 6.823,12

### 1. Insumos e Materiais

| Código | Descrição do Insumo / Material | Unid. | Coeficiente (Qtd) | Custo Unitário s/ BDI (R$) | Custo Total s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 43059 | Perfil "U" de aço laminado 3" (101 x 40 x 4,8 mm) — Estrutura | kg | 43,20 | 10,91 | 471,31 | SINAPI-ES |
| SINAPI 43057 | Chapa de aço carbono lisa e=4,0 mm (1,00 x 2,00m) — Piso base | kg | 62,80 | 8,40 | 527,52 | SINAPI-ES |
| EMOP 050104 | Chapa xadrez de alumínio antiderrapante e=2,0 mm (1,00 x 2,50m) | m² | 2,50 | 380,00 | 950,00 | EMOP / Cotação |
| COTAÇÃO-01 | Roldana em aço 2.1/2" com rolamento duplo blindado | un | 4,00 | 85,00 | 340,00 | Pesquisa Vitória-ES |
| COTAÇÃO-02 | Sistema de freio mecânico tipo alavanca com trava de segurança | cj | 2,00 | 250,00 | 500,00 | Pesquisa Vitória-ES |
| SINAPI 98510 | Eletrodo revestido E7018 3,25 mm para solda contínua | kg | 2,50 | 37,92 | 94,80 | SINAPI-ES |
| SINAPI 100772| Tinta epóxi alcatrão de hulha bicomponente (Coal Tar) | m² | 10,00 | 52,41 | 524,10 | SINAPI-ES |
| SINAPI 36148 | Kit de Equipamento de Proteção Individual (E.P.I.) | cj | 1,00 | 136,62 | 136,62 | SINAPI-ES |
| **SUBTOTAL MATERIAIS** | | | | | **R$ 3.544,35** | |

### 2. Mão de Obra Direta (com Encargos Sociais Ilonerados)

| Código | Categoria Profissional | Unid. | Coeficiente (Horas) | Custo Horário s/ BDI (R$) | Custo Total s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 88315 | Serralheiro com encargos complementares | h | 40,00 | 24,39 | 975,60 | SINAPI-ES (07/2026) |
| SINAPI 88316 | Ajudante de serralheiro com encargos complementares | h | 40,00 | 18,26 | 730,40 | SINAPI-ES (07/2026) |
| **SUBTOTAL MÃO DE OBRA** | | | | | **R$ 1.706,00** | |

### 3. Equipamentos e Ferramentas (Locação/Uso)

| Código | Equipamento / Ferramenta | Unid. | Coeficiente | Custo Unitário s/ BDI (R$) | Custo Total s/ BDI (R$) | Fonte / Referência |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| SINAPI 14120 | Máquina de solda elétrica 400A (locação) | h prod | 8,00 | 15,20 | 121,60 | SINAPI-ES |
| SINAPI 14119 | Lixadeira / Esmerilhadeira elétrica (locação) | h prod | 14,50 | 5,97 | 86,55 | SINAPI-ES |
| **SUBTOTAL EQUIPAMENTOS** | | | | | **R$ 208,15** | |

---

### 💵 Resumo da Composição do Item 1.1

| Componente de Custo | Valor sem BDI (R$) | % do Custo Direto | Valor com BDI 25% (R$) |
| :--- | :---: | :---: | :---: |
| Insumos e Materiais | R$ 3.544,35 | 64,93% | R$ 4.430,44 |
| Mão de Obra Direta | R$ 1.706,00 | 31,25% | R$ 2.132,50 |
| Equipamentos e Ferramentas | R$ 208,15 | 3,82% | R$ 260,18 |
| **CUSTO DIRETO TOTAL (Sem BDI)** | **R$ 5.458,50** | **100,00%** | — |
| **BDI (25,00%)** | **R$ 1.364,62** | — | — |
| **PREÇO TOTAL DO ITEM 1.1 (Com BDI)** | — | — | **R$ 6.823,12** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** A medição será efetuada por unidade (`un`) de carrinho fabricado, instalado e testado com carga nominal.
2. **Teste Operacional:** Teste de deslocamento suave sobre o trilho de 3/4" sob carga de no mínimo 500 kg, com verificação de eficiência do sistema de travamento dos freios.
3. **Inspeção Visual e Pintura:** Verificação da continuidade das soldas e medição da espessura de película seca da pintura epóxi alcatrão de hulha (mínimo 100 μm).

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise a descrição detalhada e os insumos do **Item 1.1 (COMP-CAG-01)** acima.  
> Assim que aprovado, prosseguiremos imediatamente para a construção do **Item 2.1 (Estrutura de Suporte e Trilhos do Carrinho)**!
