# Especificação Detalhada e Composição Analítica — Grupos 9.0 e 10.0 (Itens 9.1 e 10.1)

> **Projeto:** Reforma e Modernização da Central de Água Gelada (CAG) — Edifício Sede MGI/ES  
> **Órgão Contratante:** Superintendência Regional de Administração no Espírito Santo (SRA/ES)  
> **Responsável Técnico:** Engº. Luis Fernando Dias  
> **Grupos de Serviços:** **9.0 — REMOÇÃO E REINSTALAÇÃO DO TELHADO METÁLICO EXISTENTE** e **10.0 — LIMPEZA GERAL E DESTINAÇÃO AMBIENTAL DE RESÍDUOS**  
> **Taxa de BDI:** **25,00%**  
> **Valor Subtotal sem BDI (Grupos 9.0 e 10.0):** **R$ 1.002,60**  
> **Valor Total dos Grupos 9.0 e 10.0 (com BDI 25%):** **R$ 1.253,25**  

---

## 📝 Memorial Descritivo Detalhado — Grupos 9.0 e 10.0

### **ITEM 9.1 — REMOÇÃO E REINSTALAÇÃO DE TELHADO METÁLICO COM REAPROVEITAMENTO (SINAPI 88323)**
Desmontagem cuidadosa, armazenamento temporário e posterior remontagem/reinstalação de 20,00 m² de telhado metálico existente e sua estrutura secundária de apoio no Edifício Sede do MGI/ES.

O serviço é necessário para criação de abertura técnica temporária de passagem de vigas e içamento/posicionamento dos novos equipamentos, compressores e módulos da Central de Água Gelada (CAG).

Compreende a desfixação manual de telhas, limpeza das superfícies de sobreposição, verificação de vedação, armazenamento protegido contra intempéries, transporte vertical/horizontal e remontagem com reaproveitamento integral das telhas metálicas, utilizando parafusos autoperfurantes novos com arruelas de neoprene. Inclusos andaime tubular de encaixe, guincho elétrico e EPIs para trabalho em altura (NR-35).

### **ITEM 10.1 — LIMPEZA GERAL DE OBRA COM REMOÇÃO DE ENTULHO E DESTINAÇÃO AMBIENTAL (SINAPI 88316)**
Execução de serviços de limpeza geral final de obra em toda a área de intervenção da Central de Água Gelada (CAG), totalizando 120,00 m² de área tratada.

Compreende:
1. Varrição rigorosa, recolhimento, triagem e ensacamento de resíduos sólidos, retalhos metálicos, rebarbas de solda, sobras de materiais e embalagens.
2. Carregamento manual do entulho acumulado para caçamba/caminhão basculante de 6 m³.
3. Transporte rodoviário do entulho até aterro sanitário/unidade de reciclagem de resíduos da construção civil (RCC) devidamente credenciada e licenciada pela Prefeitura Municipal de Vitória (PMV).
4. Pagamento formal da taxa ambiental de destinação final e emissão do MTR (Manifesto de Transporte de Resíduos).

---

## 📋 Fichas Técnicas no Padrão `modelo-item-orcamentario`

```yaml
# ITEM 9.1
item:
  numero: "9.1"
  codigo: "SINAPI 88323"
  sistema: "SINAPI-ES"
  descricao: >
    Remoção e reinstalação de telhado metálico existente com reaproveitamento de materiais para permitir a passagem
    de vigas e içamento dos equipamentos da CAG, incluindo andaime tubular, guincho elétrico e fixações novas.
  unidade: "m²"
  quantidade: 20.00
  custo_unitario_sem_bdi: 21.45
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 26.81
  preco_total_com_bdi: 536.25
  fonte: {nome: "SINAPI-ES (88323)", data_base: "07/2026", arquivo_referencia: "Modernização da CAG - rev 1.xlsx"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Reaproveitamento integral das telhas removidas."

# ITEM 10.1
item:
  numero: "10.1"
  codigo: "SINAPI 88316"
  sistema: "SINAPI-ES"
  descricao: >
    Limpeza geral de obra com remoção de entulho, transporte em caminhão basculante e destinação final em aterro sanitário
    licenciado credenciado pela PMV com pagamento de taxa ambiental e MTR. AF_04/2019.
  unidade: "m²"
  quantidade: 120.00
  custo_unitario_sem_bdi: 4.78
  bdi_percentual: 25.00
  preco_unitario_com_bdi: 5.98
  preco_total_com_bdi: 717.00
  fonte: {nome: "SINAPI-ES (88316, 90776) + Taxa PMV", data_base: "07/2026", arquivo_referencia: "Modernização da CAG - rev 1.xlsx"}
  validacao: {codigo_encontrado: true, unidade_compativel: true, descricao_compativel: true}
  observacoes: "Comprovação com Manifesto de Transporte de Resíduos (MTR)."
```

---

## 📊 Tabela Consolidada de Composição — Grupos 9.0 e 10.0

| Item | Código | Descrição | Unid. | Qtd. | Custo Unit. s/ BDI (R$) | Total s/ BDI (R$) | Preço Unit. c/ BDI (R$) | Preço Total c/ BDI (R$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **9.1** | SINAPI 88323 | Remoção e reinstalação de telhado metálico existente com reaproveitamento | m² | 20,00 | 21,45 | 429,00 | 26,81 | 536,25 |
| **10.1**| SINAPI 88316 | Limpeza geral de obra com remoção de entulho e destinação em aterro PMV | m² | 120,00 | 4,78 | 573,60 | 5,98 | 717,00 |
| **TOTAL**| | **SUBTOTAL DOS GRUPOS 9.0 E 10.0** | | | | **R$ 1.002,60** | | **R$ 1.253,25** |

---

## 🔍 Critérios de Medição, Testes e Aceitação
1. **Medição:** Medição do Item 9.1 efetuada por metro quadrado (`m²`) de telhado remontado sem vazamentos, e do Item 10.1 por metro quadrado (`m²`) de área limpa e entregue.
2. **Comprovação Ambiental:** Apresentação obrigatória dos comprovantes de pagamento da taxa de destinação final e do Manifesto de Transporte de Resíduos (MTR) emitido pelo aterro credenciado pela PMV.
3. **Recebimento Definitivo:** Inspeção visual de entrega da obra sem qualquer vestígio de entulhos ou materiais sobrantes.

---

## 🛑 Ponto de Parada para Validação do Usuário

> **Aguardando aprovação final do Engº. Luis Fernando Dias:**  
> Por favor, revise as especificações dos **Itens 9.1 e 10.1 (Grupos 9.0 e 10.0)** acima.  
> Com a aprovação destes últimos itens, concluiremos a validação de 100% da **Revisão 2 (Rev. 2)** do Orçamento da CAG!
