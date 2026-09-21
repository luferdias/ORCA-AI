# Procedimento Operacional Padrão (POP)
## Pipeline de Geração do Dossiê Completo de Contratação Pública

---

## 1. Fluxo Integrado de Ponta a Ponta

```mermaid
flowchart TD
    A["1. Recebimento da Demanda / Projetos"] --> B["2. EAP & Quantitativos (Agente 2)"]
    B --> C["3. Operação Orçafascio (Agente 3 / LfD)"]
    C --> D{"Possui Insumo de Mercado?"}
    D -- Sim --> E["4. Pesquisa Escalonada (Agente 4: Vitória->RJ->SP->BH)"]
    E --> F["5. Pausa & Validação Humana"]
    F --> G["6. Composição Própria SRAES-CP (Agente 2)"]
    D -- Não --> H["7. Cálculo de BDI (Agente 5)"]
    G --> H
    H --> I["8. Cronograma Físico-Financeiro (Agente 6)"]
    I --> J["9. Especificação Técnica & TR (Agente 7)"]
    J --> K["10. Compilação das Planilhas Excel (Agente 8)"]
    K --> L["11. Auditoria de Guardrails G01-G10 (Agente 9)"]
    L --> M{"Status Auditoria?"}
    M -- Aprovado --> N["12. Emissão do Dossiê Final em PDF/DOCX"]
    M -- Bloqueado --> O["Correção Técnica pelo Agente Responsável"]
    O --> L
```

---

## 2. Relação das Peças Finais Geradas

1. `01_Planilha_Orcamentaria_Analitica.xlsx`
2. `02_Composicoes_Custos_Unitarios_Proprias.xlsx`
3. `03_Demonstrativo_e_Justificativa_BDI.pdf`
4. `04_Cronograma_Fisico_Financeiro.xlsx`
5. `05_Especificacao_Tecnica_e_Memorial_Descritivo.docx` / `.pdf`
6. `06_Mapa_Cotacoes_Pesquisa_Mercado.pdf`
7. `07_Relatorio_Conformidade_e_Auditoria_G01_G10.pdf`
