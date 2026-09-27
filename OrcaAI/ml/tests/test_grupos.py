"""Taxonomia de apresentação: cobertura integral e nenhuma equivalência implícita."""

import copy
import json
from pathlib import Path

import pandas as pd
import pytest

from orca_ml.grupos import adicionar_nichos, carregar_mapa, unidade_legivel


@pytest.fixture
def mapa_minimo():
    return {
        "nichos": [
            {"id": "pintura", "nome": "Pintura", "ordem": 1, "descricao": "Pinturas."},
            {"id": "pisos", "nome": "Pisos", "ordem": 2, "descricao": "Pisos."},
        ],
        "mapeamento": {
            "sinapi_es": {"Pintura Interna": "pintura"},
            "der_es": {"PINTURA / SOBRE PAREDES E FORROS": "pintura"},
        },
    }


def test_adiciona_nicho_sem_alterar_grupo_unidade_codigo_ordem_ou_indice(mapa_minimo):
    frame = pd.DataFrame(
        {
            "fonte": ["der_es", "sinapi_es", "der_es"],
            "grupo": ["PINTURA / SOBRE PAREDES E FORROS", "Pintura Interna", "PINTURA / SOBRE PAREDES E FORROS"],
            "unidade": ["m2", "M2", "und"],
            "codigo": ["001", "002", "003"],
            "custo": [9.5, 20.0, 1.5],
        },
        index=[8, 3, 8],
    )
    original = frame.copy(deep=True)
    resultado = adicionar_nichos(frame, mapa_minimo)
    pd.testing.assert_frame_equal(frame, original)
    pd.testing.assert_frame_equal(resultado[original.columns], original)
    assert resultado.nicho_id.tolist() == ["pintura"] * 3
    assert resultado.nicho.tolist() == ["Pintura"] * 3


def test_grupo_igual_em_fontes_distintas_pode_ter_mapeamento_diferente(mapa_minimo):
    mapa_minimo["mapeamento"] = {"sinapi_es": {"Comum": "pintura"}, "der_es": {"Comum": "pisos"}}
    frame = pd.DataFrame({"fonte": ["sinapi_es", "der_es"], "grupo": ["Comum", "Comum"]})
    assert adicionar_nichos(frame, mapa_minimo).nicho_id.tolist() == ["pintura", "pisos"]


@pytest.mark.parametrize("fonte,grupo", [("sinapi_es", "Grupo novo"), ("outra_fonte", "Pintura Interna")])
def test_grupo_novo_ou_fonte_nova_falham_sem_cair_em_outros(mapa_minimo, fonte, grupo):
    with pytest.raises(ValueError, match="não mapeados") as erro:
        adicionar_nichos(pd.DataFrame({"fonte": [fonte], "grupo": [grupo]}), mapa_minimo)
    assert fonte in str(erro.value)
    assert grupo in str(erro.value)


@pytest.mark.parametrize("campo", ["fonte", "grupo"])
def test_chave_nula_falha(mapa_minimo, campo):
    linha = {"fonte": "sinapi_es", "grupo": "Pintura Interna"}
    linha[campo] = None
    with pytest.raises(ValueError, match="vazios"):
        adicionar_nichos(pd.DataFrame([linha]), mapa_minimo)


def test_mapeamento_aponta_para_nicho_inexistente(mapa_minimo):
    mapa_minimo["mapeamento"]["sinapi_es"]["Pintura Interna"] = "inexistente"
    with pytest.raises(ValueError, match="nicho inexistente"):
        adicionar_nichos(pd.DataFrame(columns=["fonte", "grupo"]), mapa_minimo)


def test_ids_de_nicho_duplicados_falham(mapa_minimo):
    mapa_minimo["nichos"].append(copy.deepcopy(mapa_minimo["nichos"][0]))
    with pytest.raises(ValueError, match="duplicado"):
        adicionar_nichos(pd.DataFrame(columns=["fonte", "grupo"]), mapa_minimo)


def test_json_nao_permite_duas_categorias_para_o_mesmo_grupo(tmp_path):
    arquivo = tmp_path / "mapa.json"
    arquivo.write_text('{"mapeamento":{"sinapi_es":{"Pintura Interna":"pintura","Pintura Interna":"pisos"}}}', encoding="utf-8")
    with pytest.raises(ValueError, match="Chave JSON duplicada.*Pintura Interna"):
        carregar_mapa(arquivo)


def test_frame_vazio_com_schema_preservado(mapa_minimo):
    resultado = adicionar_nichos(pd.DataFrame(columns=["fonte", "grupo", "codigo"]), mapa_minimo)
    assert resultado.empty
    assert resultado.columns.tolist() == ["fonte", "grupo", "codigo", "nicho_id", "nicho"]


def test_colunas_obrigatorias_faltantes(mapa_minimo):
    with pytest.raises(ValueError, match="Colunas obrigatórias"):
        adicionar_nichos(pd.DataFrame({"grupo": ["Pintura Interna"]}), mapa_minimo)


def test_mapeamento_padrao_independente_do_diretorio_corrente(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = carregar_mapa()
    assert config["mapeamento"]["sinapi_es"]["Energia Solar para Edificações"] == "hidrossanitarias"
    assert config["mapeamento"]["sinapi_es"]["Sistemas de Medição"] == "hidrossanitarias"
    assert "limitações" in config or "limitacoes" in config


def test_totalidade_dos_grupos_nativos_dos_datasets_reais():
    raiz = Path(__file__).resolve().parents[2] / "knowledge" / "datasets" / "ml_ufg"
    config = carregar_mapa()
    for fonte, esperado in [("sinapi_es", 157), ("der_es", 125)]:
        arquivo = raiz / fonte / "custos_historicos.csv"
        if not arquivo.exists():
            pytest.skip("Datasets oficiais não estão presentes neste checkout.")
        grupos = pd.read_csv(arquivo, usecols=["fonte", "grupo"]).drop_duplicates()
        assert grupos.grupo.nunique() == esperado
        assert set(grupos.grupo) == set(config["mapeamento"][fonte])
        resultado = adicionar_nichos(grupos, config)
        assert len(resultado) == esperado
        assert resultado[["nicho_id", "nicho"]].notna().all().all()


@pytest.mark.parametrize("entrada,esperada", [("M2", "m²"), ("m3", "m³"), ("und", "un"), ("UN", "un"), ("KG", "kg"), ("MES", "mês"), ("Mês", "mês"), ("TXKM", "t·km"), ("ms", "ms"), ("unidade desconhecida", "unidade desconhecida")])
def test_unidade_legivel_apenas_formata_sem_inventar_conversao(entrada, esperada):
    assert unidade_legivel(entrada) == esperada
