# Arquitetura do ORCA-AI no Antigravity

<!-- Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão. -->

## Agentes

- `piloto-orcafascio` — A10 PilotoOrcafascio
- `pesquisador-portais-mercado` — A11 PesquisadorPortaisMercado

## Subagentes

- `navegador-orcafascio`
- `navegador-portais`
- `coletor-cotacoes`

## Skills

- `auditoria-fontes-precos`
- `orcafascio-integration`
- `orcafascio-mgi-automation`
- `pesquisa-mercado-licitacoes`
- `pesquisa-mercado-vitoria`
- `vitoria-cost-engineering`

## Workflows

- `/novo-orcamento` (claude_code)
- `/observar-orcafascio` (antigravity)
- `/orcafascio` (antigravity)
- `/pesquisar-precos` (antigravity)
- `/atualizar-bases` (antigravity)
- `/validar-orcamento` (claude_code)
- `/gerar-documentos` (codex)
- `/instruir-sei` (claude_code)
- `/gerar-dossie` (claude_code)
- `/revisar-final` (claude_code)
- `/status-orca` (qualquer)
- `/auditar-5s` (claude_code)
- `/experimento-ml` (claude_code)

Fonte única: `OrcaAI/agents/catalogo.yaml`. Fichas completas: `OrcaAI/agents/fichas/`.
