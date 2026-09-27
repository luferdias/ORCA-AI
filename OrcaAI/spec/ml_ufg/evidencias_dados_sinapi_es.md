# Evidências do SINAPI-ES — referência agosto/2026

Data da inspeção: 27/09/2026. Nota para o engenheiro Luis Fernando e para o desenho das três tarefas acadêmicas de ML: regressão, classificação e agrupamento.

## Método e alcance

O arquivo [SINAPI-2026-08-formato-xlsx.zip](../../bases/sinapi/2026-08/originais/SINAPI-2026-08-formato-xlsx.zip) foi aberto **somente para leitura** com `zipfile` e `openpyxl` (`read_only=True`) sobre bytes em memória. Nenhuma planilha foi extraída, salva ou modificada. As quatro pastas de trabalho e as abas abaixo foram inspecionadas por cabeçalhos e poucas linhas. As dimensões informadas pelo Excel incluem cabeçalhos, linhas auxiliares e possivelmente fórmulas: **não são contagens de exemplos válidos**. Não houve extração integral, validação de parser, conferência de todas as composições nem cálculo de métricas.

O nome do ZIP, as quatro planilhas e os cabeçalhos lidos indicam mês de referência **08/2026** e data de emissão **11/09/2026**. A emissão registrada no arquivo não substitui a verificação da data em que a CAIXA o disponibilizou no portal. O manifesto da cópia original guarda a identificação do arquivo; esta nota não o altera.

## Arquivos e abas observados

| Pasta de trabalho no ZIP | Abas e dimensão declarada (`max_row × max_column`) | Evidência localizada |
| --- | --- | --- |
| `SINAPI_familias_e_coeficientes_2026_08.xlsx` | `Coeficientes` (4.882 × 32) | `Coeficientes!A2` diz “RELATÓRIO DE FAMÍLIAS E COEFICIENTES”. `A6:M8` mostra **Código da Família, Código do Insumo, Descrição do Insumo, Unidade, Categoria** e coeficientes por UF; ES está em `M6`. As linhas 7–8 apresentam insumos representativo e representado da família 1. |
| `SINAPI_Manutenções_2026_08.xlsx` | `Manutenções` (32.599 × 5) | `Manutenções!A2` diz “RELATÓRIO DE MANUTENÇÕES DE INSUMOS E COMPOSIÇÕES”. `A6:E9` traz referência, tipo, código, descrição e manutenção; há eventos de alteração de insumo e de composição. |
| `SINAPI_mao_de_obra_2026_08.xlsx` | `SEM Desoneração` e `COM Desoneração` (cada uma 8.410 × 31) | Em ambas, `A6:L7` identifica grupo, código da composição, descrição, unidade e percentuais por UF; **ES é a coluna L**. Para a composição 104658, `SEM Desoneração!L7 = 0,3282` e `COM Desoneração!L7 = 0,318`. Esses valores são percentuais publicados, não coeficientes físicos de mão de obra. |
| `SINAPI_Referência_2026_08.xlsx` | `Menu` (22 × 5), `Busca` (12 × 3), `ISD`, `ICD`, `ISE` (cada 4.886 × 32), `CSD`, `CCD`, `CSE` (cada 10.557 × 58), `Analítico` (66.838 × 8), `Analítico com Custo` (201 × 9) | As abas `I*` são relatórios de preços de **insumos**; as `C*`, de custos de **composições**. Os sufixos `SD`, `CD` e `SE` distinguem regimes descritos nos próprios cabeçalhos. A aba `Analítico` contém a ligação composição–item e coeficientes, detalhada abaixo. |

## Composições, preços e Espírito Santo

**A composição analítica existe neste ZIP.** Em `SINAPI_Referência_2026_08.xlsx`, `Analítico!A10:H10` apresenta: `Grupo`, `Código da Composição`, `Tipo Item`, `Código do Item`, `Descrição`, `Unidade`, `Coeficiente`, `Situação`. `Analítico!A11:H15` exemplifica a composição **104658**, “PISO PODOTÁTIL DE ALERTA OU DIRECIONAL, DE CONCRETO, ASSENTADO SOBRE ARGAMASSA”, unidade `M2`, situação `COM CUSTO` na linha principal. As linhas seguintes relacionam `COMPOSICAO` 88316 (servente, coeficiente 1,279), `COMPOSICAO` 88309 (pedreiro, 0,639), `INSUMO` 36178 (piso tátil, 6,4375) e `INSUMO` 34357 (rejunte, 0,24). Há **subcomposições e insumos diretos**. Para obter atributos por recurso, expandir a hierarquia multiplicando os coeficientes. Na reconciliação de custos, usar o custo da subcomposição ou os recursos que a constituem, evitando incluir ambos; os insumos diretos são somados normalmente com seus próprios coeficientes.

