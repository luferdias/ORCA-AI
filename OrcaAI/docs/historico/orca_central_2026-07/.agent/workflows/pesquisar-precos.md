---
description: Conduz pesquisa de mercado para itens sem base oficial adequada, com 3 cotacoes e aprovacao humana.
---

# /pesquisar-precos

$ARGUMENTS

## Objetivo

Buscar referencias de preco quando SINAPI, IOPES, SICRO ou Orcafascio nao resolverem o item.

## Fluxo

1. Acionar `pesquisador-mercado`.
2. Acionar `quotation-harvester-subagent`.
3. Gerar `04-cotacoes/relatorio-cotacoes.md`.
4. Pausar para aprovacao.
5. Registrar decisao em `log-decisoes.md`.

## Saida

- Tabela de cotacoes.
- Criterio de preco adotado.
- Pendencia ou aprovacao humana.

