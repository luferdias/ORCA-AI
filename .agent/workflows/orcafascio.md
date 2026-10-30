---
description: Opera o Orçafascio em modo autônomo supervisionado, com trava anti-alucinação.
---

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

# /orcafascio

$ARGUMENTS

**Plataforma:** antigravity · **Aciona:** A10 PilotoOrcafascio, A4 AuditorDuplaChecagem

## Objetivo

Opera o Orçafascio em modo autônomo supervisionado, com trava anti-alucinação.

## Fluxo

1. Ler projeto.md e os padrões validados em knowledge/padroes/.
2. Abrir o Orçafascio e aguardar o login manual do engenheiro.
3. Confirmar o De acordo em log-decisoes.md antes de qualquer inserção.
4. Para cada item: buscar, submeter o código ao A4, gravar só com aprovação; sem item exato, suspender e acionar A1.
5. Exportar para bases/orcafascio-export/ e registrar base, UF, data-base e arquivo.

## Saída

- itens inseridos
- exportação
- evidências

## Regras

- Não armazenar, solicitar ou digitar senha.
- Não criar composição própria sem aprovação humana.
