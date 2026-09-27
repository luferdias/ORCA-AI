"""Regressão de uma competência à frente, com avaliação cronológica.

Custos publicados são alvos referenciais, não custos reais de execução.
Cada chamada trabalha com uma única fonte e um único regime.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd


COLUNAS = [
    "fonte", "competencia", "codigo", "descricao", "unidade", "grupo", "custo",
    "regime", "publicado_em", "arquivo_sha256", "localizador", "assinatura_tecnica",
]
ATRIBUTOS = {"linear_simples": ["custo_t"], "linear_multipla": ["custo_t", "custo_t_1", "custo_t_2"]}


def _normalizar(df: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(COLUNAS) - set(df.columns))
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")
    data = df[COLUNAS].copy()
    if data.empty:
        raise ValueError("Nenhum registro recebido")
    for column in ["fonte", "regime", "codigo", "competencia", "unidade", "grupo", "assinatura_tecnica"]:
        data[column] = data[column].astype("string").str.strip()
    for column in ["fonte", "regime"]:
        if data[column].isna().any() or data[column].eq("").any() or data[column].nunique() != 1:
            raise ValueError(f"A execução exige {column} única e preenchida")
    if data["codigo"].isna().any() or data["codigo"].eq("").any():
        raise ValueError("Código ausente")
    if not data["competencia"].str.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", na=False).all():
        raise ValueError("Competências devem usar YYYY-MM")
    if data.duplicated(["codigo", "competencia"]).any():
        raise ValueError("Mais de uma edição/revisão do mesmo código e competência; selecione a revisão explicitamente")
    data["custo"] = pd.to_numeric(data["custo"], errors="coerce")
    data["_periodo"] = pd.PeriodIndex(data["competencia"], freq="M").asi8
    data["_publicado"] = pd.to_datetime(data["publicado_em"], errors="coerce", utc=True).dt.tz_localize(None)
    return data.sort_values(["codigo", "competencia"]).reset_index(drop=True)


def construir_supervisionado(df: pd.DataFrame) -> pd.DataFrame:
    """Crie janelas consecutivas, com entradas t-2,t-1,t estáveis e custo alvo.

    A assinatura controla os campos técnicos disponíveis (no DER, somente
    descrição/unidade). Uma alteração em t+1 é anotada, sem escolher a
    amostra pela estabilidade futura. O SHA-256 do arquivo rastreia a edição.
    Datas faltantes continuam ausentes; não são inferidas da competência.
    """
    data = _normalizar(df)
    grouped = data.groupby("codigo", sort=False)
    offsets = {2: grouped.shift(2), 1: grouped.shift(1), 0: data, -1: grouped.shift(-1)}
    valid = pd.Series(True, index=data.index)
    for offset, frame in offsets.items():
        valid &= frame["_periodo"].eq(data["_periodo"] - offset)
        valid &= np.isfinite(frame["custo"]) & frame["custo"].gt(0)
        if offset >= 0:
            for column in ["assinatura_tecnica", "unidade", "grupo"]:
                valid &= frame[column].eq(data[column]).fillna(False)
                valid &= frame[column].notna() & frame[column].ne("").fillna(False)
    out = data[["fonte", "regime", "codigo", "descricao", "grupo", "unidade", "assinatura_tecnica", "arquivo_sha256", "localizador"]].copy()
    out["competencia_t"] = data["competencia"]
    out["competencia_alvo"] = offsets[-1]["competencia"]
    out["unidade_alvo"] = offsets[-1]["unidade"]
    out["grupo_alvo"] = offsets[-1]["grupo"]
    out["unidade_alvo_compativel"] = offsets[-1]["unidade"].eq(data["unidade"]).fillna(False)
    out["mudanca_tecnica_alvo"] = (
        ~offsets[-1]["assinatura_tecnica"].eq(data["assinatura_tecnica"]).fillna(False)
        | ~offsets[-1]["grupo"].eq(data["grupo"]).fillna(False)
        | ~out["unidade_alvo_compativel"]
    )
    for offset, column in [(0, "custo_t"), (1, "custo_t_1"), (2, "custo_t_2"), (-1, "custo_alvo")]:
        out[column] = offsets[offset]["custo"]
    dates = pd.concat([offsets[o]["_publicado"] for o in [0, 1, 2]], axis=1)
    out["data_corte"] = dates.max(axis=1).where(dates.notna().all(axis=1))
    out["publicado_alvo"] = offsets[-1]["_publicado"]
    out["publicacao_completa"] = dates.notna().all(axis=1) & out["publicado_alvo"].notna()
    out["admissivel_publicacao"] = out["publicacao_completa"] & out["publicado_alvo"].gt(out["data_corte"])
    out["arquivo_sha256_alvo"] = offsets[-1]["arquivo_sha256"]
    out = out.loc[valid].reset_index(drop=True)
    out.attrs["linhas_origem"] = len(data)
    out.attrs["janelas_validas"] = len(out)
    out.attrs["linhas_sem_janela_valida"] = len(data) - len(out)
    return out


def _metricas(frame: pd.DataFrame, baseline_mse: float) -> dict:
    observed = frame["custo_observado"].to_numpy(float)
    errors = frame["custo_previsto"].to_numpy(float) - observed
    mse = float(np.mean(errors ** 2))
    denominator = float(np.sum((observed - observed.mean()) ** 2))
    return {
        "n": len(frame), "n_servicos": int(frame["codigo"].nunique()),
        "n_alteracoes_tecnicas_alvo": int(frame["mudanca_tecnica_alvo"].sum()),
        "mse": mse, "mae": float(np.mean(np.abs(errors))), "rmse": float(np.sqrt(mse)),
        "r2": float(1 - np.sum(errors ** 2) / denominator) if denominator > 0 else None,
        "r2_status": "calculado" if denominator > 0 else "alvo_constante",
        "ganho_mse_percentual": 100.0 * (baseline_mse - mse) / baseline_mse if baseline_mse > 0 else None,
    }


def _janelas_futuras(data: pd.DataFrame) -> pd.DataFrame:
    """Últimas três competências, sem criar observações/alvos sintéticos."""
    grouped = data.groupby("codigo", sort=False)
    past1, past2 = grouped.shift(1), grouped.shift(2)
    valid = data["competencia"].eq(data["competencia"].max())
    for offset, frame in [(0, data), (1, past1), (2, past2)]:
        valid &= frame["_periodo"].eq(data["_periodo"] - offset)
        valid &= np.isfinite(frame["custo"]) & frame["custo"].gt(0)
        for column in ["grupo", "unidade", "assinatura_tecnica"]:
            valid &= frame[column].eq(data[column]).fillna(False)
            valid &= frame[column].notna() & frame[column].ne("").fillna(False)
    out = data[["fonte", "regime", "codigo", "descricao", "grupo", "unidade", "arquivo_sha256", "assinatura_tecnica"]].copy()
    out["competencia_t"] = data["competencia"]
    out["competencia_alvo"] = (pd.PeriodIndex(data["competencia"], freq="M") + 1).astype(str)
    out["custo_t"], out["custo_t_1"], out["custo_t_2"] = data["custo"], past1["custo"], past2["custo"]
    dates = pd.concat([f["_publicado"] for f in [data, past1, past2]], axis=1)
    out["data_corte"] = dates.max(axis=1).where(dates.notna().all(axis=1))
    return out.loc[valid].reset_index(drop=True)


def _plotar(predictions: pd.DataFrame, output: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    selected = predictions[(predictions.fase == "teste") & predictions.modelo_selecionado]
    if selected.empty:
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    # Cada gráfico preserva as unidades: um painel usa somente um recorte.
    first = selected[["grupo", "unidade"]].drop_duplicates().iloc[0]
    one = selected[(selected.grupo == first.grupo) & (selected.unidade == first.unidade)]
    lo = min(one.custo_observado.min(), one.custo_previsto.min())
    hi = max(one.custo_observado.max(), one.custo_previsto.max())
    axes[0].scatter(one.custo_observado, one.custo_previsto, alpha=.6, s=14)
    axes[0].plot([lo, hi], [lo, hi], color="black", linestyle="--")
    axes[0].set(xlabel=f"Observado (R$/{first.unidade})", ylabel=f"Previsto (R$/{first.unidade})")
    means = one.groupby("competencia_alvo")[["custo_observado", "custo_previsto"]].mean()
    means.plot(ax=axes[1], marker="o")
    axes[1].set(xlabel="Competência", ylabel=f"Média no recorte (R$/{first.unidade})")
    fig.suptitle(f"Teste congelado — {first.grupo} / {first.unidade}")
    fig.tight_layout()
    fig.savefig(output / "observado_previsto.png", dpi=140)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(one.custo_observado, one.erro, alpha=.6, s=14)
    ax.axhline(0, color="black", linestyle="--")
    ax.set(xlabel=f"Custo observado (R$/{first.unidade})", ylabel=f"Previsto − observado (R$/{first.unidade})", title=f"Resíduos no teste — {first.grupo}")
    fig.tight_layout()
    fig.savefig(output / "erros.png", dpi=140)
    plt.close(fig)


def executar_experimento(df: pd.DataFrame, output_dir: str | Path, config: dict | None = None) -> dict:
    """Avalie regressão simples/múltipla e persistência com cortes globais.

    A seleção usa apenas MSE de validação. Os coeficientes são reajustados
    uma vez antes do teste; durante o teste somente as entradas são atualizadas.
    Depois de gravar a avaliação, outro ajuste usa o histórico completo para
    um cenário da próxima competência, salvo separadamente.
    """
    import joblib
    import sklearn
    from sklearn.linear_model import LinearRegression

    settings = {
        "meses_teste": 3, "meses_validacao": 2, "min_amostras_treino": 12,
        "min_servicos": 3, "min_amostras_validacao": 3, "min_amostras_teste": 3,
    }
    unknown = set(config or {}) - set(settings)
    if unknown:
        raise ValueError(f"Configuração desconhecida: {sorted(unknown)}")
    settings.update(config or {})
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 1 for v in settings.values()):
        raise ValueError("Os limites e números de competências devem ser inteiros positivos")
    data = _normalizar(df)
    modelable = construir_supervisionado(df)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    # A entrada original não é modificada. Este CSV registra as janelas derivadas.
    modelable.to_csv(output / "dataset_modelavel.csv", index=False)
    months = sorted(data.competencia.unique().tolist())
    n_test, n_val = settings["meses_teste"], settings["meses_validacao"]
    test_months = months[-n_test:]
    validation_months = months[-n_test-n_val:-n_test]
    dates_complete = bool(data._publicado.notna().all())
    forbidden = modelable.publicacao_completa & ~modelable.admissivel_publicacao
    incompatible_unit = ~modelable.unidade_alvo_compativel
    eligible = modelable.loc[~forbidden & ~incompatible_unit].copy()
    modelable["particao"] = np.select(
        [modelable.competencia_alvo.isin(test_months), modelable.competencia_alvo.isin(validation_months)],
        ["teste", "validacao"], default="treino",
    )
    modelable["excluido_publicacao"] = forbidden
    modelable["excluido_unidade_alvo"] = incompatible_unit
    modelable.to_csv(output / "particoes.csv", index=False)
    digest = hashlib.sha256(data[COLUNAS].to_csv(index=False).encode()).hexdigest()
    signature_types = sorted(df["assinatura_tipo"].dropna().astype(str).unique().tolist()) if "assinatura_tipo" in df else ["nao_informado"]
    summary = {
        "status": "dados_insuficientes", "fonte": str(data.fonte.iloc[0]), "regime": str(data.regime.iloc[0]),
        "modo_avaliacao": "retrospectivo_com_controle_publicacao" if dates_complete else "retrospectivo_historico_revisado",
        "previsao_prospectiva_comprovada": False,
        "limites": ["Backtest retrospectivo com as revisões fornecidas; não comprova uma previsão emitida no passado."],
        "tipos_assinatura": signature_types, "config": settings,
        "competencias_validacao": validation_months, "competencias_teste": test_months,
        "linhas_origem": len(data), "janelas_modelaveis": len(modelable),
        "janelas_excluidas_publicacao": int(forbidden.sum()),
        "janelas_excluidas_unidade_alvo": int(incompatible_unit.sum()),
        "janelas_com_mudanca_tecnica_alvo": int(modelable.mudanca_tecnica_alvo.sum()),
        "unidades_metricas": {"mae_rmse": "R$/unidade do recorte", "mse": "(R$/unidade do recorte)^2", "r2": "adimensional"},
        "dataset_sha256": digest,
        "arquivos_sha256": sorted(data.arquivo_sha256.dropna().astype(str).unique().tolist()),
        "versoes": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__},
        "recortes": [],
    }
    if not dates_complete:
        summary["limites"].append("Publicação ausente/inválida em parte do histórico: disponibilidade real no passado não comprovada; datas não foram inferidas.")
    if "descricao_unidade" in signature_types or "nao_informado" in signature_types:
        summary["limites"].append("Assinatura técnica parcial ou não documentada: estabilidade da composição analítica não comprovada.")
    summary["limites"].append("Mudanças técnicas no alvo são mantidas e identificadas. Mudanças de unidade no alvo são excluídas da comparação monetária e registradas nas partições; a avaliação requer alvo publicado com custo positivo.")
    predictions, metrics, fitted_groups = [], [], []
    enough_months = len(months) > n_test + n_val and len(validation_months) == n_val

    for (group, unit), subset in eligible.groupby(["grupo", "unidade"], sort=True):
        report = {"grupo": str(group), "unidade": str(unit), "status": "dados_insuficientes"}
        summary["recortes"].append(report)
        if not enough_months:
            report["motivo"] = "Competências insuficientes para treino, validação e teste globais"
            continue
        train = subset[subset.competencia_alvo < validation_months[0]].copy()
        validation = subset[subset.competencia_alvo.isin(validation_months)].copy()
        final_train = subset[subset.competencia_alvo < test_months[0]].copy()
        test = subset[subset.competencia_alvo.isin(test_months)].copy()
        # A escolha do algoritmo também é uma decisão anterior ao teste.
        # Ela não pode usar um rótulo de validação publicado depois da origem.
        test_origin = test.data_corte.min()
        late_validation = pd.Series(False, index=validation.index)
        if pd.notna(test_origin):
            late_validation = validation.publicado_alvo.notna() & validation.publicado_alvo.gt(test_origin)
        report["n_validacao_excluida_publicacao_tardia"] = int(late_validation.sum())
        validation = validation.loc[~late_validation].copy()
        # Com datas conhecidas, o ajuste fixo de cada fase só vê alvos publicados
        # até a primeira origem de previsão daquela fase.
        for training, forecast in [(train, validation), (final_train, test)]:
            first_origin = forecast.data_corte.min()
            if pd.notna(first_origin):
                invalid = training.publicado_alvo.notna() & training.publicado_alvo.gt(first_origin)
                training.drop(index=training.index[invalid], inplace=True)
        report.update({"n_treino": len(train), "n_validacao": len(validation), "n_treino_teste": len(final_train), "n_teste": len(test), "servicos_treino": int(train.codigo.nunique())})
        if (len(train) < settings["min_amostras_treino"] or len(final_train) < settings["min_amostras_treino"]
                or train.codigo.nunique() < settings["min_servicos"]
                or len(validation) < settings["min_amostras_validacao"] or len(test) < settings["min_amostras_teste"]):
            report["motivo"] = "Recorte sem amostras/serviços suficientes nos cortes globais"
            continue
        validation_models, validation_mses = {}, {}
        for name, features in ATRIBUTOS.items():
            model = LinearRegression().fit(train[features], train.custo_alvo)
            validation_models[name] = model
            validation_mses[name] = float(np.mean((model.predict(validation[features]) - validation.custo_alvo.to_numpy()) ** 2))
        selected = "linear_simples"
        if validation_mses["linear_multipla"] < validation_mses["linear_simples"] - 1e-12:
            selected = "linear_multipla"
        baseline_val_mse = float(np.mean((validation.custo_t - validation.custo_alvo) ** 2))
        report.update({"status": "avaliado", "modelo_selecionado": selected, "mse_validacao": validation_mses,
                       "mse_persistencia_validacao": baseline_val_mse,
                       "supera_persistencia_validacao": validation_mses[selected] < baseline_val_mse - 1e-12})
        for phase, training, forecast in [("validacao", train, validation), ("teste", final_train, test)]:
            baseline_mse = float(np.mean((forecast.custo_t - forecast.custo_alvo) ** 2))
            for name in ["persistencia", *ATRIBUTOS]:
                if name == "persistencia":
                    values = forecast.custo_t.to_numpy()
                else:
                    model = validation_models[name] if phase == "validacao" else LinearRegression().fit(training[ATRIBUTOS[name]], training.custo_alvo)
                    values = model.predict(forecast[ATRIBUTOS[name]])
                result = forecast.copy()
                result["fase"], result["modelo"] = phase, name
                result["modelo_selecionado"] = name == selected
                result["custo_observado"], result["custo_previsto"] = result.custo_alvo, values
                result["erro"] = result.custo_previsto - result.custo_observado
                result["treino_ate"] = training.competencia_alvo.max()
                result["treino_publicado_ate"] = training.publicado_alvo.max()
                result["modo_avaliacao"] = summary["modo_avaliacao"]
                predictions.append(result)
                metric = {"fonte": summary["fonte"], "grupo": str(group), "unidade": str(unit), "fase": phase,
                          "modelo": name, "modelo_selecionado": name == selected, **_metricas(result, baseline_mse)}
                metrics.append(metric)
        fitted_groups.append((group, unit, selected, subset))

    all_predictions = pd.concat(predictions, ignore_index=True) if predictions else pd.DataFrame(columns=["fase", "modelo", "grupo", "unidade", "custo_observado", "custo_previsto"])
    all_predictions.to_csv(output / "previsoes_avaliacao.csv", index=False)
    metric_columns = ["fonte", "grupo", "unidade", "fase", "modelo", "modelo_selecionado", "n", "n_servicos", "n_alteracoes_tecnicas_alvo", "mse", "mae", "rmse", "r2", "r2_status", "ganho_mse_percentual"]
    pd.DataFrame(metrics, columns=metric_columns).to_csv(output / "metricas.csv", index=False)
    (output / "metricas.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    if predictions:
        _plotar(all_predictions, output)
    # A avaliação já está materializada; este refit não altera suas métricas.
    future = _janelas_futuras(data)
    future_predictions = []
    for group, unit, selected, subset in fitted_groups:
        forecast = future[(future.grupo == group) & (future.unidade == unit)].copy()
        if forecast.empty:
            continue
        final_model = LinearRegression().fit(subset[ATRIBUTOS[selected]], subset.custo_alvo)
        model_id = hashlib.sha256(f"{group}\0{unit}".encode()).hexdigest()[:16]
        model_path = output / "modelos" / f"{model_id}.joblib"
        model_path.parent.mkdir(exist_ok=True)
        joblib.dump({"modelo": final_model, "atributos": ATRIBUTOS[selected], "grupo": group, "unidade": unit,
                     "treino_ate": subset.competencia_alvo.max(), "dataset_sha256": digest, "versoes": summary["versoes"]}, model_path)
        for name, values in [(selected, final_model.predict(forecast[ATRIBUTOS[selected]])), ("persistencia", forecast.custo_t.to_numpy())]:
            result = forecast.copy()
            result["modelo"], result["custo_previsto"] = name, values
            result["custo_observado"] = np.nan
            result["treino_ate"] = subset.competencia_alvo.max()
            result["modelo_arquivo"] = str(model_path.name) if name != "persistencia" else ""
            result["dataset_sha256"] = digest
            result["tipo_resultado"] = "cenario_proxima_competencia_sem_observacao"
            future_predictions.append(result)
    future_output = pd.concat(future_predictions, ignore_index=True) if future_predictions else pd.DataFrame(columns=["codigo", "competencia_alvo", "modelo", "custo_previsto", "custo_observado"])
    future_output.to_csv(output / "previsoes_proxima_competencia.csv", index=False)
    summary["previsoes_futuras"] = len(future_output)
    if predictions:
        summary["status"] = "concluido" if all(r["status"] == "avaliado" for r in summary["recortes"]) else "parcial"
    (output / "resumo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    return summary
