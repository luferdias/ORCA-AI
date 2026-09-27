"""O documento só pode apresentar resultados completos e conciliados."""
import importlib
import json
from copy import deepcopy
from pathlib import Path

import pandas as pd
import pytest


def fixture_execucao(tmp_path):
    source = 'sinapi_es'; base = tmp_path / source
    for name in ('dados', 'regressao', 'classificacao', 'agrupamento'):
        (base / name).mkdir(parents=True)
    classes = ['pintura', 'pisos', 'revestimentos_forros']
    data = pd.DataFrame([dict(fonte=source,competencia='2026-05',codigo=str(i),classe=classes[i % 3],descricao=f'Serviço {i}',custo=10+i,grupo_particao=f'g{i}') for i in range(6)])
    data.to_csv(base / 'dados/dataset_acabamentos.csv',index=False)
    pd.DataFrame({'codigo':data.codigo,'no_catalogo_maio':True,'n_previsoes_regressao':3,'na_regressao_teste':True}).to_csv(base/'dados/populacoes_tarefas.csv',index=False)
    parts = data[['fonte','codigo','classe','grupo_particao']].copy(); parts['particao'] = ['teste']*3+['treino']*3
    parts.to_csv(base/'classificacao/particoes.csv',index=False)
    metrics=[]; predictions=[]; confusion=[]
    algos=['random_forest','arvore_decisao','knn','dummy_maioria']
    for algo in algos:
        is_dummy=algo=='dummy_maioria'
        metrics.append(dict(algoritmo=algo,selecionado_cv=algo=='random_forest',f1_macro=1/6 if is_dummy else 1.,acuracia=1/3 if is_dummy else 1.,acuracia_balanceada=1/3 if is_dummy else 1.,n=3))
        for i,cl in enumerate(classes):
            predictions.append(dict(fonte=source,codigo=str(i),classe=cl,classe_prevista='pintura' if is_dummy else cl,algoritmo=algo,selecionado_cv=algo=='random_forest'))
            for target in classes:
                confusion.append(dict(algoritmo=algo,classe_real=cl,classe_prevista=target,n=int(target==('pintura' if is_dummy else cl))))
    pd.DataFrame(metrics).to_csv(base/'classificacao/metricas_teste.csv',index=False)
    pd.DataFrame(predictions).to_csv(base/'classificacao/previsoes.csv',index=False)
    pd.DataFrame(confusion).to_csv(base/'classificacao/confusao.csv',index=False)
    cv = pd.DataFrame([dict(algoritmo=a,candidato=0,fold=i,f1_macro=v) for a,v in zip(algos[:3],[.8,.7,.6]) for i in range(3)])
    cv.to_csv(base/'classificacao/metricas_cv.csv',index=False)
    pairs=pd.DataFrame([dict(fonte=source,codigo=str(i),nicho_id=classes[i%3],competencia_alvo=month,custo_observado=10.,custo_previsto=10.1,previsto_persistencia=10.2,ape=1.,ape_persistencia=2.,modelo='linear_simples') for i in range(6) for month in ['2026-03','2026-04','2026-05']])
    pairs.to_csv(base/'regressao/previsoes_pareadas.csv',index=False)
    pd.DataFrame([dict(fonte=source,nicho_id=cl,n=6,n_servicos=2,mape=1.,mape_persistencia=2.,mdape=1.,p90=1.,dentro_5_pct=100.) for cl in classes]).to_csv(base/'regressao/estatisticas_nichos.csv',index=False)
    assign=data.copy(); assign['cluster']=[0,0,0,1,1,1];assign['pc1']=[-2,-1,0,1,2,3];assign['pc2']=[0,1,0,2,1,2];assign['distancia_centro']=1.
    assign.to_csv(base/'agrupamento/atribuicoes.csv',index=False)
    assign.to_csv(base/'agrupamento/coordenadas_pca.csv',index=False)
    centers=pd.DataFrame([dict(cluster=k,n=3,fracao_mao_obra=.5,fracao_material=.5,fracao_equipamento=0.,fracao_outros=0.,n_mao_obra=1.,n_material=1.,n_equipamento=0.,n_outros=0.,horas_mao_obra=.1,horas_equipamento=0.) for k in range(2)])
    centers.to_csv(base/'agrupamento/centroides.csv',index=False)
    cand=dict(k=2,elegivel=True,silhouette=.5,min_tamanho=3,inercia=2.,davies_bouldin=.6,calinski_harabasz=8.)
    pd.DataFrame([cand]).to_csv(base/'agrupamento/candidatos_k.csv',index=False)
    classification=dict(status='concluido',fonte=source,competencia='2026-05',n=6,n_treino=3,n_teste=3,n_grupos_treino=3,n_grupos_teste=3,algoritmo_selecionado='random_forest',metricas_teste=metrics,vencedores_cv={a:dict(candidato=0,f1_macro_media=v,parametros={}) for a,v in zip(algos[:3],[.8,.7,.6])})
    cluster=dict(status='concluido',fonte=source,competencia='2026-05',n=6,k_selecionado=2,diagnostico=False,metricas=cand,pca_variancia_explicada=[.5,.3],pca_variancia_explicada_total=.8,min_servicos_cluster=3,tamanhos_clusters={'0':3,'1':3},estabilidade={'semente':{'ari_medio':1.},'subamostra_80pct':{'ari_medio':.9}})
    reg=dict(status='concluido',fonte=source,regime='sem_desoneracao',competencias_teste=['2026-03','2026-04','2026-05'],competencias_validacao=['2026-01','2026-02'],recortes=[])
    summary=dict(fonte=source,competencia='2026-05',n_catalogo=6,n_validos=6,n_excluidos=0,n_grupos_variantes=6,classes={c:2 for c in classes},n_servicos_preco_sp=0,max_diferenca_folhas_pct=0.,dataset_sha256='a'*64,zip_sha256='b'*64,arquivo_zip='fixture.zip',atributos=[*['fracao_'+x for x in ['mao_obra','material','equipamento','outros']],*['n_'+x for x in ['mao_obra','material','equipamento','outros']],'horas_mao_obra','horas_equipamento'],classificacao=classification,agrupamento=cluster,regressao=reg,populacoes={'catalogo_e_regressao':6,'somente_catalogo':0,'somente_regressao':0})
    return {'status':'em_execucao','etapa':'todas','competencia':'2026-05','executado_em_utc':'2026-09-27T12:00:00+00:00','bases':{source:summary}}


