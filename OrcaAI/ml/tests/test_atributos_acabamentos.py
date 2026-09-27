"""Contratos de atributos e partições: expectativas derivadas de pequenos exemplos."""
import numpy as np
import pandas as pd
import pytest

from orca_ml import atributos_acabamentos as mod


def servicos():
    return pd.DataFrame([
        dict(fonte="der_es", competencia="2026-05", codigo="01", descricao="Parede A", unidade="m2", grupo="PINTURA / SOBRE PAREDES E FORROS", custo=100, status_composicao="ok"),
        dict(fonte="der_es", competencia="2026-05", codigo="02", descricao="Parede B", unidade="m2", grupo="PINTURA / SOBRE PAREDES E FORROS", custo=120, status_composicao="ok"),
    ])


def recursos():
    return pd.DataFrame([
        dict(codigo_servico="01", codigo_recurso="r1", categoria="mao_obra", unidade_recurso="H", coeficiente=2, custo_folha_sem_truncamento=60, horas_mao_obra=2, horas_equipamento=0),
        dict(codigo_servico="01", codigo_recurso="r2", categoria="material", unidade_recurso="L", coeficiente=4, custo_folha_sem_truncamento=40, horas_mao_obra=0, horas_equipamento=0),
        dict(codigo_servico="02", codigo_recurso="r1", categoria="mao_obra", unidade_recurso="H", coeficiente=4, custo_folha_sem_truncamento=120, horas_mao_obra=4, horas_equipamento=0),
    ])


def test_fracoes_contagens_e_horas_derivadas_sem_entrada_do_rotulo():
    result = mod.preparar_atributos(servicos(), recursos()).set_index("codigo")
    assert result.loc["01", "fracao_mao_obra"] == pytest.approx(.6)
    assert result.loc["01", "fracao_material"] == pytest.approx(.4)
    assert result.loc["01", "n_mao_obra"] == 1
    assert result.loc["01", "n_material"] == 1
    assert result.loc["01", "horas_mao_obra"] == 2
    assert result.loc["02", "fracao_material"] == 0
    assert result.loc["02", "fracao_mao_obra"] == 1
    assert result.loc["01", "classe"] == "pintura"
    assert np.isfinite(result[mod.ATRIBUTOS].to_numpy()).all()


def test_codigo_repetido_de_recurso_nao_duplica_participacao():
    rows = pd.concat([recursos(), recursos().iloc[:1]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicad"):
        mod.preparar_atributos(servicos(), rows)


def test_recurso_de_servico_desconhecido_impede_join_silencioso():
    rows = recursos(); rows.loc[0, "codigo_servico"] = "99"
    with pytest.raises(ValueError, match="desconhecid"):
        mod.preparar_atributos(servicos(), rows)


@pytest.mark.parametrize("value", [np.nan, -1, np.inf])
def test_custo_folha_invalido_nao_vira_zero(value):
    rows = recursos(); rows["custo_folha_sem_truncamento"] = rows.custo_folha_sem_truncamento.astype(float)
    rows.loc[0, "custo_folha_sem_truncamento"] = value
    with pytest.raises(ValueError):
        mod.preparar_atributos(servicos(), rows)


def test_composicao_excluida_nao_entra_no_treino():
    frame = servicos(); frame.loc[1, "status_composicao"] = "excluido"
    result = mod.preparar_atributos(frame, recursos())
    assert result.codigo.tolist() == ["01"]


def test_grupo_de_variantes_e_transitivo_sem_usar_classe_ou_coeficiente():
    frame = pd.DataFrame([
        dict(codigo="01", descricao="Pintura duas demãos", classe="pintura"),
        dict(codigo="02", descricao="Outro serviço", classe="pisos"),
        dict(codigo="03", descricao="Pintura três demãos", classe="pintura"),
        dict(codigo="04", descricao="Granito polido", classe="pisos"),
    ])
    rows = pd.DataFrame([
        dict(codigo_servico="01", codigo_recurso="A", categoria="material", unidade_recurso="L"),
        dict(codigo_servico="02", codigo_recurso="A", categoria="material", unidade_recurso="L"),
        dict(codigo_servico="03", codigo_recurso="B", categoria="material", unidade_recurso="L"),
        dict(codigo_servico="04", codigo_recurso="C", categoria="material", unidade_recurso="M2"),
    ])
    result = mod.agrupar_variantes(frame, rows).set_index("codigo")
    assert result.loc[["01", "02", "03"], "grupo_particao"].nunique() == 1
    assert result.grupo_particao.nunique() == 2
    shuffled = mod.agrupar_variantes(frame.iloc[::-1], rows.iloc[::-1]).set_index("codigo")
    assert result.grupo_particao.to_dict() == shuffled.grupo_particao.to_dict()


def test_recorte_preserva_historico_e_filtra_unidade_por_linha():
    frame = servicos().drop(columns="status_composicao")
    frame.loc[0, "competencia"] = "2026-04"
    frame.loc[1, "unidade"] = "m"
    result = mod.selecionar_recorte(frame)
    assert result.codigo.tolist() == ["01"]
    assert result.competencia.tolist() == ["2026-04"]
    assert mod.selecionar_recorte(frame, "2026-05").empty


def test_mes_e_codigo_duplicados_rejeitados():
    frame = pd.concat([servicos(), servicos().iloc[:1]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicad"):
        mod.selecionar_recorte(frame)


def test_reaplicar_recorte_apos_parser_preserva_classes_originais():
    primeiro = mod.selecionar_recorte(servicos())
    segundo = mod.selecionar_recorte(primeiro)
    pd.testing.assert_frame_equal(primeiro, segundo)
