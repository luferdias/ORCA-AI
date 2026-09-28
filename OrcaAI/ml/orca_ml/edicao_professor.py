"""Links permanentes da entrega ao professor, vinculados à execução publicada."""
from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.parse import quote

REPOSITORIO = 'https://github.com/luferdias/ORCA-AI'
COMMIT = 'e20741b0214dff489147fa04739bb2a1ed44bc07'
EXECUCAO = 'OrcaAI/ml/outputs/entrega_ufg_acabamentos_2026-09-27'
SHA_EXECUCAO = '4ac92b962c47abf391bd2bf2eb0c3206bcc1b040a8f99f25811a9d438544fc46'


def github(caminho: str, *, pasta: bool = False) -> str:
    return f'{REPOSITORIO}/{"tree" if pasta else "blob"}/{COMMIT}/{quote(caminho, safe="/")}'


def conferir_execucao(caminho: Path) -> dict:
    """Impede associar links fixos a dados de outra execução."""
    sha = hashlib.sha256(caminho.read_bytes()).hexdigest()
    if sha != SHA_EXECUCAO:
        raise ValueError('Esta edição exige a execução publicada de 27/09/2026; o manifesto diverge')
    return {
        'professor': 'Ronaldo', 'data_documento': '2026-09-28',
        'repositorio': REPOSITORIO, 'commit_experimental': COMMIT,
        'pasta_execucao': EXECUCAO, 'manifesto_execucao_sha256': sha,
        'visibilidade_verificada': 'publico', 'acesso_verificado_em': '2026-09-28',
    }


def _secao(titulo, paragrafos, links):
    return dict(titulo=titulo, paragrafos=paragrafos, tabelas=[], imagens=[], links=links)


