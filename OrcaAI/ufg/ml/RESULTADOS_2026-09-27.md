# Primeira execução real da regressão — ORCA-AI

**Engenheiro Luis Fernando · UFG · 27/09/2026**

O módulo foi implementado em Python e executado com dados oficiais do SINAPI-ES e DER-ES/IOPES. Compara Regressão Linear simples, Regressão Linear múltipla e persistência, que mantém o último custo conhecido. O modelo linear de cada recorte é escolhido na validação.

## 1. Dados preparados

| Fonte | Competências | Registros de custo válidos | Códigos distintos | Regime |
| --- | --- | ---: | ---: | --- |
| SINAPI-ES | 2025-01 a 2026-08 — 20 meses | 161.393 | 8.647 | Sem desoneração |
| DER-ES/IOPES | 2025-01 a 2026-05 — 17 meses | 22.796 | 1.373 | Sem desoneração; BDI zero no relatório de serviços |

Os 37 ZIPs foram preservados com seus manifestos e conferidos por CRC/SHA-256. As planilhas foram lidas em memória. Os arquivos dos doze projetos existentes permanecem preservados.

O SINAPI contém 39.301 registros de custo zero excluídos e documentados. Entre os registros positivos, 57.303 têm alguma participação de preços atribuídos a São Paulo, conforme `%AS` da fonte. Esse indicador foi preservado no dataset. Datas de republicação do SINAPI foram registradas; as datas de publicação do DER permaneceram desconhecidas.

## 2. Avaliação até a última edição de cada fonte

Um recorte corresponde a **grupo oficial × unidade**. Cada recorte tem treino, validação, teste e modelos próprios. As entradas são os três últimos custos consecutivos disponíveis; a estabilidade é exigida somente nas entradas. Mudanças técnicas no mês previsto são identificadas após a previsão. Mudanças de unidade ficam fora da comparação monetária.

| Medida | SINAPI-ES | DER-ES/IOPES |
| --- | --- | --- |
| Validação | Abril e maio/2026 | Janeiro e fevereiro/2026 |
| Teste | Junho a agosto/2026 | Março a maio/2026 |
| Recortes avaliados | 227 | 129 |
| Recortes sem amostra suficiente | 53 | 60 |
| Exemplos de teste do modelo selecionado | 22.547 | 3.642 |
| Modelo selecionado com MSE menor que a persistência | 125 recortes | 61 recortes |
| Persistência com MSE menor que o modelo selecionado | 102 recortes | 68 recortes |

Essas são contagens de recortes, sem ponderação pelo número de exemplos. Não representam acurácia nem indicam superioridade de uma fonte. No SINAPI, seis dos recortes favoráveis à persistência tiveram erro zero dessa referência; o ganho percentual ficou indefinido e foi mantido vazio.

**Conclusão inicial:** a regressão ajuda em parte dos recortes. A referência de persistência permanece necessária, pois foi superior em outros. Os dados não sustentam uma promessa geral de redução de erro.

Exemplo para leitura das métricas: em **Acessibilidade / M2 no SINAPI**, a regressão simples foi selecionada na validação. Nos nove exemplos de teste, MAE foi aproximadamente **R$ 1,69/m²**, RMSE **R$ 2,09/m²** e a redução de MSE frente à persistência foi **36,68%**. Esse pequeno recorte ilustra a saída do programa; não resume todo o catálogo.

- [Relatório da execução completa](outputs/regressao_validada_2026-09-27/RESULTADOS.md).
- [Métricas SINAPI](outputs/regressao_validada_2026-09-27/sinapi_es/metricas.csv) e [métricas DER](outputs/regressao_validada_2026-09-27/der_es/metricas.csv).

## 3. Verificação com o mesmo período de teste

Também foi executado `--fim 2026-05`, a partir de outra pasta do terminal, para verificar a independência do diretório de trabalho e reproduzir as duas fontes até a mesma competência. Ambas usaram janeiro/fevereiro na validação e março/abril/maio de 2026 no teste.

| Fonte | Recortes avaliados | Regressão superou persistência | Persistência superou regressão |
| --- | ---: | ---: | ---: |
| SINAPI-ES | 219 | 84 | 135 |
| DER-ES/IOPES | 129 | 61 | 68 |

A mudança de resultado no SINAPI mostra a importância da janela temporal. Os grupos das fontes ainda não foram harmonizados nem os serviços pareados tecnicamente; esta comparação iguala o período, mas não constitui uma comparação direta entre serviços equivalentes.

[Relatório da janela comum](outputs/janela_comum_2026-05/RESULTADOS.md).

## 4. Cenários da próxima competência

Após congelar a avaliação, os modelos escolhidos foram reajustados com o histórico elegível completo. Foram gerados cenários para:

- **SINAPI-ES:** 6.881 serviços, competência-alvo **setembro/2026**.
- **DER-ES/IOPES:** 1.079 serviços, competência-alvo **junho/2026**, seguinte à última edição coletada dessa fonte.

Cada serviço tem previsão linear e persistência. Esses cenários ainda não têm alvo observado nesta coleta. A competência-alvo do DER não deve ser interpretada como previsão do próximo mês do calendário atual.

[Cenários SINAPI](outputs/regressao_validada_2026-09-27/sinapi_es/previsoes_proxima_competencia.csv) · [Cenários DER](outputs/regressao_validada_2026-09-27/der_es/previsoes_proxima_competencia.csv).

## 5. Validação e limites

- **66 testes passaram**, incluindo verificações adicionais em subtestes, cobrindo leitores, manifestos, códigos, datas, partições, métricas e os arquivos de execução.
- A execução completa foi repetida no ambiente `.venv` isolado, com Python 3.12.14 e dependências fixadas. As métricas e previsões foram reproduzidas; `pip check` não encontrou conflitos.
- A seleção dos modelos não usa os resultados de teste nem rótulos de validação publicados depois da primeira origem do teste.
- A assinatura SINAPI considera a hierarquia analítica. A assinatura DER compara descrição e unidade e não verifica a estabilidade dos coeficientes da composição.
- A coleta usa versões revisadas hoje disponíveis. O controle das datas conhecidas reduz o uso indevido de informação futura; a falta de datas no DER limita as conclusões à avaliação retrospectiva.
- Cada teste usa três competências; muitos serviços da mesma edição compartilham variações. A quantidade de linhas não equivale à quantidade de meses independentes.
- MAE/RMSE estão em R$/unidade; MSE em (R$/unidade)². Os erros não foram agregados entre unidades incompatíveis.
- Os alvos são custos referenciais publicados. Custos reais de execução e preços de propostas não foram modelados.

## 6. Executar novamente

Abra [ORCA-ML.code-workspace](ORCA-ML.code-workspace), selecione o Python da pasta `.venv` e execute [executar_regressao.py](executar_regressao.py). As [instruções completas](README.md) explicam instalação, opções, reconstrução dos datasets e leitura dos resultados.
