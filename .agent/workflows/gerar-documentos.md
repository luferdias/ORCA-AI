---
description: Gera especificacao tecnica, memoriais, demonstrativo de BDI, termo de referencia e relatorios a partir da planilha validada.
---

# /gerar-documentos

$ARGUMENTS

## Objetivo

Produzir documentos tecnicos coerentes com a planilha orcamentaria.

## Fluxo

1. Confirmar que validacoes foram executadas.
2. Acionar `documentalista-tecnico`.
3. Escolher templates em `templates/`.
4. Gerar documentos em `06-documentos/`.
5. Acionar `document-renderer-subagent`.

## Saida

- Especificacao tecnica.
- Memorial ou termo de referencia.
- Demonstrativo de BDI.
- Relatorio de cotacoes, quando houver.