def aplicar_edicao(secoes, edicao):
    if edicao.get('commit_experimental') != COMMIT or edicao.get('manifesto_execucao_sha256') != SHA_EXECUCAO:
        raise ValueError('Metadados da edição não correspondem à versão publicada')
    capa = secoes[0]
    capa['paragrafos'][1] = (
        'Disciplina: Aprendizado de máquina aplicado a dados estruturados. '
        'Professor: Ronaldo. Autor: engenheiro Luis Fernando. '
        'Universidade Federal de Goiás (UFG). Vitória, Espírito Santo. '
        'Resultados executados em 27/09/2026; edição para entrega em 28/09/2026.'
    )
    capa['links'] = [('Abrir o desenvolvimento no GitHub - versão avaliada', github('OrcaAI/ml', pasta=True))]
    guia = _secao('Guia de leitura e acesso ao desenvolvimento', [
        'Este PDF reúne as três tarefas solicitadas: previsão por regressão, classificação supervisionada e agrupamento não supervisionado. Os títulos azuis de links são clicáveis e abrem o código ou a evidência correspondente no GitHub.',
        'Roteiro de leitura: dados e método (seções 1 e 2); regressão e exemplo de pintura (3 e 4); classificação e matrizes de confusão (5 e 6); agrupamento e perfis (7 e 8); discussão conjunta (9); reprodução e referências (10). Os apêndices organizam os arquivos de cada fonte.',
        f'Versão experimental fixada: commit {COMMIT}. Os links preservam essa versão do código e dos resultados, mesmo que a branch main receba melhorias. Esta edição acrescenta navegação e identificação acadêmica; as métricas vêm da execução já concluída.',
        'Acesso público: em 28/09/2026, o proprietário autorizou tornar o repositório público para consulta. Os links permitem ler e baixar os arquivos sem convite ou login. A escrita no repositório permanece restrita às contas autorizadas. O PDF contém os resultados e gráficos para leitura independente.',
        'Para começar pelo código, abra executar_estudo.py. Esse arquivo executa as três tarefas no mesmo recorte temático. Os scripts individuais e os módulos especializados estão ligados nas seções de resultados. CSV é uma tabela de dados que pode ser baixada e aberta no Excel, no VS Code ou em Python.'
    ], [
        ('1. Código principal - executar_estudo.py', github('OrcaAI/ml/executar_estudo.py')),
        ('2. Guia de instalação e execução no VS Code', github('OrcaAI/ml/README.md')),
        ('3. Resultados completos das duas fontes', github(EXECUCAO, pasta=True)),
        ('4. Manifesto da execução: parâmetros, versões e hashes', github(EXECUCAO+'/execucao_estudo.json')),
        ('5. Plano do experimento e critérios de avaliação', github('OrcaAI/spec/ml_ufg/plano_consolidacao_acabamentos.md')),
    ])
    secoes.insert(1, guia)
    for secao in secoes:
        title = secao['titulo']
        if title.startswith('1. Dados'):
            secao['links'] = [
                ('SINAPI-ES - dataset do recorte, 514 serviços', github(EXECUCAO+'/sinapi_es/dados/dataset_acabamentos.csv')),
                ('DER-ES/IOPES - dataset do recorte, 70 serviços', github(EXECUCAO+'/der_es/dados/dataset_acabamentos.csv')),
                ('Código de preparação dos atributos e dos grupos de variantes', github('OrcaAI/ml/orca_ml/atributos_acabamentos.py')),
            ]
        elif title.startswith('Regressão | interpretação'):
            secao['links'] = [
                ('Código Python - modelos lineares, teste temporal e persistência', github('OrcaAI/ml/orca_ml/regressao.py')),
                ('SINAPI-ES - estatísticas por nicho da regressão', github(EXECUCAO+'/sinapi_es/regressao/estatisticas_nichos.csv')),
                ('DER-ES/IOPES - estatísticas por nicho da regressão', github(EXECUCAO+'/der_es/regressao/estatisticas_nichos.csv')),
            ]
        elif title.startswith('5. Classificação'):
            secao['links'] = [
                ('Código Python - classificação, validação e escolha do modelo', github('OrcaAI/ml/orca_ml/classificacao.py')),
                ('Executar somente a classificação - executar_classificacao.py', github('OrcaAI/ml/executar_classificacao.py')),
            ]
        elif title.startswith('6. Matriz'):
            fonte = 'sinapi_es' if 'SINAPI' in title else 'der_es'
            secao['links'] = [
                ('Métricas de teste dos classificadores', github(f'{EXECUCAO}/{fonte}/classificacao/metricas_teste.csv')),
                ('Previsões por serviço para conferir acertos e erros', github(f'{EXECUCAO}/{fonte}/classificacao/previsoes.csv')),
                ('Partições de treino e teste, com os grupos de variantes', github(f'{EXECUCAO}/{fonte}/classificacao/particoes.csv')),
            ]
        elif title.startswith('7. Agrupamento'):
            fonte = 'sinapi_es' if 'SINAPI' in title else 'der_es'
            secao['links'] = [
                ('Código Python - K-Means, seleção de k e estabilidade', github('OrcaAI/ml/orca_ml/agrupamento.py')),
                ('Tabela de candidatos a k e critérios de elegibilidade', github(f'{EXECUCAO}/{fonte}/agrupamento/candidatos_k.csv')),
            ]

    secoes.append(_secao('Apêndice A. Como executar e conferir o trabalho', [
        '1. Baixe a versão pública fixada ou clone o projeto. Para reproduzir exatamente a versão avaliada, use git checkout '+COMMIT+'. No VS Code, abra a pasta OrcaAI/ml.',
        '2. Use Python 3.12. Crie o ambiente com python3.12 -m venv .venv; ative-o com source .venv/bin/activate (macOS/Linux) ou .venv\\Scripts\\Activate.ps1 (PowerShell). Instale as dependências com python -m pip install -r requirements.txt.',
        '3. Execute python executar_estudo.py. O programa lê os ZIPs e datasets incluídos no projeto, processa as fontes separadamente e cria uma nova pasta de resultados. Esse comando refaz as três tarefas no recorte de pintura, pisos e revestimentos/forros; preserve a estrutura do repositório.',
        '4. Para executar uma única tarefa, use python executar_classificacao.py ou python executar_agrupamento.py. O script executar_regressao.py preserva a avaliação original mais ampla; o recorte comum das três tarefas é executado por executar_estudo.py.',
        '5. Para conferir a implementação, instale python -m pip install -r requirements-dev.txt e rode python -m pytest -q. A versão experimental publicada passou por 221 testes e nove subtestes. Cada teste automatizado verifica uma regra do programa; isso não equivale a validação profissional dos modelos.',
        'Arquivos CSV grandes podem não ter prévia no GitHub. Use Download raw file ou baixe o repositório para ler os dados completos. Os links dos apêndices priorizam as tabelas compactas do recorte. O mapa das aulas descreve os materiais consultados; arquivos originais externos da disciplina não fazem parte deste repositório.'
    ], [
        ('Executar as três tarefas no recorte - executar_estudo.py', github('OrcaAI/ml/executar_estudo.py')),
        ('Executar a regressão original - executar_regressao.py', github('OrcaAI/ml/executar_regressao.py')),
        ('Executar a classificação - executar_classificacao.py', github('OrcaAI/ml/executar_classificacao.py')),
        ('Executar o agrupamento - executar_agrupamento.py', github('OrcaAI/ml/executar_agrupamento.py')),
        ('Dependências e versões - requirements.txt', github('OrcaAI/ml/requirements.txt')),
        ('Testes automatizados das rotinas', github('OrcaAI/ml/tests', pasta=True)),
        ('Preparação de dados - preparar_dados.py', github('OrcaAI/ml/preparar_dados.py')),
        ('Leitor e conciliação das composições SINAPI', github('OrcaAI/ml/orca_ml/sinapi_composicoes.py')),
        ('Leitor e conciliação das composições DER-ES', github('OrcaAI/ml/orca_ml/der_composicoes.py')),
        ('Mapa dos conteúdos da disciplina usados no projeto', github('OrcaAI/spec/ml_ufg/mapa_materiais_disciplina.md')),
    ]))
    for fonte,nome in [('sinapi_es','SINAPI-ES'),('der_es','DER-ES / IOPES')]:
        p=f'{EXECUCAO}/{fonte}'
        links=[(label, github(p+'/'+path, pasta=pasta)) for label,path,pasta in [
            ('Dataset: atributos e classes de cada serviço','dados/dataset_acabamentos.csv',False),
            ('Recursos extraídos das composições analíticas','dados/recursos_folha.csv',False),
            ('Auditoria da extração e conciliação dos custos','dados/auditoria_extracao.json',False),
            ('Populações: serviços presentes em cada tarefa','dados/populacoes_tarefas.csv',False),
            ('Regressão: publicado, previsto e persistência por observação','regressao/previsoes_pareadas.csv',False),
            ('Regressão: estatísticas agregadas por nicho','regressao/estatisticas_nichos.csv',False),
            ('Classificação: métricas da validação usada na seleção','classificacao/metricas_cv.csv',False),
            ('Classificação: matriz de confusão em formato de tabela','classificacao/confusao.csv',False),
            ('Classificação: parâmetros, versões e resumo','classificacao/resumo.json',False),
            ('Agrupamento: grupo atribuído a cada serviço','agrupamento/atribuicoes.csv',False),
            ('Agrupamento: médias dos atributos de cada grupo','agrupamento/centroides.csv',False),
            ('Agrupamento: resultados das verificações de estabilidade','agrupamento/estabilidade.csv',False),
            ('Agrupamento: seleção, diagnóstico e resumo','agrupamento/resumo.json',False),
            ('Todas as tabelas e modelos desta fonte','',True),
        ]]
        secoes.append(_secao('Apêndice B. Evidências por fonte | '+nome,[
            'Este índice permite seguir cada conclusão até a tabela que a originou. Código e descrição identificam serviços dentro da própria fonte; os códigos SINAPI e DER não são pares de equivalência técnica.',
            'Na classificação, compare a validação, que escolhe o algoritmo, com o teste reservado, que mede o resultado final. No agrupamento DER, preserve a indicação de diagnóstico: nenhum candidato cumpriu o tamanho mínimo de grupo.',
        ],links))
    return secoes
