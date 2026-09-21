# Especificação Detalhada e Composição Analítica — Grupo 7.0 (Itens 7.1 e 7.2)

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Grupo de Serviços:** **7.0 — SISTEMA DE COBERTURA E CALHAS DA ESTRUTURA DO CHILLER**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI (Grupo 7.0):** **R$ 7.116,70**  
> **Valor Total do Grupo 7.0 (com BDI 25%):** **R$ 8.895,88**  

---

## 📝 Memorial Descritivo Detalhado — Grupo 7.0

### **ITEM 7.1 — COBERTURA EM TELHA TRAPEZOIDAL GALVALUME COM PINTURA ELETROSTÁTICA BRANCA (SINAPI 94213)**
Fornecimento e montagem de sistema de cobertura metálica leve instalada sobre a estrutura superior dos módulos do Chiller (Detalhe Calha e Relação de Peças de 20/07/2026), com inclinação nominal de i=5%. 

O telhamento é composto por painéis de telha trapezoidal em aço galvalume (liga Al-Zn) de espessura 0,50 mm, pré-pintada eletrostaticamente na cor branca (face superior e inferior). Inclui painéis de dimensões 1,90 x 5,40 m, 1,40 x 5,40 m e 0,90 x 5,40 m, totalizando 28,50 m² de área desenvolvida de cobertura.

Compreende também o fechamento lateral metálico em telha galvalume branca, rufos, pingadeiras, parafusos autoperfurantes de fixação com arruelas de vedação em neoprene, fitas de vedação sintética e estrutura secundária de travamento.

### **ITEM 7.2 — CALHAS EM ALUMÍNIO E=3MM COM BORDA DOBRADA (SINAPI 94228)**
Fornecimento, conformação e instalação de calhas de drenagem pluvial em chapa de alumínio naval de espessura 3,0 mm, instaladas ao longo do perímetro da estrutura do Chiller.

As calhas possuem perfilação especial com borda superior de apoio dobrada de 5 cm para rigidez estrutural:
* Seção principal 30 x 15 x 10 cm (desenvolvimento de 55 cm e 60 cm), instaladas em trechos de 1,90 m e 12,30 m.
* Seção secundária 32 x 22 x 10 cm (desenvolvimento reforçado), totalizando 16,10 metros lineares de calha.

Inclusos suportes de fixação em barra de alumínio, soldagem TIG em alumínio nos encontros/cabeceiras, bocais de descida, vedação com mastique de poliuretano (PU) de alta aderência e testes de estanqueidade.

---

## 📋 Fichas Técnicas no Padrão `modelo-item-orcamentario`

```yaml
# ITEM 7.1
item:
  numero: "7.1"
  codigo: "SINAPI 94213"
  sistema: "SINAPI-ES"
  descricao: >
    Fornecimento e montagem de cobertura em telha trapezoidal Galvalume com pintura eletrostática branca (i=5%)
    sobre a estrutura do Chiller, incluindo fechamento lateral, bordas de apoio e elementos de fixação.
  unidade: "m²"
  quantidade: 28.50
  custo_unitario_sem_bdi: 145.20
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 181.50
  preco_total_com_bdi: 5172.75
  fonte: {nome: "SINAPI-ES (94213)", data_base: "07/2026", arquivo_referencia: "calha na estrutura do chiller.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Telha galvalume pré-pintada eletrostaticamente na cor branca."

# ITEM 7.2
item:
  numero: "7.2"
  codigo: "SINAPI 94228"
  sistema: "SINAPI-ES"
  descricao: >
    Fornecimento e instalação de calhas em alumínio e=3mm (seções 30x15x10cm e 32x22x10cm com borda de apoio dobrada de 5cm)
    para drenagem pluvial da estrutura do Chiller, incluindo soldagem, suporte e vedação.
  unidade: "m"
  quantidade: 16.10
  custo_unitario_sem_bdi: 185.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 231.25
  preco_total_com_bdi: 3723.13
  fonte: {nome: "SINAPI-ES (94228)", data_base: "07/2026", arquivo_referencia: "calha na estrutura do chiller.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Calhas em alumínio 3mm com bordas rígidas de 5cm."
```

---

## 📊 Tabela Consolidada de Composição — Grupo 7.0

| Item | Código | Descrição | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | Total s/ BDI (R$) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **7.1** | SINAPI 94213 | Cobertura em telha trapezoidal Galvalume branca (i=5%) sobre o Chiller | m² | 28,50 | 145,20 | 4.138,20 | 181,50 | 5.172,75 |
| **7.2** | SINAPI 94228 | Calhas em alumínio e=3mm (seções 30x15x10cm e 32x22x10cm c/ borda 5cm) | m | 16,10 | 185,00 | 2.978,50 | 231,25 | 3.723,13 |
| **TOTAL**| | **SUBTOTAL DO GRUPO 7.0** | | | | **R$ 7.116,70** | | **R$ 8.895,88** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Medição efetuada por metro quadrado (`m²`) de telhado montado e por metro linear (`m`) de calha instalada.
2. **Teste de Estanqueidade:** Teste de lâmina d'água e fluxo contínuo nas calhas para comprovação de inclinação e ausência de vazamentos nas juntas.
3. **Fixação e Estética:** Inspeção do alinhamento dos parafusos e integridade da pintura eletrostática das telhas.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise as especificações e insumos dos **Itens 7.1 e 7.2 (Grupo 7.0)** acima.  
> Assim que aprovado, prosseguiremos para o **Grupo 8.0 — Guarda-Corpo e Escada de Acesso em Aço Inox (Itens 8.1 e 8.2)**!
