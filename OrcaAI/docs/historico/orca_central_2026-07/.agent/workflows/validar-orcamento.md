---
description: Valida planilha orcamentaria, codigos SINAPI/IOPES, fontes, BDI, curva ABC e riscos de sobrepreco.
---

# /validar-orcamento

$ARGUMENTS

## Objetivo

Rodar verificacoes tecnicas antes de gerar documentos finais.

## Fluxo

1. Acionar `validador-codigos`.
2. Acionar `code-validator-subagent`.
3. Acionar `guardrail-controladoria`.
4. Aplicar `curva-abc-sobrepreco`.
5. Aplicar `auditoria-fontes-precos`.
6. Gerar relatorios em `05-validacoes/`.

## Saida

- `validacao-codigos.md`.
- `relatorio-guardrails.md`.
- `curva-abc.md`.
- Lista de bloqueios criticos.

