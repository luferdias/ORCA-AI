"""Garantias contra comparações temporais falsas e escolha oportunista de exemplos."""
import importlib

import pandas as pd
import pytest


def relatorio():
    try:
        return importlib.import_module("orca_ml.relatorio")
    except ModuleNotFoundError:
        pytest.fail("O gerador de relatório didático ainda não foi implementado")


def test_periodos_distintos_nao_sao_apresentados_como_comparacao_comum():
    summaries = {
        "sinapi_es": {"competencias_validacao": ["2026-01"], "competencias_teste": ["2026-03", "2026-04"]},
        "der_es": {"competencias_validacao": ["2026-01"], "competencias_teste": ["2026-04", "2026-05"]},
    }
    with pytest.raises(ValueError, match="período"):
        relatorio().validar_periodos(summaries)


def test_escolha_didatica_nao_usa_custo_ou_erro_futuro():
    history = pd.DataFrame([
        {"fonte": "sinapi_es", "grupo": "Pintura Interna", "unidade": "M2", "codigo": code,
         "competencia": month, "custo": price, "descricao": "Pintura"}
        for code, price in [("001", 10.), ("002", 20.), ("003", 90.)]
        for month in ["2025-12", "2026-01", "2026-02"]
    ])
    rows = pd.DataFrame([
        {"fonte": "sinapi_es", "grupo": "Pintura Interna", "unidade": "M2", "codigo": code,
         "nicho_id": "pintura", "competencia_alvo": month, "ape": error}
        for code, error in [("001", 0.), ("002", 90.), ("003", 1.)]
        for month in ["2026-03", "2026-04", "2026-05"]
    ])
    first = relatorio().selecionar_exemplos(rows, {"sinapi_es": history})
    assert first["sinapi_es"]["codigo"] == "002"
    rows["ape"] = [1000., 400., 1., 0., 0., 0., 11., 20., 88.]
    future = history.iloc[[0]].assign(competencia="2026-05", custo=999999.)
    second = relatorio().selecionar_exemplos(rows, {"sinapi_es": pd.concat([history, future])})
    assert second["sinapi_es"]["codigo"] == "002"


def test_relatorio_nao_sobrescreve_resultado_existente(tmp_path):
    output = tmp_path / "saida"
    output.mkdir()
    marker = output / "manter.txt"
    marker.write_text("resultado anterior")
    with pytest.raises(ValueError, match="contém"):
        relatorio().gerar_relatorio(tmp_path, {}, saida=output)
    assert marker.read_text() == "resultado anterior"


def test_csv_com_mes_distinto_do_manifesto_nao_recebe_rotulo_falso():
    raw = pd.DataFrame({"fonte": ["sinapi_es", "sinapi_es"], "fase": ["validacao", "teste"],
                        "competencia_alvo": ["2026-01", "2026-04"]})
    summary = {"competencias_validacao": ["2026-01"], "competencias_teste": ["2026-03"]}
    with pytest.raises(ValueError, match="competências"):
        relatorio().validar_csv(raw, summary, "sinapi_es")


def test_csv_de_outra_fonte_nao_recebe_rotulo_da_pasta():
    raw = pd.DataFrame({"fonte": ["der_es"], "fase": ["teste"], "competencia_alvo": ["2026-03"]})
    with pytest.raises(ValueError, match="fonte"):
        relatorio().validar_csv(raw, {}, "sinapi_es")


def test_validacao_pode_perder_mes_por_publicacao_mas_teste_tem_janela_comum():
    raw = pd.DataFrame({"fonte": ["sinapi_es", "sinapi_es"], "fase": ["validacao", "teste"],
                        "competencia_alvo": ["2026-01", "2026-03"]})
    summary = {"competencias_validacao": ["2026-01", "2026-02"], "competencias_teste": ["2026-03"]}
    relatorio().validar_csv(raw, summary, "sinapi_es")
