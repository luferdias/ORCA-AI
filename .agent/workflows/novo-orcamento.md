---
description: Abre um item de orçamento e conduz triagem, planejamento e extração inicial de escopo.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /novo-orcamento <slug>

$ARGUMENTS

**Plataforma:** claude_code · **Aciona:** A1 OrcaMaestro, A3 EngenheiroCivilSenior

## Objetivo

Abre um item de orçamento e conduz triagem, planejamento e extração inicial de escopo.

## Fluxo

1. Acionar A1 para a triagem e as perguntas mínimas.
2. Criar a pasta com tools/cli/criar_projeto.py <slug> e preencher projeto.md.
3. Acionar A1 para plano-execucao.md: objetivo, escopo, entradas, agentes, skills, tarefas, critérios e pausas.
4. Acionar A3 para extrair escopo e quantitativos iniciais.

## Saída

- pasta do item
- projeto.md
- plano-execucao.md
- pendências iniciais
