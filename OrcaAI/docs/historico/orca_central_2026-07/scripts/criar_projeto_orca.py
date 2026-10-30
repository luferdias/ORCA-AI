from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria um projeto Orca a partir do modelo.")
    parser.add_argument("slug", help="Nome da pasta do projeto, ex: 2026-001-limpeza-hvac")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    template = root / "projetos" / "_modelo"
    target = root / "projetos" / args.slug

    if target.exists():
        print(f"Projeto ja existe: {target}")
        return 1

    shutil.copytree(template, target)
    print(f"Projeto criado: {target}")
    print("Coloque os arquivos de entrada em 00-entrada e rode /novo-orcamento no Antigravity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

