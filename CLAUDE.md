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

## Qualidade de código

- Lint e formatação com **ruff 0.17.3**, configurado em `pyproject.toml` na raiz (regras padrão E4, E7, E9, F; Python 3.12; largura 88). Versão pinada em `OrcaAI/ml/requirements-dev.txt` e instalada no `OrcaAI/ml/.venv`.
- Rodar `ruff check .` e `ruff format .` a partir da raiz antes de commitar. Em 29/10/2026 todo o repositório passou a estar limpo e formatado.
- Hook versionado em `.githooks/pre-commit` roda `ruff check` e `ruff format --check` nos arquivos Python preparados e bloqueia o commit em caso de erro. Ativado neste clone com `git config core.hooksPath .githooks`; em outro clone é preciso repetir o comando.
- `core.fileMode false` está ativo neste clone porque o OneDrive altera permissões dos arquivos. O OneDrive também não preserva links simbólicos: não criar symlinks no repositório.
- Documentação para o usuário: seção 5 do `README.md` da raiz e seção "Qualidade de código" de `OrcaAI/ml/README.md`.
- Em 29/10/2026 o venv do ml subiu para pandas 3.1.0, numpy 2.5.4, reportlab 5.1.0 e pytest 9.2.0. O estudo de acabamentos e a regressão dos 18 nichos foram reexecutados e reproduziram as métricas, seleções e previsões de 27/09/2026; as únicas diferenças são no último dígito de ponto flutuante. As pastas em `OrcaAI/ml/outputs` não foram regeneradas e continuam sendo a referência entregue.
