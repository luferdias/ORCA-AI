# Trabalho da disciplina: três tarefas de aprendizado de máquina

**Autor:** engenheiro Luis Fernando  
**Instituição:** Universidade Federal de Goiás (UFG)  
**Professor:** Ronaldo  
**Disciplina:** Aprendizado de máquina aplicado a dados estruturados  
**Projeto aplicado:** ORCA-AI  
**Recorte:** pintura, revestimentos e forros, e pisos em m²

## Arquivos para leitura

- **[PDF para o professor Ronaldo, com links clicáveis no GitHub](entregas/professor_ronaldo_2026-09-28/relatorio.pdf).**
- [Edição para o professor em HTML](entregas/professor_ronaldo_2026-09-28/relatorio.html) e [Markdown](entregas/professor_ronaldo_2026-09-28/RELATORIO.md).
- [Desenvolvimento público no GitHub, na versão avaliada](https://github.com/luferdias/ORCA-AI/tree/e20741b0214dff489147fa04739bb2a1ed44bc07/OrcaAI/ml).
- [Dados e resultados da execução no GitHub](https://github.com/luferdias/ORCA-AI/tree/e20741b0214dff489147fa04739bb2a1ed44bc07/OrcaAI/ml/outputs/entrega_ufg_acabamentos_2026-09-27).

Em 28/09/2026, o engenheiro Luis Fernando autorizou tornar o repositório público para consulta e download. A escrita permanece restrita às contas autorizadas. Os links do PDF fixam o commit `e20741b0214dff489147fa04739bb2a1ed44bc07`, que contém o código experimental e os resultados avaliados. A edição acrescenta navegação para o professor e preserva as métricas de 27/09/2026.

### Versão anterior, preservada

- [Relatório acadêmico em PDF](outputs/entrega_ufg_acabamentos_2026-09-27/relatorio_consolidado/relatorio.pdf).
- [Relatório navegável, com gráficos e tabelas](outputs/entrega_ufg_acabamentos_2026-09-27/relatorio_consolidado/relatorio.html).
- [Texto do relatório em Markdown](outputs/entrega_ufg_acabamentos_2026-09-27/relatorio_consolidado/RELATORIO.md).
- [Registro da execução, parâmetros e hashes](outputs/entrega_ufg_acabamentos_2026-09-27/execucao_estudo.json).
- [Plano e critérios definidos para os experimentos](../spec/ml_ufg/plano_consolidacao_acabamentos.md).

## Código para executar no VS Code

Abra [ORCA-ML.code-workspace](ORCA-ML.code-workspace), selecione o Python de `.venv/bin/python` e execute:

- [executar_classificacao.py](executar_classificacao.py): classificação supervisionada.
- [executar_agrupamento.py](executar_agrupamento.py): agrupamento não supervisionado.
- [executar_estudo.py](executar_estudo.py): as três tarefas e o relatório consolidado.

No terminal integrado, dentro desta pasta:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python executar_estudo.py
```

O programa usa os ZIPs locais de maio/2026 e os históricos já preparados. Cada execução gera uma pasta nova em `outputs/`; o terminal informa os caminhos. Mantenha a estrutura de pastas, pois o arquivo principal importa o pacote `orca_ml` e lê os dados do ORCA-AI.

Para refazer somente o relatório, sem treinar de novo:

```bash
python gerar_relatorio_estudo.py --execucao outputs/entrega_ufg_acabamentos_2026-09-27 --saida outputs/relatorio_ufg_revisado
```

Para reproduzir a edição com os links do GitHub em uma pasta nova:

```bash
python gerar_entrega_professor.py --saida entregas/professor_ronaldo_revisao
```

Esse gerador confere o manifesto da execução publicada e os hashes dos resultados antes de associar os links às evidências. Os links podem ser abertos sem login no GitHub.

## Como apresentar a comparação

| Tarefa | Pergunta | Algoritmos | Medida de resultado |
| --- | --- | --- | --- |
| Regressão | Qual será o próximo custo referencial? | Regressão linear simples/múltipla; referência do último preço | Erro no teste temporal, comparado com a persistência |
| Classificação | A qual família pertence uma composição disponível? | Random Forest, árvore e KNN; referência da classe majoritária | F1 macro, acurácia balanceada e confusões em serviços reservados |
| Agrupamento | Quais serviços têm perfis semelhantes de recursos? | K-Means | Silhouette, tamanho e estabilidade dos grupos; interpretação dos perfis |

As métricas respondem a perguntas diferentes. Não existe uma nota única de “melhor modelo” entre essas três tarefas.

## Resultados centrais

- **Dados:** 514 serviços SINAPI-ES e 70 DER-ES/IOPES no catálogo de maio/2026, com custos das composições conciliados. O histórico da regressão conserva serviços elegíveis em cada mês, incluindo quatro códigos SINAPI ausentes no snapshot de maio.
- **Regressão:** nos três nichos e em ambas as bases, repetir o último custo teve MAPE menor que os modelos lineares escolhidos na validação. Essa é uma conclusão útil para definir a referência mínima do ORCA-AI.
- **Classificação:** a árvore de decisão foi escolhida pela validação nas duas fontes. F1 macro no teste: **0,7913 no SINAPI** (102 serviços) e **0,5623 no DER** (14 serviços). Random Forest teve F1 de teste maior, mas isso não foi usado para trocar a seleção.
- **Agrupamento:** SINAPI apresentou **três clusters elegíveis**, com silhouette **0,3879**. No DER, nenhum k de 2 a 5 cumpriu o mínimo de quatro serviços por cluster; o diagnóstico k=2 tem grupos de 67 e três serviços e permanece identificado como não aprovado.
- **Estabilidade:** a remoção de grupos inteiros de variantes produziu ARI mínimo de aproximadamente **0,514 no SINAPI** e **0,055 no diagnóstico DER**. Mostrar apenas os casos estáveis esconderia essa sensibilidade.

## Limites e continuidade

As classes vêm dos grupos oficiais e ainda precisam de homologação técnica. A regra de variantes reduz sobreposição entre treino e teste, mas não prova que todas as técnicas semelhantes ficaram isoladas. O teste DER é pequeno. As bases têm diferentes formas de detalhar encargos e recursos; seus serviços ainda não foram pareados como equivalentes técnicos.

O trabalho entrega experimentos acadêmicos reproduzíveis. A aplicação operacional poderá evoluir com revisão dos rótulos, mais composições independentes, avaliação prospectiva e definição de critérios de uso pelo engenheiro.