O arquivo de **famílias e coeficientes** trata de representatividade **entre insumos**. Seus códigos de família e coeficientes não são a estrutura serviço → item da aba `Analítico`. Confundir os dois produziria atributos técnicos incorretos para as três tarefas.

Nas abas `CSD`, `CCD` e `CSE`, `S9:T10` identifica **ES**, `Custo (R$)` e `%AS` (porcentagem atribuída a preços de São Paulo). A amostra `CSD!A11:T11` informa custo ES de **R$ 188,15** para a composição 104658, sem desoneração. `CSD!B6:B9` explica que `%AS` mede a parcela calculada com preços de insumos de SP por indisponibilidade na UF e que hífen no custo indica ao menos um item sem preço/custo. Assim, custo presente, custo ausente e grau de atribuição a SP precisam de campos separados. Nas abas de insumos, `ISD!A10:M13` confirma descrição, código, unidade, origem do preço e preço de ES na coluna **M**.

**Armadilha de leitura:** `CSD!B11`, `CCD!B11` e `CSE!B11` são fórmulas `HYPERLINK` cujo texto contém o código 104658 e aponta para `Analítico`. Com `data_only=True`, o valor em cache observado nessas células foi `0`; o mesmo ocorreu nas linhas 12, 100 e 1.000 amostradas. Esse zero **não é código de composição**. O código deve ser recuperado de forma validada, preferencialmente da aba `Analítico` ou do relatório de mão de obra, preservando a relação correta com custo e descrição. Não foi verificado se todas as linhas da coluna B têm a mesma fórmula.

`Analítico com Custo!A7:I11` é uma consulta/calculadora com seleção visível de regime, UF e código; `A8:C8` vinha preenchido com `SEM DESONERAÇÃO`, **SP** e `95995`. O cabeçalho informa dependência de funções modernas do Excel. Essa aba não foi tratada como tabela analítica pronta para ES; o conteúdo em cache de sua saída não comprova cálculo para Vitória.

## Implicações para as três tarefas

- **Regressão de custo:** a aba analítica oferece estrutura e coeficientes, e `CSD/CCD/CSE` oferecem custos referenciais por UF e regime. Para prever custo contemporâneo, usar o preço atual dos próprios itens ou participações calculadas desses preços como entrada revelaria o alvo por construção. Preferir características técnicas disponíveis antes de conhecer o custo; na alternativa temporal, usar apenas custos e edições já publicados antes da data de previsão. Avaliar por unidade e família comparáveis, tratando `%AS`, custos ausentes e retificações.
- **Classificação de família técnica:** a aba `Analítico` permite contagens e presença de tipos/categorias de recursos e coeficientes por composição. `Grupo` pode orientar rótulos revisados, mas fica fora das entradas, assim como código, prefixo e posição da composição no relatório. A presença de um grupo oficial não prova que o mesmo rótulo seja adequado a outra base.
- **Agrupamento de perfis:** combinar itens da aba `Analítico` com percentual de mão de obra e, depois de validar a hierarquia e os custos, calcular participações de materiais, equipamentos e outras categorias. Não interpretar coeficientes físicos de unidades diferentes como valores diretamente comparáveis. Perfis dependem da edição, regime e tratamento de custos ausentes; grupos não provam equivalência técnica ou irregularidade.

## Esquema e verificações recomendados antes de modelar

Propor tabelas derivadas separadas para **edição** (fonte, competência, publicação, emissão, regime, UF e hash), **composição** (código, descrição, unidade, grupo e situação), **item da composição** (código pai, tipo, código filho, unidade, coeficiente e situação), **custo por UF/regime** (valor, `%AS`, ausência) e **percentual de mão de obra**. Guardar localizador de pasta, aba e linha para cada registro. A chave deve preservar base, edição, UF, regime e código sem converter códigos textuais em números por conveniência.

Antes de afirmar que essas tabelas são um dataset utilizável, conferir: cabeçalhos e tipos; quantidade de composições distintas e com custo; correspondência entre códigos analíticos, custos e percentuais; nulos e hífens; duplicatas de cabeçalho; expansão de subcomposições e eventuais ciclos; unidades; totais reconciliados com a fonte; distribuição de `%AS` em ES; e exemplos de cada grupo. Separar custo ausente de custo zero. Um join serviço–item multiplica linhas por definição; essa multiplicação não pode inflar contagens de serviços. A inspeção amostral presente demonstra **disponibilidade de campos**, ainda não sua completude nem a viabilidade estatística de cada modelo.
