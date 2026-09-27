"""Regras de comparação justa para o relatório didático de regressão."""

import numpy as np
import pandas as pd
import pytest

from orca_ml.estatisticas_relatorio import (
    preparar_avaliacao,
    resumir_avaliacao,
    resumir_recortes,
)


def previsoes():
    linhas = []
    for fase, origem, alvo in (("validacao", "2026-01", "2026-02"), ("teste", "2026-02", "2026-03")):
        for codigo, observado, ultimo, previsto in (("001", 100.0, 90.0, 105.0), ("002", 200.0, 240.0, 180.0)):
            for modelo, valor in (("persistencia", ultimo), ("linear_simples", previsto), ("linear_multipla", observado)):
                linhas.append({
                    "fonte": "sinapi_es", "grupo": "Pintura", "unidade": "M2",
                    "regime": "sem_desoneracao", "codigo": codigo,
                    "fase": fase, "modelo": modelo,
                    "modelo_selecionado": modelo == "linear_simples",
                    "competencia_t": origem, "competencia_alvo": alvo,
                    "custo_t": ultimo, "custo_observado": observado, "custo_previsto": valor,
                    "treino_ate": "2025-12", "data_corte": None,
                    "treino_publicado_ate": None, "publicado_alvo": None,
                })
    return pd.DataFrame(linhas)


def test_pareia_modelo_escolhido_na_validacao_sem_escolher_melhor_teste():
    resultado = preparar_avaliacao(previsoes())
    assert len(resultado) == 2
    assert resultado.codigo.tolist() == ["001", "002"]
    assert resultado.modelo.unique().tolist() == ["linear_simples"]
    assert resultado.previsto_persistencia.tolist() == [90.0, 240.0]
    assert resultado.ape.tolist() == [5.0, 10.0]
    assert resultado.erro_pct.tolist() == [5.0, -10.0]
    assert resultado.ape_persistencia.tolist() == [10.0, 20.0]


@pytest.mark.parametrize("valor", ["False", "True", 0, 1, None])
def test_rejeita_flags_que_nao_sao_booleanos(valor):
    dados = previsoes().astype({"modelo_selecionado": object})
    dados.loc[0, "modelo_selecionado"] = valor
    with pytest.raises(ValueError, match="boolean"):
        preparar_avaliacao(dados)


def test_rejeita_modelo_trocado_depois_da_validacao():
    dados = previsoes()
    teste = dados.fase.eq("teste")
    dados.loc[teste, "modelo_selecionado"] = dados.loc[teste, "modelo"].eq("linear_multipla")
    with pytest.raises(ValueError, match="valida"):
        preparar_avaliacao(dados)


def test_rejeita_comparacao_sem_validacao():
    dados = previsoes().query("fase == 'teste'")
    with pytest.raises(ValueError, match="valida"):
        preparar_avaliacao(dados)