def gerar(path,run):
    return importlib.import_module('orca_ml.relatorio_consolidado').gerar_relatorio_consolidado(path,run)


def test_gera_tres_formatos_offline_sem_alterar_dados(tmp_path):
    run=fixture_execucao(tmp_path); before=(tmp_path/'sinapi_es/regressao/previsoes_pareadas.csv').read_bytes()
    paths=gerar(tmp_path,run)
    assert set(paths)=={'html','pdf','markdown'}
    assert all(Path(p).is_file() for p in paths.values())
    assert paths['pdf'].read_bytes().startswith(b'%PDF-')
    assert 'data:image/png;base64,' in paths['html'].read_text()
    assert (tmp_path/'sinapi_es/regressao/previsoes_pareadas.csv').read_bytes()==before
    audit=json.loads((paths['html'].parent/'manifesto_relatorio.json').read_text())
    assert audit['bases']['sinapi_es']['n_previsoes_regressao']==18
    assert audit['bases']['sinapi_es']['f1_macro_selecionado']==1.


def test_saida_anterior_e_preservada(tmp_path):
    run=fixture_execucao(tmp_path); folder=tmp_path/'relatorio_consolidado';folder.mkdir();old=folder/'original';old.write_text('guardar')
    with pytest.raises(ValueError,match='contém'):
        gerar(tmp_path,run)
    assert old.read_text()=='guardar'


@pytest.mark.parametrize('mutation', ['incompleta','fonte','competencia','metrica'])
def test_rejeita_execucao_inconsistente_antes_de_escrever(tmp_path,mutation):
    run=fixture_execucao(tmp_path)
    if mutation=='incompleta':del run['bases']['sinapi_es']['agrupamento']
    elif mutation=='fonte':run['bases']['sinapi_es']['classificacao']['fonte']='der_es'
    elif mutation=='competencia':run['bases']['sinapi_es']['competencia']='2026-04'
    else:
        p=tmp_path/'sinapi_es/regressao/estatisticas_nichos.csv';df=pd.read_csv(p);df.loc[0,'mape']=99.;df.to_csv(p,index=False)
    with pytest.raises(ValueError):gerar(tmp_path,run)
    assert not (tmp_path/'relatorio_consolidado').exists()


def test_diagnostico_sem_k_aceito_nao_e_convertido_em_selecao(tmp_path):
    run=fixture_execucao(tmp_path); cluster=run['bases']['sinapi_es']['agrupamento'];cluster.update(status='sem_candidato_valido',k_diagnostico=2,k_selecionado=None,diagnostico=True,metricas_diagnostico=cluster['metricas'],metricas=None,min_servicos_cluster=4)
    p=tmp_path/'sinapi_es/agrupamento/candidatos_k.csv';d=pd.read_csv(p);d['elegivel']=False;d.to_csv(p,index=False)
    paths=gerar(tmp_path,run); audit=json.loads((paths['html'].parent/'manifesto_relatorio.json').read_text())
    assert audit['bases']['sinapi_es']['k_selecionado'] is None
    assert audit['bases']['sinapi_es']['k_diagnostico']==2


def test_regressao_parcial_com_recortes_insuficientes_ainda_tem_resultado_valido(tmp_path):
    run=fixture_execucao(tmp_path)
    run['bases']['sinapi_es']['regressao']['status']='parcial'
    run['bases']['sinapi_es']['regressao']['recortes']=[{'grupo':'grupo pequeno','status':'dados_insuficientes'}]
    mod=importlib.import_module('orca_ml.relatorio_consolidado')
    bases,_=mod._ler_bases(tmp_path,run)
    assert len(bases['sinapi_es']['pares'])==18
