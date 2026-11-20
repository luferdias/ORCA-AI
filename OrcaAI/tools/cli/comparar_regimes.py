"""Compara o orçamento de um item nos dois regimes de encargos (regra R-B10).

Lê ``03-orcamento/planilha-normalizada.csv``, usa o índice SINAPI-ES da
competência da planilha e mostra o total com BDI nos regimes desonerado e não
desonerado. Com ``--gravar``, escreve ``05-validacoes/comparacao-regimes.md``.

Uso:
    .venv/bin/python OrcaAI/tools/cli/comparar_regimes.py 2026-007-pintura-externa [--gravar]
"""

from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.comparar_regimes import comparar, relatorio_markdown  # noqa: E402
from orca_tools.estrutura_projeto import raiz_orcaai  # noqa: E402
from orca_tools.indice_bases import Indice  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("item", help="pasta do item em OrcaAI/projetos")
    ap.add_argument("--competencia", help="AAAA-MM do SINAPI; padrão: a da planilha")
    ap.add_argument("--gravar", action="store_true", help="grava em 05-validacoes")
    args = ap.parse_args()
    pasta = raiz_orcaai() / "projetos" / args.item
    planilha = pasta / "03-orcamento" / "planilha-normalizada.csv"
    with open(planilha, encoding="utf-8") as f:
        itens = [r for r in csv.DictReader(f) if r.get("tipo_item") != "grupo"]
    datas = collections.Counter(
        r["data_base"] for r in itens if r.get("sistema") == "SINAPI"
    ) or collections.Counter(r["data_base"] for r in itens if r.get("data_base"))
    competencia = args.competencia or datas.most_common(1)[0][0]
    try:
        indice = Indice.carregar("sinapi_es", competencia)
    except FileNotFoundError:
        print(f"índice sinapi_es {competencia} ausente; rode indexar_bases.py")
        return 1
    texto = relatorio_markdown(comparar(itens, indice), args.item, competencia)
    print(texto)
    if args.gravar:
        destino = pasta / "05-validacoes" / "comparacao-regimes.md"
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        print(f"gravado em {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
