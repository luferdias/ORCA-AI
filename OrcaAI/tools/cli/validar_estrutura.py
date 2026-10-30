"""Valida a estrutura única dos itens em OrcaAI/projetos.

Uso:
    python OrcaAI/tools/cli/validar_estrutura.py           # todos os itens
    python OrcaAI/tools/cli/validar_estrutura.py 2026-012  # prefixo
Exige os três arquivos de controle; as etapas são sob demanda (R-E2).
Sai com código 1 se algum item estiver incompleto.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.estrutura_projeto import raiz_orcaai, validar_projetos  # noqa: E402


def main() -> int:
    prefixo = sys.argv[1] if len(sys.argv) > 1 else ""
    resultados = [
        r
        for r in validar_projetos(raiz_orcaai() / "projetos")
        if r.item.startswith(prefixo)
    ]
    incompletos = 0
    for r in resultados:
        estado = "ok" if r.ok else "INCOMPLETO"
        print(f"{estado:10s} {r.item}  etapas: {', '.join(r.etapas) or 'nenhuma'}")
        for f in r.faltantes:
            print(f"           falta: {f}")
        for a in r.avisos:
            print(f"           aviso: {a}")
        incompletos += 0 if r.ok else 1
    print(f"{len(resultados)} item(ns); {incompletos} incompleto(s)")
    return 1 if incompletos else 0


if __name__ == "__main__":
    raise SystemExit(main())
