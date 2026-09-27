"""Proteções do arquivo que o usuário executa no VS Code."""
from pathlib import Path

import pytest

from executar_regressao import carregar_dataset


def test_csv_preserva_codigo_com_zero_a_esquerda_e_publicacao_ausente(tmp_path):
    path = tmp_path / "custos.csv"
    path.write_text("fonte,codigo,competencia,custo,publicado_em\nder_es,001001,2026-05,123.45,\n", encoding="utf-8-sig")
    frame = carregar_dataset(path, "der_es")
    assert frame.loc[0, "codigo"] == "001001"
    assert frame.loc[0, "competencia"] == "2026-05"
    assert frame.loc[0, "publicado_em"] == ""
    assert frame.loc[0, "custo"] == 123.45


def test_nao_treina_fonte_diferente_da_solicitada(tmp_path):
    path = tmp_path / "custos.csv"
    path.write_text("fonte,codigo,competencia,custo\nsinapi_es,123,2026-05,10\n")
    with pytest.raises(ValueError, match="fonte"):
        carregar_dataset(path, "der_es")


def test_dataset_ausente_informa_o_caminho(tmp_path):
    missing = tmp_path / "ausente.csv"
    with pytest.raises(FileNotFoundError, match="ausente.csv"):
        carregar_dataset(missing, "sinapi_es")


@pytest.fixture
def ambiente_cli(tmp_path, monkeypatch):
    """Dados locais reais; isole apenas treino e renderização demorados."""
    import json
    import sys
    from types import ModuleType

    import pandas as pd
    import executar_regressao as cli
    import orca_ml.regressao as regressao

    orca = tmp_path / "OrcaAI"
    ml = orca / "ml"
    ml.mkdir(parents=True)
    (ml / "configs").mkdir()
    (ml / "configs" / "regressao.json").write_text("{}")
    monkeypatch.setattr(cli, "PASTA_ML", ml)
    monkeypatch.setattr(cli, "PASTA_ORCA", orca)
    for fonte, fim in [("sinapi_es", "2026-08"), ("der_es", "2026-05")]:
        pasta = orca / "knowledge" / "datasets" / "ml_ufg" / fonte
        pasta.mkdir(parents=True)
        pd.DataFrame([
            {"fonte": fonte, "competencia": str(mes), "codigo": "001", "custo": 20}
            for mes in pd.period_range("2025-01", fim, freq="M")
        ]).to_csv(pasta / "custos_historicos.csv", index=False)

    def experimento(frame, output, config):
        output.mkdir(parents=True)
        meses = sorted(frame.competencia.unique())
        result = {
            "status": "ok", "recortes": [{"status": "avaliado"}],
            "competencias_validacao": meses[-5:-3], "competencias_teste": meses[-3:],
            "modo_avaliacao": "retrospectivo", "janelas_excluidas_publicacao": 0, "limites": [],
        }
        (output / "resumo.json").write_text(json.dumps(result))
        (output / "metricas.csv").write_text("mae\n1\n")
        return result

    module = ModuleType("orca_ml.relatorio")

    def relatorio(execucao_dir, historicos, saida=None):
        destination = saida or execucao_dir / "relatorio_didatico"
        destination.mkdir(parents=True)
        (destination / "fontes.json").write_text(json.dumps({
            fonte: str(frame.competencia.max()) for fonte, frame in historicos.items()
        }))
        paths = {kind: destination / f"relatorio.{extension}" for kind, extension in [
            ("html", "html"), ("pdf", "pdf"), ("markdown", "md")
        ]}
        for path in paths.values():
            path.write_text("relatorio")
        return paths

    module.gerar_relatorio = relatorio
    monkeypatch.setitem(sys.modules, "orca_ml.relatorio", module)
    monkeypatch.setattr(regressao, "executar_experimento", experimento)
    return cli, tmp_path / "saida", module


def test_cli_preserva_latest_e_compara_com_mesmo_corte(ambiente_cli):
    import json
    cli, output, _ = ambiente_cli
    assert cli.main(["--saida", str(output)]) == 0
    original = json.loads((output / "execucao.json").read_text())
    assert original["bases"]["sinapi_es"]["competencias_teste"] == ["2026-06", "2026-07", "2026-08"]
    comum = output / "comparacao_mesma_janela"
    comparacao = json.loads((comum / "execucao.json").read_text())
    assert comparacao["fim_solicitado"] == "2026-05"
    assert comparacao["bases"]["sinapi_es"]["competencias_teste"] == ["2026-03", "2026-04", "2026-05"]
    assert comparacao["bases"]["der_es"]["competencias_teste"] == ["2026-03", "2026-04", "2026-05"]
    assert json.loads((comum / "relatorio_didatico" / "fontes.json").read_text()) == {
        "sinapi_es": "2026-05", "der_es": "2026-05"
    }
    assert (comum / "RESULTADOS.md").is_file()
    assert Path(original["relatorio"]["html"]).is_file()


