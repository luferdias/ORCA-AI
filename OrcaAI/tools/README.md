# Ferramentas Python do ORCA-AI (`orca_tools`)

Pacote com os módulos de cálculo e validação que antes ficavam em `OrcaAI/skills/` e `OrcaAI/scripts/`.

| Pasta | Conteúdo |
| --- | --- |
| `orca_tools/` | `bdi_calculator`, `cronograma_generator`, `excel_budget_generator`, `code_guardrail_validator`, `estrutura_projeto` |
| `cli/` | `criar_projeto.py`, `validar_estrutura.py`, `gerar_indice_dossie.py`, `orcafascio_es_automation.py` |
| `windows/` | scripts PowerShell de conversão para PDF, da época em que o projeto rodava no Windows |
| `tests/` | testes do pacote |

Executar, com o ambiente de `OrcaAI/ml/.venv` (tem `openpyxl` e `pytest`):

```bash
cd OrcaAI/tools
../ml/.venv/bin/python -m pytest -q
../ml/.venv/bin/python cli/validar_estrutura.py
../ml/.venv/bin/python cli/criar_projeto.py 2026-013-nome-do-servico
```

Scripts de uso único de documentos SEI ficam em `projetos/_governanca_sei_agu_cgu/scripts/`; os do Entregável 3 (TRL e PI) ficam em `docs/historico/entregavel_3_scripts/`.
