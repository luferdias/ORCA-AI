# Log de Decisões

| Data | Decisão | Motivo | Responsável | Evidência |
| --- | --- | --- | --- | --- |
| 29/10/2026 | Migração da pasta `Item 07 - Pintura_externa_MGIES` para `2026-007-pintura-externa` na estrutura única 00-entrada a 07-assinados | Fase F2 da especificação ORCA-AI 2.0 | Eng.º Luis Fernando, com o Claude Code | `docs/manifesto_migracao_2026.md` |
| 07/11/2026 | Ressalva G-02 do item 2.11 (BDI 24,95%) reconhecida como falso positivo e removida; status do item passa a APROVADO. Orçamento assinado não alterado | O BDI aplicado é 25,00%. O Orçafascio trunca o valor do BDI (R$ 3,6275 → R$ 3,62), e a comparação de um centavo no normalizador falhava por ponto flutuante (0,010000000000001 > 0,01). O truncamento deixa o total R$ 31,78 abaixo do arredondamento, a favor da Administração | Eng.º Luis Fernando (autorização), com o Claude Code | `orca_tools.normalizar_planilha.preco_bate_com_bdi`; `05-validacoes/relatorio-guardrails.md` |
