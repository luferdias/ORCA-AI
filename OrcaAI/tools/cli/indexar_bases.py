"""Constrói o índice local de uma base oficial (comando /atualizar-bases, agente A9).

Uso:
    OrcaAI/ml/.venv/bin/python OrcaAI/tools/cli/indexar_bases.py sinapi_es 2026-04
    OrcaAI/ml/.venv/bin/python OrcaAI/tools/cli/indexar_bases.py der_es 2026-04
    OrcaAI/ml/.venv/bin/python OrcaAI/tools/cli/indexar_bases.py --todas 2026-04

O ZIP original deve estar em OrcaAI/bases/<fonte>/<competencia>/originais/.
Gera OrcaAI/knowledge/indices/<fonte>/<competencia>/servicos.csv (ignorado pelo
Git), insumos.csv para o SINAPI e manifesto.json (versionado).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.indice_bases import FONTES, construir  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Constrói índices locais das bases oficiais."
    )
    ap.add_argument(
        "fonte", nargs="?", choices=sorted(FONTES), help="sinapi_es ou der_es"
    )
    ap.add_argument("competencia", help="AAAA-MM")
    ap.add_argument(
        "--todas", action="store_true", help="todas as fontes da competência"
    )
    args = ap.parse_args()
    fontes = sorted(FONTES) if args.todas else [args.fonte]
    if not fontes or fontes == [None]:
        ap.error("informe a fonte ou --todas")
    for fonte in fontes:
        try:
            pasta = construir(fonte, args.competencia)
        except FileNotFoundError as erro:
            print(f"{fonte} {args.competencia}: {erro}")
            continue
        m = json.loads((pasta / "manifesto.json").read_text(encoding="utf-8"))
        print(
            f"{fonte} {args.competencia}: {m['servicos']} serviços, {m.get('insumos', 0)} insumos, {m['duracao_s']}s -> {pasta}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
