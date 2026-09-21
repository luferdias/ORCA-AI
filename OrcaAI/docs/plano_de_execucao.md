# Plano de Execucao

## Objetivo

Elaborar a planilha orçamentária para a Reforma da Estrutura Suporte da CAG no Edifício Sede MGI/ES, Vitória/ES (Órgão: SRA-ES)

## Agentes Envolvidos

| Agente | Papel |
| --- | --- |
| `central-orchestrator` | Coordenacao |
| `engenheiro-orcamentista-publico` | Analise tecnica |
| `compositor-custos` | Orcamento |
| `validador-codigos` | Validacao |
| `guardrail-controladoria` | Controle |
| `documentalista-tecnico` | Documentos |
| `revisor-final` | Revisao final |

## Tarefas

| Fase | Tarefa | Responsavel | Saida | Status |
| --- | --- | --- | --- | --- |
| 0 | Triagem | intake-triage-agent | projeto.md | concluido |
| 1 | Quantitativos | quantity-takeoff-subagent | quadro de quantitativos | pendente |
| 2 | Bases oficiais | pesquisador-bases-oficiais | mapa de fontes | pendente |
| 3 | Composicao | compositor-custos | planilha normalizada | pendente |
| 4 | Validacao | validador-codigos | relatorio | pendente |
| 5 | Guardrails | guardrail-controladoria | achados | pendente |
| 6 | Documentos | documentalista-tecnico | documentos finais | pendente |
| 7 | Dossie | revisor-final | checklist final | pendente |

## Pontos de Aprovacao

| Ponto | Motivo | Status |
| --- | --- | --- |
| 1. Escopo e Quantitativos | Validar se o levantamento atende às necessidades da reforma da CAG | pendente |
| 2. Bases e Fontes de Preços | Aprovar as fontes oficiais (SINAPI/IOPES) e eventuais cotações locais | pendente |
| 3. Planilha Preliminar | Validação e aprovação do valor total estimado | pendente |


# python scripts\orcafascio_es_automation.py

