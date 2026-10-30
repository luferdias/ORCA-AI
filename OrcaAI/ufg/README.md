# Bloco UFG — projeto final do curso de Agentes Inteligentes

Este bloco reúne tudo o que é acadêmico no ORCA-AI, separado do trabalho
profissional da SRA-ES (regras R-E3 e R-E4 da entrevista de maturidade de
30/10/2026). O restante de `OrcaAI/` é o **modo SRAES**, padrão de toda
sessão; este bloco é o **modo UFG**, acionado por `/experimento-ml` ou quando
o engenheiro disser que está no projeto da UFG.

| Pasta | Conteúdo |
| --- | --- |
| `ml/` | Código, testes, dados derivados e entregas da disciplina de aprendizado de máquina (antes `OrcaAI/ml/`). As execuções ficam em `ml/outputs/`, fora do Git, com manifestos versionados. |
| `spec/` | Proposta, plano, critérios de dados e avaliação, organograma e contrato da API Knowledge (antes `OrcaAI/spec/ml_ufg/`). |
| `ml/entregas/` | Entregas feitas, com links permanentes ao commit `e20741b`, que continuam válidos porque apontam para a versão antiga do repositório. |

Regras do modo UFG:

- Lê as bases em `OrcaAI/bases/`, os índices em `OrcaAI/knowledge/indices/` e o
  acervo em `OrcaAI/projetos/`; nunca escreve neles.
- Não altera `OrcaAI/agents/catalogo.yaml` nem `OrcaAI/knowledge/padroes/`.
- Agentes: A12 PesquisadorMLUFG e os cinco subagentes de ML do catálogo.
- Ambiente Python: `.venv` na raiz do repositório
  (`python3.12 -m venv .venv && .venv/bin/pip install -r OrcaAI/ufg/ml/requirements-dev.txt`).
- Testes: `cd OrcaAI/ufg/ml && ../../../.venv/bin/python -m pytest -q`.

A ferramenta para a estrutura da apresentação do projeto final ainda será
confirmada pelo engenheiro (registro em
`OrcaAI/knowledge/padroes/entrevista-maturidade-2026-10.md`, pergunta 14).