def test_cli_mesmo_periodo_nao_duplica_experimento(ambiente_cli):
    cli, output, _ = ambiente_cli
    assert cli.main(["--fim", "2026-05", "--saida", str(output)]) == 0
    assert (output / "relatorio_didatico" / "relatorio.html").is_file()
    assert not (output / "comparacao_mesma_janela").exists()


def test_cli_uma_fonte_gera_relatorio_individual(ambiente_cli):
    import json
    cli, output, _ = ambiente_cli
    assert cli.main(["--base", "sinapi_es", "--saida", str(output)]) == 0
    assert json.loads((output / "relatorio_didatico" / "fontes.json").read_text()) == {"sinapi_es": "2026-08"}
    assert not (output / "der_es").exists()
    assert not (output / "comparacao_mesma_janela").exists()


def test_cli_sem_relatorio_preserva_execucao_rapida(ambiente_cli):
    cli, output, _ = ambiente_cli
    assert cli.main(["--sem-relatorio", "--saida", str(output)]) == 0
    assert (output / "sinapi_es" / "metricas.csv").is_file()
    assert not (output / "relatorio_didatico").exists()
    assert not (output / "comparacao_mesma_janela").exists()


def test_cli_falha_relatorio_preserva_metricas_e_sinaliza_erro(ambiente_cli, capsys):
    import json
    cli, output, module = ambiente_cli

    def falhar(*args, **kwargs):
        raise ValueError("períodos divergentes")

    module.gerar_relatorio = falhar
    assert cli.main(["--base", "der_es", "--saida", str(output)]) != 0
    assert (output / "der_es" / "metricas.csv").is_file()
    assert "períodos divergentes" in capsys.readouterr().err
    run = json.loads((output / "execucao.json").read_text())
    assert run["relatorio"]["status"] == "erro"


def test_regeneracao_usa_execucao_comum_sem_treinar_novamente(ambiente_cli, monkeypatch):
    import importlib.util
    import json
    import orca_ml.regressao as regressao

    cli, output, _ = ambiente_cli
    assert cli.main(["--saida", str(output)]) == 0
    spec = importlib.util.find_spec("gerar_relatorio")
    assert spec is not None, "O CLI de regeneração precisa existir"
    import gerar_relatorio as relatorio_cli
    monkeypatch.setattr(relatorio_cli, "PASTA_ORCA", cli.PASTA_ORCA)

    def proibir_treino(*args, **kwargs):
        pytest.fail("Regenerar a apresentação não deve reajustar modelos")

    monkeypatch.setattr(regressao, "executar_experimento", proibir_treino)
    nova = output.parent / "apresentacao"
    assert relatorio_cli.main(["--execucao", str(output), "--saida", str(nova)]) == 0
    assert json.loads((nova / "fontes.json").read_text()) == {"sinapi_es": "2026-05", "der_es": "2026-05"}
    assert (nova / "relatorio.pdf").is_file()


def test_regeneracao_rejeita_dataset_modificado(ambiente_cli, monkeypatch, capsys):
    import importlib.util
    cli, output, _ = ambiente_cli
    assert cli.main(["--base", "der_es", "--sem-relatorio", "--saida", str(output)]) == 0
    spec = importlib.util.find_spec("gerar_relatorio")
    assert spec is not None, "O CLI de regeneração precisa existir"
    import gerar_relatorio as relatorio_cli
    monkeypatch.setattr(relatorio_cli, "PASTA_ORCA", cli.PASTA_ORCA)
    csv_path = cli.PASTA_ORCA / "knowledge/datasets/ml_ufg/der_es/custos_historicos.csv"
    csv_path.write_text(csv_path.read_text().replace(",20", ",99"))
    assert relatorio_cli.main(["--execucao", str(output)]) != 0
    assert "SHA-256" in capsys.readouterr().err
    assert not (output / "relatorio_didatico").exists()
