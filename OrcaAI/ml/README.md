# Aprendizado de máquina em custos referenciais — ORCA-AI / UFG

## Estudo consolidado: pintura e acabamentos

**Comece pelo [guia da entrega UFG](ENTREGA_UFG.md), com relatório de 16 páginas, resultados e instruções para o VS Code.**

O novo estudo reúne **regressão, classificação supervisionada e agrupamento não supervisionado**, usando pintura, revestimentos e forros, e pisos em m². SINAPI-ES e DER-ES/IOPES são processados separadamente. As composições analíticas usam maio/2026; a regressão usa o histórico até essa competência, com teste em março-maio/2026.

No VS Code, abra `ORCA-ML.code-workspace`, selecione o interpretador `.venv/bin/python` e execute um destes arquivos:

| Arquivo | Resultado |
| --- | --- |
| [executar_classificacao.py](executar_classificacao.py) | Random Forest, árvore, KNN e referência majoritária; métricas e partições |
| [executar_agrupamento.py](executar_agrupamento.py) | K-Means, perfis, representantes e estabilidade |
| [executar_estudo.py](executar_estudo.py) | As três tarefas e o relatório acadêmico HTML/PDF |

```bash
# No terminal, dentro da pasta ml e com o ambiente ativado:
python -m pip install -r requirements.txt
python executar_estudo.py

# Somente uma tarefa ou fonte:
python executar_classificacao.py --base sinapi_es
python executar_agrupamento.py --base der_es
```

Os scripts usam os ZIPs e datasets locais já preparados; não precisam de download. Cada execução cria uma pasta nova em `outputs/`. O terminal mostra os caminhos. O relatório consolidado é produzido pelo estudo completo; os dois scripts individuais geram os arquivos técnicos da tarefa.

As classes são derivadas dos grupos oficiais e ainda não foram homologadas por revisão humana. Códigos, descrições e nomes de grupos não são entradas dos modelos. Variantes são mantidas no mesmo bloco de classificação por uma regra conservadora de recursos e descrição. O melhor classificador é escolhido pela validação, nunca pelo teste final.

O K-Means pode retornar `sem_candidato_valido`: isso significa que nenhum k respeitou o tamanho mínimo de grupo definido antes do teste. Nesse caso, o programa preserva os resultados, gera um diagnóstico identificado e conclui as demais tarefas. Esse diagnóstico não é promovido a agrupamento aprovado.

Consulte o [plano e os critérios do estudo](../spec/ml_ufg/plano_consolidacao_acabamentos.md). Registre as populações de cada tarefa: um serviço no snapshot da classificação não equivale a uma observação serviço/mês da regressão. MAPE, F1 e silhouette respondem a perguntas diferentes e não devem ser somados ou transformados em uma classificação única dos algoritmos.

## Regressão original

Aplicação em Python para o engenheiro Luis Fernando. Primeiro experimento da disciplina: **Regressão Linear simples e múltipla**, com SINAPI-ES e DER-ES/IOPES separados.

**Comece pela [apresentação didática atual](APRESENTACAO_RESULTADOS.md): relatório navegável, PDF de 28 páginas e gráficos por 18 nichos da obra.**

[Resultados verificados da primeira execução, em 27/09/2026](RESULTADOS_2026-09-27.md).

## Executar no VS Code

1. Abra [ORCA-ML.code-workspace](ORCA-ML.code-workspace) no VS Code.
2. Selecione o interpretador de `ml/.venv` em **Python: Select Interpreter**. O ambiente local foi preparado com Python 3.12.
3. Abra [executar_regressao.py](executar_regressao.py) e clique em **Run Python File / Executar Arquivo Python**.

O programa lê os dois datasets já preparados, avalia os modelos e salva uma nova pasta em `outputs/`. **Agora também gera uma apresentação didática em HTML e PDF**, com gráficos por grupo de serviços, legendas, valores e explicações estatísticas. Ao terminar, o terminal mostra os caminhos dos relatórios. A execução padrão é local, sem download ou acesso aos portais.

