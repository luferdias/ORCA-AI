---
description: Abre um novo projeto de orcamento publico na Central Orca e conduz o fluxo completo de triagem, planejamento, composicao, validacao e dossie.
---

# /novo-orcamento

$ARGUMENTS

## Objetivo

Criar ou iniciar um projeto de orcamento publico assistido por agentes.

## Fluxo

1. Acionar `central-orchestrator`.
2. Acionar `intake-triage-agent`.
3. Criar pasta em `projetos/`.
4. Criar `projeto.md` e `log-decisoes.md`.
5. Acionar `project-planner`.
6. Classificar servico e skills obrigatorias.
7. Iniciar extracao de escopo e quantitativos.

## Saida

- Pasta de projeto criada.
- `projeto.md`.
- `plano-execucao.md`.
- Lista de pendencias iniciais.

