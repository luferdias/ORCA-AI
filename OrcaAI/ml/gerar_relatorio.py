#!/usr/bin/env python3
"""Regere a apresentação de uma execução salva, sem treinar modelos.

Exemplo: python gerar_relatorio.py --execucao outputs/minha_execucao
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from executar_regressao import FONTES, PASTA_ML, PASTA_ORCA, carregar_dataset


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--execucao", required=True, type=Path, help="Pasta de uma execução concluída")
    parser.add_argument("--saida", type=Path, help="Pasta nova para HTML, PDF, gráficos e tabelas")
    args = parser.parse_args(argv)
    execucao = args.execucao.resolve()
    # A execução padrão preserva a última edição de cada fonte e guarda a
    # comparação temporal na subpasta; a apresentação usa essa comparação.
    comum = execucao / "comparacao_mesma_janela"
    if (comum / "execucao.json").is_file():
        execucao = comum
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    saida = args.saida.resolve() if args.saida else execucao / f"relatorio_didatico_{run_id}"
    if saida.exists():
        parser.error(f"A pasta de apresentação já existe: {saida}. Escolha uma pasta nova.")
    try:
        run = json.loads((execucao / "execucao.json").read_text(encoding="utf-8"))
        bases = run.get("bases", {})
        if not bases or set(bases) - set(FONTES):
            raise ValueError("A execução deve identificar SINAPI-ES e/ou DER-ES em execucao.json")
        historicos = {}
        for fonte, result in bases.items():
            if result.get("status") == "erro":
                raise ValueError(f"A execução da base {fonte} não foi concluída")
            relative = result.get("csv_origem", f"knowledge/datasets/ml_ufg/{fonte}/custos_historicos.csv")
            csv_path = (PASTA_ORCA / relative).resolve()
            expected_sha = result.get("csv_origem_sha256")
            if expected_sha and hashlib.sha256(csv_path.read_bytes()).hexdigest() != expected_sha:
                raise ValueError(f"SHA-256 diferente do dataset utilizado na execução: {csv_path}. Restaure a cópia correspondente ou faça uma nova avaliação.")
            frame = carregar_dataset(csv_path, fonte)
            fim = result.get("historico", {}).get("fim") or run.get("fim_solicitado")
            if not fim:
                fim = max(result.get("competencias_teste", []), default=None)
            if not fim:
                raise ValueError(f"A execução não informa a competência final de {fonte}")
            frame = frame.loc[frame.competencia <= fim].copy()
            if frame.empty:
                raise ValueError(f"Nenhum registro de {fonte} no período da execução")
            historicos[fonte] = frame
        from orca_ml.relatorio import gerar_relatorio

        paths = gerar_relatorio(execucao, historicos, saida)
        for key in ("html", "pdf", "markdown"):
            if key in paths:
                print(f"Relatório {key.upper()}: {paths[key]}", flush=True)
        return 0
    except Exception as error:
        print(f"ERRO ao gerar a apresentação: {error}. Os resultados originais permanecem em {execucao}.", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ModuleNotFoundError as error:
        print(f"Dependência ausente: {error.name}. Selecione o Python da .venv. Instalação: python -m pip install -r \"{PASTA_ML / 'requirements.txt'}\"", file=sys.stderr)
        raise SystemExit(2)
