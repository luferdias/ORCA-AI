---
description: Executa revisao final de coerencia entre escopo, orcamento, memoria, documentos e dossie.
---

# /revisar-final

$ARGUMENTS

## Objetivo

Fazer a revisao final antes de assinatura, envio ou instrucao processual.

## Fluxo

1. Acionar `revisor-final`.
2. Conferir bloqueios do `guardrail-controladoria`.
3. Revisar documentos finais.
4. Gerar `checklist-final.md`.
5. Pausar para aprovacao humana.

## Saida

Status final: aprovado, aprovado com ressalvas ou bloqueado.

