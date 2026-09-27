# API Knowledge — contrato inicial

Estado: proposta de contrato; serviço ainda não implementado.

## 1. Responsabilidade

A API liga o orquestrador às fontes documentais, aos modelos publicados e ao registro de insights. Qdrant atende à recuperação vetorial. O registro de modelos e as revisões de insights precisam de armazenamento próprio, definido na implementação; Qdrant não será tratado como registro universal de experimentos.

## 2. Endpoints propostos

| Endpoint | Comportamento |
| --- | --- |
| `GET /context/{context_id}` | Retorna o manifesto do contexto. Com `q` e `top_k`, devolve trechos relevantes, referências e versão do índice |
| `GET /models/latest?context_id=...&task_id=...` | Retorna o manifesto da última versão publicada para aquele contexto e tarefa |
| `POST /insights` | Registra uma sugestão rastreável, inicialmente pendente de revisão |

`GET /context/heineken` é uma instância da primeira rota. Só terá conteúdo depois de existir um contexto cadastrado com fontes fornecidas para esse fim. O contexto acadêmico de orçamento será identificado separadamente, por exemplo `sra-es`. Um contexto desconhecido retorna 404.

### Consulta ao conhecimento

A resposta identifica `context_id`, `index_version`, `embedding_model_version` e `results`. Cada resultado contém `chunk_id`, texto, score, `project_id`, caminho e hash da fonte, e localização no documento. O score de similaridade não será apresentado como probabilidade de correção.

O serviço aplica filtros de contexto e, quando necessário, de projetos permitidos na avaliação. O valor de `top_k` deve ter limite definido no contrato implementado. Sem correspondências, retorna uma lista vazia; falha de conexão com o Qdrant gera um erro explícito de indisponibilidade.

### Registro de modelos

O manifesto contém `model_id`, `version`, `context_id`, `task_id`, `dataset_version`, `evaluation_id`, métricas, localização e hash do artefato, além de estado e data de publicação. `latest` considera versões publicadas para uso no experimento após avaliação e decisão registrada; não escolhe automaticamente o arquivo modificado mais recentemente.

Sem modelo publicado para o par contexto/tarefa, o endpoint retorna 404. O modelo de embeddings e o modelo supervisionado possuem identificadores e versões próprios.

### Insights e revisão

Campos de entrada: `request_id`, `context_id`, `project_id`, `task_id`, `model_id`, `model_version`, `input_reference`, `result` e `evidence_refs`. O servidor atribui `insight_id`, data e estado inicial `pending_review`. Uma repetição do mesmo `request_id` não deve criar duplicatas; conteúdo divergente para a mesma chave gera conflito.

O POST não treina um modelo nem publica uma recomendação. O registro de revisão humana acrescenta autor, data, decisão e eventual correção. Na primeira demonstração, essa revisão poderá ser registrada em arquivo estruturado pelo orquestrador. Uma rota específica de revisão pode ser acrescentada quando o fluxo de uso for implementado. O SA-ML-01 incorpora apenas revisões válidas na próxima versão do dataset.

## 3. Configuração fornecida pelo usuário

```dotenv
KNOWLEDGE_PATH=../knowledge
VECTOR_DB=qdrant
QDRANT_URL=http://localhost:6333
```

No arranjo futuro proposto, `OrcaAI/api/` e `OrcaAI/ml/` são componentes irmãos de `OrcaAI/knowledge/`. O código resolverá `KNOWLEDGE_PATH` a partir da raiz declarada de cada componente, independentemente do diretório de onde o processo for iniciado. Carregar a variável e aplicar essa regra são responsabilidades da implementação.

`QDRANT_URL` aponta para o Qdrant acessível pelo processo da API. Em execução local, usa o endereço informado. Se forem usados contêineres separados, o endereço deve refletir a rede entre os serviços. A referência oficial apresenta a porta HTTP 6333 e persistência local: [Qdrant Local Quickstart](https://qdrant.tech/documentation/quickstart/).

Antes de indexar, definir coleção, versão/dimensão do modelo de embeddings e armazenamento persistente do Qdrant. A pasta `embeddings/` guarda manifestos ou exportações; sua existência não configura a persistência do banco.

## 4. Critérios de verificação na implementação

- Consultar um contexto não retorna documentos de outro contexto.
- Todo trecho recuperado aponta para uma fonte existente e sua versão.
- Alterações incompatíveis de embeddings exigem índice compatível e identificado.
- `latest` respeita contexto, tarefa e estado de publicação.
- Insights repetidos não duplicam exemplos; uma previsão não se torna rótulo por conta própria.
- Falhas de Qdrant e ausência de modelo têm respostas distintas.
- As rotas não alteram os arquivos originais dos 12 projetos.
