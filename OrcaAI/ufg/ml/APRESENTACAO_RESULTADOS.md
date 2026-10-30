# Resultados da regressão, explicados por etapa da obra

**Engenheiro Luis Fernando · ORCA-AI / UFG · 27/09/2026**

- [Abrir o relatório navegável](outputs/relatorio_final_2026-09-27/relatorio.html).
- [Abrir o PDF de 28 páginas](outputs/relatorio_final_2026-09-27/relatorio.pdf).
- [Ler o relatório em Markdown](outputs/relatorio_final_2026-09-27/RELATORIO.md).
- [Executar novamente o programa Python](executar_regressao.py).

## O que mudou

A execução agora produz gráficos com valores, legendas, fontes, períodos e tamanhos de amostra, além de explicações em linguagem direta. O relatório organiza os serviços em **18 nichos**: fundações, estruturas, alvenaria, coberturas, pintura, instalações e demais etapas. A comparação principal usa **março a maio/2026** nas duas fontes. As avaliações até a última competência de cada base também são preservadas.

O catálogo contém **282 grupos originais**. Destes, **281 possuem registros até maio/2026**. “Sistemas de Medição de Gás”, do SINAPI, surge em julho/agosto e fica identificado como fora do período comparado. As tabelas também mostram os grupos sem amostra suficiente; ausência de resultado não é erro zero.

## Exemplos para a apresentação

| Tema | Resultado do teste | Interpretação |
|---|---|---|
| Coberturas / SINAPI | MAPE de 1,33% na persistência e 1,18% na regressão; 450 previsões de 150 serviços | Redução relativa de 11,05% no erro médio percentual deste nicho |
| Pintura / SINAPI | 99,25% das 402 previsões com erro até 5%; MAPE de 1,35% | Aproximação com erros pequenos; a persistência foi melhor, com MAPE de 0,40% |
| Pintura / DER-ES | 81,48% das 81 previsões com erro até 5%; MAPE de 2,74% | A persistência foi melhor no período, com MAPE de 2,51% |

O limite de 5% é didático. Estes valores não representam tolerância oficial, economia financeira ou garantia para uma próxima obra. Os nichos aproximam assuntos; composições SINAPI e DER ainda não foram pareadas tecnicamente.

## Por que explicar média e mediana

O DER apresenta MAPE global de 122,44%, mas mediana de 1,67%. Os maiores erros incluem códigos auxiliares que passaram a identificar outros serviços em maio, com custos de poucos centavos. Os valores foram conferidos nos ZIPs oficiais. Isso é uma quebra de identidade técnica e não deve ser descrito como queda de preço do mesmo serviço. As observações foram mantidas e documentadas no [diagnóstico dos extremos](outputs/relatorio_final_2026-09-27/diagnostico_extremos.csv).

No SINAPI, custos auxiliares muito baixos também ampliam o erro percentual. O relatório apresenta mediana, P90, faixas de erro e evolução mensal para complementar a média. Nenhuma faixa foi apresentada como intervalo de confiança.

## Reprodução e verificação

O comando padrão continua sendo `python executar_regressao.py`. Quando as competências disponíveis diferem, ele executa uma segunda avaliação até o último mês comum para produzir a apresentação. `--sem-relatorio` mantém apenas os resultados técnicos.

Para refazer somente a apresentação a partir da execução salva, em uma pasta nova:

```bash
python gerar_relatorio.py --execucao outputs/apresentacao_2026-09-27 --saida outputs/minha_apresentacao
```

A suíte passou com **138 testes e 9 subtestes**. Foram conferidos o pareamento entre previsões e persistência, as janelas reais dos CSVs, a seleção do exemplo sem usar erros futuros, a cobertura dos grupos, os links e a renderização do PDF. A validação nominal previa janeiro/fevereiro; o SINAPI usou somente janeiro, porque as versões retificadas de janeiro e fevereiro foram publicadas no mesmo dia e o alvo fevereiro já era conhecido.

As métricas monetárias permanecem separadas por grupo original e unidade. O arquivo [previsoes_pareadas.csv](outputs/relatorio_final_2026-09-27/previsoes_pareadas.csv) permite conferir todos os cálculos.
