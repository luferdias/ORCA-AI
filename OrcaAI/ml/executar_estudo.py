#!/usr/bin/env python3
"""Execute no VS Code: estudo de pintura e acabamentos, ORCA-AI / UFG.

Prepara composições oficiais de maio/2026 e executa as tarefas selecionadas.
A execução das três tarefas gera relatório acadêmico HTML/PDF. Não requer rede.
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
COMPETENCIA = "2026-05"
FONTES = ("sinapi_es", "der_es")


def _sha(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def criar_saida(path: Path) -> Path:
    path = Path(path).resolve()
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise ValueError(f"A pasta de saída já contém arquivos: {path}. Escolha outra pasta.")
    path.mkdir(parents=True, exist_ok=True)
    return path


def conferir_zip(path, snapshot):
    expected = set(snapshot.arquivo_sha256)
    actual = _sha(Path(path))
    if expected != {actual}:
        raise ValueError(f"SHA-256 do ZIP diverge da versão usada no dataset: {path}")
    return actual


def comparar_populacoes(catalogo, previsoes):
    """Mostre diferenças de população, sem apagar serviços ausentes no snapshot."""
    import pandas as pd

    count = previsoes.groupby("codigo").size().rename("n_previsoes_regressao")
    codes = sorted(set(catalogo.codigo) | set(count.index))
    result = pd.DataFrame({"codigo": codes})
    result["no_catalogo_maio"] = result.codigo.isin(catalogo.codigo)
    result["n_previsoes_regressao"] = result.codigo.map(count).fillna(0).astype(int)
    result["na_regressao_teste"] = result.n_previsoes_regressao.gt(0)
    return result


def executar_fonte(fonte, saida, etapa):
    import pandas as pd
    from executar_regressao import carregar_dataset
    from orca_ml.atributos_acabamentos import ATRIBUTOS, preparar_atributos, selecionar_recorte

    pasta = saida / fonte
    dados = pasta / "dados"; dados.mkdir(parents=True)
    csv = PASTA_ORCA / "knowledge" / "datasets" / "ml_ufg" / fonte / "custos_historicos.csv"
    historico = carregar_dataset(csv, fonte)
    historico = historico.loc[historico.competencia.le(COMPETENCIA)].copy()
    snapshot = selecionar_recorte(historico, COMPETENCIA)
    if snapshot.empty:
        raise ValueError(f"Não há serviços em m² no recorte {fonte}/{COMPETENCIA}")
    raw_dir = PASTA_ORCA / "bases" / ("sinapi" if fonte == "sinapi_es" else "der_es") / COMPETENCIA / "originais"
    zips = sorted(raw_dir.glob("*.zip"))
    if len(zips) != 1:
        raise ValueError(f"Esperado exatamente um ZIP oficial em {raw_dir}")
    sha_zip = conferir_zip(zips[0], snapshot)
    print(f"\n[{fonte}] Extraindo composições de {len(snapshot)} serviços em m²...", flush=True)
    if fonte == "sinapi_es":
        from orca_ml.sinapi_composicoes import ler_composicoes_sinapi
        servicos, recursos, auditoria = ler_composicoes_sinapi(zips[0], COMPETENCIA, snapshot)
    else:
        from orca_ml.der_composicoes import ler_composicoes_der
        servicos, recursos, auditoria = ler_composicoes_der(zips[0], COMPETENCIA, snapshot)
    servicos.to_csv(dados / "composicoes_auditadas.csv", index=False, encoding="utf-8-sig")
    recursos.to_csv(dados / "recursos_folha.csv", index=False, encoding="utf-8-sig")
    _json(dados / "auditoria_extracao.json", auditoria)
    dataset = preparar_atributos(servicos, recursos)
    dataset.to_csv(dados / "dataset_acabamentos.csv", index=False, encoding="utf-8-sig")
    _json(dados / "atributos.json", ATRIBUTOS)
    dataset[["fonte", "codigo", "descricao", "classe", "assinatura_recursos", "descricao_normalizada", "grupo_particao"]].to_csv(dados / "grupos_variantes.csv", index=False, encoding="utf-8-sig")
    summary = {
        "fonte": fonte, "competencia": COMPETENCIA, "n_catalogo": len(snapshot), "n_validos": len(dataset),
        "n_excluidos": len(snapshot) - len(dataset), "n_grupos_variantes": int(dataset.grupo_particao.nunique()),
        "classes": {str(k): int(v) for k, v in dataset.classe.value_counts().items()},
        "n_servicos_preco_sp": int(dataset.n_recursos_preco_sp.gt(0).sum()),
        "max_diferenca_folhas_pct": float(dataset.diferenca_folhas_pct.abs().max()),
        "dataset_sha256": _sha(csv), "arquivo_dataset": str(csv.relative_to(PASTA_ORCA)),
        "zip_sha256": sha_zip, "arquivo_zip": str(zips[0].relative_to(PASTA_ORCA)), "atributos": ATRIBUTOS,
    }
    if etapa in ("todas", "classificacao"):
        from orca_ml.classificacao import executar_classificacao
        print(f"[{fonte}] Classificação com grupos de variantes separados...", flush=True)
        summary["classificacao"] = executar_classificacao(dataset, ATRIBUTOS, pasta / "classificacao")
    if etapa in ("todas", "agrupamento"):
        from orca_ml.agrupamento import executar_agrupamento
        print(f"[{fonte}] Agrupamento e verificação de estabilidade...", flush=True)
        summary["agrupamento"] = executar_agrupamento(dataset, ATRIBUTOS, pasta / "agrupamento")
    if etapa == "todas":
        from orca_ml.regressao import executar_experimento
        from orca_ml.estatisticas_relatorio import preparar_avaliacao, resumir_avaliacao, resumir_recortes
        from orca_ml.grupos import adicionar_nichos
        print(f"[{fonte}] Regressão temporal no mesmo recorte temático...", flush=True)
        temporal = selecionar_recorte(historico)
        config = json.loads((PASTA_ML / "configs" / "regressao.json").read_text(encoding="utf-8"))
        summary["regressao"] = executar_experimento(temporal, pasta / "regressao", config)
        previsoes = pd.read_csv(pasta / "regressao" / "previsoes_avaliacao.csv", dtype={"codigo": str})
        pares = adicionar_nichos(preparar_avaliacao(previsoes))
        pares.to_csv(pasta / "regressao" / "previsoes_pareadas.csv", index=False, encoding="utf-8-sig")
        resumir_avaliacao(pares, ["fonte", "nicho_id"]).to_csv(pasta / "regressao" / "estatisticas_nichos.csv", index=False, encoding="utf-8-sig")
        resumir_recortes(pares).to_csv(pasta / "regressao" / "estatisticas_recortes.csv", index=False, encoding="utf-8-sig")
        populacoes = comparar_populacoes(dataset, pares)
        populacoes.to_csv(dados / "populacoes_tarefas.csv", index=False, encoding="utf-8-sig")
        summary["populacoes"] = {
            "catalogo_e_regressao": int((populacoes.no_catalogo_maio & populacoes.na_regressao_teste).sum()),
            "somente_catalogo": int((populacoes.no_catalogo_maio & ~populacoes.na_regressao_teste).sum()),
            "somente_regressao": int((~populacoes.no_catalogo_maio & populacoes.na_regressao_teste).sum()),
        }
    _json(pasta / "resumo_fonte.json", summary)
    return summary


def main(argv=None, *, etapa_padrao="todas"):
    parser = argparse.ArgumentParser(description=f"{__doc__}\nEtapa padrão desta entrada: {etapa_padrao}.", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", choices=[*FONTES, "ambas"], default="ambas")
    parser.add_argument("--etapa", choices=["todas", "classificacao", "agrupamento"], default=etapa_padrao)
    parser.add_argument("--saida", type=Path, help="Pasta nova de resultados")
    parser.add_argument("--sem-relatorio", action="store_true", help="Salvar apenas resultados técnicos")
    args = parser.parse_args(argv)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    try:
        output = criar_saida(args.saida or PASTA_ML / "outputs" / f"estudo_acabamentos_{stamp}")
    except ValueError as error:
        parser.error(str(error))
    run = {"executado_em_utc": datetime.now(timezone.utc).isoformat(), "competencia": COMPETENCIA,
           "etapa": args.etapa, "status": "em_execucao", "bases": {}, "python": sys.version,
           "codigo_sha256": {str(p.relative_to(PASTA_ML)): _sha(p)
                             for p in [Path(__file__).resolve(), *sorted((PASTA_ML / "orca_ml").glob("*.py"))]},
           "taxonomia_sha256": _sha(PASTA_ML / "configs" / "grupos_didaticos.json")}
    registro = output / "execucao_estudo.json"
    _json(registro, run)
    try:
        requested = FONTES if args.base == "ambas" else (args.base,)
        for fonte in requested:
            run["bases"][fonte] = executar_fonte(fonte, output, args.etapa)
            _json(registro, run)
        run["resultados_sha256"] = {
            str(path.relative_to(output)): _sha(path)
            for fonte in requested for path in sorted((output / fonte).rglob("*")) if path.is_file()
        }
        _json(registro, run)
        if args.etapa == "todas" and not args.sem_relatorio:
            from orca_ml.relatorio_consolidado import gerar_relatorio_consolidado
            paths = gerar_relatorio_consolidado(output, run)
            run["relatorios"] = {key: str(path) for key, path in paths.items()}
        run["status"] = "concluido"
        _json(registro, run)
        print(f"\nEstudo concluído. Resultados: {output}", flush=True)
        for key, path in run.get("relatorios", {}).items():
            print(f"Relatório {key.upper()}: {path}", flush=True)
        return 0
    except Exception as error:
        run["status"] = "erro"; run["erro"] = str(error)
        _json(registro, run)
        print(f"ERRO: {error}\nResultados parciais preservados em: {output}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
