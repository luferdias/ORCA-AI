---
description: Gera especificação, memorial, TR, demonstrativo de BDI e relatórios a partir da planilha validada.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /gerar-documentos

$ARGUMENTS

**Plataforma:** codex · **Aciona:** A6 DescritorEspecificador, subagente `renderizador-documentos`

## Objetivo

Gera especificação, memorial, TR, demonstrativo de BDI e relatórios a partir da planilha validada.

## Fluxo

1. Confirmar que /validar-orcamento foi executado sem bloqueios.
2. Acionar A6 com os templates de OrcaAI/templates/.
3. Acionar renderizador-documentos para DOCX e PDF em 06-documentos/.

## Saída

- especificação técnica
- memorial ou TR
- demonstrativo de BDI
- relatório de cotações quando houver
