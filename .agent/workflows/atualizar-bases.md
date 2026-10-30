---
description: Baixa a edição vigente das tabelas oficiais e reconstrói o índice local.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /atualizar-bases

$ARGUMENTS

**Plataforma:** antigravity · **Aciona:** A11 PesquisadorPortaisMercado, A9 MineradorBases

## Objetivo

Baixa a edição vigente das tabelas oficiais e reconstrói o índice local.

## Fluxo

1. Acionar A11 para consultar cada portal do catálogo pela regra da última tabela.
2. Guardar o ZIP original em bases/<fonte>/<competencia>/originais/ com manifesto (URL, publicação, tamanho, SHA-256).
3. Acionar A9 para ingerir e reconstruir knowledge/indices/ com manifesto.
4. Atualizar bases/catalogo_fontes_referenciais.json.

## Saída

- ZIP original
- manifesto
- índice
