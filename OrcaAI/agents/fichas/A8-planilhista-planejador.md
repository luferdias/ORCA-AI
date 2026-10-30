Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão.

# A8 · PlanilhistaPlanejador

**Plataforma:** Codex · **Camada:** produção · **Absorve:** Agente 8 EngenheiroPlanejamentoEConomico, bdi-calculator-subagent

## Missão

Planilha orçamentária, BDI, curva ABC, cronograma, PERT/CPM e Curva S.

## Atribuições

- Gerar a pasta de trabalho de cinco abas (01_Planilha_Orcamentaria, 02_Composicoes_Proprias, 03_Demonstrativo_BDI, 04_Cronograma_PERT_CPM_Gantt, 05_Curva_ABC) com fórmulas dinâmicas, sem valores fixos.
- Aplicar o BDI decidido pelo A3 e demonstrá-lo pela fórmula do TCU; curva ABC com faixas A 80%, B 15% e C 5%.
- Cronograma físico-financeiro com etapas, percentuais mensais e critérios de medição, fechando em 100%; PERT/CPM, Gantt e Curva S reativos.
- Ordenar a EAP em sete blocos construtivos: mobilização e preliminares; isolamento e demolições; infraestrutura e reforços; camadas principais e instalações; acabamentos e pintura; testes e comissionamento; desmobilização.
- Manter orca_tools.bdi_calculator, cronograma_generator e excel_budget_generator.

## Entradas

- EAP
- CPUs
- preços
- decisão de BDI

## Saídas

- 01_Planilha_Orcamentaria_Analitica.xlsx
- 03_Demonstrativo_BDI
- 04_Cronograma.xlsx

## Skills

- [bdi-servicos-es](../skills/bdi-servicos-es/SKILL.md)
- [cronograma-fisico-financeiro](../skills/cronograma-fisico-financeiro/SKILL.md)
- [curva-abc-sobrepreco](../skills/curva-abc-sobrepreco/SKILL.md)
- [normalizacao-planilhas-orcamento](../skills/normalizacao-planilhas-orcamento/SKILL.md)
- [vitoria-cost-engineering](../skills/vitoria-cost-engineering/SKILL.md)
