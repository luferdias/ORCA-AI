# Três tarefas de ML em pintura e acabamentos

Data: 27/09/2026. Responsável: engenheiro Luis Fernando. Execução solicitada pelo usuário; recorte confirmado nesta conversa.

## Objetivo e escopo

Entregar código Python executável no VS Code, datasets rastreáveis, experimentos de classificação e agrupamento e relatório acadêmico consolidado com a regressão já implementada. Preservar os originais e os 12 orçamentos.

O estudo principal abrange pintura, revestimentos e forros, e pisos, em **m²**, nas bases SINAPI-ES e DER-ES/IOPES, sem desoneração. Modelos separados por fonte. Snapshot das composições: **maio/2026**, última competência comum coletada. Catálogo esperado antes das conferências: 514 serviços SINAPI e 70 DER.

As classes são derivadas do mapa dos grupos oficiais já existente. Não representam rótulos homologados por revisão humana. Equivalência temática não comprova substituição técnica de serviços entre bases.

## Desenho fixado antes do treinamento

### Atributos e rastreabilidade

Expandir composições até recursos-folha, com detecção de ciclos e conciliação hierárquica dos custos. Registrar arquivos, hashes, células, categorias, coeficientes, preços efetivos e exclusões. No SINAPI, registrar quando o preço efetivo procede de SP por ausência de preço ES e conferir o indicador oficial de origem do preço.

Entradas comuns: frações calculadas de custo de mão de obra/encargos, materiais, equipamentos e outros; número de recursos distintos de cada categoria; horas de mão de obra e equipamentos por m². As frações usam a soma dos custos das folhas antes dos truncamentos, com diferença para o custo oficial explicitada. As horas de mão de obra não somam novamente os itens de encargos complementares.

Código, descrição, grupo oficial, classe e custo total não entram no treinamento da classificação nem do agrupamento. Código e descrição servem apenas à rastreabilidade, à apresentação e à divisão de variantes.

### Classificação supervisionada

- Random Forest como candidato principal; árvore e KNN como comparadores; classe majoritária como referência.
- Um exemplo por serviço no snapshot. Agrupar variantes conservadoramente pela união do conjunto de recursos-folha e da descrição normalizada sem medidas/demãos. Um grupo pode atravessar classes e deve continuar indivisível.
- Teste no primeiro bloco de `StratifiedGroupKFold(5, shuffle=True, random_state=42)`; validar cobertura antes dos ajustes. Validação interna de três blocos por grupos, semente 43. Caso insuficiente, informar a limitação sem quebrar grupos.
- Busca pequena predefinida: RF com 200 árvores e folha mínima 1/2/4; árvore com profundidade 3/5/ilimitada e folha mínima 2; KNN com 3/5/7 vizinhos e pesos por distância.
- Escalonamento aprendido somente no treino de cada bloco. Escolha por F1 macro de validação; teste final não orienta ajustes.
- Exportar F1 macro, acurácia balanceada, métricas por classe, matriz de confusão, previsões e partições auditáveis.

### Agrupamento não supervisionado

- Mesmo catálogo e atributos numéricos da classificação, sem fornecer classes ao ajuste.
- K-Means, padronização por fonte, k de 2 a 5, 30 inicializações, semente 42.
- Escolha por silhouette, exigindo ao menos três serviços e 5% da amostra em cada cluster. Preservar métricas de todos os candidatos.
- Complementos: inércia, Davies-Bouldin, Calinski-Harabasz, estabilidade entre sementes, 20 subamostras de 80% dos serviços e 20 subamostras de 80% dos grupos de variantes. Estas últimas mantêm as variantes juntas.
- Centroides em unidades originais, exemplos próximos dos centroides e PCA apenas para visualização, com variância explicada.
- Os clusters são perfis exploratórios. Não são classes oficiais ou equivalências técnicas. Métricas sob escalas ajustadas por fonte não formam um ranking das bases.

**Tratamento de resultado negativo, registrado após a execução inicial:** o DER produziu um perfil raro de três serviços com equipamento; todos os k de 2 a 5 ficaram abaixo do mínimo de quatro serviços por cluster. O limite não foi reduzido. A execução registra `sem_candidato_valido`, mantém `k_selecionado` vazio e fornece apenas um diagnóstico com o menor k calculável (k=2 neste caso), identificado nos arquivos e no texto. Esse resultado científico não interrompe a regressão nem a consolidação. O modelo diagnóstico é salvo separadamente de um modelo aprovado. A primeira execução permanece preservada.

### Regressão e comparação

Executar o protocolo temporal existente nos mesmos três nichos e unidade, com histórico até maio/2026 e teste março-maio/2026. A seleção histórica depende dos atributos da própria competência; não restringir silenciosamente o passado aos códigos sobreviventes em maio. Informar interseção e diferenças de serviços entre tarefas.

Regressão responde ao próximo custo; classificação à família de uma composição; agrupamento aos perfis semelhantes. Não combinar MAPE, F1 e silhouette em uma nota única. Conservar resultados desfavoráveis e referências simples.

## Componentes e execução

1. `sinapi_composicoes.py` e `der_composicoes.py`: leitores analíticos independentes, recursos-folha e auditorias.
2. `atributos_acabamentos.py`: recorte, atributos comuns e grupos conservadores de variantes.
3. `classificacao.py` e `agrupamento.py`: experimentos, partições, modelos e resultados.
4. `executar_estudo.py`: preparação e execução reproduzível das três tarefas, sem sobrescrever execuções anteriores.
5. `relatorio_consolidado.py` e gráficos: relatório acadêmico HTML/PDF/Markdown, com método, resultados, discussão, limitações e reprodução.

## Verificações de aceitação

- Testes antes da implementação para custos, expansão, categorias, duplicatas, grupos, partições e isolamento do teste.
- Conferir os recursos e os totais em exemplos reais de cada fonte.
- Validar que alterações no rótulo não mudam o K-Means e que campos de identificação não entram em X.
- Executar as três tarefas nos dados oficiais e conferir métricas a partir dos CSVs.
- Renderizar o PDF e inspecionar legibilidade, legendas, números e tabelas.
- Conferir sincronização no repositório principal e preservação dos 12 projetos.

## Referências metodológicas

- [Divisão estratificada por grupos](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html).
- [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).
- [K-Means e avaliação de agrupamentos](https://scikit-learn.org/stable/modules/clustering.html).
- [Métricas de avaliação](https://scikit-learn.org/stable/modules/model_evaluation.html).
- [Mapa dos materiais da disciplina](mapa_materiais_disciplina.md).
