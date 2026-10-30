from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera indice simples de dossie para um projeto Orca.")
    parser.add_argument("projeto", help="Slug do projeto dentro de projetos/")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    project = root / "projetos" / args.projeto
    if not project.is_dir():
        print(f"Projeto nao encontrado: {project}")
        return 1

    files = []
    for path in sorted(project.rglob("*")):
        if path.is_file():
            files.append(path.relative_to(project).as_posix())

    output = project / "indice-dossie.md"
    lines = [
        "# Indice do Dossie",
        "",
        f"- Projeto: {args.projeto}",
        f"- Data: {date.today().isoformat()}",
        "",
        "| Ordem | Arquivo |",
        "| ---: | --- |",
    ]
    for index, file_name in enumerate(files, start=1):
        lines.append(f"| {index} | `{file_name}` |")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Indice gerado: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

