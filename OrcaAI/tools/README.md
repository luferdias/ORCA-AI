# Ferramentas Python do ORCA-AI (`orca_tools`)

Pacote com os módulos de cálculo e validação que antes ficavam em `OrcaAI/skills/` e `OrcaAI/scripts/`.

| Pasta | Conteúdo |
| --- | --- |
| `orca_tools/` | `bdi_calculator`, `cronograma_generator`, `excel_budget_generator`, `code_guardrail_validator`, `estrutura_projeto`, `catalogo` (fonte única dos agentes), `indice_bases` (A9), `normalizar_planilha` (A8), `renderizar` (DOCX e PDF) |
| `cli/` | `criar_projeto.py`, `validar_estrutura.py`, `gerar_indice_dossie.py`, `orcafascio_es_automation.py`, `gerar_projecoes.py` (projeções do catálogo), `indexar_bases.py` (índices locais), `validar_item.py` (item de ponta a ponta: normaliza, audita G-01 e G-02, confere códigos nos índices) |
| `windows/` | scripts PowerShell de conversão para PDF, da época em que o projeto rodava no Windows |
| `tests/` | testes do pacote |

Executar, com o ambiente `.venv` da raiz do repositório (tem `openpyxl` e `pytest`):

```bash
cd OrcaAI/tools
../../.venv/bin/python -m pytest -q
../../.venv/bin/python cli/validar_estrutura.py
../../.venv/bin/python cli/criar_projeto.py 2026-013-nome-do-servico
../../.venv/bin/python cli/criar_projeto.py 2026-013-nome-do-servico --etapa 03-orcamento
../../.venv/bin/python cli/gerar_projecoes.py --verificar
../../.venv/bin/python cli/indexar_bases.py --todas 2026-04
../../.venv/bin/python cli/validar_item.py 2026-007-pintura-externa
```

O ambiente precisa de `pyyaml` (catálogo) e `openpyxl` (planilhas), ambos em `OrcaAI/ufg/ml/requirements.txt`. Os índices locais ficam em `OrcaAI/knowledge/indices/` e só os manifestos são versionados.

Scripts de uso único de documentos SEI ficam em `projetos/_governanca_sei_agu_cgu/scripts/`; os do Entregável 3 (TRL e PI) ficam em `docs/historico/entregavel_3_scripts/`.
