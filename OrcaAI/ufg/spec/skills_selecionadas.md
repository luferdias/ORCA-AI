# Cinco skills selecionadas para o ORCA-AI + ML

Pesquisa no skills.sh e nos repositórios de origem em 27/09/2026. Estado: seleção para adoção futura. Nenhuma skill externa foi instalada ou executada nesta etapa.

O critério foi acrescentar capacidades às 24 skills locais de `.agent/skills/`: qualidade dos dados, modelagem, experimentos reproduzíveis, embeddings e integração com Qdrant. Skills são instruções reutilizáveis para agentes; bibliotecas, serviços e modelos precisam ser implementados ou configurados separadamente.

## Seleção principal

| Skill | Origem | Aplicação proposta | Responsável |
| --- | --- | --- | --- |
| [analyze-data-quality](https://www.skills.sh/openai/plugins/analyze-data-quality) | `openai/plugins` | Verificar se os dados dos orçamentos são utilizáveis no experimento | SA-ML-01 |
| [scikit-learn](https://www.skills.sh/k-dense-ai/scientific-agent-skills/scikit-learn) | `K-Dense-AI/scientific-agent-skills` | Preparar modelos e avaliar previsões | SA-ML-03 e SA-ML-05 |
| [ml-pipeline-workflow](https://www.skills.sh/wshobson/agents/ml-pipeline-workflow) | `wshobson/agents` | Organizar dados, treino, avaliação e versões | A11 e SA-ML-03 |
| [embedding-strategies](https://www.skills.sh/wshobson/agents/embedding-strategies) | `wshobson/agents` | Selecionar embeddings e a divisão dos documentos em trechos | SA-ML-02 |
| [qdrant-clients-sdk](https://www.skills.sh/qdrant/skills/qdrant-clients-sdk) | `qdrant/skills` | Integrar a API Knowledge ao banco vetorial escolhido | SA-ML-04 |

## Conteúdo verificado e adaptação ao projeto

### 1. analyze-data-quality

A fonte orienta definir a unidade de análise, identificar chaves, examinar nulos e duplicatas, conferir consistência e investigar vazamento de informação. Sua aplicação será um relatório de qualidade por projeto, com as linhas que exigem revisão.

Cita notebooks e conectores que podem não estar disponíveis no ambiente. A adoção deve usar os arquivos locais e ferramentas já acessíveis. Complementa as verificações de códigos e de orçamento existentes.

[SKILL.md original](https://github.com/openai/plugins/blob/main/plugins/data-analytics/skills/analyze-data-quality/SKILL.md).

### 2. scikit-learn

O conteúdo cobre pré-processamento, estimadores, pipelines e avaliação. Sua referência de avaliação inclui separação por grupos. No ORCA-AI, o identificador de projeto será considerado na divisão experimental para reduzir a contaminação entre treino e avaliação.

A versão consultada declara Python 3.11+ e scikit-learn 1.7+. Essas dependências precisam ser confrontadas com o ambiente antes da adoção. O frontmatter informa BSD-3-Clause e a licença geral do repositório informa MIT; a condição aplicável deve ser esclarecida antes de copiar ou redistribuir a skill.

[SKILL.md original](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scikit-learn/SKILL.md), [referência de avaliação](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scikit-learn/references/model_evaluation.md) e [licença do repositório](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/LICENSE.md).

### 3. ml-pipeline-workflow

A fonte organiza o ciclo de dados, preparação, treino, validação e operação, com registro de versões e métricas. A aplicação inicial será um fluxo local reproduzível, com manifesto do dataset e registro dos experimentos.

As opções de infraestrutura mencionadas pela skill, como orquestradores de tarefas e serviços de rastreamento, serão avaliadas conforme a necessidade. Um primeiro experimento pode usar scripts e registros locais.

[SKILL.md original](https://github.com/wshobson/agents/blob/main/plugins/machine-learning-ops/skills/ml-pipeline-workflow/SKILL.md).

### 4. embedding-strategies

Orienta escolha de modelos, divisão em trechos, tratamento multilíngue, cache e metadados. A aplicação será comparar a recuperação de descrições técnicas em português, preservando referências de página, aba ou item.

Os exemplos incluem serviços externos e modelos locais com diferentes custos de execução. A escolha dependerá de teste no corpus e dos recursos disponíveis. O mesmo espaço vetorial deve ser usado na indexação e nas consultas.

[SKILL.md original](https://github.com/wshobson/agents/blob/main/plugins/llm-application-dev/skills/embedding-strategies/SKILL.md).

### 5. qdrant-clients-sdk

É mantida pela organização Qdrant e reúne referências dos clientes, REST/gRPC e exemplos de integração. Será usada na construção do adaptador da API Knowledge.

É um guia de integração; o serviço API, os contratos e os testes continuam sendo entregas do projeto. O exemplo Python inclui o extra `fastembed`, cuja necessidade depende de onde os embeddings serão calculados.

[SKILL.md original](https://github.com/qdrant/skills/blob/main/skills/qdrant-clients-sdk/SKILL.md).

## Ordem sugerida de adoção

1. Qualidade de dados: conhecer o material disponível e definir a tarefa.
2. Pipeline e scikit-learn: construir uma referência de desempenho reproduzível.
3. Embeddings e cliente Qdrant: adicionar consulta documental e integração.

Na adoção, registrar a revisão de origem e as adaptações locais de cada skill, conferir suas dependências e demonstrar seu uso numa tarefa pequena. Preservar referências e licenças aplicáveis. A instalação deve ser restrita às skills escolhidas, evitando importar coleções completas que dupliquem os agentes e fluxos existentes.

## Candidatas para uma segunda etapa

- [qdrant-hybrid-search](https://www.skills.sh/qdrant/skills/qdrant-hybrid-search): pode combinar recuperação semântica e termos exatos, útil quando códigos e siglas aparecerem nos testes. [Fonte original](https://github.com/qdrant/skills/blob/main/skills/qdrant-search-quality/search-strategies/hybrid-search/SKILL.md).
- [rag-implementation](https://www.skills.sh/wshobson/agents/rag-implementation): referência mais ampla para recuperação e geração. Os exemplos consultados usam outra combinação de serviços; exigiriam adaptação ao Qdrant. [Fonte original](https://github.com/wshobson/agents/blob/main/plugins/llm-application-dev/skills/rag-implementation/SKILL.md).

Essas duas opções são reservas; a seleção inicial contém exatamente cinco skills.
