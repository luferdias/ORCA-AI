#!/usr/bin/env python3
"""Reconstrua os datasets a partir dos ZIPs locais, sem baixar arquivos.

Execute no VS Code com o Python da pasta .venv. Os caminhos padrão são
resolvidos a partir deste script; a pasta atual do terminal não os altera.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PASTA_ML = Path(__file__).resolve().parent
PASTA_ORCA = PASTA_ML.parent
FONTES = ("sinapi_es", "der_es")


def conferir_manifesto(manifesto_path: str | Path) -> tuple[dict, Path]:
    """Valide o ZIP exato selecionado no manifesto, sem procurar substitutos."""
    manifest_path = Path(manifesto_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    name = manifest.get("arquivo")
    if not isinstance(name, str) or not name or Path(name).name != name or "\\" in name:
        raise ValueError(f"Nome de arquivo inválido no manifesto: {manifest_path}")
    if Path(name).suffix.lower() != ".zip":
        raise ValueError(f"O manifesto deve selecionar um ZIP: {manifest_path}")
    archive = manifest_path.parent / name
    if archive.resolve().parent != manifest_path.parent.resolve():
        raise ValueError(f"ZIP fora do diretório de originais: {archive}")
    if not archive.is_file():
        raise FileNotFoundError(f"ZIP indicado pelo manifesto não encontrado: {archive}")
    expected = manifest.get("sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
        raise ValueError(f"SHA-256 ausente ou inválido: {manifest_path}")
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != expected.lower():
        raise ValueError(f"SHA-256 divergente: {archive}; original não será utilizado")
    if manifest.get("bytes") is not None and manifest["bytes"] != archive.stat().st_size:
        raise ValueError(f"Tamanho divergente do manifesto: {archive}")
    zip_files = [p for p in manifest_path.parent.iterdir() if p.is_file() and p.suffix.lower() == ".zip"]
    if len(zip_files) != 1:
        raise ValueError(f"Múltiplos ZIPs/revisões em {manifest_path.parent}; mantenha uma edição explicitamente selecionada")
    return manifest, archive


def preparar_der(base: str | Path, dest: str | Path) -> dict:
    """Leia <base>/YYYY-MM/originais/manifesto.json e grave CSV + curadoria.

    Todos os manifestos e registros são validados antes de substituir o CSV.
    Nenhum arquivo no diretório de originais é alterado.
    """
    from orca_ml.der import parse_der_zip, preparar_csv

    base, dest = Path(base), Path(dest)
    if dest.resolve().is_relative_to(base.resolve()):
        raise ValueError("O dataset derivado deve ficar fora da árvore de arquivos originais")
    if not base.is_dir():
        raise FileNotFoundError(f"Pasta de originais DER-ES não encontrada: {base}")
    directories = sorted(p for p in base.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", p.name))
    if not directories:
        raise ValueError(f"Nenhuma competência local em {base}; a preparação não faz downloads")
    rows, editions, seen = [], [], set()
    for directory in directories:
        manifest_path = directory / "originais" / "manifesto.json"
        manifest, archive = conferir_manifesto(manifest_path)
        month = manifest.get("competencia")
        if month != directory.name:
            raise ValueError(f"Competência do manifesto diverge da pasta: {manifest_path}")
        if month in seen:
            raise ValueError(f"Competência/revisão duplicada: {month}")
        seen.add(month)
        if manifest.get("fonte") not in {"DER-ES", "der_es"} or manifest.get("regime") != "sem_desoneracao":
            raise ValueError(f"Fonte/regime inesperados no manifesto: {manifest_path}")
        published = manifest.get("publicado_em") or ""
        if published:
            datetime.strptime(published, "%Y-%m-%d")
        extracted = parse_der_zip(archive, month, publicado_em=published)
        costs = defaultdict(list)
        for row in extracted:
            value = row["custo"]
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"Custo inválido: {month}, código {row['codigo']}")
            costs[row["unidade"]].append(value)
        editions.append({
            "competencia": month, "arquivo": archive.name,
            "manifesto": str(manifest_path.relative_to(base)),
            "bytes": archive.stat().st_size, "sha256": manifest["sha256"].lower(),
            "publicado_em": published or None, "registros": len(extracted),
            "codigos_unicos": len({r["codigo"] for r in extracted}),
            "codigos": sorted({r["codigo"] for r in extracted}),
            "grupos": sorted({r["grupo"] for r in extracted}),
            "custos_por_unidade": {unit: {"quantidade": len(values), "minimo": min(values), "maximo": max(values)} for unit, values in sorted(costs.items())},
        })
        rows.extend(extracted)
    preparar_csv(rows, dest)
    report = {
        "fonte": "der_es", "regime": "sem_desoneracao", "uf": "ES",
        "preparado_em_utc": datetime.now(timezone.utc).isoformat(),
        "operacao": "reconstrucao_offline", "downloads_realizados": False,
        "registros": len(rows), "codigos_unicos": len({r["codigo"] for r in rows}),
        "competencias": editions,
        "dataset": dest.name, "dataset_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
        "assinatura_tipo": "descricao_unidade",
        "limite_assinatura": "A assinatura compara descrição e unidade; não verifica insumos, coeficientes nem subcomposições da CPU.",
        "publicacoes_ausentes": sum(not e["publicado_em"] for e in editions),
        "metricas_de_modelo_calculadas": False,
        "limites": [
            "As contagens descrevem serviços extraídos; não demonstram suficiência estatística para treinamento.",
            "Os mínimos e máximos são conferências de preços por unidade, não métricas de previsão.",
            "Datas de publicação ausentes permanecem desconhecidas; a competência não as substitui.",
        ],
    }
    (dest.parent / "curadoria.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", choices=(*FONTES, "ambas"), default="ambas", help="Fontes locais a preparar; padrão: ambas")
    args = parser.parse_args(argv)
    requested = FONTES if args.base == "ambas" else (args.base,)
    failed = False
    for source in requested:
        dest = PASTA_ORCA / "knowledge" / "datasets" / "ml_ufg" / source / "custos_historicos.csv"
        try:
            if source == "sinapi_es":
                from orca_ml.sinapi import preparar_historico_sinapi
                preparar_historico_sinapi(PASTA_ORCA / "bases" / "sinapi", dest)
            else:
                preparar_der(PASTA_ORCA / "bases" / "der_es", dest)
            print(f"[{source}] Dataset reconstruído: {dest}", flush=True)
        except (ValueError, FileNotFoundError) as error:
            failed = True
            print(f"[{source}] ERRO: {error}", file=sys.stderr, flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ModuleNotFoundError as error:
        print(f"Dependência ausente: {error.name}. Selecione o Python de .venv no VS Code.\nInstalação: python -m pip install -r \"{PASTA_ML / 'requirements.txt'}\"", file=sys.stderr)
        raise SystemExit(2)
