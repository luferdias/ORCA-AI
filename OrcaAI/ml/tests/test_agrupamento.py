"""Agrupamento ignora rótulos; valida estabilidade e dimensões reais."""
import json

import joblib
import numpy as np
import pandas as pd
import pytest


def dados():
    rng = np.random.default_rng(80)
    x = np.vstack([rng.normal(loc=[-5, -5], scale=.2, size=(20, 2)),
                   rng.normal(loc=[5, 5], scale=.2, size=(20, 2))])
    return pd.DataFrame({"fonte": "exemplo", "competencia": "2026-05",
                         "codigo": [f"{i:04}" for i in range(40)],
                         "descricao": "serviço sintético", "grupo_particao": [f"g{i}" for i in range(40)],
                         "classe": ["pintura"]*20 + ["pisos"]*20,
                         "material": x[:, 0], "horas": x[:, 1]})


@pytest.fixture(scope="module")
def execucao(tmp_path_factory):
    from orca_ml.agrupamento import executar_agrupamento
    out = tmp_path_factory.mktemp("agrupamento")
    summary = executar_agrupamento(dados(), ["material", "horas"], out)
    return out, summary


def test_separa_dois_perfis_e_exporta_dados_interpretaveis(execucao):
    out, summary = execucao
    assert summary["k_selecionado"] == 2
    attrs = pd.read_csv(out / "atribuicoes.csv")
    assert sorted(attrs.cluster.value_counts().tolist()) == [20, 20]
    assert attrs.iloc[:20].cluster.nunique() == 1
    centers = pd.read_csv(out / "centroides.csv")
    assert centers.material.min() < -4.5 and centers.material.max() > 4.5
    reps = pd.read_csv(out / "representantes.csv")
    assert len(reps) == 2
    assert summary["pca_variancia_explicada_total"] > .99
    stability = pd.read_csv(out / "estabilidade.csv")
    assert len(stability) == 43
    assert stability.ari.min() > .95
    assert len(pd.read_csv(out / "candidatos_k.csv")) == 4


def test_rotulos_e_ordem_das_linhas_nao_mudam_agrupamento(tmp_path, execucao):
    from orca_ml.agrupamento import executar_agrupamento
    old_out, _ = execucao
    df = dados().sample(frac=1, random_state=1)
    df["classe"] = "rótulo deliberadamente arbitrário"
    executar_agrupamento(df, ["material", "horas"], tmp_path)
    a = pd.read_csv(old_out / "atribuicoes.csv").sort_values("codigo")
    b = pd.read_csv(tmp_path / "atribuicoes.csv").sort_values("codigo")
    np.testing.assert_array_equal(a.cluster, b.cluster)
    np.testing.assert_allclose(a.distancia_centro, b.distancia_centro)


def test_modelo_salvo_reproduz_particao(execucao):
    out, _ = execucao
    model = joblib.load(out / "modelo.joblib")
    attrs = pd.read_csv(out / "atribuicoes.csv")
    np.testing.assert_array_equal(model.predict(dados()[["material", "horas"]]), attrs.cluster)


def test_estabilidade_por_grupos_nunca_retira_so_uma_variante(tmp_path):
    from orca_ml.agrupamento import executar_agrupamento
    df = dados()
    df["grupo_particao"] = [f"familia-{i // 2:02}" for i in range(len(df))]
    summary = executar_agrupamento(df, ["material", "horas"], tmp_path)
    audit = pd.read_csv(tmp_path / "subamostras.csv", dtype={"codigo": str})
    grouped = audit[audit.tipo == "subamostra_grupos_80pct"]
    assert grouped.semente.nunique() == 20
    for _, selection in grouped.groupby("semente"):
        ids = set(selection.codigo)
        selected = df[df.codigo.isin(ids)]
        assert selected.groupby("grupo_particao").size().eq(2).all()
        assert selected.grupo_particao.nunique() == 16
    rows = pd.read_csv(tmp_path / "estabilidade.csv")
    stats = rows[rows.tipo == "subamostra_grupos_80pct"]
    assert stats.n_grupos_ajuste.eq(16).all()
    assert stats.n_ajuste.eq(32).all()
    assert summary["estabilidade"]["subamostra_grupos_80pct"]["n_total"] == 20


@pytest.mark.parametrize("problema,match", [("constante", "constante"), ("poucos", "insuficiente"),
                                            ("infinito", "finit"), ("fonte", "fonte")])
def test_rejeita_dados_sem_agrupamento_valido(tmp_path, problema, match):
    from orca_ml.agrupamento import executar_agrupamento
    df = dados()
    if problema == "constante": df[["material", "horas"]] = 1
    if problema == "poucos": df = df.head(4)
    if problema == "infinito": df.loc[1, "material"] = np.inf
    if problema == "fonte": df.loc[1, "fonte"] = "outra"
    with pytest.raises(ValueError, match=match):
        executar_agrupamento(df, ["material", "horas"], tmp_path)


def test_nao_esconde_candidato_com_cluster_minimo_invalido(tmp_path):
    from orca_ml.agrupamento import executar_agrupamento
    df = dados()
    df[["material", "horas"]] = 0.
    df.loc[0, ["material", "horas"]] = 100.
    result = executar_agrupamento(df, ["material", "horas"], tmp_path)
    candidates = pd.read_csv(tmp_path / "candidatos_k.csv")
    assert len(candidates) == 4
    assert not candidates.elegivel.any()
    assert candidates.loc[candidates.k == 2, "min_tamanho"].iloc[0] == 1
    summary = json.loads((tmp_path / "resumo.json").read_text())
    assert summary["status"] == result["status"] == "sem_candidato_valido"
    assert result["k_selecionado"] is None
    assert result["k_diagnostico"] == 2
    assert result["diagnostico"] is True
    assert result["metricas"] is None
    assert result["metricas_diagnostico"]["elegivel"] is False
    assert result["min_servicos_cluster"] == 3
    assert not (tmp_path / "modelo.joblib").exists()
    assert (tmp_path / "modelo_diagnostico.joblib").is_file()
    for filename in ["atribuicoes", "centroides", "representantes", "coordenadas_pca", "estabilidade"]:
        assert pd.read_csv(tmp_path / f"{filename}.csv").diagnostico.eq(True).all()
