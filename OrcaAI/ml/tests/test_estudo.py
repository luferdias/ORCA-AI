import json
from pathlib import Path

import pandas as pd
import pytest

import executar_estudo as estudo


def test_saida_existente_nao_e_sobrescrita(tmp_path):
    folder = tmp_path / "anterior"; folder.mkdir()
    original = folder / "relatorio.txt"; original.write_text("preservar")
    with pytest.raises(ValueError, match="contém"):
        estudo.criar_saida(folder)
    assert original.read_text() == "preservar"


def test_zip_precisa_corresponder_a_versao_do_dataset(tmp_path):
    source = tmp_path / "tabela.zip"; source.write_bytes(b"zip alterado")
    frame = pd.DataFrame({"arquivo_sha256": ["a" * 64]})
    with pytest.raises(ValueError, match="SHA-256"):
        estudo.conferir_zip(source, frame)


def test_populacoes_preservam_servico_historico_ausente_no_snapshot():
    catalog = pd.DataFrame({"codigo": ["01", "02"], "classe": ["pintura", "pisos"]})
    forecasts = pd.DataFrame({"codigo": ["01", "01", "03"], "nicho_id": ["pintura", "pintura", "pisos"]})
    result = estudo.comparar_populacoes(catalog, forecasts).set_index("codigo")
    assert result.loc["01", "n_previsoes_regressao"] == 2
    assert result.loc["02", "n_previsoes_regressao"] == 0
    assert not result.loc["03", "no_catalogo_maio"]
    assert result.loc["03", "n_previsoes_regressao"] == 1


def test_falha_preserva_manifesto_e_nao_anuncia_sucesso(tmp_path, monkeypatch):
    monkeypatch.setattr(estudo, "PASTA_ORCA", tmp_path / "sem_dados")
    output = tmp_path / "run"
    assert estudo.main(["--saida", str(output), "--sem-relatorio"]) == 1
    manifest = json.loads((output / "execucao_estudo.json").read_text())
    assert manifest["status"] == "erro"
    assert "datasets" in manifest["erro"]


def test_manifesto_impede_relatorio_com_resultado_alterado(tmp_path):
    import hashlib
    import gerar_relatorio_estudo

    path = tmp_path / "sinapi_es" / "metricas.csv"; path.parent.mkdir()
    path.write_bytes(b"original")
    run = {"resultados_sha256": {"sinapi_es/metricas.csv": hashlib.sha256(b"original").hexdigest()}}
    gerar_relatorio_estudo.validar_resultados(tmp_path, run)
    path.write_bytes(b"alterado")
    with pytest.raises(ValueError, match="alterado"):
        gerar_relatorio_estudo.validar_resultados(tmp_path, run)


def test_manifesto_nao_pode_acessar_caminhos_fora_da_execucao(tmp_path):
    import gerar_relatorio_estudo
    with pytest.raises(ValueError, match="Caminho"):
        gerar_relatorio_estudo.validar_resultados(tmp_path, {"resultados_sha256": {"../segredo": "a" * 64}})
