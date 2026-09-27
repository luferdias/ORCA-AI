#!/usr/bin/env python3
"""Recrie apenas o relatório acadêmico a partir de resultados já executados."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from executar_estudo import _sha


def validar_resultados(execucao: Path, run: dict):
    hashes = run.get("resultados_sha256")
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError("Manifesto sem hashes dos resultados; execute executar_estudo.py para produzir uma execução auditável")
    root = Path(execucao).resolve()
    for relative, expected in hashes.items():
        rel = Path(relative)
        path = root / rel
        if rel.is_absolute() or ".." in rel.parts or not path.resolve().is_relative_to(root):
            raise ValueError(f"Caminho inválido no manifesto: {relative}")
        if not path.is_file() or _sha(path) != expected:
            raise ValueError(f"Resultado ausente ou alterado: {relative}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execucao", type=Path, required=True, help="Pasta com execucao_estudo.json")
    parser.add_argument("--saida", type=Path, help="Pasta nova para a apresentação")
    args = parser.parse_args(argv)
    run = json.loads((args.execucao / "execucao_estudo.json").read_text(encoding="utf-8"))
    if run.get("status") != "concluido" or run.get("etapa") != "todas":
        parser.error("O relatório consolidado exige uma execução concluída das três tarefas")
    try:
        validar_resultados(args.execucao, run)
        from orca_ml.relatorio_consolidado import gerar_relatorio_consolidado
        paths = gerar_relatorio_consolidado(args.execucao, run, saida=args.saida)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    for label, path in paths.items():
        print(f"Relatório {label.upper()}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