def test_rejeita_duplicata_antes_do_pareamento():
    dados = previsoes()
    dados = pd.concat([dados, dados.iloc[[7]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplic"):
        preparar_avaliacao(dados)


@pytest.mark.parametrize("modelo", ["persistencia", "linear_simples"])
def test_rejeita_par_ausente_nos_dois_sentidos(modelo):
    dados = previsoes()
    dados = dados[~(dados.fase.eq("teste") & dados.codigo.eq("001") & dados.modelo.eq(modelo))]
    with pytest.raises(ValueError, match="pares|pareamento"):
        preparar_avaliacao(dados)


@pytest.mark.parametrize("coluna,valor", [
    ("custo_observado", 100.1),
    ("competencia_t", "2026-01"),
    ("data_corte", "2026-03-11"),
    ("treino_ate", "2026-01"),
])
def test_rejeita_pares_com_janelas_ou_observado_diferentes(coluna, valor):
    dados = previsoes()
    dados.loc[6, coluna] = valor
    with pytest.raises(ValueError):
        preparar_avaliacao(dados)


@pytest.mark.parametrize("coluna", ["custo_observado", "custo_previsto", "custo_t"])
@pytest.mark.parametrize("valor", [0.0, -1.0, float("nan"), float("inf")])
def test_rejeita_custos_nao_positivos_ou_nao_finitos(coluna, valor):
    dados = previsoes()
    dados.loc[7, coluna] = valor
    with pytest.raises(ValueError, match="positivos|finitos"):
        preparar_avaliacao(dados)


def test_rejeita_baseline_que_nao_repete_custo_atual():
    dados = previsoes()
    dados.loc[6, "custo_previsto"] = 91.0
    with pytest.raises(ValueError, match="persist"):
        preparar_avaliacao(dados)


def test_candidato_descartado_na_validacao_nao_afeta_relatorio():
    dados = previsoes()
    dados.loc[2, "custo_previsto"] = -100.0
    assert len(preparar_avaliacao(dados)) == 2


def test_resumo_percentual_calculado_das_linhas_sem_media_de_medias():
    pareado = preparar_avaliacao(previsoes())
    extra = pareado.iloc[[0]].assign(codigo="003", grupo="Estruturas", unidade="M3")
    dados = pd.concat([pareado, extra], ignore_index=True)
    resumo = resumir_avaliacao(dados, ["fonte"]).iloc[0]
    assert resumo["n"] == 3
    assert resumo.n_servicos == 3
    assert resumo.n_meses == 1
    assert resumo.mape == pytest.approx(20 / 3)
    assert resumo.mdape == 5
    assert resumo.p90 == pytest.approx(9)
    assert resumo.mape_persistencia == pytest.approx(40 / 3)
    assert resumo.ganho_mape_pct == pytest.approx(50)
    assert resumo.dentro_5_pct == pytest.approx(200 / 3)
    assert resumo.vies_pct == pytest.approx(0)
    assert "mae" not in resumo.index
    assert "rmse" not in resumo.index


def test_custos_monetarios_sao_resumidos_apenas_em_recortes():
    pareado = preparar_avaliacao(previsoes())
    extra = pareado.iloc[[0]].assign(codigo="003", unidade="M3", grupo="Estruturas")
    resumo = resumir_recortes(pd.concat([pareado, extra], ignore_index=True))
    assert len(resumo) == 2
    pintura = resumo.loc[resumo.grupo.eq("Pintura")].iloc[0]
    assert pintura.mae == pytest.approx(12.5)
    assert pintura.mse == pytest.approx(212.5)
    assert pintura.rmse == pytest.approx(np.sqrt(212.5))
    assert pintura.mae_persistencia == pytest.approx(25)
    assert pintura.r2 == pytest.approx(1 - 425 / 5000)
    assert pd.isna(resumo.loc[resumo.grupo.eq("Estruturas"), "r2"].iloc[0])


def test_baseline_perfeito_nao_produz_infinito_nem_ganho_inventado():
    pareado = preparar_avaliacao(previsoes())
    pareado["previsto_persistencia"] = pareado.custo_observado
    resumo = resumir_avaliacao(pareado, ["fonte"]).iloc[0]
    assert resumo.mape_persistencia == 0
    assert pd.isna(resumo.ganho_mape_pct)
    assert resumo.dentro_5_pct_persistencia == 100


def test_n_servicos_distingue_codigos_identicos_entre_fontes():
    pareado = preparar_avaliacao(previsoes())
    outro = pareado.assign(fonte="der_es")
    resumo = resumir_avaliacao(pd.concat([pareado, outro], ignore_index=True), [])
    assert resumo.iloc[0].n_servicos == 4


def test_r2_indefinido_quando_observado_constante():
    pareado = preparar_avaliacao(previsoes())
    pareado["custo_observado"] = 100.0
    resumo = resumir_recortes(pareado).iloc[0]
    assert pd.isna(resumo.r2)
    assert pd.isna(resumo.r2_persistencia)


def test_rejeita_agrupamento_que_seleciona_por_erro():
    pareado = preparar_avaliacao(previsoes())
    with pytest.raises(ValueError, match="agrupamento"):
        resumir_avaliacao(pareado, ["ape"])


def test_resumo_vazio_tem_schema_estavel():
    pareado = preparar_avaliacao(previsoes()).iloc[:0]
    resumo = resumir_avaliacao(pareado, ["fonte", "grupo"])
    assert resumo.empty
    assert {"fonte", "grupo", "n", "mape", "ganho_mape_pct"}.issubset(resumo.columns)
