---
description: Usa automacao segura do Orcafascio para consultar bases, compor itens, exportar planilhas e registrar evidencias.
---

# /orcafascio

$ARGUMENTS

## Objetivo

Consultar ou operar o Orcafascio dentro de um projeto orcamentario.

## Fluxo

1. Ler `projeto.md`.
2. Acionar `orcamentista-mgi-es`.
3. Acionar `browser-orcafascio-subagent`.
4. Aguardar o login manual do engenheiro na tela do Orcafascio.
5. Consultar bases e exportar evidencias.
6. Registrar resultados em `log-decisoes.md`.

## Regras

- Nao armazenar, solicitar ou digitar senha; o engenheiro faz o login.
- Nao criar composicao propria sem aprovacao humana.
- Registrar base, UF, data-base e arquivo exportado.

