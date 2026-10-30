---
name: guardrails-orcamento-publico
description: >
  Skill de validação cruzada e controle de qualidade para orçamentos da
  Administração Pública Federal. Atua como camada de guardrail, executando
  verificações automáticas de conformidade legal, consistência de
  coeficientes, ausência de sobrepreço, integridade da EAP e
  rastreabilidade de fontes. Aciona automaticamente após qualquer geração
  de planilha orçamentária.
allowed-tools: search_web, run_command, read_file
---

# Guardrails de Orçamento Público

Sempre que a planilha orçamentária final for gerada, você deve executar as seguintes verificações de conformidade antes de apresentar os resultados ao usuário:

## Validadores (G-01 a G-10)

1.  **G-01 (Código referencial válido):** Verificar se todos os itens possuem código de fonte oficial (SINAPI, SICRO, IOPES, Orçafascio) ou prefixo `SRAES-FV-` para composições próprias. Não devem existir "códigos inventados".
2.  **G-02 (BDI compatível com a natureza):** Garantir que os itens de fornecimento de material aplicam o BDI diferenciado (Ex: 14%), e itens de serviço aplicam o BDI de serviço (Ex: 25% para Vitória).
3.  **G-03 (Coeficiente plausível):** Analisar a produtividade adotada para a limpeza e manutenção.
4.  **G-04 (Dupla contagem):** Se houver manutenção menor já inclusa na limpeza (item 1), o item 6 (manutenção menor) deve estar com quantidade 0 (zero) na planilha.
5.  **G-05 (Curva ABC):** Nenhum item isolado deve concentrar o risco (excesso de dependência), a menos que devidamente justificado.
6.  **G-06 (Encargos sociais):** Verificar se a planilha foi orçada toda com encargos Desonerados ou Não Desonerados. Não misturar regimes.
7.  **G-07 (Data-base coerente):** Todos os preços devem refletir o mesmo mês de referência (Ex: 05/2026). Se usar cotações, garantir que estejam validadas na mesma janela temporal.
8.  **G-08 (Fundamentação legal):** O orçamento deve citar as normativas (Lei 14.133, Decreto 7.983, Acórdãos do TCU).
9.  **G-09 (Regime jurídico declarado):** Indicar explicitamente quais itens são de "engenharia" (Decreto 7.983) e quais são de "comum/aquisição" (IN 65/2021).
10. **G-10 (Cotação válida - itens 4 e 5):** Para fornecimento (ex: módulos fotovoltaicos), atestar que foi realizada pesquisa com 3 propostas para definir o preço, se aplicável.

## Relatório de Auditoria
A saída desta validação deve ser formatada em um bloco de resultados como **Relatório de Conformidade**, indicando o Status de cada validação e eventuais "Ressalvas" ou "Necessita Revisão Humana".
