import pytest

from orca_tools.estrutura_projeto import (
    ARQUIVOS_CONTROLE,
    ETAPAS,
    criar_etapa,
    criar_item,
    etapa_vazia,
    raiz_orcaai,
    validar_item,
    validar_projetos,
)


def _modelo(tmp_path):
    modelo = tmp_path / "_modelo"
    for e in ETAPAS:
        (modelo / e).mkdir(parents=True)
        (modelo / e / "LEIA-ME.md").write_text(f"# {e}\n")
    for a in ARQUIVOS_CONTROLE:
        (modelo / a).write_text("# x\n")
    return modelo


def test_criar_item_nasce_com_controle_e_entrada(tmp_path):
    _modelo(tmp_path)
    destino = criar_item(tmp_path, "2026-099-teste-unitario")
    r = validar_item(destino)
    assert r.ok and not r.avisos
    assert r.etapas == ["00-entrada"]
    assert (destino / "00-entrada" / "LEIA-ME.md").read_text() == "# 00-entrada\n"
    assert all((destino / a).is_file() for a in ARQUIVOS_CONTROLE)


def test_criar_etapa_sob_demanda_e_idempotente(tmp_path):
    modelo = _modelo(tmp_path)
    item = criar_item(tmp_path, "2026-097-b")
    e = criar_etapa(item, "03-orcamento", modelo)
    assert e.is_dir() and etapa_vazia(e)
    (e / "planilha.csv").write_text("a,b\n")
    assert criar_etapa(item, "03-orcamento", modelo) == e and not etapa_vazia(e)
    sem_modelo = criar_etapa(item, "05-validacoes")
    assert "R-C2" in (sem_modelo / "LEIA-ME.md").read_text()
    with pytest.raises(ValueError):
        criar_etapa(item, "08-inexistente")
    assert validar_item(item).etapas == ["00-entrada", "03-orcamento", "05-validacoes"]


def test_slug_invalido_e_duplicado(tmp_path):
    _modelo(tmp_path)
    with pytest.raises(ValueError):
        criar_item(tmp_path, "Item 13 - Teste")
    criar_item(tmp_path, "2026-098-a")
    with pytest.raises(FileExistsError):
        criar_item(tmp_path, "2026-098-a")


def test_validacao_aponta_faltas_e_avisos(tmp_path):
    item = tmp_path / "2026-001-x"
    (item / "00-entrada").mkdir(parents=True)
    (item / "99-outra").mkdir()
    (item / "solto.txt").write_text("")
    r = validar_item(item)
    assert not r.ok
    assert "projeto.md" in r.faltantes and "07-assinados/" not in r.faltantes
    assert any("solto.txt" in a for a in r.avisos)
    assert any("99-outra" in a for a in r.avisos)


def test_acervo_real_esta_completo():
    resultados = validar_projetos(raiz_orcaai() / "projetos")
    assert len(resultados) >= 12
    assert all(r.ok for r in resultados), [
        (r.item, r.faltantes) for r in resultados if not r.ok
    ]
    assert all("03-orcamento" in r.etapas for r in resultados[:12])
