"""Gráficos da consolidação: valores e denominadores dentro da figura."""
from pathlib import Path
from textwrap import fill
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FONTES={'sinapi_es':'SINAPI-ES','der_es':'DER-ES / IOPES'}
CLASSES=['pintura','pisos','revestimentos_forros']
NOMES={'pintura':'Pintura','pisos':'Pisos','revestimentos_forros':'Revestimentos\ne forros'}
ALGORITMOS={'random_forest':'Random Forest','arvore_decisao':'Árvore de decisão','knn':'KNN','dummy_maioria':'Classe majoritária'}
AZUL='#17618B'; LARANJA='#D87821'; CORES=[AZUL,LARANJA,'#62519B','#4C7D65','#666666']


def numero(value, casas=2):
    return f'{float(value):.{casas}f}'.replace('.',',')


def _figura(title,subtitle,height=4.2):
    fig=plt.figure(figsize=(7.2,height),layout='constrained')
    fig.suptitle(fill(title,68)+'\n'+fill(subtitle,72),fontsize=13,fontweight='bold')
    return fig


def _save(fig,path):
    fig.savefig(path.with_suffix('.png'),dpi=170,facecolor='white',bbox_inches='tight')
    fig.savefig(path.with_suffix('.svg'),facecolor='white',bbox_inches='tight')
    plt.close(fig)
    return path.with_suffix('.png')


