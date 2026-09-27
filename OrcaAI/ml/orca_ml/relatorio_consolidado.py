"""Documento acadêmico rastreável, sem retreinar ou escolher modelos."""
from __future__ import annotations

import base64
import hashlib
import html
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

from .graficos_consolidacao import ALGORITMOS, CLASSES, FONTES, NOMES, gerar_graficos_consolidacao, numero


def _perto(a,b,contexto):
    if not np.isclose(float(a),float(b),rtol=1e-8,atol=1e-8):
        raise ValueError(f'Métrica inconsistente: {contexto}: {a} != {b}')


def _ler_bases(root,run):
    if run.get('etapa')!='todas' or run.get('status') not in {'em_execucao','concluido'} or not run.get('bases'):
        raise ValueError('O relatório exige uma execução completa das três tarefas')
    comp=run.get('competencia'); result={}; hashes={}
    files={'dados':'dados/dataset_acabamentos.csv','populacoes':'dados/populacoes_tarefas.csv','pares':'regressao/previsoes_pareadas.csv','estatisticas':'regressao/estatisticas_nichos.csv','metricas_class':'classificacao/metricas_teste.csv','previsoes_class':'classificacao/previsoes.csv','particoes':'classificacao/particoes.csv','confusao':'classificacao/confusao.csv','cv':'classificacao/metricas_cv.csv','candidatos':'agrupamento/candidatos_k.csv','atribuicoes':'agrupamento/atribuicoes.csv','pca':'agrupamento/coordenadas_pca.csv','centros':'agrupamento/centroides.csv'}
    for source,summary in run['bases'].items():
        if source not in FONTES or summary.get('fonte')!=source or summary.get('competencia')!=comp:
            raise ValueError('Fonte ou competência divergente no resumo')
        for stage in ('classificacao','agrupamento','regressao'):
            s=summary.get(stage,{})
            if s.get('fonte')!=source or (stage!='regressao' and s.get('competencia')!=comp):
                raise ValueError(f'Execução incompleta ou fonte/competência divergente: {stage}')
            allowed={'concluido','sem_candidato_valido'} if stage=='agrupamento' else ({'concluido','parcial'} if stage=='regressao' else {'concluido'})
            if s.get('status') not in allowed:raise ValueError(f'Etapa não concluída: {stage}')
        b={'resumo':summary}
        for key,relative in files.items():
            path=root/source/relative
            if not path.is_file():raise ValueError(f'Arquivo de resultado ausente: {path}')
            hashes[str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()
            df=pd.read_csv(path,dtype={'codigo':str})
            if 'fonte' in df and not df.fonte.eq(source).all():raise ValueError(f'Fonte divergente em {relative}')
            if key in {'dados','pca'} and not df.competencia.eq(comp).all():raise ValueError(f'Competência divergente em {relative}')
            b[key]=df
        data=b['dados'];pairs=b['pares'];stats=b['estatisticas'];cls=summary['classificacao'];cl=summary['agrupamento']
        if len(data)!=summary['n_validos'] or data.codigo.duplicated().any() or set(data.classe)!=set(CLASSES):raise ValueError('População/classificação inválida no catálogo')
        if data.classe.value_counts().to_dict()!=summary['classes']:raise ValueError('Contagem das classes diverge do catálogo')
        if set(pairs.competencia_alvo)!=set(summary['regressao']['competencias_teste']):raise ValueError('Competências do teste de regressão divergentes')
        if set(pairs.nicho_id)!=set(CLASSES) or pairs.duplicated(['codigo','competencia_alvo']).any():raise ValueError('Recorte/duplicatas na regressão')
        if not (pairs.custo_observado.gt(0).all() and np.isfinite(pairs[['custo_observado','custo_previsto','previsto_persistencia']]).all().all()):raise ValueError('Preços inválidos na regressão')
        calc=100*(pairs.custo_previsto-pairs.custo_observado).abs()/pairs.custo_observado
        calc_base=100*(pairs.previsto_persistencia-pairs.custo_observado).abs()/pairs.custo_observado
        if not np.allclose(calc,pairs.ape) or not np.allclose(calc_base,pairs.ape_persistencia):raise ValueError('Erros percentuais não correspondem aos preços')
        for row in stats.itertuples():
            sub=pairs.loc[pairs.nicho_id.eq(row.nicho_id)]
            _perto(row.n,len(sub),'n regressão');_perto(row.mape,sub.ape.mean(),'MAPE');_perto(row.mape_persistencia,sub.ape_persistencia.mean(),'MAPE persistência')
        selected=cls['algoritmo_selecionado'];metrics=b['metricas_class'];preds=b['previsoes_class']
        if metrics.loc[metrics.selecionado_cv.eq(True),'algoritmo'].tolist()!=[selected]:raise ValueError('Seleção de classificação divergente')
        winner=max(cls['vencedores_cv'],key=lambda x:cls['vencedores_cv'][x]['f1_macro_media'])
        if winner!=selected:raise ValueError('Modelo selecionado não é vencedor da validação')
        for row in metrics.itertuples():
            p=preds.loc[preds.algoritmo.eq(row.algoritmo)]
            if p.codigo.duplicated().any() or len(p)!=cls['n_teste']:raise ValueError('População de teste inconsistente')
            for col,fn in [('f1_macro',lambda x,y:f1_score(x,y,labels=CLASSES,average='macro',zero_division=0)),('acuracia',accuracy_score),('acuracia_balanceada',balanced_accuracy_score)]:
                _perto(getattr(row,col),fn(p.classe,p.classe_prevista),col)
            matches=b['confusao'].loc[b['confusao'].algoritmo.eq(row.algoritmo)]
            for q in matches.itertuples():_perto(q.n,((p.classe==q.classe_real)&(p.classe_prevista==q.classe_prevista)).sum(),'matriz de confusão')
        parts=b['particoes'];test_codes=set(parts.loc[parts.particao.eq('teste'),'codigo'])
        if test_codes!=set(preds.codigo) or set(parts.codigo)!=set(data.codigo):raise ValueError('Partições e previsões divergem')
        if parts.groupby('grupo_particao').particao.nunique().gt(1).any():raise ValueError('Grupo de variantes compartilhado pelo treino e teste')
        if set(b['atribuicoes'].codigo)!=set(data.codigo) or set(b['pca'].codigo)!=set(data.codigo):raise ValueError('População de agrupamento divergente')
        counts=b['atribuicoes'].cluster.value_counts().sort_index()
        for row in b['centros'].itertuples():_perto(row.n,counts.get(row.cluster,0),'tamanho cluster')
        diagnostic=cl.get('status')=='sem_candidato_valido'
        if diagnostic:
            if cl.get('k_selecionado') is not None or not cl.get('k_diagnostico') or b['candidatos'].elegivel.eq(True).any():raise ValueError('Diagnóstico foi promovido a seleção válida')
        elif cl.get('k_selecionado') not in set(b['candidatos'].loc[b['candidatos'].elegivel.eq(True),'k']):raise ValueError('k selecionado não elegível')
        fractions=b['centros'][['fracao_mao_obra','fracao_material','fracao_equipamento','fracao_outros']]
        if fractions.min().min() < -1e-8 or not np.allclose(fractions.sum(axis=1),1):raise ValueError('Participações dos centros inválidas')
        preferred={'sinapi_es':'96130','der_es':'190115'}[source]
        candidates=data.loc[data.classe.eq('pintura')&data.codigo.isin(pairs.codigo)]
        if candidates.empty:raise ValueError('Não há exemplo de pintura comum ao catálogo e à regressão')
        if preferred in set(candidates.codigo):example=candidates.loc[candidates.codigo.eq(preferred)].iloc[0]
        else:example=candidates.assign(dist=(candidates.custo-candidates.custo.median()).abs()).sort_values(['dist','codigo']).iloc[0]
        code=example.codigo;sp=parts.loc[parts.codigo.eq(code)].iloc[0];classification_prediction=preds.loc[preds.codigo.eq(code)&preds.algoritmo.eq(selected)]
        cluster_row=b['atribuicoes'].loc[b['atribuicoes'].codigo.eq(code)].iloc[0]
        b['exemplo']={'codigo':code,'descricao':example.descricao,'custo':float(example.custo),'particao':sp.particao,'classe_prevista':None if classification_prediction.empty else classification_prediction.iloc[0].classe_prevista,'cluster':int(cluster_row.cluster)}
        result[source]=b
    windows={tuple(b['resumo']['regressao']['competencias_teste']) for b in result.values()}
    if len(windows)!=1:raise ValueError('As fontes usam janelas de teste diferentes')
    return result,hashes


def _tabela(headers,rows):return {'cabecalho':headers,'linhas':[[str(v) for v in row] for row in rows]}
def _nome(value):return NOMES.get(value,value).replace('\n',' ')


def _secoes(run,bases,graphs):
    sections=[]
    def add(title,paragraphs=None,tables=None,images=None,links=None):
        sections.append(dict(titulo=title,paragrafos=paragraphs or [],tabelas=tables or [],imagens=images or [],links=links or []))
    executive=[]
    for source,b in bases.items():
        s=b['resumo'];selected=s['classificacao']['algoritmo_selecionado'];m=b['metricas_class'].set_index('algoritmo').loc[selected];cl=s['agrupamento'];better=int((b['estatisticas'].mape<b['estatisticas'].mape_persistencia).sum())
        group_text=f"K-Means selecionou {cl['k_selecionado']} grupos" if cl.get('k_selecionado') else 'nenhum k atendeu aos critérios; o agrupamento é somente diagnóstico'
        executive.append(f"{FONTES[source]}: {s['n_validos']} serviços no catálogo. O recorte abrange pintura, pisos e revestimentos/forros. A regressão superou o último preço em {better} de 3 nichos. {ALGORITMOS[selected]} obteve F1 macro {numero(m.f1_macro,3)} em {int(m.n)} serviços de teste; {group_text}.")
    add('Aprendizado de máquina aplicado ao ORCA-AI',[
        'Relatório de consolidação | Universidade Federal de Goiás (UFG)',
        'Disciplina: Aprendizado de máquina aplicado a dados estruturados. Responsável: engenheiro Luis Fernando. Vitória, Espírito Santo. Edição do estudo: 27 de setembro de 2026.',
        'Tema: previsão de custos, classificação de famílias técnicas e descoberta de perfis de recursos em pintura e acabamentos. Fontes: SINAPI-ES e DER-ES/IOPES, analisadas separadamente. Regime: sem desoneração. Catálogo de referência: maio/2026.',
        'Resumo executivo',*executive,
        'As três tarefas respondem a perguntas diferentes. Seus indicadores não formam uma nota única nem um ranking entre as tabelas oficiais. O experimento apoia conferência e estudo acadêmico; a equivalência técnica dos serviços continua dependente de revisão de engenharia.'
    ],tables=[_tabela(['Tarefa','Pergunta','Saída'],[['Regressão','Qual o custo da próxima competência?','Valor em R$/m² e erro'],['Classificação','A qual nicho pertence a composição?','Classe sugerida e matriz de erros'],['Agrupamento','Quais serviços têm perfis de recursos semelhantes?','Grupos exploratórios e seus perfis']])])
    rows=[]
    for source,b in bases.items():
        s=b['resumo'];p=s['populacoes'];rows.append([FONTES[source],s['n_validos'],s['n_grupos_variantes'],p['catalogo_e_regressao'],p['somente_catalogo'],p['somente_regressao']])
    add('1. Dados, recorte e unidades de observação',[
        'Foram usados os mesmos três nichos e apenas serviços em m². Classificação e agrupamento utilizam uma composição por serviço em maio/2026. A regressão usa o histórico e avalia pares serviço-competência entre março e maio/2026; portanto, sua quantidade de previsões é maior que a quantidade de serviços.',
        'A interseção abaixo torna explícitos os serviços presentes em ambas as análises. Não foram removidos retrospectivamente serviços que deixaram de existir no catálogo de maio. A distribuição reflete os catálogos, não a frequência desses serviços em obras.'
    ],tables=[_tabela(['Fonte','Catálogo','Variantes','Em ambas','Só catálogo','Só regressão'],rows)],images=[graphs['cobertura']])
    add('2. Método e controles do experimento',[
        'As classes pintura, pisos e revestimentos/forros derivam do mapeamento dos grupos oficiais. Não representam rótulos homologados por revisão humana. Os serviços foram unidos em grupos de variantes quando têm os mesmos recursos-folha ou descrições normalizadas semelhantes; esse procedimento reduz vazamento, mas não garante independência técnica completa.',
        'Regressão: LinearRegression simples (último custo) e múltipla (três custos consecutivos); seleção por erro quadrático na validação e comparação com a persistência, que repete o último preço. Teste cronológico de março a maio/2026. Cada previsão olha apenas uma competência à frente, incorporando preços anteriores disponíveis. O estudo é retrospectivo, com histórico revisado.',
        'A validação nominal da regressão é janeiro-fevereiro/2026. No SINAPI, o controle de publicação deixa apenas janeiro efetivamente avaliável: as revisões de janeiro e fevereiro foram publicadas em 25/03/2026, quando o alvo de fevereiro já era conhecido. No DER, janeiro e fevereiro são usados; faltam datas reais de publicação e a interpretação é retrospectiva.',
        'Classificação: Random Forest, árvore de decisão e KNN. O primeiro dos cinco folds estratificados por grupos forma o teste; três folds internos escolhem parâmetros por F1 macro. A referência é prever a classe mais frequente. Escalonamento e modelos são ajustados dentro de cada treino. Código, descrição e grupo oficial do serviço ficam fora das dez entradas [3, 4].',
        'Agrupamento: K-Means com escala própria por fonte, 30 inicializações, semente 42 e k entre 2 e 5. Seleção pela maior silhouette entre candidatos cujo menor grupo tem ao menos max(3, teto de 5% do catálogo). Classes não entram no ajuste. A estabilidade é reavaliada com outras sementes e subamostras de 80% [5].',
        'Extração: subcomposições são expandidas até recursos-folha. No SINAPI, o total hierárquico concilia exatamente após truncar cada parcela a centavos em cada nível. As participações de recursos usam a soma sem truncamento e são aproximações. Preços SP usados na ausência de ES ficam identificados. O DER incorpora encargos à mão de obra; o SINAPI discrimina diversos encargos complementares, impedindo comparar suas contagens como se fossem equivalentes.'
    ],tables=[_tabela(['Entradas de classificação e agrupamento','Unidade'],[['4 participações de custo: mão de obra, material, equipamento, outros','Fração de 0 a 1'],['4 contagens de recursos distintos nas mesmas categorias','Recursos por composição'],['Horas de mão de obra e equipamento extraídas das folhas em H','h/m²']]),_tabela(['Indicador','Leitura didática'],[['MAPE','Média do erro absoluto em %, menor é melhor.'],['F1 macro','Equilibra precisão e recall, dando o mesmo peso às três classes.'],['Silhouette','Coesão e separação dos grupos, de -1 a 1; maior favorece separação.'],['ARI de estabilidade','Concordância entre agrupamentos após reajuste; 1 indica igualdade.']])])
    regrows=[]
    for source,b in bases.items():
        for r in b['estatisticas'].itertuples():regrows.append([FONTES[source],_nome(r.nicho_id),int(r.n),numero(r.mape)+'%',numero(r.mape_persistencia)+'%',numero(r.mdape)+'%'])
    add('3. Regressão: previsões comparadas ao último preço',[
        'O gráfico compara o erro médio percentual da regressão selecionada na validação com a previsão simples do último preço. n conta previsões serviço-competência. Cada observação tem o mesmo peso; estes números não medem economia financeira de uma obra.',
        'Recortes nativos sem amostra suficiente permanecem explicitamente fora da regressão; o resultado parcial do DER não foi preenchido com estimativas inventadas. A cobertura por serviço está na tabela de populações e os motivos constam em regressao/resumo.json.',
        'Erros pequenos podem coexistir com desempenho inferior ao último preço. A mediana descreve o erro típico e reduz a influência de casos extremos. MAE, RMSE e MSE por grupo nativo estão preservados nos arquivos técnicos. O limite de 5% usado em análises auxiliares é didático, sem caráter de tolerância oficial [4].'
    ],images=[graphs['regressao']])
    add('Regressão | interpretação das estatísticas',[
        'A tabela reúne os mesmos valores do gráfico e acrescenta a mediana. MAPE = média de 100 × |previsto - publicado| / publicado. A referência último preço é calculada nas mesmas observações, permitindo uma comparação pareada.',
        'Exemplo de interpretação: um erro de 1,32% significa que a distância percentual absoluta entre estimativa e custo publicado foi, em média, 1,32%. Não significa probabilidade de acerto, aumento do preço, economia contratual nem precisão garantida para um serviço novo.',
        'A mediana divide as observações em duas metades: metade dos erros é menor ou igual a ela. Quando a média supera muito a mediana, alguns erros maiores estão influenciando a média. Os CSVs estatisticas_nichos.csv e estatisticas_recortes.csv conservam P90, dispersão e indicadores complementares.',
        'Comparação do MAPE por fonte: '+ '; '.join(FONTES[f]+': regressão superior ao último preço em '+str(int((b['estatisticas'].mape < b['estatisticas'].mape_persistencia).sum()))+' de 3 nichos' for f,b in bases.items())+'. Os resultados sustentam manter a referência simples na avaliação e estudar novos atributos e horizontes em experimentos futuros.'
    ],tables=[_tabela(['Fonte','Nicho','n','MAPE modelo','Último preço','Mediana'],regrows)])
    for source,b in bases.items():
        s=b['resumo'];e=b['exemplo'];p=b['pares'].loc[b['pares'].codigo.eq(e['codigo'])].sort_values('competencia_alvo');pred=e['classe_prevista']; cl=s['agrupamento'];diag=cl.get('diagnostico',False)
        class_text=f"No teste de classificação, a classe prevista foi {_nome(pred)}." if pred else f"Este serviço pertence ao {e['particao']} da classificação; nenhuma previsão de teste foi inventada para ele."
        add('4. Pintura em detalhe | '+FONTES[source],[
            f"Exemplo {e['codigo']}: {e['descricao']}",
            'O código foi escolhido para continuidade com a apresentação de regressão, sem selecionar pelo acerto. Os exemplos de SINAPI e DER ilustram seus próprios catálogos e não foram homologados como serviços tecnicamente equivalentes.',
            class_text+f" No agrupamento, aparece no grupo {e['cluster']}"+(' do diagnóstico, sem candidato aceito.' if diag else ' do K-Means selecionado.')
        ],tables=[_tabela(['Competência','Publicado R$/m²','Regressão R$/m²','Último R$/m²','Erro modelo %'],[[r.competencia_alvo,numero(r.custo_observado),numero(r.custo_previsto),numero(r.previsto_persistencia),numero(r.ape)] for r in p.itertuples()])],images=[graphs['pintura_'+source]])
    add('5. Classificação: seleção independente do teste',[
        'As barras azuis mostram a média de F1 macro na validação para o melhor candidato de cada algoritmo; os traços representam o desvio entre três folds, não um intervalo de confiança. As barras laranja mostram o teste reservado. A classe majoritária é a referência e não participou da seleção.',
        'Um algoritmo pode obter resultado maior no teste e ainda assim não ser o selecionado. A escolha continua baseada na validação, evitando selecionar retrospectivamente o modelo que mais acertou o teste. F1 macro tem escala de 0 a 1 e não deve ser apresentado como porcentagem de serviços corretamente classificados.'
    ],images=[graphs['classificacao']])
    for source,b in bases.items():
        cls=b['resumo']['classificacao'];sel=cls['algoritmo_selecionado'];p=b['previsoes_class'].loc[b['previsoes_class'].algoritmo.eq(sel)];m=b['metricas_class'].set_index('algoritmo').loc[sel];rows=[]
        for c in CLASSES:
            real=p.classe.eq(c);pred=p.classe_prevista.eq(c);tp=(real&pred).sum();precision=tp/pred.sum() if pred.sum() else 0;recall=tp/real.sum() if real.sum() else 0
            rows.append([_nome(c),int(real.sum()),numero(precision,3),numero(recall,3),numero(2*precision*recall/(precision+recall),3) if precision+recall else '0,000'])
        add('6. Matriz de confusão | '+FONTES[source],[
            f"Modelo selecionado: {ALGORITMOS[sel]}. Treino: {cls['n_treino']} serviços em {cls['n_grupos_treino']} grupos de variantes. Teste: {cls['n_teste']} serviços em {cls['n_grupos_teste']} grupos. F1 macro = {numero(m.f1_macro,3)}; acurácia balanceada = {numero(m.acuracia_balanceada,3)}; acurácia = {numero(m.acuracia*100,1)}%.",
            'Leia cada linha como a classe real. A diagonal contém acertos; as outras células mostram para qual classe os serviços foram confundidos. O percentual dentro de cada célula usa o total da própria linha. Precisão pergunta se as sugestões da classe acertaram; recall pergunta quantos serviços reais da classe foram reconhecidos.'
        ],tables=[_tabela(['Classe','n teste','Precisão','Recall','F1'],rows)],images=[graphs['confusao_'+source]])
    for source,b in bases.items():
        cl=b['resumo']['agrupamento'];diag=cl.get('diagnostico',False);k=cl.get('k_diagnostico') if diag else cl['k_selecionado'];m=cl.get('metricas_diagnostico') if diag else cl['metricas'];text=f"Nenhum k foi aceito. O menor k calculável, {k}, é apresentado apenas como diagnóstico. O critério mínimo era {cl['min_servicos_cluster']} serviços no menor grupo; esse critério não foi alterado após observar os dados." if diag else f"Foi selecionado k={k}, com silhouette {numero(m['silhouette'],3)}, entre os candidatos elegíveis. Cada grupo precisava de ao menos {cl['min_servicos_cluster']} serviços."
        st=cl['estabilidade']; stability=[]
        for key,label in [('semente','Outras sementes'),('subamostra_80pct','80% dos serviços'),('subamostra_grupos_80pct','80% dos grupos de variantes')]:
            if key in st:stability.append([label,numero(st[key]['ari_medio'],3),numero(st[key].get('ari_minimo',st[key]['ari_medio']),3)])
        add('7. Agrupamento | '+FONTES[source],[text,'Silhouette maior só torna um candidato preferível quando os demais critérios também são atendidos. Davies-Bouldin favorece valores menores; Calinski-Harabasz favorece valores maiores dentro deste mesmo conjunto. A estabilidade por grupos de variantes é a verificação mais conservadora quando variantes semelhantes estão presentes.',
            'A média e o mínimo do ARI são apresentados juntos: uma mediana elevada pode esconder uma reamostragem instável. A estabilidade descreve reajustes no catálogo; não mede desempenho preditivo em uma obra nova.'
        ],tables=[_tabela(['k','Elegível','Silhouette','Davies-Bouldin','Calinski-H.'],[[int(r.k),'sim' if r.elegivel else 'não',numero(r.silhouette,3),numero(r.davies_bouldin,3),numero(r.calinski_harabasz,1)] for r in b['candidatos'].itertuples()]),_tabela(['Reajuste','ARI médio','ARI mínimo'],stability)],images=[graphs['selecao_k_'+source]])
        add('8. Perfis de recursos | '+FONTES[source],[
            f"A projeção PCA mostra {numero(cl['pca_variancia_explicada_total']*100,1)}% da variância em duas dimensões. O K-Means calcula distâncias nos dez atributos padronizados, não apenas neste desenho. {'Todos os perfis abaixo são diagnósticos; nenhum agrupamento foi aceito.' if diag else 'Os números dos grupos são identificadores arbitrários, sem correspondência automática com os grupos da outra base.'}",
            'As barras mostram a média das participações aproximadas de recursos de cada grupo. Horas de equipamento iguais a zero significam ausência de folhas mensuradas em H, não ausência de equipamento: aquisições podem estar representadas em outras unidades.'
        ],images=[graphs['pca_'+source],graphs['perfis_'+source]])
    conclusions=[]
    for source,b in bases.items():
        s=b['resumo'];cl=s['agrupamento'];stat=b['estatisticas'];ma=b['metricas_class'].set_index('algoritmo');selected=s['classificacao']['algoritmo_selecionado'];conclusions.append(f"{FONTES[source]}: o classificador selecionado obteve F1 macro {numero(ma.loc[selected,'f1_macro'],3)}, frente a {numero(ma.loc['dummy_maioria','f1_macro'],3)} da classe majoritária. {'O agrupamento possui candidato elegível, sujeito à revisão dos perfis.' if cl.get('k_selecionado') else 'O agrupamento não passou pelos critérios; revisar atributos e tratamento dos poucos perfis raros é uma evolução futura, que exige novo experimento.'}")
    add('9. Consolidação, discussão e conclusão',[
        *conclusions,
        'A contribuição ao ORCA-AI é oferecer três recursos complementares: cenários de custo com referência simples, sugestão de classe para composições estruturadas e exploração de perfis. Um agrupamento não comprova substituição técnica de serviços; uma sugestão de classe exige conferência antes do uso profissional.',
        'Limitações: catálogo pequeno no DER, classes derivadas e não homologadas, dependência residual entre variantes, história revisada, participação de preços SP no SINAPI e diferentes convenções de encargos. A comparação é descritiva em cada fonte. Não foram estimados intervalos de confiança tratando observações dependentes como independentes.',
        'As três tarefas do enunciado foram executadas e seus resultados preservados, incluindo resultados desfavoráveis. Aprendizado por reforço permanece fora do escopo. A continuidade recomendada é revisar os rótulos e os perfis raros, testar em novas composições e ampliar a avaliação temporal sem reutilizar este teste para decisões de ajuste.'
    ],tables=[_tabela(['Aspecto','Regressão','Classificação','Agrupamento'],[['Unidade','Serviço-mês','Serviço de maio','Serviço de maio'],['Supervisão','Custo conhecido como alvo','Nicho como rótulo','Sem rótulo no ajuste'],['Modelo','Linear simples/múltipla','RF, árvore e KNN','K-Means'],['Referência','Último preço','Classe majoritária','Critério de tamanho e estabilidade'],['Indicador','MAPE, MAE, RMSE, MSE','F1 macro e matriz de erros','Silhouette, DB, CH e ARI'],['Decisão apoiada','Planejamento do próximo custo','Conferência da família técnica','Exploração de perfis semelhantes']])])
    provenance=[]
    for source,b in bases.items():
        s=b['resumo'];provenance.append(f"{FONTES[source]}: ZIP SHA-256 {s['zip_sha256']}. Serviços com preço SP: {s['n_servicos_preco_sp']}. Diferença máxima entre soma das folhas sem truncamento e custo publicado: {numero(s['max_diferenca_folhas_pct'],4)}%.")
    add('10. Reprodução e referências',[
        'No VS Code, abra a pasta OrcaAI/ml, selecione o Python de .venv e execute executar_estudo.py. Para recriar somente a apresentação, utilize gerar_relatorio_estudo.py com a pasta da execução concluída. O relatório não treina modelos. Cada nova execução usa uma pasta nova para preservar resultados anteriores.',
        'Os CSVs de dados, previsões, partições, matrizes, centroides, projeções e métricas ficam nas pastas de cada fonte. execucao_estudo.json registra parâmetros e hashes do código; manifesto_relatorio.json registra os hashes dos arquivos efetivamente usados nesta apresentação. As sementes e versões de Python/scikit-learn estão nos resumos das tarefas.',
        *provenance,
        'Materiais da disciplina: OrcaAI/spec/ml_ufg/mapa_materiais_disciplina.md identifica as aulas e exemplos que fundamentaram a escolha de LinearRegression, Random Forest, árvore, KNN e K-Means. O código, os dados derivados e as tabelas de auditoria acompanham esta entrega.'
    ],links=[('[1] CAIXA - SINAPI: tabelas e documentação oficial','https://www.caixa.gov.br/poder-publico/modernizacao-gestao/sinapi/Paginas/default.aspx'),('[2] DER-ES - referencial de preços de edificações','https://der.es.gov.br/referencial-de-precos-edificacoes'),('[3] scikit-learn - divisão estratificada por grupos','https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html'),('[4] scikit-learn - métricas de avaliação','https://scikit-learn.org/stable/modules/model_evaluation.html'),('[5] scikit-learn - agrupamento e seus indicadores','https://scikit-learn.org/stable/modules/clustering.html')])
    return sections


def _pdf(path,sections):
    from matplotlib import font_manager
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
    regular=font_manager.findfont('DejaVu Sans');bold=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans',weight='bold'))
    pdfmetrics.registerFont(TTFont('OrcaSans',regular));pdfmetrics.registerFont(TTFont('OrcaSansBold',bold))
    styles={'title':ParagraphStyle('title',fontName='OrcaSansBold',fontSize=17,leading=21,textColor=colors.HexColor('#174B6C'),spaceAfter=13),'body':ParagraphStyle('body',fontName='OrcaSans',fontSize=10.2,leading=14.1,spaceAfter=8,splitLongWords=True),'cell':ParagraphStyle('cell',fontName='OrcaSans',fontSize=10.1,leading=13.1),'head':ParagraphStyle('head',fontName='OrcaSansBold',fontSize=10.1,leading=13.1,textColor=colors.white)}
    width=A4[0]-76; story=[]
    for index,s in enumerate(sections):
        if index:story.append(PageBreak())
        story.append(Paragraph(html.escape(s['titulo']),styles['title']))
        for p in s['paragrafos']:story.append(Paragraph(html.escape(p),styles['body']))
        for image in s['imagens']:
            from PIL import Image as PILImage
            with PILImage.open(image) as source:iw,ih=source.size
            story.append(Image(str(image),width=width,height=width*ih/iw));story.append(Spacer(1,8))
        for table in s['tabelas']:
            rows=[[Paragraph(html.escape(x),styles['head']) for x in table['cabecalho']]]+[[Paragraph(html.escape(x),styles['cell']) for x in row] for row in table['linhas']]
            t=Table(rows,colWidths=[width/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17618B')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F5F8'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,10)])
        for label,url in s['links']:story.append(Paragraph(f'<link href="{html.escape(url,quote=True)}" color="#17618B">{html.escape(label)}</link>',styles['body']))
    def footer(canvas,doc):
        canvas.setFont('OrcaSans',8.5);canvas.setFillColor(colors.HexColor('#536572'));canvas.drawString(38,23,'ORCA-AI | UFG | engenheiro Luis Fernando');canvas.drawRightString(A4[0]-38,23,str(doc.page));canvas.line(38,35,A4[0]-38,35)
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=35,bottomMargin=45,title='Aprendizado de máquina aplicado ao ORCA-AI',author='Engenheiro Luis Fernando')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


