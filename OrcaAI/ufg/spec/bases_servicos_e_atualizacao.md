# Bases de serviços e atualização por projeto

> **Escopo vigente:** a [proposta atual do trabalho](proposta_projeto_ml_es.md) define as três tarefas sobre dados estruturados, começando pelo SINAPI-ES e depois pelo DER-ES/IOPES. A classificação por texto mencionada abaixo permanece como alternativa futura. Este documento continua orientando o catálogo de fontes e a atualização por projeto.

Data: 27/09/2026. Especificação para a aplicação acadêmica de ML no ORCA-AI.

## Objetivo

Usar os referenciais oficiais como catálogo de serviços, descrições, unidades e composições. O primeiro recorte atende à rotina da SRA-ES em Vitória: classificação de serviços e recuperação de composições candidatas, com a referência exata do documento usado.

O [catálogo de fontes](../../bases/catalogo_fontes_referenciais.json) registra os portais verificados e os limites de acesso. A [auditoria de 27/09/2026](../../docs/auditoria_bases_referenciais_2026-09-27.md) documenta as evidências. Essas observações precisam ser renovadas ao iniciar cada orçamento.

## 1. Seleção da fonte

Para o contexto usual de edificações da SRA-ES, a ordem operacional proposta é SINAPI-ES, DER-ES Edificações e fontes complementares tecnicamente pertinentes. Serviços rodoviários acionam SICRO-ES e DER-ES Rodovias conforme o objeto e as regras aplicáveis ao projeto. Serviços de elaboração de projetos usam a tabela específica de projetos quando pertinente.

O A1 e o A5 registram qual regra do projeto ou instrumento da contratação determina a referência. A preferência operacional não constitui uma regra universal de precedência entre sistemas. Referências de SP, RJ e MG exigem identificação da região, período, condições e motivo da escolha antes de compor um orçamento no ES.

SINAPI e SICRO possuem recortes por UF. DNIT é o órgão responsável pelo SICRO, e não uma segunda tabela a ser contada como outra amostra. CUB e ANP entram como indicadores auxiliares; não fornecem a mesma unidade de observação dos catálogos de serviços.

## 2. Entidades e campos

| Entidade | Conteúdo |
| --- | --- |
| Fonte | Órgão, base, alias histórico, endereço oficial, área de aplicação e condição de acesso |
| Edição | Competência, data de publicação quando conhecida, atualização do portal, captura, revisão, URL, formato e hash |
| Serviço/composição | Código textual, descrição oficial, unidade, grupo nativo e custo de referência quando disponível |
| Insumo | Código, descrição, unidade, categoria e preço de referência |
| Composição analítica | Ligação serviço–insumo, coeficiente, produtividade e demais condições presentes na fonte |
| Exemplo revisado | Texto da demanda, classe atribuída, candidatos, escolha/correção humana e origem |

A chave de um serviço deve incluir base e código. Sua versão acrescenta edição, UF, regime e revisão. O mesmo código em bases diferentes não é automaticamente o mesmo serviço. Preservar zeros iniciais e o valor bruto do código.

Campos adicionais necessários: `descricao_oficial`, `descricao_normalizada`, `unidade_original`, `unidade_normalizada`, `grupo_nativo`, `classe_revisada`, `source_locator`, `regime_encargos`, `bdi_incluso`, `bdi_percentual`, `preco_status` e observações de transporte ou outros itens incluídos/excluídos.

A descrição oficial permanece vinculada à fonte. Uma descrição redigida pelo agente fica em `descricao_proposta`, com revisão técnica própria. Sufixos, datas de aferição e códigos somente são copiados da referência quando efetivamente presentes.

## 3. Regra da última tabela