Abra o **HTML** para consultar os gráficos e as tabelas no navegador; use o **PDF** para leitura e apresentação. O relatório mostra tanto as melhorias da regressão quanto os grupos em que repetir o último custo apresentou menor erro. As cores e as legendas identificam SINAPI, DER e a referência de comparação.

O arquivo principal importa o pacote `orca_ml/`, que está nesta mesma pasta. Mantenha essa estrutura ao copiar a aplicação para outro computador. Classificação e agrupamento estão disponíveis nos scripts apresentados no início deste documento.

### Instalação em outro ambiente

No terminal integrado, dentro desta pasta, usando Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python executar_regressao.py
```

No Windows, a ativação correspondente é `.venv\Scripts\Activate.ps1`. Se o ambiente ainda não estiver disponível, o arquivo principal informa como instalar as dependências. As versões verificadas estão em [requirements.txt](requirements.txt).

### Opções

```bash
# Uma base por vez
python executar_regressao.py --base sinapi_es
python executar_regressao.py --base der_es

# Repetir as duas fontes até uma competência comum
python executar_regressao.py --fim 2026-05

# Escolher uma pasta nova de resultados
python executar_regressao.py --saida outputs/minha_execucao

# Avaliar modelos sem gerar o relatório didático
python executar_regressao.py --sem-relatorio

# Refazer somente a apresentação de uma execução salva
python gerar_relatorio.py --execucao outputs/minha_execucao

# Escolher uma pasta nova para a apresentação
python gerar_relatorio.py --execucao outputs/minha_execucao --saida outputs/apresentacao_revisada

