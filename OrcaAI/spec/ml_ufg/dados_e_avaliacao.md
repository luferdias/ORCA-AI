# Dados e avaliação acadêmica

> **Escopo vigente:** a [proposta atual do trabalho](proposta_projeto_ml_es.md) define regressão, classificação de composições estruturadas e agrupamento, alinhados às aulas da disciplina. A classificação por texto descrita neste documento é uma alternativa anterior, reservada para evolução futura. Os critérios de preservação e rastreabilidade abaixo continuam aplicáveis.

Estado: especificação proposta. Amostras de tabelas oficiais foram inspecionadas; nenhum dataset de treinamento foi preparado e nenhum modelo foi treinado nesta etapa.

## 1. Acervo de origem

Os referenciais oficiais fornecem o catálogo de serviços e composições. Os projetos fornecem exemplos de demandas e escolhas feitas na rotina da SRA-ES. A [especificação das bases](bases_servicos_e_atualizacao.md) define fontes, edições, campos e atualização; a [auditoria de acesso](../../docs/auditoria_bases_referenciais_2026-09-27.md) registra o que foi efetivamente conferido.

Os 12 projetos permanecem em `OrcaAI/projetos/`, com os seguintes nomes:

1. `Item 01 - teto_elevadores`
2. `Item 02 - Limpeza_robotizada_AC`
3. `Item 03 - Lavagem_envidracada`
4. `Item 04 - Junta_dilatacao`
5. `Item 05 - Pintura_grade`
6. `Item 06 - insulfilm`
7. `Item 07 - Pintura_externa_MGIES`
8. `Item 08 - impermeabilizacao_cisterna`
9. `Item 09 - limpeza_FV`
10. `Item 10 - MNT_gerador_subestacao`
11. `Item 11 - Impermeabilizacao_Marquise`
12. `Item 12 - Reforma_Suporte_CAG`

O acervo de `Projetos Básicos` e `_governanca_sei_agu_cgu` também permanece no lugar. A leitura para pesquisa usará uma lista explícita de fontes. Extrações, normalizações e correções serão gravadas como artefatos derivados, vinculados aos originais por caminho e hash. Um manifesto registrará os arquivos selecionados, formato, tamanho, hash e projeto de origem.

Antes e depois de cada etapa de extração, os hashes dos originais selecionados serão comparados. Os documentos fonte ficam fora dos diretórios de saída. Conteúdo de configuração, credenciais e arquivos de ambiente não fazem parte do corpus documental.

O SA-ML-01 também revisará o conteúdo extraído dos documentos permitidos, inclusive campos pessoais e assinaturas sem utilidade para o experimento. Segredos e dados pessoais desnecessários serão removidos ou mascarados nas cópias derivadas antes da geração de datasets e embeddings. O manifesto identificará a versão dessa preparação e o responsável pela revisão.

## 2. Primeiro experimento recomendado

**Hipótese de trabalho:** classificar a família de serviço de um item a partir da descrição disponível no início da análise e da unidade, apoiando o encaminhamento aos especialistas do ORCA-AI.

Essa é uma proposta de recorte, sujeita ao enunciado da disciplina e à inspeção dos dados. A consulta a composições semelhantes pode acompanhar a demonstração; os códigos e preços usados no orçamento continuam sujeitos à verificação nas fontes do domínio.

Antes de treinar, verificar quantos exemplos revisados existem por classe e por projeto. Os 12 projetos não equivalem a 12 amostras independentes nem garantem um dataset suficiente. Classes presentes em apenas um projeto exigem outro recorte, mais dados ou declaração explícita de que sua generalização não pôde ser medida.

## 3. Registro mínimo de um exemplo