1. **Abrir a pesquisa do projeto.** Registrar data/hora de consulta, UF, objeto, fontes aplicáveis e regime de encargos.
2. **Consultar o publicador.** Localizar a maior competência efetivamente disponibilizada até aquele momento, dentro do escopo selecionado. Para uma mesma competência, verificar revisões, erratas e notas de uso.
3. **Confirmar o arquivo.** Validar formato real e conteúdo: um link listado ou HTTP 200 que entregue HTML não comprova acesso à tabela. Guardar evidência do nível de acesso.
4. **Conferir o conteúdo.** Checar competência no cabeçalho, região, regime, colunas, grupos, unidades e eventuais valores ausentes ou provisórios. Descrições podem ser aproveitáveis mesmo quando preços ainda não estiverem validados; registrar as duas condições separadamente.
5. **Guardar a edição original.** Usar arquivo imutável, URL e hash. Manter versões anteriores. Retificação que altere o conteúdo gera uma nova revisão, mesmo com o mesmo nome de arquivo.
6. **Fixar as referências do orçamento.** Registrar no manifesto do projeto as edições escolhidas e a data-base do orçamento. Se fontes tiverem competências diferentes, registrar a diferença e o tratamento adotado pelo responsável técnico.
7. **Atualizar com rastreabilidade.** Na revisão seguinte do orçamento, repetir a consulta. Uma atualização produz nova versão do orçamento e comparação das mudanças; os 12 projetos anteriores conservam os seus documentos e referências históricas.

Se o portal estiver indisponível ou depender de acesso autorizado, marcar `atualidade_nao_confirmada`. Um arquivo antigo disponível localmente continua sendo histórico e não recebe o rótulo de última edição.

O caminho sugerido para futura coleta é `OrcaAI/bases/<fonte>/<uf>/<competencia>/<revisao>/`. Dados preparados para ML ficam em `OrcaAI/knowledge/datasets/`; modelos e experimentos ficam em `OrcaAI/ml/`, conforme a arquitetura proposta. A auditoria atual não implantou um coletor nem uma rotina agendada.

## 4. Aplicação de Machine Learning

**Tarefa principal:** dado o texto inicial de uma demanda, classificar sua família de serviço e apresentar composições candidatas, com descrição, unidade, código, base e edição.

- A taxonomia começa pelos grupos que existem nas fontes e é harmonizada pelos A2, A5 e A7. Disciplina/sistema e ação podem ser eixos distintos: instalações elétricas versus manutenção, por exemplo.
- O catálogo fornece descrições e grupos; os 12 projetos fornecem exemplos de escolha e aplicação, desde que revisados. O código escolhido ao final da análise não entra como informação de entrada da tarefa que tenta prever essa escolha.
- Referência de classificação: classe mais frequente no treino. Primeiro modelo: TF-IDF com regressão logística. O uso de embeddings será comparado em partições equivalentes.
- Referência de busca: correspondência lexical, como BM25; comparação com recuperação vetorial. Métricas propostas: macro-F1 e resultados por classe para classificação; Recall@5 e MRR@5 para recuperação, além da correção das referências.
- Descrições iguais ou equivalentes reaparecem em diferentes meses, UFs, bases e projetos. Agrupar ou remover essas repetições antes de medir generalização. Em um teste temporal, o treinamento usa apenas informação publicada até a data de corte e a avaliação usa demandas posteriores.
- O catálogo oficial permitido no momento da consulta pode ser indexado. As respostas dos casos de teste e suas revisões humanas ficam fora do treinamento do classificador ou ranqueador.
- Preços são obtidos da edição aplicável e verificada. O objetivo inicial de classificação não exige prever preços nem usar preço como rótulo.

O SA-ML-05 deve relatar classes sem exemplos suficientes, equivalências não confirmadas e erros entre serviços parecidos. A afirmação de cobertura de “95%” fornecida no texto inicial não foi comprovada pela auditoria e não será usada como resultado acadêmico.

## 5. Responsáveis

| Etapa | Responsável |
| --- | --- |
| Prioridade por objeto e UF | A1 e A5 |
| Acesso, edição e rastreabilidade | A5 com SA-ML-01 |
| Catálogo de serviços e taxonomia | A2, A5 e A7 |
| Embeddings e busca | SA-ML-02 e SA-ML-04 |
| Treinamento | SA-ML-03, coordenado pelo A11 |
| Avaliação acadêmica | SA-ML-05 e A9 |
| Integridade dos 12 projetos | Agente 5S |
| Validação das escolhas técnicas | Usuário e especialistas do domínio |
