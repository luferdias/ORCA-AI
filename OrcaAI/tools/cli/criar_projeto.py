"""Cria um item de orçamento a partir de projetos/_modelo.

Uso, a partir de qualquer pasta:
    python OrcaAI/tools/cli/criar_projeto.py 2026-013-nome-do-servico
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.estrutura_projeto import criar_item, raiz_orcaai  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cria um item de orçamento a partir do modelo."
    )
    parser.add_argument("slug", help="Nome da pasta, ex.: 2026-013-limpeza-hvac")
    args = parser.parse_args()
    raiz = raiz_orcaai()
    try:
        destino = criar_item(raiz / "projetos", args.slug)
    except (ValueError, FileExistsError) as erro:
        print(erro)
        return 1
    print(f"Item criado: {destino}")
    print("Coloque os arquivos recebidos em 00-entrada e preencha projeto.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
