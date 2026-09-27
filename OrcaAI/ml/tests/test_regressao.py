"""Temporal safeguards; fixtures here are synthetic and never reported as results."""

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def painel(meses=16, servicos=4, publicado=False):
    rows = []
    for n, mes in enumerate(pd.period_range("2025-01", periods=meses, freq="M")):
        for s in range(servicos):
            rows.append({
                "fonte": "SINAPI", "competencia": str(mes), "codigo": f"00{s}",
                "descricao": f"Servico {s}", "unidade": "M2", "grupo": "PINTURA",
                "custo": 30.0 + 7 * s + 0.7 * n,
                "regime": "sem_desoneracao",
                "publicado_em": str((mes + 1).start_time.date()) if publicado else "",
                "arquivo_sha256": f"arquivo-{mes}", "localizador": f"A{s+1}",
                "assinatura_tecnica": f"estavel-{s}",
            })
    return pd.DataFrame(rows)


class RegressaoTest(unittest.TestCase):
    def setUp(self):
        module = Path(__file__).resolve().parents[1] / "orca_ml" / "regressao.py"
        self.assertTrue(module.exists(), "Falta o modulo real de regressao temporal")
        self.mod = importlib.import_module("orca_ml.regressao")

    def test_lags_exatos_e_hash_de_arquivo_nao_e_identidade_tecnica(self):
        result = self.mod.construir_supervisionado(painel(meses=4, servicos=1))
        self.assertEqual(len(result), 1)
        row = result.iloc[0]
        self.assertEqual(row["codigo"], "000")
        self.assertEqual(row["competencia_t"], "2025-03")
        self.assertEqual(row["competencia_alvo"], "2025-04")
        np.testing.assert_allclose(row[["custo_t", "custo_t_1", "custo_t_2"]].astype(float), [31.4, 30.7, 30.0])
        self.assertAlmostEqual(row["custo_alvo"], 32.1)

    def test_lacuna_assinatura_unidade_ou_custo_invalido_impedem_janela(self):
        original = painel(meses=4, servicos=1)
        cases = [original.drop(index=1)]
        for coluna, valor in [("assinatura_tecnica", "outra"), ("unidade", "M"), ("grupo", "OUTRO"), ("custo", 0), ("custo", np.nan), ("custo", np.inf)]:
            altered = original.copy()
            altered.loc[1, coluna] = valor
            cases.append(altered)
        for case in cases:
            with self.subTest(case=case.to_dict("records")):
                self.assertTrue(self.mod.construir_supervisionado(case).empty)

    def test_fontes_regimes_e_edicoes_duplicadas_sao_rejeitados(self):
        for coluna, valor in [("fonte", "DER_ES"), ("regime", "com_desoneracao")]:
            df = painel(meses=4)
            df.loc[0, coluna] = valor
            with self.assertRaises(ValueError):
                self.mod.construir_supervisionado(df)
        df = painel(meses=4)
        with self.assertRaises(ValueError):
            self.mod.construir_supervisionado(pd.concat([df, df.iloc[[0]]]))

    def test_publicacao_nao_e_inventada(self):
        row = self.mod.construir_supervisionado(painel(meses=4, servicos=1)).iloc[0]
        self.assertTrue(pd.isna(row["data_corte"]))
        self.assertFalse(row["publicacao_completa"])
        row = self.mod.construir_supervisionado(painel(meses=4, servicos=1, publicado=True)).iloc[0]
        self.assertEqual(str(pd.Timestamp(row["data_corte"]).date()), "2025-04-01")
        self.assertEqual(str(pd.Timestamp(row["publicado_alvo"]).date()), "2025-05-01")

    def executar(self, df, **config):
        self.assertTrue(hasattr(self.mod, "executar_experimento"), "Falta executar o experimento real")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name)
        summary = self.mod.executar_experimento(df, path, config)
        return summary, path

    def test_cortes_globais_e_predicoes_sem_treino_futuro(self):
        summary, path = self.executar(painel())
        self.assertEqual(summary["competencias_teste"], ["2026-02", "2026-03", "2026-04"])
        self.assertEqual(summary["competencias_validacao"], ["2025-12", "2026-01"])
        pred = pd.read_csv(path / "previsoes_avaliacao.csv")
        for fase, limite in [("validacao", "2025-12"), ("teste", "2026-02")]:
            subset = pred[pred.fase == fase]
            self.assertFalse(subset.empty)
            self.assertTrue((subset.treino_ate < limite).all())
            self.assertTrue((subset.treino_ate < subset.competencia_alvo).all())
        self.assertEqual(summary["modo_avaliacao"], "retrospectivo_historico_revisado")
        self.assertFalse(summary["previsao_prospectiva_comprovada"])
        self.assertTrue((path / "observado_previsto.png").is_file())
        self.assertTrue((path / "erros.png").is_file())

    def test_dados_de_teste_nao_escolhem_modelo(self):
        original = painel()
        summary1, path1 = self.executar(original)
        alterado = original.copy()
        alterado.loc[alterado.competencia == "2026-04", "custo"] += 5000
        summary2, path2 = self.executar(alterado)
        self.assertEqual(summary1["recortes"][0]["modelo_selecionado"], summary2["recortes"][0]["modelo_selecionado"])
        p1, p2 = [pd.read_csv(p / "previsoes_avaliacao.csv") for p in [path1, path2]]
        pd.testing.assert_frame_equal(p1[p1.fase == "validacao"], p2[p2.fase == "validacao"])
        p1 = p1[(p1.fase == "teste") & (p1.modelo != "persistencia")]
        p2 = p2[(p2.fase == "teste") & (p2.modelo != "persistencia")]
        np.testing.assert_allclose(p1.custo_previsto, p2.custo_previsto)

    def test_recorte_antigo_nao_redefine_periodo_global_de_teste(self):
        df = painel()
        antigo = painel(meses=10)
        antigo["codigo"] = "a" + antigo.codigo
        antigo["grupo"] = "ANTIGO"
        summary, path = self.executar(pd.concat([df, antigo], ignore_index=True))
        old = next(r for r in summary["recortes"] if r["grupo"] == "ANTIGO")
        self.assertEqual(old["status"], "dados_insuficientes")
        predictions = pd.read_csv(path / "previsoes_avaliacao.csv")
        self.assertNotIn("ANTIGO", set(predictions.grupo))

    def test_constante_nao_gera_infinito_nem_percentual_com_divisor_zero(self):
        df = painel()
        df["custo"] = 12.0
        summary, path = self.executar(df)
        metrics = json.loads((path / "metricas.json").read_text())
        self.assertTrue(metrics)
        self.assertTrue(all(m["mse"] == 0 for m in metrics))
        self.assertTrue(all(m["ganho_mse_percentual"] is None for m in metrics))
        self.assertTrue(all(m["r2"] is None for m in metrics))
        json.dumps(summary, allow_nan=False)

    def test_publicacao_futura_exclui_janelas_inadmissiveis(self):
        df = painel(publicado=True)
        df.loc[df.competencia.isin(["2025-08", "2025-09"]), "publicado_em"] = "2025-11-01"
        summary, path = self.executar(df)
        self.assertGreater(summary["janelas_excluidas_publicacao"], 0)
        pred = pd.read_csv(path / "previsoes_avaliacao.csv")
        self.assertTrue((pd.to_datetime(pred.publicado_alvo) > pd.to_datetime(pred.data_corte)).all())
        self.assertTrue((pd.to_datetime(pred.treino_publicado_ate) <= pd.to_datetime(pred.data_corte)).all())

    def test_historico_insuficiente_produz_relatorio_sem_metricas_inventadas(self):
        summary, path = self.executar(painel(meses=4))
        self.assertEqual(summary["status"], "dados_insuficientes")
        self.assertEqual(json.loads((path / "metricas.json").read_text()), [])
        self.assertTrue(pd.read_csv(path / "metricas.csv").empty)
        self.assertTrue((path / "dataset_modelavel.csv").is_file())

    def test_previsao_futura_separada_do_teste_e_nao_fabrica_alvo(self):
        df = painel()
        df["assinatura_tipo"] = "descricao_unidade"
        summary, path = self.executar(df)
        futuro = pd.read_csv(path / "previsoes_proxima_competencia.csv")
        self.assertEqual(set(futuro.competencia_alvo), {"2026-05"})
        self.assertTrue(futuro.custo_observado.isna().all())
        self.assertEqual(set(futuro.treino_ate), {"2026-04"})
        self.assertIn("descricao_unidade", summary["tipos_assinatura"])
        self.assertTrue(list((path / "modelos").glob("*.joblib")))

    def test_mudanca_tecnica_no_alvo_nao_seleciona_amostra_pelo_futuro(self):
        df = painel(meses=4, servicos=1)
        df.loc[3, "assinatura_tecnica"] = "cpu-revisada-no-futuro"
        result = self.mod.construir_supervisionado(df)
        self.assertEqual(len(result), 1)
        self.assertTrue(result.iloc[0]["mudanca_tecnica_alvo"])
        self.assertTrue(result.iloc[0]["unidade_alvo_compativel"])

    def test_unidade_futura_diferente_fica_auditavel_fora_de_metricas_monetarias(self):
        df = painel(meses=4, servicos=1)
        df.loc[3, "unidade"] = "M"
        result = self.mod.construir_supervisionado(df)
        self.assertEqual(len(result), 1)
        self.assertFalse(result.iloc[0]["unidade_alvo_compativel"])

    def test_validacao_publicada_depois_da_origem_teste_nao_escolhe_modelo(self):
        df = painel(publicado=True)
        # Serviço ausente no primeiro mês de teste: sua validação tardia
        # não altera a origem inicial de teste dos demais serviços.
        df = df[~((df.codigo == "000") & (df.competencia >= "2026-02"))].copy()
        df.loc[(df.codigo == "000") & (df.competencia == "2026-01"), "publicado_em"] = "2026-04-15"
        summary, path = self.executar(df)
        pred = pd.read_csv(path / "previsoes_avaliacao.csv")
        val = pred[(pred.fase == "validacao") & (pred.codigo.astype(str).str.zfill(3) == "000")]
        self.assertNotIn("2026-01", set(val.competencia_alvo))
        self.assertEqual(summary["recortes"][0]["n_validacao_excluida_publicacao_tardia"], 1)


if __name__ == "__main__":
    unittest.main()
