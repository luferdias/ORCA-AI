# Mapa dos materiais da disciplina e seleção de modelos

Data: 27/09/2026. Destinatário: engenheiro Luis Fernando.

Este mapa fundamenta a proposta acadêmica do ORCA-AI em Python, executada no VS Code. O escopo decidido compreende **regressão, classificação e agrupamento**. SINAPI-ES e DER/IOPES-ES serão preparados e avaliados separadamente antes de qualquer comparação entre bases. Não houve treinamento nesta etapa.

## 1. Materiais consultados

A equipe leu os sete PDFs abaixo e inspecionou os dois ZIPs. As páginas citadas são as posições no PDF, começando em 1. A leitura dos materiais não implica executar seus comandos nem adotar todos os algoritmos apresentados.

| Material local | Extensão | Papel na proposta |
| --- | --- | --- |
| [Aula 1a — Apresentação](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-1a_-_Apresentacao.pdf>) | 30 páginas | Contexto e organização da disciplina |
| [Aula 1b — Revisão](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-1b_-_Revisao.pdf>) | 36 páginas | Fundamentos e revisão |
| [Aula 1c — Regressão](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-1c_-_Regressao.pdf>) | 85 páginas | Regressão, transformação de atributos e avaliação |
| [Aula 2 — Treinamento supervisionado](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-2_-_Supervisionados_-_Treinamento.pdf>) | 70 páginas | Treino, validação, teste, pipelines e métricas |
| [Aula 3 — Algoritmos supervisionados](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-3_-_Supervisionados_-_Algoritmos.pdf>) | 83 páginas | Classificadores e análise de atributos |
| [Aula 4.1 — Não supervisionados](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-4.1_-_Nao_Supervisionados.pdf>) | 43 páginas | KMeans e redução de dimensionalidade; inclui também LDA supervisionado |
| [Aula 4.2 — Aprendizado por reforço](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-4.2_-_Aprendizado_por_reforco.pdf>) | 39 páginas | Referência para evolução futura, fora da entrega atual |
| [Scripts Python](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/T2-python_scripts.zip>) | ZIP inspecionado | Exemplos de algoritmos, pré-processamento, avaliação e gráficos |
| [Projeto Python/Django](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/T2-python_django.zip>) | ZIP inspecionado | Exemplo de aplicação web; Django não é requisito para os experimentos |

A planilha [am-aula-1_-_MSE.xlsx](</Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/am-aula-1_-_MSE.xlsx>) foi **somente inventariada**. Suas células e fórmulas não foram validadas e não fundamentam conclusões deste mapa.

## 2. Seleção final para a proposta

| Tarefa | Modelo selecionado | Comparações e limites |
| --- | --- | --- |
| Regressão | `LinearRegression`, nas formas simples e múltipla | Comparar uma entrada com várias entradas pertinentes ao mesmo alvo. Regressão polinomial foi estudada, mas permanece extensão opcional. |
| Classificação | `RandomForestClassifier` | Comparar com `DecisionTreeClassifier` e `KNeighborsClassifier`, todos ensinados. O melhor modelo dependerá da validação. |
| Agrupamento | `KMeans` | Escolher o número de grupos pela avaliação quantitativa e interpretação técnica. PCA pode apoiar exploração/visualização. |

As referências mínimas de desempenho serão o último custo conhecido para a regressão temporal, a mediana do treino na alternativa de regressão contemporânea e a classe mais frequente para classificação. Elas permitem verificar se o aprendizado acrescenta informação.

**Q-learning fica fora do escopo atual.** Não haverá ambiente de reforço, política de ações ou treinamento por recompensas nesta entrega.

## 3. Regressão: evidências e exemplos

| Localizador | Conteúdo confirmado | Uso proposto |
| --- | --- | --- |
| Aula 1c, p. 28–31 | Regressão linear com scikit-learn | Modelo simples e interpretação da relação entre entrada e alvo |
| Aula 1c, p. 56–57 | Regressão polinomial | Comparação opcional; não confundir transformação polinomial com regressão múltipla |
| Aula 1c, p. 58–63 | Regressão múltipla | Modelo com várias características |
| Aula 1c, p. 68–78 | Pré-processamento e pipeline | Preparação reproduzível dos atributos |
| ZIP de scripts: `python_scripts/regressao_05.py` a `regressao_07.py` | Exemplos com `LinearRegression` e MSE | Referência de implementação e avaliação |
| ZIP de scripts: `python_scripts/regressao_08.py` | `PolynomialFeatures`, `Pipeline`, `StandardScaler`, `LinearRegression`, MSE e R² | Referência da extensão polinomial |
| ZIP de scripts: `python_scripts/regressao_09.py` | `LinearRegression`, MSE e R² | Referência do experimento com várias entradas |

A definição do alvo e das entradas precisa respeitar o momento da previsão. Não apresentar a recomposição exata de um preço, a partir de todos os seus componentes já conhecidos, como evidência de previsão de um valor desconhecido. Qualquer teste temporal será desenhado para usar somente informação disponível na data de corte.

## 4. Classificação: evidências e exemplos

