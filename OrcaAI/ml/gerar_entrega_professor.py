#!/usr/bin/env python3
"""Gere a edição para o professor Ronaldo com links permanentes do GitHub."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gerar_relatorio_estudo import validar_resultados
from orca_ml.edicao_professor import conferir_execucao
from orca_ml.relatorio_consolidado import gerar_relatorio_consolidado

PASTA = Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, default=PASTA/'entregas/professor_ronaldo_2026-09-28')
    args = parser.parse_args(argv)
    raiz = PASTA/'outputs/entrega_ufg_acabamentos_2026-09-27'
    arquivo = raiz/'execucao_estudo.json'
    try:
        edicao = conferir_execucao(arquivo)
        run = json.loads(arquivo.read_text(encoding='utf-8'))
        validar_resultados(raiz, run)
        paths = gerar_relatorio_consolidado(raiz, run, args.saida, edicao=edicao)
    except (ValueError, FileNotFoundError) as error:
        parser.error(str(error))
    for label, path in paths.items():
        print(f'{label.upper()}: {path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
