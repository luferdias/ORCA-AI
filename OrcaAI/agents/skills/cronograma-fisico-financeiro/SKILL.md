---
name: cronograma-fisico-financeiro
description: Cria cronogramas fisico-financeiros vinculados ao orcamento, com etapas, percentuais mensais, desembolso e criterios de medicao.
allowed-tools: read_file, run_command
---

# Cronograma Fisico-Financeiro

Use esta skill quando o orcamento precisar de distribuicao temporal, medicao mensal ou planejamento de execucao.

## Procedimento

1. Agrupar itens por etapa de execucao.
2. Definir duracao prevista.
3. Distribuir percentuais por periodo.
4. Vincular parcelas aos criterios de medicao.
5. Conferir se a soma fisica e financeira fecha em 100%.

## Saida Padrao

```markdown
| Etapa | Mes 1 | Mes 2 | Mes 3 | Total | Criterio de medicao |
| --- | ---: | ---: | ---: | ---: | --- |
```

## Regras

- Nao criar cronograma incompatível com a sequencia executiva.
- Declarar premissas de produtividade e mobilizacao.
- Destacar itens de entrega unica ou fornecimento isolado.

