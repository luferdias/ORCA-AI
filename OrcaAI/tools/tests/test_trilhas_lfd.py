import pytest

from orca_tools.trilhas_lfd import Evento, Trilha, listar_trilhas


def test_registra_le_e_resume(tmp_path):
    t = Trilha(
        tmp_path / "2026-012-reforma-suporte-cag" / "2026-10-29-orcafascio.jsonl"
    )
    t.registrar(
        Evento(
            "orcafascio",
            "busca",
            "pintura latex",
            "104642",
            campos={"base": "SINAPI", "codigo": "104642", "bdi": 25.0},
        )
    )
    t.registrar(
        Evento(
            "orcafascio",
            "selecao",
            "104642",
            "item inserido",
            campos={"base": "SINAPI", "codigo": "104642", "bdi": 25.0},
            justificativa="andaime incluso",
        )
    )
    r = t.resumo()
    assert (
        r["eventos"] == 2
        and r["bases"] == {"SINAPI": 2}
        and r["familias_de_codigo"] == {"10": 2}
    )
    assert (
        r["justificativas"] == ["andaime incluso"]
        and r["item"] == "2026-012-reforma-suporte-cag"
    )
    assert len(listar_trilhas(tmp_path)) == 1


def test_rejeita_evento_invalido_e_senha(tmp_path):
    t = Trilha(tmp_path / "x" / "2026-10-29-excel.jsonl")
    with pytest.raises(ValueError):
        t.registrar(Evento("planilha", "busca"))
    with pytest.raises(ValueError):
        t.registrar(Evento("orcafascio", "digitacao", campos={"senha": "abc"}))
    with pytest.raises(ValueError):
        Trilha(tmp_path / "x" / "sem-data.jsonl")
