# Registro de implementação da regressão

Plano: `../spec/ml_ufg/proposta_projeto_ml_es.md`. Autorização: pedido do engenheiro Luis Fernando em 27/09/2026 para baixar as duas bases, criar datasets e executar regressão em Python/VS Code.

## Etapas

- [x] Coletar histórico oficial SINAPI-ES e DER-ES/IOPES, com manifestos e hashes.
- [x] Implementar e testar leitores de custos sem desoneração.
- [x] Implementar e testar partições temporais, modelos lineares e persistência.
- [x] Preparar datasets reais separados e executar os experimentos.
- [x] Entregar arquivo de execução, ambiente VS Code, resultados e instruções verificadas.
- [x] Revisar código, metodologia, dados e preservação do acervo.

## Decisões de implementação

- SINAPI: janeiro/2025 a agosto/2026, 20 versões atualmente disponibilizadas pela CAIXA. Retificações e datas de publicação ficam registradas; dados revisados não serão apresentados como reconstrução integral do conhecimento histórico.
- DER: assinatura inicial de descrição e unidade é um controle parcial de mudanças observáveis; não comprova invariabilidade de todos os recursos da CPU. O relatório deve explicitar esse limite.
- Regressão temporal de uma competência: validar antes dos três meses finais de teste, comparar regressão simples e múltipla com persistência. Ajustar cenário futuro somente depois de congelar a avaliação.
- Execução padrão local, com datasets preparados. Coleta e reconstrução dos datasets são operações explícitas, para que apertar Executar no VS Code não dependa da disponibilidade dos portais.
- Alterações ficam no módulo de ML e nos dados derivados; os doze projetos e módulos existentes são preservados.
- A revisão identificou seleção da amostra por estabilidade técnica futura. Correção: exigir estabilidade apenas nas entradas t-2..t, identificar mudanças em t+1 e mantê-las na avaliação; excluir mudanças de unidade somente da comparação monetária, com registro nas partições. Dois testes falharam e passaram com a correção.
- A seleção do algoritmo também obedece à publicação: rótulos de validação posteriores à primeira origem de teste ficam fora da escolha. Um teste específico falhou e passou com a correção.
- MSE tem unidade (R$/unidade do serviço)²; MAE e RMSE têm unidade R$/unidade do serviço. Não agregar moedas de unidades incompatíveis.

## Evidências de execução

- SINAPI: 20 ZIPs, 302.191.678 bytes, todos com CRC e hash verificados; dataset com 161.393 registros positivos e 8.647 códigos. Foram excluídos e documentados 39.301 registros de custo zero.
- DER: 17 ZIPs, 127.948.550 bytes, todos com CRC e hash verificados; dataset com 22.796 registros e 1.373 códigos.
- Execução real final: `outputs/regressao_validada_2026-09-27/`, com 227 recortes SINAPI e 129 recortes DER avaliados. Recortes insuficientes ficam identificados.
- Reconstrução DER executada de `/tmp`, confirmando independência da pasta atual do terminal.
- Revisão de integridade SINAPI concluída: a reconstrução exige concordância entre arquivo e manifestos (nome, competência, tamanho, SHA-256 e publicação). Testes detectaram a aceitação indevida de ZIP substituído antes da correção; 20 ZIPs e 21 manifestos reais conferidos após a correção. Os dados e resultados anteriores não mudaram.
- Suíte final: 66 testes passaram, incluindo verificações adicionais em subtestes, no ambiente `.venv` isolado com Python 3.12.14. `pip check` não encontrou conflitos de dependências. A execução completa reproduziu as métricas e previsões da primeira rodada.
- Execução adicional com `--fim 2026-05`, iniciada de `/tmp`: 219 recortes SINAPI e 129 DER, teste março–maio/2026. Dados de serviços ainda não harmonizados para comparação direta.

## Interfaces compartilhadas