| Localizador | Conteúdo confirmado | Decisão |
| --- | --- | --- |
| Aula 3, p. 2–6; `python_scripts/supervisionado_01.py` | KNN, vizinhos e escalonamento | Comparador |
| Aula 3, p. 7–30; `supervisionado_02A.py` e `supervisionado_02B.py` | Árvore de decisão; Gini, entropia e log loss na p. 21 | Comparador com complexidade controlada |
| Aula 3, p. 31–35; `python_scripts/supervisionado_03.py` | Random Forest e diversidade das árvores | Candidato principal |
| Aula 3, p. 36–54; `python_scripts/supervisionado_04.py` | SVM e kernels | Estudado, não necessário ao conjunto inicial |
| Aula 3, p. 55–66; `python_scripts/supervisionado_05.py` | Ensemble, boosting e XGBoost | Estudado, não necessário ao conjunto inicial |
| Aula 3, p. 68–75; `python_scripts/supervisionado_06.py` | LDA | Estudado; alternativa supervisionada |
| Aula 3, p. 76–82; `python_scripts/supervisionado_07.py` | Avaliação de atributos, incluindo permutation importance | Apoio à interpretação na validação |

QDA aparece apenas como menção na Aula 3, p. 67. Não foi desenvolvido como os modelos da tabela. A função logística usada na explicação de XGBoost não equivale a uma aula do classificador `LogisticRegression`; ele não integra a seleção final.

O recorte tabular pode usar unidade do serviço, contagens de recursos e coeficientes compatíveis da composição para prever uma família técnica revisada. Código, prefixo do código, grupo oficial e posição na tabela ficam fora das entradas quando revelam a classe. Esses dados de composição só podem entrar se estiverem disponíveis no momento da previsão.

## 5. Agrupamento e recursos complementares

| Localizador | Conteúdo confirmado | Decisão |
| --- | --- | --- |
| Aula 4.1, p. 5–7 e 11–21; `python_scripts/Nsupervisionado_01.py` | KMeans; script inclui padronização, silhouette, Davies–Bouldin e Calinski–Harabasz | Modelo de agrupamento selecionado |
| Aula 4.1, p. 23–33; `python_scripts/Nsupervisionado_02.py` | PCA | Apoio à exploração/visualização; não substitui o agrupamento |
| Aula 4.1, p. 34–42; `python_scripts/Nsupervisionado_03.py` | LDA com informação de classes | Método supervisionado; não usar como prova de agrupamento não supervisionado |
| Aula 4.2, p. 33–36; `python_scripts/reforco_01.py` | Q-learning | Somente referência futura |

Os grupos do KMeans serão examinados pelo perfil dos recursos e pelos serviços representativos. A classe oficial não entra no ajuste dos grupos; pode ajudar na interpretação posterior. Rótulos de cluster não representam automaticamente famílias técnicas nem equivalência de serviços.

## 6. Treinamento e métricas: aula e adaptação ao ORCA-AI

| Evidência nas aulas | Aplicação na proposta |
| --- | --- |
| Aula 2, p. 12–18: treino, validação, teste e validação cruzada | Separar escolha do modelo e avaliação final |
| Aula 2, p. 22–24: exemplo com teste de 15%, estratificação e semente 42 | Referência didática; adaptar a separação às classes e grupos realmente disponíveis |
| Aula 2, p. 25/27: `GridSearchCV`, `cv=10`, `scoring="accuracy"`, ajuste em `X_train` | Busca dentro do treino; número de partições condicionado aos dados |
| Aula 2, p. 29–36: matriz de confusão | Inspecionar confusões entre famílias técnicas |
| Aula 2, p. 37–53: precisão e recall; p. 62–68: F1 e médias | Selecionar classificação por F1 macro e apresentar resultados por classe |
| Aula 3, p. 76–78: permutation importance | Investigar quais entradas sustentam as previsões na validação |

**Adaptações da equipe, além dos exemplos didáticos:** na classificação, manter duplicatas e composições tecnicamente equivalentes no mesmo grupo de partição; controlar versões mensais e datas de publicação; avaliar previsão temporal com cortes cronológicos; harmonizar classes e unidades antes de comparar SINAPI-ES e DER/IOPES-ES. Partições aleatórias de linhas podem misturar o mesmo serviço dos dois lados. Na regressão temporal de serviços conhecidos, o mesmo serviço pode aparecer no passado e no futuro, respeitando o corte de informação.

Transformações aprendidas e seleção de atributos usam somente o treino de cada partição. Resultados das duas bases terão seu tamanho, cobertura e distribuição informados; diferenças nas métricas não demonstram, isoladamente, superioridade de uma base.

## 7. Condições para a implementação

- Confirmar os campos disponíveis nos arquivos SINAPI-ES e DER/IOPES-ES; os esquemas não serão considerados equivalentes por antecipação.
- Fixar alvos, atributos, unidades de observação e critérios de exclusão antes de treinar.
- Preservar originais, versões das fontes e os 12 projetos; gerar dados preparados e resultados em arquivos derivados.
- Registrar versões de Python/bibliotecas, sementes, partições, parâmetros e métricas.
- Usar os scripts das aulas como referência; adaptar caminhos locais e regras metodológicas antes da execução.
- Manter os experimentos em Python no VS Code. Django, LLM, embeddings e Qdrant não são requisitos para demonstrar os três modelos selecionados.
