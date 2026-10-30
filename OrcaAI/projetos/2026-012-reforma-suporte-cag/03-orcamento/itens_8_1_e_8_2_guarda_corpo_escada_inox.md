# Especificação Detalhada e Composição Analítica — Grupo 8.0 (Itens 8.1 e 8.2)

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Grupo de Serviços:** **8.0 — GUARDA-CORPO E ESCADA DE ACESSO EM AÇO INOX NA COBERTURA DA CAIXA D'ÁGUA**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI (Grupo 8.0):** **R$ 10.810,00**  
> **Valor Total do Grupo 8.0 (com BDI 25%):** **R$ 13.512,50**  

---

## 📝 Memorial Descritivo Detalhado — Grupo 8.0

### **ITEM 8.1 — GUARDA-CORPO EM TUBOS DE AÇO INOX 2" E 1/2" NA COBERTURA (SINAPI 100862)**
Fabricação, fornecimento, transporte e instalação de 22,00 metros lineares de guarda-corpo de proteção coletiva em aço inoxidável austenítico AISI 304 (acabamento escovado/polido), instalado no perímetro da cobertura da caixa d'água (Detalhe Guarda-Corpo e Relação de Peças de 20/07/2026), compreendendo trechos de 3,60 m e 11,40 m.

A estrutura do guarda-corpo possui altura acabada de h=1,10 m em relação ao topo do murete/laje e é constituída por:
* **Corrimão Superior:** Tubo contínuo de aço inox de 2" (50,8 mm) de diâmetro.
* **Travessas Intermediárias:** 3 (três) linhas paralelas em tubos de aço inox de 1/2" (12,7 mm) de diâmetro.
* **Postes de Sustentação Verticais:** 15 (quinze) colunas prumadas em tubo de aço inox de 2" com altura de 1,10 m, espaçadas a cada 1,20 m.
* **Bases de Ancoragem e Acabamento:** 15 placas de base quadradas em chapa de aço inox (10 x 10 cm) com 4 furos fixadas à laje por parafusos/parabolts de aço inox, e 15 canoplas redondas de acabamento metálico em inox de 4" cobrindo totalmente os chumbadores.

Atendimento integral às exigências de proteção coletiva da NR-35 (Trabalho em Altura) e NR-12.

### **ITEM 8.2 — ESCADA METÁLICA DE ACESSO AO TELHADO EM AÇO INOX (COMP-CAG-15)**
Fabricação e montagem de 01 (uma) escada metálica inclinada de acesso seguro da laje ao telhado em aço inoxidável AISI 304.
* **Montantes e Estrutura:** Lances em tubos de aço inox de 2" (lances de h=1,45 m e h=1,10 m) e longarinas de sustentação principal em tubo de aço inox de 4" (L=1,45 m).
* **Degraus:** 4 degraus confeccionados em chapa dobrada de aço inox com estamparia/relevo antiderrapante, dimensões de 0,45 m de largura x 0,10 m de piso.
* **Ancoragem:** Fixação superior na borda da laje e inferior no piso da cobertura com flanges e chumbadores de expansão em aço inox.

---

## 📋 Fichas Técnicas no Padrão `modelo-item-orcamentario`

```yaml
# ITEM 8.1
item:
  numero: "8.1"
  codigo: "SINAPI 100862"
  sistema: "SINAPI-ES"
  descricao: >
    Guarda-corpo na cobertura da caixa d'água em tubos de aço inox 2" (corrimão e postes h=1,10m) e 1/2" (3 travessas intermediárias),
    15 postes com canoplas de acabamento redondo 4" e bases 10x10cm fixadas à laje com parafusos inox.
  unidade: "m"
  quantidade: 22.00
  custo_unitario_sem_bdi: 380.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 475.00
  preco_total_com_bdi: 10450.00
  fonte: {nome: "SINAPI-ES (100862) + Composição Inox", data_base: "07/2026", arquivo_referencia: "guarda corpo cobertura e escada de acesso ao telhado.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "22 metros lineares de guarda-corpo em inox AISI 304."

# ITEM 8.2
item:
  numero: "8.2"
  codigo: "COMP-CAG-15"
  sistema: "SINAPI / COTAÇÃO INOX"
  descricao: >
    Escada metálica de acesso ao telhado em tubos de aço inox 2" com degraus em chapa inox (0,45x0,10m) e longarinas em tubo inox 4".
  unidade: "un"
  quantidade: 1.00
  custo_unitario_sem_bdi: 2450.00
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 3062.50
  preco_total_com_bdi: 3062.50
  fonte: {nome: "Composição Própria", data_base: "07/2026", arquivo_referencia: "guarda corpo cobertura e escada de acesso ao telhado.pdf"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Escada inox para acesso seguro à laje superior."
```

---

## 📊 Tabela Consolidada de Composição — Grupo 8.0

| Item | Código | Descrição | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | Total s/ BDI (R$) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **8.1** | SINAPI 100862 | Guarda-corpo na cobertura da caixa d'água em tubos de aço inox 2" e 1/2", bases 10x10cm e canoplas 4" | m | 22,00 | 380,00 | 8.360,00 | 475,00 | 10.450,00 |
| **8.2** | COMP-CAG-15 | Escada metálica de acesso ao telhado em tubos de aço inox 2" com degraus inox e longarinas 4" | un | 1,00 | 2.450,00 | 2.450,00 | 3.062,50 | 3.062,50 |
| **TOTAL**| | **SUBTOTAL DO GRUPO 8.0** | | | | **R$ 10.810,00** | | **R$ 13.512,50** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Medição realizada por metro linear (`m`) de guarda-corpo e por unidade (`un`) de escada inox instalada.
2. **Resistência Mecânica (NR-35 / NR-12):** Teste de aplicação de carga estática horizontal de 100 kgf/m sobre o corrimão sem deformação permanente.
3. **Qualidade do Inox:** Inspeção das soldas TIG limpas/passivadas e ausência de pontos de contaminação por aço carbono.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação do Engº. Luis Fernando Dias:**  
> Por favor, revise as especificações e insumos dos **Itens 8.1 e 8.2 (Grupo 8.0)** acima.  
> Assim que aprovado, prosseguiremos para a conclusão com o **Grupo 9.0 (Remoção do Telhado)** e **Grupo 10.0 (Limpeza Geral da Obra)**!