- Leitores → modelos: CSV com `fonte, competencia, codigo, descricao, unidade, grupo, custo, regime, publicado_em, arquivo_sha256, localizador, assinatura_tecnica`; colunas adicionais identificam a força da assinatura e indicadores da fonte.
- Modelos → execução: `executar_experimento(df, output_dir, config=None)` devolve resumo e grava métricas, previsões, gráficos e modelos por fonte.
- Modelos → relatório: a seleção depende apenas da validação; o relatório informa fonte, recortes, competências, exclusões, erros e limites da publicação.

## Apresentação didática por grupos — 27/09/2026

- `executar_regressao.py` gera automaticamente HTML/PDF e uma segunda avaliação em janela comum quando as fontes têm últimas competências diferentes. `gerar_relatorio.py` permite regenerar a apresentação sem treinar novamente.
- A taxonomia organiza 282 grupos em 18 nichos e mantém nomes originais, unidades e observações dos grupos mistos. Até maio/2026 há 281 grupos; o grupo posterior fica identificado na cobertura.
- Estatísticas percentuais são recalculadas das previsões pareadas. Métricas monetárias continuam por grupo original e unidade. O MSE da validação segue escolhendo o modelo.
- Exemplos de pintura escolhidos por cobertura e preço mediano anteriores ao teste, sem seleção por erro favorável. Extremos e resultados desfavoráveis continuam visíveis.
- Auditoria direta das planilhas oficiais confirmou custos de poucos centavos no SINAPI e reutilização de códigos para outros serviços auxiliares no DER em maio. O relatório explica o efeito sobre o MAPE.
- Execução completa: `outputs/apresentacao_2026-09-27/`. Apresentação revisada: `outputs/relatorio_final_2026-09-27/`, com 28 páginas PDF, HTML autônomo, gráficos PNG/SVG, métricas e diagnóstico em CSV.
- Verificação: 138 testes e 9 subtestes aprovados; revisão visual das páginas, conferência de cobertura, valores e links; busca do HTML e abertura da tabela por teclado verificadas no navegador.

## Consolidação das três tarefas — 27/09/2026

- Recorte confirmado pelo engenheiro Luis Fernando: pintura e acabamentos. Estudo restrito a pintura, revestimentos/forros e pisos em m², com fontes separadas e catálogo de maio/2026.
- Leitores de composições analíticas conciliam exatamente os 514 serviços SINAPI e 70 DER selecionados; recursos são expandidos até as folhas, mantendo origem, localizador, encargos e substituições de preço SP documentados.
- Classificação compara Random Forest, árvore e KNN com referência majoritária. Seleção por F1 macro na validação, escalonamento dentro dos folds e grupos de variantes separados. Árvore selecionada em ambas as fontes; F1 macro de teste 0,7913 e 0,5623, respectivamente.
- K-Means compara k=2..5, com mínimo de 5% do catálogo e três serviços por grupo. SINAPI: k=3 elegível. DER: nenhum candidato elegível; k=2 fica somente como diagnóstico, sem alterar o critério de aceitação. Reamostragem adicional por grupos inteiros revela instabilidade que a reamostragem por linhas não mostrou.
- Regressão reexecutada nos mesmos nichos, preservando a população histórica elegível em cada mês. Teste março-maio/2026. A persistência teve menor MAPE em todos os seis pares fonte/nicho.
- Execução completa final: `outputs/entrega_ufg_acabamentos_2026-09-27/`. Relatório de 16 páginas em PDF, HTML autônomo, Markdown, gráficos PNG/SVG e resultados CSV/JSON, com modelos salvos e hashes verificáveis.
- Scripts para VS Code: `executar_classificacao.py`, `executar_agrupamento.py` e `executar_estudo.py`; regeneração independente por `gerar_relatorio_estudo.py`.
- Verificação final: 221 testes e nove subtestes aprovados; execução real das três tarefas concluída nas duas bases. O relatório distingue amostras, métricas, limitações e diagnóstico não aprovado.
