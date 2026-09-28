# Regressão de custos referenciais — resultado da execução

SINAPI-ES e DER-ES/IOPES são avaliados separadamente. Cada recorte preserva sua família e unidade; não há uma média monetária que misture unidades.

## der_es

- Histórico: 2025-01 a 2026-05; 22,796 registros e 1,373 códigos.
- Recortes avaliados: 129; sem amostra suficiente: 60.
- Validação: 2026-01, 2026-02.
- Teste: 2026-03, 2026-04, 2026-05.
- Modo: `retrospectivo_historico_revisado`.
- Janelas excluídas por publicação: 0.
- [Métricas por família/unidade](der_es/metricas.csv), [previsões avaliadas](der_es/previsoes_avaliacao.csv) e [cenário da próxima competência](der_es/previsoes_proxima_competencia.csv).

- Limite: Backtest retrospectivo com as revisões fornecidas; não comprova uma previsão emitida no passado.
- Limite: Publicação ausente/inválida em parte do histórico: disponibilidade real no passado não comprovada; datas não foram inferidas.
- Limite: Assinatura técnica parcial ou não documentada: estabilidade da composição analítica não comprovada.

## Leitura dos resultados

Compare o modelo selecionado na validação com a persistência nas mesmas linhas do teste. Ganho negativo significa que repetir o último custo foi melhor. Uma previsão futura é um cenário de custo referencial; ainda não tem erro observado. A origem temporal é a competência indicada no CSV, que pode ser anterior ao mês atual do calendário.

Os grupos nativos das duas fontes ainda não constituem uma taxonomia harmonizada. A comparação direta de serviços requer equivalência técnica revisada, mesma competência, regime e unidade. O parâmetro `--fim` permite repetir o estudo numa janela comum; ele não comprova essa equivalência por si só.
