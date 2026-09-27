#!/usr/bin/env python3
"""Abra este arquivo no VS Code e use Executar Arquivo Python.

Padrão: treina e avalia SINAPI-ES e DER-ES separadamente, usando os CSVs
reais já preparados, e gera o relatório didático HTML/PDF. Consulte README.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PASTA_ML = Path(__file__).resolve().parent
PASTA_ORCA = PASTA_ML.parent
FONTES = ("sinapi_es", "der_es")


def carregar_dataset(path: str | Path, fonte: str):
    """Leia IDs como texto e preserve datas desconhecidas sem inventá-las."""
    import pandas as pd

    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Dataset não encontrado: {path}. Execute preparar_dados.py.")
    frame = pd.read_csv(path, encoding="utf-8-sig", dtype={"codigo": str, "competencia": str}, keep_default_na=False)
    if "fonte" not in frame or frame.empty or set(frame.fonte.unique()) != {fonte}:
        raise ValueError(f"O dataset deve conter apenas a fonte {fonte}: {path}")
    return frame


def _executar_bases(requested, output, config, fim):
    """A mesma avaliação serve às últimas edições e à janela de comparação."""
    from orca_ml.regressao import executar_experimento

    output.mkdir(parents=True, exist_ok=True)
    historicos = {}
    run = {"executado_em_utc": datetime.now(timezone.utc).isoformat(), "fim_solicitado": fim, "config": config, "bases": {}}
    paragraphs = ["# Regressão de custos referenciais — resultado da execução", "", "SINAPI-ES e DER-ES/IOPES são avaliados separadamente. Cada recorte preserva sua família e unidade; não há uma média monetária que misture unidades.", ""]
    failed = False
    for fonte in requested:
        csv_path = PASTA_ORCA / "knowledge" / "datasets" / "ml_ufg" / fonte / "custos_historicos.csv"
        print(f"\n[{fonte}] Lendo {csv_path}", flush=True)
        try:
            frame = carregar_dataset(csv_path, fonte)
            if fim:
                frame = frame.loc[frame.competencia <= fim].copy()
            if frame.empty:
                raise ValueError("Nenhum dado disponível no período solicitado")
            historicos[fonte] = frame
            result = executar_experimento(frame, output / fonte, config)
            result["historico"] = {"inicio": str(frame.competencia.min()), "fim": str(frame.competencia.max()), "registros": len(frame), "codigos": int(frame.codigo.nunique())}
            result["csv_origem"] = str(csv_path.relative_to(PASTA_ORCA))
            result["csv_origem_sha256"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
            run["bases"][fonte] = result
            valid = [g for g in result["recortes"] if g["status"] == "avaliado"]
            skipped = len(result["recortes"]) - len(valid)
            failed |= not valid
            paragraphs += [f"## {fonte}", "", f"- Histórico: {frame.competencia.min()} a {frame.competencia.max()}; {len(frame):,} registros e {frame.codigo.nunique():,} códigos.", f"- Recortes avaliados: {len(valid)}; sem amostra suficiente: {skipped}.", f"- Validação: {', '.join(result['competencias_validacao'])}.", f"- Teste: {', '.join(result['competencias_teste'])}.", f"- Modo: `{result['modo_avaliacao']}`.", f"- Janelas excluídas por publicação: {result['janelas_excluidas_publicacao']}.", f"- [Métricas por família/unidade]({fonte}/metricas.csv), [previsões avaliadas]({fonte}/previsoes_avaliacao.csv) e [cenário da próxima competência]({fonte}/previsoes_proxima_competencia.csv).", "", *[f"- Limite: {v}" for v in result["limites"]], ""]
            print(f"[{fonte}] {len(valid)} recortes avaliados; {skipped} sem amostra suficiente. Resultados: {output / fonte}", flush=True)
        except (ValueError, FileNotFoundError) as error:
            failed = True
            run["bases"][fonte] = {"status": "erro", "mensagem": str(error)}
            paragraphs += [f"## {fonte}", "", f"Execução não concluída: {error}", ""]
            print(f"[{fonte}] ERRO: {error}", file=sys.stderr, flush=True)
    paragraphs += ["## Leitura dos resultados", "", "Compare o modelo selecionado na validação com a persistência nas mesmas linhas do teste. Ganho negativo significa que repetir o último custo foi melhor. Uma previsão futura é um cenário de custo referencial; ainda não tem erro observado. A origem temporal é a competência indicada no CSV, que pode ser anterior ao mês atual do calendário.", "", "Os grupos nativos das duas fontes ainda não constituem uma taxonomia harmonizada. A comparação direta de serviços requer equivalência técnica revisada, mesma competência, regime e unidade. O parâmetro `--fim` permite repetir o estudo numa janela comum; ele não comprova essa equivalência por si só.", ""]
    (output / "execucao.json").write_text(json.dumps(run, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (output / "RESULTADOS.md").write_text("\n".join(paragraphs), encoding="utf-8")
    print(f"\nRelatório: {output / 'RESULTADOS.md'}", flush=True)
    return failed, run, historicos


def _periodos_iguais(bases):
    periodos = {
        (tuple(result.get("competencias_validacao", [])), tuple(result.get("competencias_teste", [])))
        for result in bases.values()
    }
    return len(periodos) == 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", choices=(*FONTES, "ambas"), default="ambas", help="Fonte a executar; padrão: ambas")
    parser.add_argument("--fim", help="Última competência incluída (YYYY-MM), por exemplo 2026-05 para uma janela comum")
    parser.add_argument("--saida", type=Path, help="Diretório novo para guardar esta execução")
    parser.add_argument("--config", type=Path, default=PASTA_ML / "configs" / "regressao.json")
    parser.add_argument("--sem-relatorio", action="store_true", help="Avaliar modelos sem gerar a apresentação HTML/PDF")
    args = parser.parse_args(argv)
    if args.fim:
        import re
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", args.fim):
            parser.error("--fim deve usar YYYY-MM")

    config = json.loads(args.config.read_text(encoding="utf-8"))
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    output = args.saida.resolve() if args.saida else PASTA_ML / "outputs" / run_id
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error(f"A pasta de saída já contém arquivos: {output}. Escolha uma pasta nova.")
    requested = FONTES if args.base == "ambas" else (args.base,)
    failed, run, historicos = _executar_bases(requested, output, config, args.fim)
    if not args.sem_relatorio and not failed:
        report_dir = output
        try:
            from orca_ml.relatorio import gerar_relatorio

            if len(requested) > 1 and not _periodos_iguais(run["bases"]):
                fim_comum = min(str(frame.competencia.max()) for frame in historicos.values())
                report_dir = output / "comparacao_mesma_janela"
                print(f"\nComparação didática: nova avaliação das duas bases até {fim_comum}.", flush=True)
                common_failed, common_run, historicos = _executar_bases(requested, report_dir, config, fim_comum)
                if common_failed:
                    raise ValueError("A avaliação no período comum não produziu recortes suficientes. Confira comparacao_mesma_janela/RESULTADOS.md.")
                if not _periodos_iguais(common_run["bases"]):
                    raise ValueError("As fases de validação e teste ainda divergem após o corte comum; confira lacunas nas competências dos datasets.")
            paths = gerar_relatorio(report_dir, historicos)
            run["relatorio"] = {"status": "gerado", "execucao_origem": str(report_dir), **{key: str(value) for key, value in paths.items()}}
            with (output / "RESULTADOS.md").open("a", encoding="utf-8") as file:
                file.write("\n## Relatório didático\n\n")
                for key in ("html", "pdf", "markdown"):
                    if key in paths:
                        file.write(f"- [{key.upper()}](<{Path(paths[key]).relative_to(output)}>).\n")
            for key in ("html", "pdf"):
                if key in paths:
                    print(f"Relatório {key.upper()}: {paths[key]}", flush=True)
        except Exception as error:
            failed = True
            run["relatorio"] = {"status": "erro", "execucao_origem": str(report_dir), "mensagem": str(error)}
            print(f"ERRO ao gerar o relatório didático: {error}. Os dados e as métricas foram preservados em {output}. Para tentar novamente: python gerar_relatorio.py --execucao \"{report_dir}\" --saida <pasta_nova>.", file=sys.stderr, flush=True)
        (output / "execucao.json").write_text(json.dumps(run, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return 1 if failed else 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ModuleNotFoundError as error:
        print(f"Dependência ausente: {error.name}. Selecione o Python do ambiente .venv no VS Code.\nInstalação: python -m pip install -r \"{PASTA_ML / 'requirements.txt'}\"", file=sys.stderr)
        raise SystemExit(2)
