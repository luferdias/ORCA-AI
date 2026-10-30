---
description: Monta o pacote final com índice, checklist, planilha, memória, validações, documentos e pendências.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /gerar-dossie

$ARGUMENTS

**Plataforma:** claude_code · **Aciona:** A1 OrcaMaestro, A4 AuditorDuplaChecagem

## Objetivo

Monta o pacote final com índice, checklist, planilha, memória, validações, documentos e pendências.

## Fluxo

1. Acionar A4 para a revisão final.
2. Aplicar dossie-licitacao-publica; gerar indice-dossie.md com tools/cli/gerar_indice_dossie.py.
3. Acionar A1 para listar finais e pendências.

## Saída

- indice-dossie.md
- checklist-final.md
- lista de documentos finais
