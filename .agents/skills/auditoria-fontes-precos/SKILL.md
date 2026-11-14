---
name: auditoria-fontes-precos
description: Audita fontes de preco, data-base, rastreabilidade, coerencia de unidades e evidencias usadas em orcamentos publicos.
allowed-tools: read_file, run_command
---

# Auditoria de Fontes de Precos

Use esta skill como revisao independente antes de finalizar o orcamento.

## Checklist

- Todo item tem fonte.
- Toda fonte tem data-base.
- A unidade da fonte bate com a unidade orcada.
- O BDI aplicado e coerente com o tipo de item.
- Pesquisa de mercado tem 3 cotacoes ou justificativa.
- Composicao propria tem memoria e aprovacao.
- Itens A da curva ABC foram revisados.
- Itens importados do Orcafascio foram exportados ou registrados.

## Saida Padrao

```markdown
| Severidade | Item | Problema | Evidencia | Acao recomendada |
| --- | --- | --- | --- | --- |
```

