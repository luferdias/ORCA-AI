---
description: Pesquisa de mercado para itens sem base oficial, com três cotações e aprovação humana.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /pesquisar-precos

$ARGUMENTS

**Plataforma:** antigravity · **Aciona:** A11 PesquisadorPortaisMercado, subagente `coletor-cotacoes`

## Objetivo

Pesquisa de mercado para itens sem base oficial, com três cotações e aprovação humana.

## Fluxo

1. Acionar A11 na cascata Vitória, RJ, SP e BH.
2. Acionar coletor-cotacoes para organizar propostas e evidências.
3. Gerar 04-cotacoes/relatorio-cotacoes.md com mediana e descartes motivados.
4. Pausar para aprovação e registrar em log-decisoes.md.

## Saída

- tabela de cotações
- critério de preço adotado
- pendência ou aprovação
