import shutil

import openpyxl
import pytest

from orca_tools.indice_bases import Indice
from orca_tools.normalizar_planilha import gravar_csv, normalizar_orcafascio_sintetico


def _planilha_orcafascio(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orçamento Sintético"
    ws.append(["Obra", "Bancos", "B.D.I.", "Encargos Sociais"])
    ws.append(
        ["Obra teste", "SINAPI - 04/2026 - Espírito Santo", "25,0%", "Desonerado"]
    )
    ws.append(["Orçamento Sintético"])
    ws.append(
        [
            "Item",
            "Código",
            "Banco",
            "Descrição",
            "Und",
            "Quant.",
            "Valor Unit",
            "Valor Unit com BDI",
            "Total",
            "Peso (%)",
        ]
    )
    ws.append(
        [" 1 ", None, None, "SERVIÇOS PRELIMINARES", None, 1, None, None, 125.0, 0.5]
    )
    ws.append(
        [
            " 1.1 ",
            " 88316 ",
            "SINAPI",
            "SERVENTE COM ENCARGOS",
            "H",
            5,
            20.0,
            25.0,
            125.0,
            0.5,
        ]
    )
    ws.append([" 2 ", None, None, "PRÓPRIOS", None, 1, None, None, 125.0, 0.5])
    ws.append(
        [
            " 2.1 ",
            " SRAES-CP-001 ",
            "Próprio",
            "COMPOSIÇÃO PRÓPRIA",
            "m2",
            1,
            100.0,
            125.0,
            125.0,
            0.5,
        ]
    )
    ws.append([])
    ws.append(["Total sem BDI", 200.0])
    p = tmp_path / "orc.xlsx"
    wb.save(p)
    return p


def test_normaliza_exportacao_orcafascio(tmp_path):
    n = normalizar_orcafascio_sintetico(_planilha_orcafascio(tmp_path))
    assert (
        n.obra == "Obra teste" and n.data_base == "2026-04" and n.bdi_percentual == 25.0
    )
    assert [r["codigo"] for r in n.itens] == ["88316", "SRAES-CP-001"]
    assert n.itens[0]["sistema"] == "SINAPI" and n.itens[1]["sistema"] == "PROPRIA"
    assert n.itens[0]["bdi_percentual"] == 25.0 and n.itens[0]["grupo"].startswith("1")
    csv = gravar_csv(n, tmp_path / "saida" / "planilha-normalizada.csv")
    assert (
        csv.read_text(encoding="utf-8")
        .splitlines()[0]
        .startswith("item,codigo,sistema,descricao")
    )


def test_indice_consulta_e_busca(tmp_path):
    pasta = tmp_path / "sinapi_es" / "2026-04"
    pasta.mkdir(parents=True)
    (pasta / "servicos.csv").write_text(
        "fonte,competencia,codigo,descricao,unidade,grupo,custo,regime,publicado_em,arquivo_sha256,localizador\n"
        "sinapi_es,2026-04,88316,SERVENTE COM ENCARGOS COMPLEMENTARES,H,MAO DE OBRA,22.5,sem_desoneracao,,x,y\n"
        "sinapi_es,2026-04,88309,PEDREIRO COM ENCARGOS COMPLEMENTARES,H,MAO DE OBRA,28.0,sem_desoneracao,,x,y\n",
        encoding="utf-8",
    )
    idx = Indice.carregar("sinapi_es", "2026-04", tmp_path)
    assert idx.codigo("88316")["unidade"] == "H"
    assert idx.codigo("00000") is None
    assert [r["codigo"] for r in idx.buscar("pedreiro encargos")][0] == "88309"


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc ausente")
def test_renderiza_markdown_em_docx(tmp_path):
    from orca_tools.renderizar import markdown_para_docx

    md = tmp_path / "doc.md"
    md.write_text(
        "# Título\n\nParágrafo com **negrito**.\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n",
        encoding="utf-8",
    )
    docx = markdown_para_docx(md, tmp_path / "doc.docx")
    assert docx.exists() and docx.stat().st_size > 2000
