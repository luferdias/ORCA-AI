import pytest

from orca_tools.estrutura_projeto import (
    ARQUIVOS_CONTROLE,
    ETAPAS,
    criar_item,
    raiz_orcaai,
    validar_item,
    validar_projetos,
)


def _modelo(tmp_path):
    modelo = tmp_path / "_modelo"
    for e in ETAPAS:
        (modelo / e).mkdir(parents=True)
    for a in ARQUIVOS_CONTROLE:
        (modelo / a).write_text("# x\n")
    return modelo


def test_criar_e_validar_item(tmp_path):
    _modelo(tmp_path)
    destino = criar_item(tmp_path, "2026-099-teste-unitario")
    r = validar_item(destino)
    assert r.ok and not r.avisos


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
    (item / "solto.txt").write_text("")
    r = validar_item(item)
    assert not r.ok
    assert "07-assinados/" in r.faltantes and "projeto.md" in r.faltantes
    assert any("solto.txt" in a for a in r.avisos)


def test_acervo_real_esta_completo():
    resultados = validar_projetos(raiz_orcaai() / "projetos")
    assert len(resultados) == 12
    assert all(r.ok for r in resultados), [
        (r.item, r.faltantes) for r in resultados if not r.ok
    ]
