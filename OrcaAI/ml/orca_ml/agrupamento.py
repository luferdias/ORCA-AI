"""KMeans exploratório: rótulos técnicos não entram no ajuste nem na seleção.

Cada fonte recebe sua própria escala. Métricas descrevem aquele catálogo;
não constituem ranking de qualidade entre tabelas oficiais.
"""
from __future__ import annotations

import math
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score,
                             davies_bouldin_score, silhouette_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .classificacao import _preparar_saida, _proveniencia, _salvar_json, _validar_dataset


def _modelo(k: int, seed: int) -> Pipeline:
    return Pipeline([("escala", StandardScaler()),
                     ("modelo", KMeans(n_clusters=k, n_init=30, random_state=seed, algorithm="lloyd"))])


def executar_agrupamento(dataset: pd.DataFrame, atributos: list[str], saida: Path) -> dict:
    """Agrupe um catálogo, selecione k pela silhouette e meça estabilidade.

    A comparação entre sementes usa o catálogo inteiro. A análise por
    subamostras reajusta escala e centros em 80% sem reposição, por linhas
    e por grupos inteiros de variantes, e compara as atribuições dos mesmos
    serviços do catálogo. Não é teste preditivo.

    Se nenhum k atende aos critérios predefinidos, o menor k calculável
    é exportado exclusivamente como diagnóstico. O resultado continua
    sem candidato válido e nenhum modelo aceito é salvo nesse caso.
    """
    data = _validar_dataset(dataset, atributos, supervisionado=False)
    if len(data) < 6 or len(atributos) < 2:
        raise ValueError("Amostra insuficiente: use ao menos seis serviços e dois atributos para agrupamento/PCA")
    x = data[atributos]
    n_unique = int(x.drop_duplicates().shape[0])
    if n_unique < 2:
        raise ValueError("Dados constantes: menos de dois perfis distintos")
    out = _preparar_saida(saida)
    min_cluster = max(3, math.ceil(len(data) * .05))
    rows, fitted = [], {}
    for k in range(2, 6):
        row = {"k": k, "elegivel": False, "motivo": "", "silhouette": None,
               "davies_bouldin": None, "calinski_harabasz": None, "inercia": None,
               "min_tamanho": None, "tamanhos": ""}
        if k > n_unique or k >= len(data):
            row["motivo"] = "Quantidade insuficiente de perfis distintos"
            rows.append(row)
            continue
        model = _modelo(k, 42).fit(x)
        z = model.named_steps["escala"].transform(x)
        labels = model.named_steps["modelo"].labels_
        sizes = np.bincount(labels, minlength=k)
        row.update({"inercia": float(model.named_steps["modelo"].inertia_),
                    "min_tamanho": int(sizes.min()), "tamanhos": ";".join(map(str, sizes))})
        if len(np.unique(labels)) != k:
            row["motivo"] = "Centros coincidentes; menos grupos observados que k"
        else:
            row.update({"silhouette": float(silhouette_score(z, labels)),
                        "davies_bouldin": float(davies_bouldin_score(z, labels)),
                        "calinski_harabasz": float(calinski_harabasz_score(z, labels))})
            finite = all(np.isfinite(row[c]) for c in ["silhouette", "davies_bouldin", "calinski_harabasz"])
            row["elegivel"] = bool(sizes.min() >= min_cluster and finite)
            row["motivo"] = "elegível" if row["elegivel"] else f"Grupo menor que {min_cluster} serviços ou métrica indefinida"
        rows.append(row)
        fitted[k] = model
    candidates = pd.DataFrame(rows)
    candidates.to_csv(out / "candidatos_k.csv", index=False, encoding="utf-8-sig")
    valid = [r for r in rows if r["elegivel"]]
    diagnostic = not bool(valid)
    if diagnostic:
        calculable = [r for r in rows if r["k"] in fitted and all(
            r[c] is not None and np.isfinite(r[c]) for c in ["silhouette", "davies_bouldin", "calinski_harabasz"])]
        if not calculable:
            raise ValueError("Nenhum k calculável para diagnóstico: confira a variação dos atributos e candidatos_k.csv")
        # Regra predefinida: menor k calculável, sem selecionar diagnóstico pelo desempenho.
        chosen = min(calculable, key=lambda r: r["k"])
    else:
        chosen = max(valid, key=lambda r: (r["silhouette"], -r["k"]))
    k = chosen["k"]
    model = fitted[k]
    labels = model.named_steps["modelo"].labels_
    z = model.named_steps["escala"].transform(x)
    distances = model.named_steps["modelo"].transform(z)[np.arange(len(data)), labels]
    metadata = [c for c in ["fonte", "competencia", "codigo", "descricao", "classe", "grupo_particao"] if c in data]
    # A classe, quando presente, só é copiada para interpretação após os ajustes.
    assignments = data[metadata].copy()
    assignments["cluster"], assignments["distancia_centro"] = labels, distances
    assignments["diagnostico"] = diagnostic
    assignments.to_csv(out / "atribuicoes.csv", index=False, encoding="utf-8-sig")
    original_centers = model.named_steps["escala"].inverse_transform(model.named_steps["modelo"].cluster_centers_)
    centers = pd.DataFrame(original_centers, columns=atributos)
    centers.insert(0, "n", np.bincount(labels, minlength=k))
    centers.insert(0, "cluster", range(k))
    centers["diagnostico"] = diagnostic
    centers.to_csv(out / "centroides.csv", index=False, encoding="utf-8-sig")
    nearest = assignments.loc[assignments.groupby("cluster").distancia_centro.idxmin()].sort_values("cluster")
    nearest.to_csv(out / "representantes.csv", index=False, encoding="utf-8-sig")
    pca = PCA(n_components=2, svd_solver="full")
    projection = pca.fit_transform(z)
    coords = assignments[metadata + ["cluster"]].copy()
    coords["pc1"], coords["pc2"] = projection[:, 0], projection[:, 1]
    coords["diagnostico"] = diagnostic
    coords.to_csv(out / "coordenadas_pca.csv", index=False, encoding="utf-8-sig")
    loadings = pd.DataFrame(pca.components_.T, columns=["pc1", "pc2"])
    loadings.insert(0, "atributo", atributos)
    loadings.to_csv(out / "cargas_pca.csv", index=False, encoding="utf-8-sig")
    stability, samples = [], []
    for seed in [7, 21, 84]:
        alternative = _modelo(k, seed).fit(x)
        stability.append({"tipo": "semente", "semente": seed, "n_ajuste": len(data),
                          "n_grupos_ajuste": int(data.grupo_particao.nunique()),
                          "ari": float(adjusted_rand_score(labels, alternative.predict(x))), "status": "calculado"})
    sample_size = math.floor(.8 * len(data))
    for seed in range(100, 120):
        positions = np.sort(np.random.default_rng(seed).choice(len(data), size=sample_size, replace=False))
        subset = x.iloc[positions]
        samples.extend({"tipo": "subamostra_80pct", "semente": seed, "codigo": str(record.codigo),
                        "grupo_particao": str(record.grupo_particao), "diagnostico": diagnostic}
                       for record in data.iloc[positions].itertuples())
        row = {"tipo": "subamostra_80pct", "semente": seed, "n_ajuste": len(subset), "ari": None,
               "n_grupos_ajuste": int(data.iloc[positions].grupo_particao.nunique()),
               "status": "perfis_distintos_insuficientes"}
        if subset.drop_duplicates().shape[0] >= k:
            alternative = _modelo(k, seed).fit(subset)
            row.update({"ari": float(adjusted_rand_score(labels, alternative.predict(x))), "status": "calculado"})
        stability.append(row)
    variant_groups = np.array(sorted(data.grupo_particao.unique()), dtype=object)
    n_sample_groups = math.floor(.8 * len(variant_groups))
    for seed in range(200, 220):
        chosen_groups = np.random.default_rng(seed).choice(variant_groups, size=n_sample_groups, replace=False)
        positions = np.flatnonzero(data.grupo_particao.isin(chosen_groups))
        subset = x.iloc[positions]
        samples.extend({"tipo": "subamostra_grupos_80pct", "semente": seed, "codigo": str(record.codigo),
                        "grupo_particao": str(record.grupo_particao), "diagnostico": diagnostic}
                       for record in data.iloc[positions].itertuples())
        row = {"tipo": "subamostra_grupos_80pct", "semente": seed, "n_ajuste": len(subset),
               "n_grupos_ajuste": n_sample_groups, "ari": None,
               "status": "grupos_insuficientes" if n_sample_groups < 1 else "perfis_distintos_insuficientes"}
        if subset.drop_duplicates().shape[0] >= k:
            alternative = _modelo(k, seed).fit(subset)
            row.update({"ari": float(adjusted_rand_score(labels, alternative.predict(x))), "status": "calculado"})
        stability.append(row)
    for row in stability:
        row["diagnostico"] = diagnostic
    pd.DataFrame(stability).to_csv(out / "estabilidade.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(samples).to_csv(out / "subamostras.csv", index=False, encoding="utf-8-sig")
    model_filename = "modelo_diagnostico.joblib" if diagnostic else "modelo.joblib"
    joblib.dump(model, out / model_filename)
    joblib.dump(pca, out / "pca.joblib")
    by_type = {}
    for kind in ["semente", "subamostra_80pct", "subamostra_grupos_80pct"]:
        values = [r["ari"] for r in stability if r["tipo"] == kind and r["ari"] is not None]
        by_type[kind] = {"n_calculado": len(values), "n_total": sum(r["tipo"] == kind for r in stability),
                         "ari_medio": float(np.mean(values)) if values else None,
                         "ari_mediano": float(np.median(values)) if values else None,
                         "ari_minimo": float(min(values)) if values else None}
    summary = {**_proveniencia(data, atributos), "status": "sem_candidato_valido" if diagnostic else "concluido", "tarefa": "agrupamento",
               "algoritmo": "kmeans", "k_selecionado": None if diagnostic else k,
               "k_diagnostico": k if diagnostic else None, "diagnostico": diagnostic,
               "criterio_selecao": "maior_silhouette_com_tamanho_minimo",
               "criterio_diagnostico": "menor_k_calculavel" if diagnostic else None,
               "motivo": "Nenhum k satisfaz o tamanho mínimo e as métricas finitas" if diagnostic else "candidato elegível",
               "arquivo_modelo": model_filename,
               "desempate": "menor k", "min_servicos_cluster": min_cluster, "n_vetores_distintos": n_unique,
               "n_init": 30, "semente": 42, "metricas": None if diagnostic else chosen,
               "metricas_diagnostico": chosen if diagnostic else None, "estabilidade": by_type,
               "pca_variancia_explicada": pca.explained_variance_ratio_.tolist(),
               "pca_variancia_explicada_total": float(pca.explained_variance_ratio_.sum()),
               "tamanhos_clusters": {str(i): int(n) for i, n in enumerate(np.bincount(labels, minlength=k))},
               "limites": ["Agrupamento exploratório ajustado ao catálogo inteiro, sem rótulos de classe.",
                           "Cada fonte usa sua própria padronização; silhouette não é ranking de tabelas oficiais.",
                           "PCA exibe duas dimensões; a distância do KMeans é calculada em todos os atributos.",
                           "Estabilidade compara atribuições do catálogo após reajustes; não mede generalização preditiva.",
                           "Subamostras por linhas podem manter variantes da mesma família; a análise por grupos retira famílias inteiras usando 80% dos grupos, com quantidade variável de serviços.",
                           "Tamanhos contam serviços do catálogo, incluindo variantes; não representam frequência em obras.",
                           "Identificadores de cluster são arbitrários e não demonstram equivalência técnica."]}
    if diagnostic:
        summary["limites"].append("Nenhum k foi aceito. Gráficos, centros, representantes e estabilidade descrevem somente o diagnóstico do menor k calculável.")
    _salvar_json(out / "resumo.json", summary)
    return summary
