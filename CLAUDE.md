# Memória de trabalho do ORCA-AI

## Usuário e comunicação

- Nome: **Luis Fernando**, com **S**.
- Forma de tratamento solicitada: **engenheiro Luis Fernando**.
- Não usar “compadre”. A preferência explícita por S prevalece sobre grafias divergentes da transcrição.
- Responder em português, com linguagem clara e direta.
- Perfil: [memory/people/luis-fernando.md](memory/people/luis-fernando.md).

## Projeto acadêmico em andamento

- Aplicação de ML no ORCA-AI para a disciplina da UFG de aprendizado de máquina aplicado a dados estruturados.
- Fontes confirmadas: **SINAPI-ES** e **DER-ES/IOPES**; começar por SINAPI-ES, manter datasets e experimentos separados e comparar os resultados posteriormente.
- Escopo confirmado em 27/09/2026: **somente regressão, classificação e agrupamento**. Aprendizado por reforço fica para uma evolução futura.
- Entrega ao professor Ronaldo em 28/09/2026: PDF com links permanentes do GitHub em `OrcaAI/ml/entregas/professor_ronaldo_2026-09-28/relatorio.pdf`. O usuário autorizou explicitamente tornar `luferdias/ORCA-AI` público para leitura e download; visibilidade alterada e acesso anônimo verificado. Permissões de escrita permanecem restritas às contas autorizadas. A edição referencia o commit experimental `e20741b0214dff489147fa04739bb2a1ed44bc07` e preserva os resultados de 27/09/2026.
- Proposta alinhada às aulas: `LinearRegression`, `RandomForestClassifier` (comparadores árvore/KNN) e `KMeans`. Ver [proposta do projeto](OrcaAI/spec/ml_ufg/proposta_projeto_ml_es.md).
- Três tarefas implementadas em Python para VS Code: [executar_estudo.py](OrcaAI/ml/executar_estudo.py), [executar_classificacao.py](OrcaAI/ml/executar_classificacao.py), [executar_agrupamento.py](OrcaAI/ml/executar_agrupamento.py) e [instruções](OrcaAI/ml/README.md). A regressão original continua em [executar_regressao.py](OrcaAI/ml/executar_regressao.py).
- Estudo confirmado de pintura e acabamentos: pintura, revestimentos/forros e pisos, somente m², snapshot maio/2026, 514 serviços SINAPI e 70 DER; três classes derivadas dos grupos oficiais, sem alegar homologação humana. Modelos e escalas separados por fonte. Plano: [consolidação](OrcaAI/spec/ml_ufg/plano_consolidacao_acabamentos.md).
- Classificação seleciona por validação com grupos de variantes; na execução, a árvore venceu a validação nas duas fontes, ainda que RF tenha melhor F1 no teste. K-Means selecionou k=3 no SINAPI. No DER, nenhum k atendeu ao mínimo de quatro serviços por cluster: preservar diagnóstico k=2 identificado, sem tratá-lo como aprovado. A regressão nos três nichos não superou a persistência em MAPE.
- Apresentação didática da regressão: [relatório atual](OrcaAI/ml/APRESENTACAO_RESULTADOS.md), com HTML/PDF, 18 nichos e comparação em janela comum. O programa gera a apresentação automaticamente; `gerar_relatorio.py` refaz apenas os relatórios. Explicar ganhos e perdas frente à persistência, preservar extremos e identificar mudanças de serviço associadas ao mesmo código.
- Histórico coletado para regressão: SINAPI-ES 2025-01 a 2026-08 (20 competências); DER-ES 2025-01 a 2026-05 (17). Os datasets são separados; datas DER desconhecidas não são inferidas.
- Preservar os 12 projetos existentes e os arquivos originais. Trabalhar com dados derivados e versões identificadas.
- Materiais da disciplina: `/Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/`.
- ZIP SINAPI agosto/2026 obtido no site da CAIXA: `OrcaAI/bases/sinapi/2026-08/originais/`; conferir o manifesto antes de usar.
