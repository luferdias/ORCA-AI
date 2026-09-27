"""Comparações pareadas e estatísticas descritivas do relatório didático.

Cada observação é um serviço em uma competência. Comparamos apenas o algoritmo
linear escolhido na validação com a persistência nas mesmas observações de teste.
MAPE/MdAPE/P90 e viés são percentuais por observação, sem ponderação pelo preço.
Nenhum resumo aqui é uma prova de significância ou de desempenho prospectivo.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


CHAVES = ["fonte", "grupo", "unidade", "codigo", "competencia_alvo"]
RECORTES = ["fonte", "grupo", "unidade"]
LINEARES = {"linear_simples", "linear_multipla"}
AGRUPAMENTOS = {
    "fonte", "grupo", "unidade", "codigo", "regime", "modelo",
    "competencia_alvo", "modo_avaliacao", "nicho_id", "nicho", "nicho_nome",
    "nome_nicho", "macrogrupo", "grupo_didatico",
}
METRICAS_PERCENTUAIS = [
    "n", "n_servicos", "n_meses", "modelos", "competencia_inicio", "competencia_fim",
    "mape", "mdape", "p90", "q1_ape", "q3_ape", "mape_persistencia",
    "mdape_persistencia", "p90_persistencia", "ganho_mape_pct", "dentro_5_pct",
    "dentro_5_pct_persistencia", "vies_pct", "vies_pct_persistencia",
]
METRICAS_MONETARIAS = [
    "mae", "rmse", "mse", "r2", "mae_persistencia", "rmse_persistencia",
    "mse_persistencia", "r2_persistencia", "ganho_mse_pct",
]


def _exigir_colunas(frame: pd.DataFrame, colunas: list[str]) -> None:
    faltantes = sorted(set(colunas) - set(frame.columns))
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")


def _validar_positivos(frame: pd.DataFrame, colunas: list[str]) -> None:
    for coluna in colunas:
        try:
            valores = pd.to_numeric(frame[coluna], errors="raise").to_numpy(dtype=float)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{coluna} deve conter números positivos e finitos.") from exc
        if not (np.isfinite(valores).all() and (valores > 0).all()):
            raise ValueError(f"{coluna} deve conter números positivos e finitos.")


def _iguais(a: pd.Series, b: pd.Series) -> pd.Series:
    """Igualdade de metadados, incluindo ausente nos dois lados."""
    return a.eq(b).fillna(False) | (a.isna() & b.isna())


def preparar_avaliacao(previsoes: pd.DataFrame) -> pd.DataFrame:
    """Valida o CSV completo e pareia linear escolhido x persistência no teste.

    Preserva todas as colunas da previsão linear. Adiciona previsto_persistencia,
    erro_abs (na unidade monetária original), erro_pct, ape, ape_persistencia e
    erro_pct_persistencia (estes quatro últimos em porcentagem). Viés positivo
    significa previsão acima do observado.

    Não escolhe o algoritmo a partir dos erros de teste. Uma flag de seleção em
    formato textual ou numérico é rejeitada: ``"False"`` não pode virar True por
    coerção. As colunas de data e janela, quando presentes, precisam coincidir.
    """
    obrigatorias = CHAVES + [
        "fase", "modelo", "modelo_selecionado", "competencia_t",
        "custo_t", "custo_observado", "custo_previsto",
    ]
    _exigir_colunas(previsoes, obrigatorias)
    dados = previsoes.copy()
    if dados.empty:
        raise ValueError("Não há previsões de validação e teste para comparar.")
    if not dados.modelo_selecionado.map(lambda x: isinstance(x, (bool, np.bool_))).all():
        raise ValueError("modelo_selecionado deve conter valores booleanos reais.")
    if dados[CHAVES + ["fase", "modelo", "competencia_t"]].isna().any().any():
        raise ValueError("Chaves e competências não podem estar ausentes.")
    if dados[CHAVES].astype(str).apply(lambda c: c.str.strip().eq("")).any().any():
        raise ValueError("Chaves de pareamento não podem estar vazias.")
    if not dados.fase.isin(["validacao", "teste"]).all():
        raise ValueError("A avaliação aceita somente as fases validacao e teste.")
    if not dados.modelo.isin(LINEARES | {"persistencia"}).all():
        raise ValueError("Modelo desconhecido no arquivo de avaliação.")
    if dados.duplicated(CHAVES + ["fase", "modelo"]).any():
        raise ValueError("Previsões duplicadas nas chaves de pareamento.")
    _validar_positivos(dados, ["custo_t", "custo_observado"])
    for coluna in ("competencia_t", "competencia_alvo"):
        if not dados[coluna].astype(str).str.fullmatch(r"\d{4}-(0[1-9]|1[0-2])").all():
            raise ValueError(f"Competência inválida em {coluna}; esperado YYYY-MM.")
    origens = pd.PeriodIndex(dados.competencia_t, freq="M")
    alvos = pd.PeriodIndex(dados.competencia_alvo, freq="M")
    if not ((origens + 1) == alvos).all():
        raise ValueError("A competência alvo deve ser o mês seguinte à origem.")
    if "regime" in dados and dados.groupby("fonte").regime.nunique(dropna=False).gt(1).any():
        raise ValueError("Não misture regimes na avaliação de uma fonte.")
    selecionados = dados.loc[dados.modelo_selecionado]
    if not selecionados.modelo.isin(LINEARES).all():
        raise ValueError("O modelo selecionado na validação precisa ser linear.")
    escolhas = selecionados[RECORTES + ["fase", "modelo"]].drop_duplicates()
    if escolhas.duplicated(RECORTES + ["fase"]).any():
        raise ValueError("Mais de um modelo foi selecionado no mesmo recorte/fase.")
    val = escolhas.loc[escolhas.fase.eq("validacao"), RECORTES + ["modelo"]]
    teste = escolhas.loc[escolhas.fase.eq("teste"), RECORTES + ["modelo"]]
    if val.empty or teste.empty:
        raise ValueError("São necessárias seleções nas fases validação e teste.")
    conferir = val.merge(teste, on=RECORTES, how="outer", suffixes=("_val", "_teste"), indicator=True)
    if not conferir._merge.eq("both").all() or not conferir.modelo_val.eq(conferir.modelo_teste).all():
        raise ValueError("A escolha de teste precisa coincidir com a escolha na validação.")

    lin = selecionados.loc[selecionados.fase.eq("teste")].copy()
    base = dados.loc[dados.fase.eq("teste") & dados.modelo.eq("persistencia")].copy()
    # Um candidato descartado na validação pode ter feito previsões negativas.
    # Ele não entra no relatório; exigir positividade nele apagaria uma execução
    # válida. As previsões efetivamente comparadas continuam sendo verificadas.
    _validar_positivos(lin, ["custo_previsto"])
    _validar_positivos(base, ["custo_previsto"])
    if lin.duplicated(CHAVES).any() or base.duplicated(CHAVES).any():
        raise ValueError("Duplicação impede pareamento um a um.")
    cobertura = lin[CHAVES].merge(base[CHAVES], on=CHAVES, how="outer", indicator=True)
    if not cobertura._merge.eq("both").all():
        raise ValueError("Há observações sem pares entre modelo e persistência.")
    if not np.allclose(base.custo_previsto, base.custo_t, rtol=1e-12, atol=1e-10):
        raise ValueError("A previsão de persistência precisa repetir o custo atual.")
    correspondencias = [
        "competencia_t", "regime", "custo_t", "custo_observado", "data_corte",
        "publicado_alvo", "treino_ate", "treino_publicado_ate", "unidade_alvo",
        "grupo_alvo", "modo_avaliacao", "arquivo_sha256", "arquivo_sha256_alvo",
    ]
    presentes = [c for c in correspondencias if c in dados]
    par = lin.merge(
        base[CHAVES + presentes + ["custo_previsto"]],
        on=CHAVES, how="inner", validate="one_to_one", suffixes=("", "_baseline"),
    )
    for coluna in presentes:
        if coluna in {"custo_t", "custo_observado"}:
            confere = np.isclose(par[coluna], par[f"{coluna}_baseline"], rtol=1e-12, atol=1e-10)
        else:
            confere = _iguais(par[coluna], par[f"{coluna}_baseline"])
        if not confere.all():
            raise ValueError(f"Os pares divergem em {coluna}; não use janelas ou observações diferentes.")
    par = par.rename(columns={"custo_previsto_baseline": "previsto_persistencia"})
    par = par.drop(columns=[f"{c}_baseline" for c in presentes])
    par["erro_abs"] = (par.custo_previsto - par.custo_observado).abs()
    par["erro_pct"] = 100 * (par.custo_previsto - par.custo_observado) / par.custo_observado
    par["ape"] = par.erro_pct.abs()
    par["erro_pct_persistencia"] = 100 * (par.previsto_persistencia - par.custo_observado) / par.custo_observado
    par["ape_persistencia"] = par.erro_pct_persistencia.abs()
    return par.sort_values(CHAVES).reset_index(drop=True)


def _preparar_resumo(frame: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    if len(colunas) != len(set(colunas)) or set(colunas) - AGRUPAMENTOS:
        raise ValueError("Colunas de agrupamento precisam descrever fontes, grupos, serviços ou competências.")
    _exigir_colunas(frame, ["fonte", "codigo", "competencia_alvo", "modelo", "custo_observado", "custo_previsto", "previsto_persistencia"] + colunas)
    if frame[colunas].isna().any().any():
        raise ValueError("Valores ausentes nas colunas de agrupamento.")
    _validar_positivos(frame, ["custo_observado", "custo_previsto", "previsto_persistencia"])
    # Recalcular evita usar colunas de erro antigas depois de filtrar/atualizar valores.
    dados = frame.copy()
    dados["erro_pct"] = 100 * (dados.custo_previsto - dados.custo_observado) / dados.custo_observado
    dados["ape"] = dados.erro_pct.abs()
    dados["erro_pct_persistencia"] = 100 * (dados.previsto_persistencia - dados.custo_observado) / dados.custo_observado
    dados["ape_persistencia"] = dados.erro_pct_persistencia.abs()
    return dados


def _percentuais(grupo: pd.DataFrame) -> dict:
    mape = float(grupo.ape.mean())
    base = float(grupo.ape_persistencia.mean())
    return {
        "n": len(grupo),
        "n_servicos": len(grupo[["fonte", "codigo"]].drop_duplicates()),
        "n_meses": int(grupo.competencia_alvo.nunique()),
        "modelos": ", ".join(sorted(grupo.modelo.unique())),
        "competencia_inicio": grupo.competencia_alvo.min(),
        "competencia_fim": grupo.competencia_alvo.max(),
        "mape": mape, "mdape": float(grupo.ape.median()),
        "p90": float(grupo.ape.quantile(0.9)),
        "q1_ape": float(grupo.ape.quantile(0.25)),
        "q3_ape": float(grupo.ape.quantile(0.75)),
        "mape_persistencia": base,
        "mdape_persistencia": float(grupo.ape_persistencia.median()),
        "p90_persistencia": float(grupo.ape_persistencia.quantile(0.9)),
        "ganho_mape_pct": 100 * (base - mape) / base if base > 0 else None,
        "dentro_5_pct": float((grupo.ape <= 5 + 1e-10).mean() * 100),
        "dentro_5_pct_persistencia": float((grupo.ape_persistencia <= 5 + 1e-10).mean() * 100),
        "vies_pct": float(grupo.erro_pct.mean()),
        "vies_pct_persistencia": float(grupo.erro_pct_persistencia.mean()),
    }


def resumir_avaliacao(frame: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    """Resume porcentagens diretamente das linhas, com peso igual por serviço-mês.

    MAPE é a média do erro percentual absoluto; MdAPE é a mediana; P90 é o
    percentil 90 (interpolação linear). Dentro de 5% usa um limiar didático,
    não um limite normativo. Ganho positivo significa menor MAPE que a
    persistência. Com erro basal zero o ganho relativo é indefinido (None/NaN).

    Pode combinar unidades porque resume percentuais; não produz MAE ou RMSE
    monetários. Uma comparação agregada entre fontes continua sujeita às
    diferenças de composição dos serviços. Use colunas=[] para um total.
    """
    dados = _preparar_resumo(frame, colunas)
    linhas = []
    if not dados.empty:
        grupos = dados.groupby(colunas, sort=True, dropna=False) if colunas else [((), dados)]
        for chave, grupo in grupos:
            chave = chave if isinstance(chave, tuple) else (chave,)
            linhas.append(dict(zip(colunas, chave)) | _percentuais(grupo))
    return pd.DataFrame(linhas, columns=colunas + METRICAS_PERCENTUAIS)


def _r2(observado: np.ndarray, previsto: np.ndarray) -> float | None:
    if len(observado) < 2 or np.all(observado == observado[0]):
        return None
    return float(1 - np.sum((previsto - observado) ** 2) / np.sum((observado - observado.mean()) ** 2))


def resumir_recortes(frame: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta métricas monetárias somente por fonte, grupo nativo e unidade.

    MAE/RMSE têm unidade R$/unidade; MSE tem (R$/unidade)^2. R² é indefinido
    para uma observação ou alvo constante. Não comparar magnitudes de erros
    monetários entre unidades diferentes, nem inferir equivalência técnica de
    serviços de fontes distintas apenas pelo nome do grupo.
    """
    dados = _preparar_resumo(frame, RECORTES)
    linhas = []
    for chave, grupo in dados.groupby(RECORTES, sort=True, dropna=False):
        observado = grupo.custo_observado.to_numpy(dtype=float)
        previsto = grupo.custo_previsto.to_numpy(dtype=float)
        base = grupo.previsto_persistencia.to_numpy(dtype=float)
        mse = float(np.mean((previsto - observado) ** 2))
        mse_base = float(np.mean((base - observado) ** 2))
        linhas.append(dict(zip(RECORTES, chave)) | _percentuais(grupo) | {
            "mae": float(np.mean(np.abs(previsto - observado))),
            "rmse": float(np.sqrt(mse)), "mse": mse, "r2": _r2(observado, previsto),
            "mae_persistencia": float(np.mean(np.abs(base - observado))),
            "rmse_persistencia": float(np.sqrt(mse_base)), "mse_persistencia": mse_base,
            "r2_persistencia": _r2(observado, base),
            "ganho_mse_pct": 100 * (mse_base - mse) / mse_base if mse_base > 0 else None,
        })
    return pd.DataFrame(linhas, columns=RECORTES + METRICAS_PERCENTUAIS + METRICAS_MONETARIAS)
