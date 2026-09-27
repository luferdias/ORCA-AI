"""Proteções contra vazamento e escolha pelo teste, em dados sintéticos."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest


def dados():
    rng = np.random.default_rng(130)
    rows = []
    for i, classe in enumerate(["pintura", "pisos", "revestimentos_forros"]):
        for grupo in range(20):
            for variante in range(2):
                rows.append({"fonte": "exemplo", "competencia": "2026-05",
                             "codigo": f"{i:01}{grupo:03}{variante}", "descricao": "serviço sintético",
                             "classe": classe, "grupo_particao": f"{i}-{grupo}",
                             "material": i * 15 + rng.normal(0, .3),
                             "horas": (2-i) * 12 + rng.normal(0, .2)})
    return pd.DataFrame(rows)


@pytest.fixture(scope="module")
def execucao(tmp_path_factory):
    from orca_ml.classificacao import executar_classificacao
    out = tmp_path_factory.mktemp("classificacao")
    df = dados()
    result = executar_classificacao(df, ["material", "horas"], out)
    return df, out, result


def test_grupos_e_variantes_nunca_cruzam_holdout_ou_folds(execucao):
    _, out, result = execucao
    parts = pd.read_csv(out / "particoes.csv", dtype={"codigo": str})
    assert parts.groupby("grupo_particao").particao.nunique().max() == 1
    train = parts[parts.particao == "treino"]
    assert train.groupby("grupo_particao").fold_validacao.nunique().max() == 1
    assert set(train.fold_validacao) == {0, 1, 2}
    for _, fold in train.groupby("fold_validacao"):
        assert set(fold.classe) == {"pintura", "pisos", "revestimentos_forros"}
    assert result["algoritmo_selecionado"] in ["random_forest", "arvore_decisao", "knn"]


def test_scaler_do_modelo_salvo_aprende_so_treino(execucao):
    df, out, _ = execucao
    parts = pd.read_csv(out / "particoes.csv", dtype={"codigo": str})
    train = df[df.codigo.isin(parts.loc[parts.particao == "treino", "codigo"])]
    model = joblib.load(out / "modelo.joblib")
    np.testing.assert_allclose(model.named_steps["escala"].mean_, train[["material", "horas"]].mean())
    assert not np.allclose(model.named_steps["escala"].mean_, df[["material", "horas"]].mean())


def test_escala_de_cada_fold_exclui_validacao_e_teste(execucao):
    df, out, _ = execucao
    parts = pd.read_csv(out / "particoes.csv", dtype={"codigo": str})
    adjustments = json.loads((out / "preprocessamento_cv.json").read_text())["ajustes"]
    for item in adjustments:
        ids = parts.loc[(parts.particao == "treino") & (parts.fold_validacao != item["fold"]), "codigo"]
        expected = df.loc[df.codigo.isin(ids), ["material", "horas"]].mean().to_numpy()
        np.testing.assert_allclose(item["media_treino"], expected)


def test_teste_extremo_e_ordem_das_linhas_nao_influenciam_selecao(tmp_path, execucao):
    from orca_ml.classificacao import executar_classificacao
    df, old_out, original = execucao
    parts = pd.read_csv(old_out / "particoes.csv", dtype={"codigo": str})
    changed = df.copy()
    changed.loc[changed.codigo.isin(parts.loc[parts.particao == "teste", "codigo"]), ["material", "horas"]] += 10000
    result = executar_classificacao(changed.sample(frac=1, random_state=51), ["material", "horas"], tmp_path)
    assert result["vencedores_cv"] == original["vencedores_cv"]
    assert result["algoritmo_selecionado"] == original["algoritmo_selecionado"]
    pd.testing.assert_frame_equal(pd.read_csv(tmp_path / "metricas_cv.csv"), pd.read_csv(old_out / "metricas_cv.csv"))


def test_exporta_referencias_e_erros_recalculaveis(execucao):
    _, out, summary = execucao
    metrics = pd.read_csv(out / "metricas_teste.csv")
    assert set(metrics.algoritmo) == {"random_forest", "arvore_decisao", "knn", "dummy_maioria"}
    assert metrics.loc[metrics.algoritmo == "random_forest", "f1_macro"].iloc[0] > .9
    assert metrics.loc[metrics.algoritmo == "dummy_maioria", "f1_macro"].iloc[0] < .3
    confusion = pd.read_csv(out / "confusao.csv")
    assert confusion.groupby("algoritmo").n.sum().eq(summary["n_teste"]).all()
    cv = pd.read_csv(out / "metricas_cv.csv")
    assert len(cv) == 27
    assert (out / "resumo.json").is_file()
    assert json.loads((out / "resumo.json").read_text())["criterio_selecao"] == "f1_macro_validacao"


@pytest.mark.parametrize("problema,match", [("duplicado", "duplicad"), ("fonte", "fonte"),
                                            ("nan", "finit"), ("rotulo", "classe"),
                                            ("grupos", "grupos"), ("constante", "constante")])
def test_rejeita_entradas_sem_avaliacao_valida(tmp_path, problema, match):
    from orca_ml.classificacao import executar_classificacao
    df = dados()
    if problema == "duplicado": df.loc[1, "codigo"] = df.loc[0, "codigo"]
    if problema == "fonte": df.loc[1, "fonte"] = "outra"
    if problema == "nan": df.loc[1, "horas"] = np.nan
    if problema == "rotulo": df.loc[1, "classe"] = "inventado"
    if problema == "grupos": df["grupo_particao"] = df["classe"]
    if problema == "constante": df[["material", "horas"]] = 1
    with pytest.raises(ValueError, match=match):
        executar_classificacao(df, ["material", "horas"], tmp_path)


@pytest.mark.parametrize("atributo", ["classe", "codigo", "descricao", "grupo_particao", "custo"])
def test_rejeita_atributo_que_revela_identidade_ou_rotulo(tmp_path, atributo):
    from orca_ml.classificacao import executar_classificacao
    df = dados()
    df["custo"] = 1
    with pytest.raises(ValueError, match="atributo"):
        executar_classificacao(df, [atributo], tmp_path)


def test_nao_sobrescreve_resultado_existente(tmp_path):
    from orca_ml.classificacao import executar_classificacao
    old = tmp_path / "resumo.json"
    old.write_text("preservar")
    with pytest.raises(ValueError, match="vazi"):
        executar_classificacao(dados(), ["material", "horas"], tmp_path)
    assert old.read_text() == "preservar"
