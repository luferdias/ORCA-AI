---
name: matriz-riscos-contratacao
description: Estrutura matriz de riscos para contratacoes publicas de obras e servicos de engenharia, vinculada ao escopo, orcamento e fiscalizacao.
allowed-tools: read_file
---

# Matriz de Riscos da Contratacao

Use esta skill para identificar riscos tecnicos, financeiros, operacionais, ambientais, contratuais e de medicao.

## Categorias

- Escopo insuficiente.
- Quantitativo incerto.
- Base de preco fraca.
- Composicao propria sensivel.
- Mobilizacao complexa.
- Interferencia predial.
- Risco de seguranca do trabalho.
- Risco ambiental.
- Risco de prazo.
- Risco de aditivo.

## Saida Padrao

```markdown
| Risco | Causa | Consequencia | Probabilidade | Impacto | Alocacao | Mitigacao |
| --- | --- | --- | --- | --- | --- | --- |
```

## Regras

- Todo risco com impacto no preco deve apontar item orcamentario relacionado.
- Todo risco de medicao deve apontar criterio de recebimento.
- Nao usar termos genericos sem acao de mitigacao.

