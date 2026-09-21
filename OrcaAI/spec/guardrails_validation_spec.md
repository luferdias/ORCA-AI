# Especificação dos Validadores e Guardrails (G-01 a G-10)
## Controle de Qualidade, Rastreabilidade e Conformidade Legal

---

## 1. Matriz de Guardrails

O OrcaAI executa 10 validações automatizadas antes de autorizar a emissão de qualquer planilha, memória de cálculo ou arquivo para assinatura:

| ID | Validador | Regra e Critério de Conformidade | Bloqueio / Ação |
| :--- | :--- | :--- | :--- |
| **G-01** | **Código Referencial Válido** | Todo item deve ter código oficial existente (SINAPI, IOPES, SICRO, ORSE) ou código próprio no formato `SRAES-CP-XXX` / `SRAES-INS-XXX`. | Bloqueio imediato se houver código inexistente ou arbitrário. |
| **G-02** | **BDI por Natureza** | Serviços aplicam **25,00%** de BDI; Fornecimento puro de materiais/equipamentos aplica **14,02%** (Acórdão TCU 2.622/2013). | Alerta e recálculo automático do BDI divergente. |
| **G-03** | **Produtividade Plausível** | Coeficientes de mão de obra (horas/unidade) e equipamentos devem respeitar os limites médios das tabelas SINAPI/IOPES. | Notificação de discrepância de rendimento. |
| **G-04** | **Prevenção de Dupla Contagem** | Serviços contínuos (O&M, limpeza) não podem cobrar separadamente por manutenções menores já embutidas na taxa global. | Zera quantitativo do item em duplicidade. |
| **G-05** | **Curva ABC Auditada** | Itens da Faixa A (que concentram 80% do valor da obra) devem ter 100% de conferência documental e cotações robustas. | Exige justificativa técnica reforçada para a Faixa A. |
| **G-06** | **Encargos Sociais Homogêneos** | Toda a planilha deve adotar o mesmo regime de encargos (Desonerado ou Não Desonerado). É vedada a mescla de regimes. | Bloqueio de orçamentos com regimes conflitantes. |
| **G-07** | **Data-Base Coerente** | Todos os preços devem pertencer à mesma janela temporal de referência regional (ex: mês/ano atual de Vitória-ES). | Notificação de preços defasados temporalmente. |
| **G-08** | **Fundamentação Legal Expressa** | Os documentos técnicos devem citar expressamente a Lei 14.133/2021, Decreto 7.983/2013 e Acórdão TCU 2.622/2013. | Injeção automática das notas legais obrigatórias. |
| **G-09** | **Regime Jurídico Declarado** | Segregação clara entre serviços de engenharia (Decreto 7.983) e aquisições/serviços comuns (IN 65/2021). | Separação das parcelas no termo de referência. |
| **G-10** | **Cotações Válidas (Mercado)** | Qualquer insumo de mercado deve possuir no mínimo 3 propostas formais válidas com identificação de fornecedor. | Bloqueio de inclusão de preço próprio sem 3 propostas. |