| Campo | Finalidade |
| --- | --- |
| `example_id`, `context_id`, `project_id` | Identificação estável e vínculo com o caso |
| `source_path`, `source_hash`, `source_locator` | Documento original e página, aba ou linha |
| `description_input`, `unit_input` | Informações disponíveis no momento da previsão |
| `label`, `label_status`, `reviewer`, `reviewed_at` | Rótulo, situação de revisão e autoria |
| `dataset_version`, `duplicate_group_id` | Versão e agrupamento de cópias/itens repetidos |
| `base_reference`, `reference_date` | Contexto da fonte, quando aplicável |
| `source_id`, `edition_id`, `uf`, `regime_encargos` | Identificação da edição oficial e das condições da referência |

Sugestões do modelo ficam em uma tabela de previsões. Aceite, correção ou rejeição humana ficam em eventos de revisão separados. Somente exemplos com rótulo revisado entram no conjunto supervisionado. Novas revisões criam outra versão do dataset.

## 4. Protocolo de avaliação

1. **Congelar a pergunta e os dados.** Registrar tarefa, campos de entrada, rótulos e casos incluídos.
2. **Separar por projeto e por duplicatas.** Um projeto não aparece simultaneamente no treino e na avaliação de uma mesma partição. Cópias presentes em projetos diferentes precisam ser removidas ou os projetos ligados por essas cópias devem compor o mesmo grupo de validação. Agrupar somente pelo ID de projeto não resolve duplicatas entre projetos. Descrições repetidas em diferentes meses, UFs ou bases também devem ser agrupadas ou removidas antes de avaliar a generalização do classificador.
3. **Verificar as classes em cada partição.** Se a divisão não suportar a tarefa, registrar a limitação e revisar o desenho antes de publicar métricas.
4. **Comparar modelos.** Referência inicial: classe mais frequente, identificada no treino de cada partição. Candidato simples: TF-IDF e regressão logística em um pipeline. Um candidato com embeddings pode ser comparado depois, mantendo as mesmas partições.
5. **Ajustar somente no treino.** Vocabulário, normalização, seleção de variáveis e hiperparâmetros não utilizam o teste final. A escolha de modelo usa validação interna; quando viável, reservar projetos para um teste final ou utilizar avaliação agrupada aninhada.
6. **Registrar resultados completos.** Para classificação: macro-F1, precisão/recall por classe, matriz de confusão, resultados por projeto e quantidade de exemplos. Não tratar a variação entre folds como intervalo de confiança automático.
7. **Avaliar a recuperação separadamente.** Usar consultas revisadas, fontes relevantes esperadas, Recall@5, MRR@5 e presença de referências corretas. O índice pode conter o catálogo oficial publicado até a data da consulta, inclusive a composição que se espera recuperar. Ficam fora do treinamento e do índice os rótulos, escolhas humanas e documentos dos projetos reservados que revelem a solução do caso de teste.
8. **Documentar limites.** Registrar erros, casos sem cobertura, custo de execução e diferença frente à referência. A conclusão pode ser melhoria, empate, piora ou evidência insuficiente.

Um experimento temporal adicional deve treinar com informação disponível até uma data de corte e avaliar demandas posteriores. Versões retificadas publicadas depois dessa data não podem ser usadas retroativamente no treino. Catálogos consultados no teste respeitam a disponibilidade na data de cada demanda.

`GroupKFold` mantém grupos fora dos dois lados da mesma partição; a adaptação proposta usa projetos como grupos. Pipelines ajudam a manter transformações aprendidas dentro do treino. Fontes: [GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) e [prevenção de vazamento de dados](https://scikit-learn.org/stable/common_pitfalls.html).

## 5. Pacote acadêmico de um experimento

- Manifesto do dataset, dicionário de campos e protocolo de rotulagem.
- Arquivo com a atribuição de cada exemplo às partições.
- Versão do código, dependências, parâmetros e sementes aleatórias.
- Previsões por exemplo, métricas calculadas e análise dos erros.
- Manifesto do modelo com contexto, tarefa, dataset e avaliação associados.
- Relatório com problema, método, resultados, limitações e instruções de reprodução.

O apoio `documentation-writer` produz o texto a partir desses artefatos. O SA-ML-05 confere se tabelas e conclusões correspondem aos resultados executados. Não há meta de acurácia ou ganho garantido definida nesta proposta.
