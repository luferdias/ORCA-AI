"""Classificação tabular com variantes agrupadas e teste reservado.

Os rótulos são derivados do catálogo; não pressupõem homologação humana.
A escolha dos candidatos e do algoritmo usa somente validação interna.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, precision_recall_fscore_support)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


CLASSES = ["pintura", "pisos", "revestimentos_forros"]
RESERVADAS = {"fonte", "codigo", "descricao", "classe", "grupo", "grupo_particao", "custo",
              "competencia", "regime", "unidade", "localizador", "arquivo_sha256", "nicho", "nicho_id",
              "y", "rotulo", "alvo", "cluster"}


def _validar_dataset(dataset: pd.DataFrame, atributos: list[str], *, supervisionado: bool) -> pd.DataFrame:
    """Compartilhe validação tabular, sem consultar rótulos no KMeans."""
    required = {"fonte", "codigo", "descricao", "grupo_particao"}
    if supervisionado:
        required.add("classe")
    if not isinstance(atributos, list) or not atributos or any(not isinstance(a, str) for a in atributos):
        raise ValueError("Forneça uma lista explícita e não vazia de atributos numéricos")
    if len(set(atributos)) != len(atributos) or any(a.lower() in RESERVADAS for a in atributos):
        raise ValueError("Lista de atributos duplicada ou com identidade, custo ou rótulo proibido")
    missing = (required | set(atributos)) - set(dataset.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {sorted(missing)}")
    if dataset.empty or not dataset.columns.is_unique:
        raise ValueError("Dataset vazio ou colunas duplicadas")
    data = dataset.copy()
    for c in ["fonte", "codigo", "grupo_particao"]:
        data[c] = data[c].astype("string").str.strip()
        if data[c].isna().any() or data[c].eq("").any():
            raise ValueError(f"{c} precisa estar preenchido")
    if data.fonte.nunique() != 1:
        raise ValueError("A execução exige uma única fonte")
    if data.codigo.duplicated().any():
        raise ValueError("Códigos duplicados: forneça um único registro por serviço e edição")
    if "competencia" in data:
        if data.competencia.isna().any() or data.competencia.astype(str).nunique() != 1:
            raise ValueError("A execução exige uma única competência preenchida")
    for col in atributos:
        if not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"O atributo {col} deve ser numérico")
    if not np.isfinite(data[atributos].to_numpy(dtype=float)).all():
        raise ValueError("Os atributos devem conter somente valores finitos e preenchidos")
    if data[atributos].nunique().max() < 2:
        raise ValueError("Todos os atributos são constantes; não há informação para modelar")
    if supervisionado:
        if data.classe.isna().any() or set(data.classe) != set(CLASSES):
            raise ValueError(f"São necessárias as três classes: {CLASSES}")
    return data.sort_values("codigo", kind="stable").reset_index(drop=True)


def _preparar_saida(saida: Path) -> Path:
    out = Path(saida)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("A pasta de saída deve estar vazia para preservar resultados anteriores")
    out.mkdir(parents=True, exist_ok=True)
    return out


def _salvar_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def _proveniencia(data: pd.DataFrame, atributos: list[str]) -> dict:
    return {"fonte": str(data.fonte.iloc[0]), "competencia": str(data.competencia.iloc[0]) if "competencia" in data else None,
            "n": len(data), "n_grupos": int(data.grupo_particao.nunique()), "atributos": atributos,
            "dataset_sha256": hashlib.sha256(data.to_csv(index=False).encode()).hexdigest(),
            "versoes": {"python": platform.python_version(), "numpy": np.__version__,
                        "pandas": pd.__version__, "sklearn": sklearn.__version__}}


def _conferir_particao(y, groups, treino, avaliacao, contexto: str) -> None:
    if set(groups.iloc[treino]) & set(groups.iloc[avaliacao]):
        raise ValueError(f"Vazamento de grupos na partição {contexto}")
    if set(y.iloc[treino]) != set(CLASSES) or set(y.iloc[avaliacao]) != set(CLASSES):
        raise ValueError(f"Cobertura de classes insuficiente na partição fixa {contexto}; não trocar a semente pelo resultado")


def executar_classificacao(dataset: pd.DataFrame, atributos: list[str], saida: Path) -> dict:
    """Avalie três algoritmos, por grupos, com primeiro fold fixo como teste.

    O modelo salvo foi ajustado apenas no treino externo. Pode reproduzir o
    teste publicado. As previsões não são probabilidades calibradas.
    """
    data = _validar_dataset(dataset, atributos, supervisionado=True)
    x, y, groups = data[atributos], data.classe, data.grupo_particao
    group_counts = data.groupby("classe").grupo_particao.nunique()
    if group_counts.min() < 5:
        raise ValueError("Quantidade insuficiente de grupos por classe: são necessários ao menos cinco")
    outer = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    train, test = next(outer.split(x, y, groups))
    _conferir_particao(y, groups, train, test, "teste")
    xt, yt, gt = x.iloc[train], y.iloc[train], groups.iloc[train]
    if data.iloc[train].groupby("classe").grupo_particao.nunique().min() < 3:
        raise ValueError("Grupos insuficientes para três partições internas")
    folds = list(StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=43).split(xt, yt, gt))
    for i, (fit, val) in enumerate(folds):
        _conferir_particao(yt, gt, fit, val, f"validação {i}")
        if len(fit) < 7:
            raise ValueError("Amostra insuficiente no treino interno para KNN com sete vizinhos")
    out = _preparar_saida(saida)
    parts = data[["fonte", "codigo", "classe", "grupo_particao"]].copy()
    parts["particao"] = "teste"
    parts["fold_validacao"] = pd.Series(pd.NA, index=parts.index, dtype="Int64")
    parts.loc[train, "particao"] = "treino"
    for i, (_, val) in enumerate(folds):
        parts.loc[train[val], "fold_validacao"] = i
    parts.to_csv(out / "particoes.csv", index=False, encoding="utf-8-sig")
    candidates = {
        "random_forest": [RandomForestClassifier(n_estimators=200, min_samples_leaf=leaf, random_state=42, n_jobs=1)
                          for leaf in [1, 2, 4]],
        "arvore_decisao": [DecisionTreeClassifier(max_depth=depth, min_samples_leaf=2, random_state=42)
                           for depth in [3, 5, None]],
        "knn": [KNeighborsClassifier(n_neighbors=k, weights="distance") for k in [3, 5, 7]],
    }
    cv_rows, cv_summary, winners, preprocessing = [], [], {}, []
    for algo, estimators in candidates.items():
        best_score = -1.0
        for candidate, estimator in enumerate(estimators):
            scores = []
            params = estimator.get_params(deep=False)
            for fold, (fit, val) in enumerate(folds):
                model = Pipeline([("escala", StandardScaler()), ("modelo", clone(estimator))])
                model.fit(xt.iloc[fit], yt.iloc[fit])
                pred = model.predict(xt.iloc[val])
                score = float(f1_score(yt.iloc[val], pred, labels=CLASSES, average="macro", zero_division=0))
                scores.append(score)
                cv_rows.append({"algoritmo": algo, "candidato": candidate, "parametros": json.dumps(params, sort_keys=True),
                                "fold": fold, "f1_macro": score,
                                "acuracia_balanceada": float(balanced_accuracy_score(yt.iloc[val], pred)),
                                "n_treino": len(fit), "n_validacao": len(val)})
                preprocessing.append({"algoritmo": algo, "candidato": candidate, "fold": fold,
                                      "media_treino": model.named_steps["escala"].mean_.tolist(),
                                      "escala_treino": model.named_steps["escala"].scale_.tolist()})
            mean = float(np.mean(scores))
            cv_summary.append({"algoritmo": algo, "candidato": candidate, "parametros": json.dumps(params, sort_keys=True),
                               "f1_macro_media": mean, "f1_macro_desvio": float(np.std(scores, ddof=1))})
            if mean > best_score:
                best_score = mean
                winners[algo] = {"estimador": estimator, "score_cv": mean, "candidato": candidate}
    # Ordem predefinida resolve empates, sem consultar nenhuma previsão de teste.
    selected = max(winners, key=lambda name: winners[name]["score_cv"])
    pd.DataFrame(cv_rows).to_csv(out / "metricas_cv.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(cv_summary).to_csv(out / "candidatos_cv.csv", index=False, encoding="utf-8-sig")
    _salvar_json(out / "preprocessamento_cv.json", {"ajustes": preprocessing, "atributos": atributos})
    metrics, class_rows, confusion_rows, predictions = [], [], [], []
    models_dir = out / "modelos"
    models_dir.mkdir()
    final_estimators = {algo: item["estimador"] for algo, item in winners.items()}
    final_estimators["dummy_maioria"] = DummyClassifier(strategy="most_frequent")
    for algo, estimator in final_estimators.items():
        model = Pipeline([("escala", StandardScaler()), ("modelo", clone(estimator))])
        model.fit(xt, yt)
        pred = model.predict(x.iloc[test])
        truth = y.iloc[test]
        metrics.append({"algoritmo": algo, "selecionado_cv": algo == selected,
                        "f1_macro": float(f1_score(truth, pred, labels=CLASSES, average="macro", zero_division=0)),
                        "acuracia_balanceada": float(balanced_accuracy_score(truth, pred)),
                        "acuracia": float(accuracy_score(truth, pred)), "n": len(test)})
        precision, recall, f1, support = precision_recall_fscore_support(truth, pred, labels=CLASSES, zero_division=0)
        for i, cls in enumerate(CLASSES):
            class_rows.append({"algoritmo": algo, "classe": cls, "precisao": float(precision[i]),
                               "recall": float(recall[i]), "f1": float(f1[i]), "suporte": int(support[i])})
        matrix = confusion_matrix(truth, pred, labels=CLASSES)
        for i, real in enumerate(CLASSES):
            for j, predicted in enumerate(CLASSES):
                confusion_rows.append({"algoritmo": algo, "classe_real": real, "classe_prevista": predicted, "n": int(matrix[i, j])})
        predicted_frame = data.iloc[test][["fonte", "codigo", "descricao", "classe", "grupo_particao"]].copy()
        predicted_frame["algoritmo"], predicted_frame["classe_prevista"] = algo, pred
        predicted_frame["selecionado_cv"] = algo == selected
        predictions.append(predicted_frame)
        joblib.dump(model, models_dir / f"{algo}.joblib")
        if algo == selected:
            joblib.dump(model, out / "modelo.joblib")
    for name, rows in [("metricas_teste", metrics), ("metricas_por_classe", class_rows), ("confusao", confusion_rows)]:
        pd.DataFrame(rows).to_csv(out / f"{name}.csv", index=False, encoding="utf-8-sig")
    pd.concat(predictions, ignore_index=True).to_csv(out / "previsoes.csv", index=False, encoding="utf-8-sig")
    summary = {**_proveniencia(data, atributos), "status": "concluido", "tarefa": "classificacao",
               "algoritmo_principal": "random_forest", "algoritmo_selecionado": selected,
               "criterio_selecao": "f1_macro_validacao", "desempate": "ordem fixa: random_forest, arvore_decisao, knn; primeiro candidato",
               "sementes": {"teste": 42, "cv": 43, "modelos": 42}, "n_treino": len(train), "n_teste": len(test),
               "n_grupos_treino": int(gt.nunique()), "n_grupos_teste": int(groups.iloc[test].nunique()),
               "classes": CLASSES, "contagem_classes": data.classe.value_counts().sort_index().astype(int).to_dict(),
               "grupos_por_classe": group_counts.astype(int).to_dict(),
               "vencedores_cv": {a: {"candidato": d["candidato"], "f1_macro_media": d["score_cv"],
                                      "parametros": d["estimador"].get_params(deep=False)} for a, d in winners.items()},
               "metricas_teste": metrics,
               "limites": ["Classes derivadas dos grupos oficiais; revisão humana não presumida.",
                           "Grupos de variantes são aproximações conservadoras, não equivalências técnicas homologadas.",
                           "Teste único por grupos; amostra pequena limita generalização.",
                           "Métricas de teste não participam da seleção. Não são probabilidades calibradas."]}
    _salvar_json(out / "resumo.json", summary)
    return summary
