# Agentes e subagentes — extensão ML/UFG

Estado: fichas de responsabilidades propostas, sem registro automático em um runtime.

## Papéis existentes que serão aproveitados

| Papel | Contribuição para o trabalho acadêmico |
| --- | --- |
| A1 — OrcaMasterOrchestrator | Define escopo, delega tarefas, consolida decisões e apresenta resultados ao usuário |
| A2 — EngenheiroCustosSenior | Explica escopos, serviços, unidades e significado dos rótulos |
| A3 — OrcafascioPilot | Fornece contexto das escolhas no Orçafascio; a captura estruturada de feedback será uma funcionalidade futura |
| A4 — PesquisadorMercado | Esclarece a origem e a comparabilidade de cotações |
| A5 — MineradorBasesOficiais | Identifica fontes, códigos, localidades e datas-base |
| A6 — CompositorCustosUnitarios | Revisa relações entre serviços, composições e insumos |
| A7 — EspecialistaEspecificacao | Ajuda a normalizar descrições e terminologia técnica |
| A8 — EngenheiroPlanejamentoEConomico | Revisa variáveis de orçamento e cronograma pertinentes à tarefa |
| A9 — AuditorConformidade | Revisa rastreabilidade e uso das recomendações; recebe avaliação experimental especializada |
| A10 — EspecialistaInstrucaoProcessualSEI | Contextualiza documentos processuais e seus vínculos com a contratação |
| Agente 5S | Verifica integridade do acervo, caminhos, inventário e separação de artefatos derivados |
| project-planner / explorer-agent / documentation-writer | Reutilizados para planejamento, inspeção e redação acadêmica |

As skills locais de códigos SINAPI/IOPES, engenharia, BDI, Orçafascio, documentos técnicos e guardrails continuam associadas aos especialistas correspondentes. A modelagem não modifica fórmulas ou substitui verificações técnicas de orçamento.

## A11 — PesquisadorMLUFG

**Missão:** conduzir a aplicação acadêmica de ML dentro do ORCA-AI, com experimentos rastreáveis e resultados interpretáveis.

- **Reporta a:** A1.
- **Entradas:** pergunta de pesquisa, critérios da disciplina quando disponíveis, inventário de fontes, decisões do usuário e restrições de recursos.
- **Decisões:** propor tarefa, rótulos, modelos comparáveis, organização dos experimentos e prioridades de curadoria.
- **Delegações:** SA-ML-01 a SA-ML-04, conforme a tarefa.
- **Saídas:** plano do experimento, registro das versões, resumo das métricas, limitações e pacote de demonstração.
- **Apoio:** `plan-writing` e `documentation-templates` locais; `ml-pipeline-workflow` selecionada para adoção futura.
- **Critério de conclusão:** cada resultado tem dataset, código, configuração, previsões e avaliação associados. O parecer independente chega por A9/SA-ML-05.
- **Limites:** alterações ao acervo original, promoção de um modelo e escolhas técnicas de orçamento permanecem sob os responsáveis do domínio e o usuário.

## Subagentes propostos

### SA-ML-01 — Curadoria de dados

**Reporta a:** A11. **Skill selecionada:** `analyze-data-quality`.

Recebe uma lista explícita de fontes dos projetos e produz inventário, extrações, dicionário de campos, candidatos a rótulos e relatório de qualidade. Mantém a ligação com arquivo, página/aba/linha e projeto de origem. Identifica duplicatas, unidades incompatíveis, versões conflitantes e campos disponíveis somente depois da decisão que o modelo tentará prever.

Entrega um dataset versionado com a situação de revisão de cada exemplo. Os especialistas de domínio e o usuário validam os rótulos. Divergências são registradas para revisão, sem sobrescrever os documentos originais.

### SA-ML-02 — Conhecimento e busca documental

**Reporta a:** A11. **Skill selecionada:** `embedding-strategies`. Usa a integração Qdrant fornecida pelo SA-ML-04.

Recebe documentos derivados e identificados; propõe divisão em trechos, modelo de embeddings adequado ao português técnico e metadados de recuperação. Entrega manifesto do índice, consultas de referência e resultados citando as fontes. Registra versão e dimensão do modelo de embeddings.

As consultas respeitam contexto, projeto e partição experimental. A qualidade da busca é avaliada pelo SA-ML-05 sobre consultas revisadas. Sem fonte suficiente, devolve resultado insuficiente, evitando preencher lacunas com códigos ou preços presumidos.

### SA-ML-03 — Treinamento de modelos

**Reporta a:** A11. **Skills selecionadas:** `scikit-learn` e `ml-pipeline-workflow`.

Recebe dataset e partições congelados. Compara uma referência simples com modelos apropriados à tarefa; ajusta pré-processamento somente nos dados de treino. Entrega configurações, versões, modelos candidatos e previsões por exemplo e partição.

Não usa rótulos do teste para ajustar escolhas. Resultados fracos e execuções com falha também entram no registro experimental. O modelo permanece candidato até a revisão dos resultados.

### SA-ML-04 — Integração e API Knowledge

**Reporta a:** A11. **Skill selecionada:** `qdrant-clients-sdk`.

Recebe os contratos da API, manifestos do índice e modelos avaliados. Na implementação, fará a conexão com Qdrant, a consulta a contextos, a leitura do registro de modelos e a gravação de insights. Entrega testes de contrato e rastreamento entre resposta, fonte e versão.

O nome `latest` aponta para uma versão publicada no registro, identificada por contexto e tarefa. O envio de um insight cria uma proposta pendente de revisão. A revisão humana é um evento separado da previsão do modelo.

### SA-ML-05 — Avaliação experimental

**Reporta a:** A9; envia parecer ao A1. **Skill selecionada:** `scikit-learn`, com as métricas definidas na spec de avaliação.

Recebe previsões, partições, configurações e critérios previamente definidos. Verifica isolamento entre projetos, duplicatas, cobertura dos rótulos, comparação com baseline e correspondência entre resultados e relatório.

Entrega métricas por classe/projeto, erros representativos, limitações e parecer: reproduzível, inconclusivo ou inválido. Não altera o conjunto de teste para favorecer um modelo. A9 mantém a revisão técnica de orçamento; o usuário valida o uso dos resultados.

## Contrato de uma delegação

Cada tarefa informa: `task_id`, pergunta, `context_id`, fontes permitidas, versões de dados, artefatos de entrada, diretório de saída e critério de conclusão. A resposta informa: estado, artefatos produzidos, evidências, decisões tomadas, limitações e próximo responsável.

Scripts de extração, cálculo, treino e avaliação serão ferramentas executadas por esses papéis. A ficha de um subagente não implica que um novo modelo ou serviço permanente tenha sido criado.
