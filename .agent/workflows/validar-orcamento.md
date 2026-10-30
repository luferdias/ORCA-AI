---
description: Valida planilha, códigos, fontes, BDI, curva ABC e riscos antes dos documentos finais.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /validar-orcamento

$ARGUMENTS

**Plataforma:** claude_code · **Aciona:** A4 AuditorDuplaChecagem, subagente `validador-codigos`

## Objetivo

Valida planilha, códigos, fontes, BDI, curva ABC e riscos antes dos documentos finais.

## Fluxo

1. Acionar validador-codigos (validate_codes.py) contra as bases locais.
2. Acionar A4 para G-01 a G-10, curva ABC, auditoria de fontes e matriz de riscos.
3. Gerar relatórios em 05-validacoes/.

## Saída

- validacao-codigos.md
- relatorio-guardrails.md
- curva-abc.md
- lista de bloqueios