# Reconstruir os datasets a partir dos ZIPs locais, sem internet
python preparar_dados.py
```

Os caminhos dos dados são resolvidos a partir do próprio arquivo Python. A execução funciona mesmo quando o terminal está em outra pasta. A saída informada por `--saida` não pode conter resultados anteriores.

## Como a comparação fica justa e legível

A execução padrão mantém a última competência disponível de **cada base** para a avaliação individual e o cenário seguinte. Quando as janelas de validação ou teste diferem, o programa faz uma segunda avaliação em `comparacao_mesma_janela/`, limitada à última competência comum. O relatório comparativo usa essa segunda avaliação. Com os arquivos atuais:

- **Validação comum:** janeiro e fevereiro de 2026.
- **Teste comum:** março, abril e maio de 2026.
- **Avaliação individual SINAPI:** mantém o histórico até agosto de 2026.
- **Avaliação individual DER:** mantém o histórico até maio de 2026.

Se `--fim 2026-05` já produz as mesmas fases, a avaliação é aproveitada diretamente, sem repetir o treinamento. Com `--base sinapi_es` ou `--base der_es`, o relatório apresenta somente a fonte escolhida.

Os **grupos temáticos** organizam a apresentação por nichos, como fundações, estruturas, alvenaria, cobertura, pintura e instalações. Essa organização é didática: pertencer ao mesmo nicho **não comprova equivalência técnica** entre serviços das duas tabelas. Os grupos oficiais e as unidades permanecem identificados e os modelos continuam separados por base, grupo oficial e unidade.

O resumo por nicho usa erros percentuais por observação, para permitir a leitura de diferentes unidades sem somar erros monetários incompatíveis. Cada observação representa um serviço em um mês; portanto, um serviço observado em três meses participa três vezes. Valores em reais aparecem em recortes que preservam grupo e unidade. O tamanho da amostra e o período precisam acompanhar a interpretação.

O script [gerar_relatorio.py](gerar_relatorio.py) recria somente a apresentação, sem treinar novamente. Ele usa automaticamente `comparacao_mesma_janela/` quando ela existe, verifica o SHA-256 do dataset original e respeita o corte da execução salva. A saída padrão recebe um identificador novo; `--saida` também exige uma pasta nova. Se o dataset mudou, é necessário restaurar a versão correspondente ou executar uma nova avaliação. Em caso de erro no relatório, as métricas já calculadas são preservadas e o programa termina com código de erro.

## Dados utilizados

| Base | Histórico coletado | Fonte local |
| --- | --- | --- |
| SINAPI-ES | Janeiro/2025 a agosto/2026 — 20 competências | [Dataset SINAPI](../knowledge/datasets/ml_ufg/sinapi_es/custos_historicos.csv) |
| DER-ES/IOPES | Janeiro/2025 a maio/2026 — 17 competências | [Dataset DER](../knowledge/datasets/ml_ufg/der_es/custos_historicos.csv) |

Regime: **sem desoneração**. Os ZIPs oficiais permanecem em `../bases/sinapi/` e `../bases/der_es/`, com competência, URL, hash e manifesto. Os CSVs são derivados desses arquivos; os doze projetos existentes não são usados como se fossem doze amostras de treinamento.

- **SINAPI:** custos da UF ES na aba `CSD`; código recuperado da fórmula quando necessário e conferido na composição analítica. O indicador `percentual_as` registra a participação atribuída a preços de São Paulo. Zeros e custos ausentes não se tornam exemplos de custo válido.
- **DER:** relatório sintético de serviços, com conferência de competência, regime e BDI zero. Códigos são preservados como texto, inclusive zeros iniciais.
- **Estabilidade:** SINAPI usa a estrutura analítica para identificar alterações; DER controla descrição e unidade. A assinatura DER é parcial e não prova estabilidade dos coeficientes e insumos.
- **Publicação:** SINAPI registra a data exibida para a versão disponível, incluindo retificações. DER deixa a publicação desconhecida quando o portal informa apenas atualização. As datas não foram inferidas a partir do mês de referência.

O [catálogo SINAPI](fontes_sinapi.json) identifica URLs e retificações. As origens são o [portal SINAPI/CAIXA](https://www.caixa.gov.br/site/Paginas/downloads.aspx#categoria_888) e o [referencial DER-ES Edificações](https://der.es.gov.br/referencial-de-precos-edificacoes).

## O que o modelo aprende

Uma linha representa um serviço em uma competência. O modelo simples recebe `custo_t`; o múltiplo recebe `custo_t`, `custo_t_1` e `custo_t_2`. Ambos estimam `custo_alvo`, correspondente a `t+1`.

As quatro competências precisam ser consecutivas e ter custos positivos para a avaliação. As entradas t-2, t-1 e t devem ter identificação técnica estável segundo os campos disponíveis. Alterações técnicas em t+1 ficam identificadas, sem selecionar previamente apenas os serviços que se provaram estáveis no futuro. Mudanças de unidade no alvo são registradas e excluídas da comparação monetária. Cada modelo é ajustado dentro de um recorte de **grupo oficial e unidade**, e cada fonte mantém seus próprios modelos.

### Treino, validação e teste

1. Reservar as três últimas competências como teste.
2. Usar as duas competências anteriores para validação e seleção entre regressão simples e múltipla.
3. Treinar com as competências anteriores à validação.
4. Após a seleção, reajustar com o período anterior ao teste e manter os coeficientes fixos durante a avaliação.
5. Comparar ambos os modelos e a **persistência**, que repete o último custo conhecido, nas mesmas linhas.
6. Depois de congelar as métricas, reajustar o modelo escolhido com o histórico elegível completo para gerar o cenário da próxima competência.

Quando há datas conhecidas, excluir previsões cujo alvo já estava publicado quando suas entradas ficaram disponíveis e impedir que o treino use alvos publicados depois da primeira origem da fase. A escolha do modelo também exclui rótulos de validação publicados depois da primeira origem do teste. A falta de datas no DER limita o estudo a uma avaliação retrospectiva do histórico revisado.

A configuração está em [configs/regressao.json](configs/regressao.json). Grupos pequenos são registrados como insuficientes; o programa não fabrica observações para completá-los. Isso pode produzir o estado `parcial` no resumo mesmo quando a execução terminou normalmente.

## Arquivos de resultados

Cada execução gera `outputs/<identificador>/`, com `RESULTADOS.md`, `execucao.json` e uma pasta por base. A apresentação HTML/PDF, os gráficos explicativos e as tabelas derivadas ficam na pasta do relatório didático. Quando há uma avaliação adicional para comparação, ela fica em `comparacao_mesma_janela/`, com seu próprio registro de execução e resultados.

Os arquivos técnicos de cada base continuam disponíveis:

| Arquivo | Como usar |
| --- | --- |
| `dataset_modelavel.csv` | Conferir as entradas históricas e o alvo de cada exemplo |
| `particoes.csv` | Auditar treino, validação, teste e exclusões por publicação |
| `previsoes_avaliacao.csv` | Comparar custo observado, previsto, persistência e erro |
| `metricas.csv` / `.json` | Ler MSE, MAE, RMSE e R² por modelo, fase, família e unidade |
| `previsoes_proxima_competencia.csv` | Consultar o cenário do modelo reajustado e a persistência |
| `resumo.json` | Conferir cobertura, competências, parâmetros, versões e hashes |
| `observado_previsto.png` / `erros.png` | Visualizar um recorte identificado no título; os CSVs contêm os demais |
| `modelos/*.joblib` | Modelos ajustados para o cenário da próxima competência |

`ganho_mse_percentual` compara o erro com a persistência. Um valor negativo significa que repetir o último custo foi melhor. Se a persistência tiver erro zero, o ganho percentual fica vazio; não há divisão por zero. R² também fica vazio quando o alvo é constante.

MAE e RMSE estão em **R$/unidade do recorte**; MSE está em **(R$/unidade)²**. R² é adimensional. A coluna `n_alteracoes_tecnicas_alvo` mostra quantos casos avaliados tiveram mudança técnica observável no mês previsto.

A coluna `modelo_selecionado` identifica a escolha feita na **validação**. Consultar o teste não muda essa escolha. A previsão de uma próxima competência ainda não tem valor observado nem erro medido.

## Limites da interpretação

- Os resultados estimam **custos referenciais publicados**. O custo efetivo de uma obra exigiria dados adicionais.
- O mês previsto é o seguinte ao último dado de cada fonte. Com DER até maio/2026, o cenário é junho/2026, mesmo que a execução ocorra em setembro.
- Retificações e datas incompletas impedem apresentar esta coleta como reconstrução integral do que era conhecido em cada momento histórico.
- A avaliação de estabilidade usa os atributos disponíveis; não assegura que um serviço ainda não publicado manterá a mesma composição.
- As bases possuem grupos próprios e diferentes coberturas. `--fim` iguala o limite temporal, mas uma comparação direta de serviços ainda exige equivalência técnica revisada. Não somar erros de R$/m², R$/m e R$/un numa média única.

## Verificação

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Os testes verificam leitura de códigos, coluna ES, regime e competência, integridade dos arquivos, revisões duplicadas, consecutividade das janelas, mudanças técnicas, partições cronológicas e referência de persistência. A integração do relatório verifica também a janela comum, a preservação da última competência por fonte, a execução individual, a regeneração sem treinamento e a conservação das métricas quando a apresentação falha. Os dados artificiais dos testes ficam em diretórios temporários; as execuções entregues usam os arquivos oficiais coletados.

## Relação com a disciplina

[Proposta aprovada para implementação](../spec/ml_ufg/proposta_projeto_ml_es.md) · [Mapa das aulas](../spec/ml_ufg/mapa_materiais_disciplina.md) · [Registro de implementação](IMPLEMENTACAO.md).