def gerar_relatorio_consolidado(execucao_dir:Path,run:dict,saida:Path|None=None)->dict:
    root=Path(execucao_dir).resolve();out=Path(saida).resolve() if saida is not None else root/'relatorio_consolidado'
    if out.exists() and (not out.is_dir() or any(out.iterdir())):raise ValueError(f'A pasta de relatório já contém arquivos: {out}')
    bases,hashes=_ler_bases(root,run)
    out.mkdir(parents=True,exist_ok=True)
    graphs=gerar_graficos_consolidacao(bases,out/'graficos');sections=_secoes(run,bases,graphs)
    paths={'html':out/'relatorio.html','pdf':out/'relatorio.pdf','markdown':out/'RELATORIO.md'}
    parts=['<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ORCA-AI | UFG | três tarefas de ML</title><style>body{font:17px/1.65 system-ui,sans-serif;color:#203746;background:#eef3f6;margin:0}main{max-width:980px;margin:auto;padding:24px}section{background:white;padding:32px;margin:24px 0;border-radius:12px}h1,h2{color:#174b6c;line-height:1.3}img{width:100%;height:auto}table{width:100%;border-collapse:collapse;margin:18px 0;font-size:15px}th{background:#17618b;color:white}td,th{padding:9px;border:1px solid #d7e1e6;text-align:left}tbody tr:nth-child(even){background:#f0f5f8}a{color:#17618b}.table{overflow:auto}nav{background:#fff;padding:18px;border-radius:12px}nav a{display:inline-block;margin-right:12px}@media print{section{break-before:page}nav{display:none}}</style><main><nav><a href="relatorio.pdf">PDF para entrega</a><a href="RELATORIO.md">Texto em Markdown</a>']
    parts.extend(f'<a href="#sec{i}">{html.escape(s["titulo"])}</a>' for i,s in enumerate(sections));parts.append('</nav>');md=[]
    for i,s in enumerate(sections):
        parts.append(f'<section id="sec{i}"><h2>{html.escape(s["titulo"])}</h2>');md.extend(['# '+s['titulo'],''])
        for p in s['paragrafos']:parts.append('<p>'+html.escape(p)+'</p>');md.extend([p,''])
        for image in s['imagens']:
            encoded=base64.b64encode(image.read_bytes()).decode();alt=s['titulo']+'; valores, unidades e amostras indicados na figura';parts.append(f'<img alt="{html.escape(alt)}" src="data:image/png;base64,{encoded}">');md.extend([f'![{alt}](graficos/{image.name})',''])
        for table in s['tabelas']:
            parts.append('<div class="table"><table><thead><tr>'+''.join('<th>'+html.escape(v)+'</th>' for v in table['cabecalho'])+'</tr></thead><tbody>')
            parts.extend('<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in row)+'</tr>' for row in table['linhas']);parts.append('</tbody></table></div>')
            md.extend(['| '+' | '.join(table['cabecalho'])+' |','| '+' | '.join(['---']*len(table['cabecalho']))+' |']);md.extend('| '+' | '.join(v.replace('|','/') for v in row)+' |' for row in table['linhas']);md.append('')
        for label,url in s['links']:parts.append(f'<p><a href="{html.escape(url,quote=True)}">{html.escape(label)}</a></p>');md.extend([f'[{label}]({url})',''])
        parts.append('</section>')
    parts.append('</main></html>');paths['html'].write_text('\n'.join(parts),encoding='utf-8');paths['markdown'].write_text('\n'.join(md),encoding='utf-8');_pdf(paths['pdf'],sections)
    manifest={'competencia':run['competencia'],'execucao_origem':str(root),'arquivos_entrada_sha256':hashes,'bases':{}}
    for source,b in bases.items():
        c=b['resumo']['classificacao'];a=b['resumo']['agrupamento'];row=b['metricas_class'].set_index('algoritmo').loc[c['algoritmo_selecionado']]
        manifest['bases'][source]={'n_catalogo':len(b['dados']),'n_previsoes_regressao':len(b['pares']),'classificador_selecionado':c['algoritmo_selecionado'],'f1_macro_selecionado':float(row.f1_macro),'k_selecionado':a.get('k_selecionado'),'k_diagnostico':a.get('k_diagnostico'),'status_agrupamento':a['status'],'codigo_exemplo_pintura':b['exemplo']['codigo']}
    manifest['arquivos_saida_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}
    (out/'manifesto_relatorio.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return paths