def gerar_graficos_consolidacao(bases,saida):
    saida=Path(saida);saida.mkdir(parents=True,exist_ok=True);out={}
    with plt.rc_context({'font.size':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':11,'legend.fontsize':10,'axes.spines.top':False,'axes.spines.right':False,'text.parse_math':False}):
        fig=_figura('Três nichos, catálogos de tamanhos diferentes','Serviços únicos em m² | maio/2026',4.0); ax=fig.subplots()
        y=np.arange(3); width=.34
        for i,(fonte,b) in enumerate(bases.items()):
            vals=[int(b['dados'].classe.eq(c).sum()) for c in CLASSES]
            bars=ax.barh(y+(i-(len(bases)-1)/2)*width,vals,height=width,label=f'{FONTES[fonte]} (n={len(b["dados"])})',color=CORES[i],hatch='' if i==0 else '//')
            ax.bar_label(bars,padding=3,fontsize=11)
        ax.set_yticks(y,[NOMES[c] for c in CLASSES]);ax.invert_yaxis();ax.set_xlabel('Número de serviços');ax.set_xlim(0,max(len(b['dados']) for b in bases.values())*.85+5);ax.legend(loc='lower right');ax.grid(axis='x',alpha=.15)
        out['cobertura']=_save(fig,saida/'cobertura')

        fig=_figura('Quanto a regressão errou em cada nicho?','MAPE no teste de março a maio/2026 | menor é melhor',3.5*len(bases)); axes=np.atleast_1d(fig.subplots(len(bases),1))
        maxval=max(b['estatisticas'][['mape','mape_persistencia']].max().max() for b in bases.values())
        for ax,(fonte,b) in zip(axes,bases.items()):
            d=b['estatisticas'].set_index('nicho_id').reindex(CLASSES);y=np.arange(3)
            for dy,col,color,lab,hatch in [(-.18,'mape',AZUL,'Regressão',''),(.18,'mape_persistencia',LARANJA,'Último preço','//')]:
                bars=ax.barh(y+dy,d[col],height=.34,color=color,label=lab,hatch=hatch)
                ax.bar_label(bars,labels=[numero(x)+'%' for x in d[col]],padding=3,fontsize=10)
            ax.set_yticks(y,[NOMES[c]+f' (n={int(d.loc[c,"n"])})' for c in CLASSES]);ax.invert_yaxis();ax.set_title(FONTES[fonte],fontsize=12);ax.set_xlabel('Erro percentual absoluto médio (%)');ax.set_xlim(0,maxval*1.35+.1);ax.legend(loc='lower right');ax.grid(axis='x',alpha=.15)
        out['regressao']=_save(fig,saida/'regressao')

        fig=_figura('Classificação: validação escolhe, teste avalia','F1 macro (0 a 1) | maior é melhor | * selecionado na validação',3.7*len(bases));axes=np.atleast_1d(fig.subplots(len(bases),1))
        algos=list(ALGORITMOS)
        for ax,(fonte,b) in zip(axes,bases.items()):
            test=b['metricas_class'].set_index('algoritmo'); summ=b['resumo']['classificacao'];winner=summ['algoritmo_selecionado']; y=np.arange(4)
            cv=[summ['vencedores_cv'].get(a,{}).get('f1_macro_media',np.nan) for a in algos]
            std=[]
            for a in algos:
                cand=summ['vencedores_cv'].get(a,{}).get('candidato',-1)
                sub=b['cv'].loc[b['cv'].algoritmo.eq(a)&b['cv'].candidato.eq(cand),'f1_macro'];std.append(float(sub.std()) if len(sub)>1 else 0.)
            for dy,vals,label,color,hatch in [(-.18,cv,'Validação: média de 3 folds',AZUL,''),(.18,[test.loc[a,'f1_macro'] for a in algos],'Teste reservado',LARANJA,'//')]:
                bars=ax.barh(y+dy,vals,height=.32,label=label,color=color,hatch=hatch)
                ax.bar_label(bars,labels=[numero(v,3) if np.isfinite(v) else '' for v in vals],padding=3,fontsize=10)
            ax.errorbar(cv,y-.18,xerr=std,fmt='none',ecolor='#222222',capsize=3)
            ax.set_yticks(y,[ALGORITMOS[a]+(' *' if a==winner else '') for a in algos]);ax.invert_yaxis();ax.set_xlim(0,1.15);ax.set_title(FONTES[fonte]+f' | teste: {summ["n_teste"]} serviços',fontsize=12);ax.set_xlabel('F1 macro; barras finas = desvio entre folds');ax.legend(loc='lower right',fontsize=10)
        out['classificacao']=_save(fig,saida/'classificacao')

        for fonte,b in bases.items():
            summary=b['resumo']; display=FONTES[fonte]; cluster=summary['agrupamento'];diag=cluster.get('diagnostico',False); kind='diagnóstico, sem k aceito' if diag else 'agrupamento selecionado'; k=cluster.get('k_diagnostico') if diag else cluster['k_selecionado']
            example=b['exemplo']; paint=b['pares'].loc[b['pares'].codigo.eq(example['codigo'])].sort_values('competencia_alvo')
            fig=_figura(display+' | um serviço de pintura',f'Código {example["codigo"]} | {len(paint)} previsões de teste | R$/m²',4.8);ax,table_ax=fig.subplots(2,1,gridspec_kw={'height_ratios':[3,1]});x=np.arange(len(paint))
            for column,label,color,marker,style in [('custo_observado','Publicado',AZUL,'o','-'),('custo_previsto','Regressão',LARANJA,'s','--'),('previsto_persistencia','Último preço','#666666','^',':')]:
                vals=paint[column].to_numpy();ax.plot(x,vals,label=label,color=color,marker=marker,linestyle=style,linewidth=2)
            ax.set_xticks(x,[v[5:7]+'/'+v[:4] for v in paint.competencia_alvo]);ax.set_ylabel('Custo referencial (R$/m²)');ax.set_xlabel('Competência prevista');ax.grid(alpha=.2);ax.legend(loc='best');ax.margins(x=.15,y=.25)
            table_ax.axis('off')
            table=table_ax.table(cellText=[[r.competencia_alvo,numero(r.custo_observado),numero(r.custo_previsto),numero(r.previsto_persistencia)] for r in paint.itertuples()],colLabels=['Competência','Publicado','Regressão','Último preço'],loc='center',cellLoc='center');table.auto_set_font_size(False);table.set_fontsize(10);table.scale(1,1.2)
            out['pintura_'+fonte]=_save(fig,saida/('pintura_'+fonte))

            selected=summary['classificacao']['algoritmo_selecionado'];conf=b['confusao'].loc[b['confusao'].algoritmo.eq(selected)].pivot(index='classe_real',columns='classe_prevista',values='n').reindex(index=CLASSES,columns=CLASSES)
            fig=_figura(display+' | onde a classificação acertou?',ALGORITMOS[selected]+f' | {int(conf.to_numpy().sum())} serviços de teste',4.9);ax=fig.subplots();matrix=conf.to_numpy();im=ax.imshow(matrix,cmap='Blues',vmin=0)
            for i in range(3):
                for j in range(3):
                    n=int(matrix[i,j]);p=n/matrix[i].sum()*100 if matrix[i].sum() else 0;ax.text(j,i,f'{n}\n({numero(p,1)}%)',ha='center',va='center',color='white' if n>matrix.max()*.55 else '#182A35',fontsize=12)
            ax.set_xticks(range(3),[NOMES[c] for c in CLASSES]);ax.set_yticks(range(3),[NOMES[c] for c in CLASSES]);ax.set_xlabel('Classe prevista');ax.set_ylabel('Classe real');fig.colorbar(im,ax=ax,shrink=.8,label='Número de serviços')
            out['confusao_'+fonte]=_save(fig,saida/('confusao_'+fonte))

            candidates=b['candidatos'];fig=_figura(display+' | seleção do número de grupos',kind+f' | n={len(b["dados"])} serviços',3.8);axes=fig.subplots(2,1,sharex=True)
            axes[0].plot(candidates.k,candidates.silhouette,'o-',color=AZUL)
            for r in candidates.itertuples():
                if np.isfinite(r.silhouette):axes[0].annotate(numero(r.silhouette,3),(r.k,r.silhouette),xytext=(0,9),textcoords='offset points',ha='center',fontsize=10)
            axes[0].set_ylabel('Silhouette');axes[0].set_ylim(min(0,candidates.silhouette.min()-.1),min(1,candidates.silhouette.max()+.2));axes[0].grid(alpha=.2)
            bars=axes[1].bar(candidates.k,candidates.min_tamanho,color=LARANJA);axes[1].bar_label(bars,padding=3);limit=cluster['min_servicos_cluster'];axes[1].axhline(limit,color=AZUL,linestyle='--',label=f'Mínimo exigido: {limit}')
            axes[1].set_xticks(candidates.k);axes[1].set_xlabel('Número de grupos (k)');axes[1].set_ylabel('Menor grupo (serviços)');axes[1].set_ylim(0,max(limit,candidates.min_tamanho.max())*1.4+1);axes[1].legend(loc='upper right')
            out['selecao_k_'+fonte]=_save(fig,saida/('selecao_k_'+fonte))

            fig=_figura(display+' | mapa dos perfis de recursos',kind+f' | k={k}; cada ponto = um serviço',4.1);ax=fig.subplots(); coords=b['pca']; markers=['o','s','^','D','P']
            for label,frame in coords.groupby('cluster'):
                ax.scatter(frame.pc1,frame.pc2,label=f'Grupo {label} (n={len(frame)})',color=CORES[int(label)],marker=markers[int(label)],s=28,alpha=.65,edgecolors='white',linewidths=.3)
            var=cluster['pca_variancia_explicada'];ax.set_xlabel(f'Componente 1 ({numero(100*var[0],1)}% da variância)');ax.set_ylabel(f'Componente 2 ({numero(100*var[1],1)}%)');ax.legend(fontsize=10,loc='best');ax.grid(alpha=.15)
            out['pca_'+fonte]=_save(fig,saida/('pca_'+fonte))

            centers=b['centros'];fig=_figura(display+' | perfil médio de cada grupo','Custo dos recursos (%) | '+kind,3.1);ax=fig.subplots();left=np.zeros(len(centers)); names=['Mão de obra e encargos','Material','Equipamento','Outros']
            for i,col in enumerate(['fracao_mao_obra','fracao_material','fracao_equipamento','fracao_outros']):
                vals=np.clip(centers[col].to_numpy()*100,0,100);bars=ax.barh(np.arange(len(centers)),vals,left=left,color=CORES[i],label=names[i],hatch=['','//','xx','..'][i])
                for j,val in enumerate(vals):
                    if val>=6:ax.text(left[j]+val/2,j,numero(val,1)+'%',ha='center',va='center',color='white',fontsize=10)
                left+=vals
            ax.set_yticks(range(len(centers)),[f'Grupo {int(r.cluster)} (n={int(r.n)})' for r in centers.itertuples()]);ax.set_xlim(0,100);ax.set_xlabel('Participação média (%)');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.28),ncol=2,fontsize=10)
            out['perfis_'+fonte]=_save(fig,saida/('perfis_'+fonte))
    return out
