"""Valida um item do acervo de ponta a ponta (comando /validar-orcamento).

1. Localiza a planilha sintética do Orçafascio em ``03-orcamento``.
2. Normaliza para o modelo único em ``03-orcamento/planilha-normalizada.csv``.
3. Audita G-01 e G-02 com ``orca_tools.code_guardrail_validator``.
4. Confere os códigos contra o índice local da competência da planilha com
   ``check-sinapi-iopes-codes/scripts/validate_codes.py`` (se o índice existir).
5. Escreve ``05-validacoes/relatorio-guardrails.md`` e ``validacao-codigos.md``.

Uso:
    OrcaAI/ml/.venv/bin/python OrcaAI/tools/cli/validar_item.py 2026-001-teto-elevadores [--planilha ARQ.xlsx]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.catalogo import carregar  # noqa: E402
from orca_tools.code_guardrail_validator import auditar_orcamento  # noqa: E402
from orca_tools.estrutura_projeto import raiz_orcaai  # noqa: E402
from orca_tools.normalizar_planilha import gravar_csv, normalizar_orcafascio_sintetico  # noqa: E402


def _unidade(u: str) -> str:
    """Normaliza unidades para a comparação com as bases (m² → m2, m³ → m3)."""
    return (u or "").replace("²", "2").replace("³", "3").strip()


def _sem_acento(texto: str) -> str:
    import unicodedata

    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    ).lower()


def localizar_planilha(pasta: Path):
    """Devolve a primeira planilha que o normalizador reconhece, preferindo nomes com 'orcamento'."""
    excluir = ("analit", "bdi", "cronograma", "rela", "normalizada")
    candidatos = [
        p
        for p in sorted(pasta.glob("*.xlsx"))
        if not any(x in _sem_acento(p.name) for x in excluir)
    ]
    candidatos.sort(
        key=lambda p: (0 if "orcamento" in _sem_acento(p.name) else 1, p.name)
    )
    erros = []
    for c in candidatos:
        try:
            return c, normalizar_orcafascio_sintetico(c)
        except ValueError as e:
            erros.append(f"{c.name}: {e}")
    raise FileNotFoundError(
        "nenhuma planilha sintética reconhecida em "
        + str(pasta)
        + "; "
        + "; ".join(erros)
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Valida um item do acervo de ponta a ponta."
    )
    ap.add_argument("item", help="slug do item em OrcaAI/projetos")
    ap.add_argument(
        "--planilha",
        help="planilha sintética (.xlsx); padrão: primeira em 03-orcamento",
    )
    args = ap.parse_args()
    raiz = raiz_orcaai()
    pasta_item = raiz / "projetos" / args.item
    if not pasta_item.is_dir():
        print("item não encontrado:", pasta_item)
        return 1
    if args.planilha:
        planilha = Path(args.planilha)
        plan = normalizar_orcafascio_sintetico(planilha)
    else:
        planilha, plan = localizar_planilha(pasta_item / "03-orcamento")
    csv_norm = gravar_csv(
        plan, pasta_item / "03-orcamento" / "planilha-normalizada.csv"
    )
    itens = [
        {
            "item": r["item"],
            "codigo": r["codigo"],
            # o sistema é derivado do banco e do código; a coluna Banco da exportação
            # às vezes vem deslocada, por isso ele prevalece
            "fonte": r["sistema"]
            if r["sistema"] not in ("", "DESCONHECIDO")
            else r["fonte"],
            "bdi": r["bdi_percentual"] or 0.0,
            "tipo": r["tipo_item"],
        }
        for r in plan.itens
    ]
    cat = carregar(raiz / "agents" / "catalogo.yaml")
    limite = str(cat["parametros_fixos"].get("itens_historicos_ate", ""))
    historico = bool(limite) and args.item[: len(limite)] <= limite
    audit = auditar_orcamento(itens, series_historicas_toleradas=historico)
    hoje = time.strftime("%d/%m/%Y")
    val = pasta_item / "05-validacoes"
    val.mkdir(exist_ok=True)

    # --- validação de códigos contra o índice local -------------------
    cat_args, cat_nota = [], []
    comp = plan.data_base
    import csv as _csv

    for fonte, nome in (("sinapi_es", "SINAPI"), ("der_es", "IOPES")):
        pasta_idx = raiz / "knowledge" / "indices" / fonte / comp
        if not comp or not (pasta_idx / "servicos.csv").exists():
            cat_nota.append(
                f"índice {fonte} {comp or '(sem data-base)'} ausente; rode tools/cli/indexar_bases.py"
            )
            continue
        # catálogo temporário no formato que validate_codes.py reconhece
        cat_csv = (
            Path(tempfile.mkdtemp(prefix="orca-cat-"))
            / f"catalogo-{nome.lower()}-{comp}.csv"
        )
        with open(cat_csv, "w", newline="", encoding="utf-8") as f:
            w = _csv.DictWriter(
                f, fieldnames=["codigo", "sistema", "descricao", "unidade", "preco"]
            )
            w.writeheader()
            for arq, col_preco in (("servicos.csv", "custo"), ("insumos.csv", "preco")):
                if (pasta_idx / arq).exists():
                    with open(pasta_idx / arq, encoding="utf-8") as g:
                        for r in _csv.DictReader(g):
                            w.writerow(
                                {
                                    "codigo": r["codigo"],
                                    "sistema": nome,
                                    "descricao": r["descricao"],
                                    "unidade": _unidade(r["unidade"]),
                                    "preco": r.get(col_preco, ""),
                                }
                            )
        cat_args.append(f"{nome.lower()}={cat_csv}")
    codigos_md = [
        f"# Validação de códigos — {args.item}",
        "",
        f"Data: {hoje}. Planilha: `{planilha.name}`. Data-base declarada: {comp or 'não identificada'}.",
    ]
    oficiais = [r for r in plan.itens if r["sistema"] in ("SINAPI", "IOPES")]
    csv_oficiais = val / "codigos-oficiais.csv"
    with open(csv_oficiais, "w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(
            f, fieldnames=["n", "codigo", "sistema", "descricao", "unidade"]
        )
        w.writeheader()
        for r in oficiais:
            w.writerow(
                {
                    "n": r["item"],
                    "codigo": r["codigo"],
                    "sistema": r["sistema"],
                    "descricao": r["descricao"],
                    "unidade": _unidade(r["unidade"]),
                }
            )
    if cat_args and oficiais:
        script = (
            raiz
            / "agents"
            / "skills"
            / "check-sinapi-iopes-codes"
            / "scripts"
            / "validate_codes.py"
        )
        saida_json = val / "validacao-codigos.json"
        cmd = [
            sys.executable,
            str(script),
            "--source",
            str(csv_oficiais),
            "--json-out",
            str(saida_json),
        ]
        for c in cat_args:
            cmd += ["--catalog", c]
        r = subprocess.run(cmd, capture_output=True, text=True)
        codigos_md += [
            "",
            "Catálogos: " + ", ".join(f"`{c.split('=')[0]}`" for c in cat_args) + ".",
            "",
            "```",
            (r.stdout or r.stderr).strip()[:4000],
            "```",
        ]
        codigos_md.insert(
            3,
            f"Itens com código SINAPI ou IOPES submetidos ao validador: {len(oficiais)} de {len(plan.itens)}.",
        )
        if saida_json.exists():
            rel = json.loads(saida_json.read_text(encoding="utf-8"))
            resumo = rel.get("summary") or rel.get("resumo") or {}
            if resumo:
                codigos_md += ["", "| Situação | Quantidade |", "| --- | ---: |"] + [
                    f"| {k} | {v} |" for k, v in resumo.items()
                ]
    elif cat_args:
        codigos_md += [
            "",
            "Nenhum item com código SINAPI ou IOPES nesta planilha; validação externa não aplicável.",
        ]
    if cat_nota:
        codigos_md += ["", "Observações:", ""] + [f"- {n}" for n in cat_nota]
    proprios = [r for r in plan.itens if r["sistema"] == "PROPRIA"]
    codigos_md += [
        "",
        f"Itens com código próprio (chancela SRAES-): {len(proprios)} de {len(plan.itens)}. Códigos próprios não constam nas bases oficiais por definição; sua validação é a memória de cálculo da composição (G-01) e as cotações (G-10).",
    ]
    (val / "validacao-codigos.md").write_text(
        "\n".join(codigos_md) + "\n", encoding="utf-8"
    )

    # --- relatório de guardrails ----------------------------------------
    total = round(sum((r["preco_total_com_bdi"] or 0) for r in plan.itens), 2)
    g = [
        f"# Relatório de guardrails — {args.item}",
        "",
        f"Data: {hoje}. Obra: {plan.obra}. Bancos: {'; '.join(plan.bancos.splitlines())}. BDI declarado: {plan.bdi_percentual}%. Encargos: {plan.encargos}.",
        "",
        f"**Status: {audit['status_geral']}** · itens: {len(plan.itens)} · total com BDI: R$ {total:,.2f}".replace(
            ",", "X"
        )
        .replace(".", ",")
        .replace("X", "."),
        "",
        "## Bloqueios",
        "",
        *([f"- {b}" for b in audit["bloqueios"]] or ["- nenhum"]),
        "",
        "## Ressalvas",
        "",
        *([f"- {a}" for a in audit["alertas"]] or ["- nenhuma"]),
        "",
        "## Conformidades",
        "",
        f"- {len(audit['conformidades'])} verificações conformes (G-01 e G-02).",
        "",
        "## Escopo desta validação automática",
        "",
        "- G-01 e G-02 executados por `orca_tools.code_guardrail_validator`; G-03 a G-10 exigem revisão do A4 com memórias de cálculo, cotações e documentos.",
        (
            "- Item aprovado do acervo: séries próprias históricas toleradas pelo G-01 (R-B6)."
            if historico
            else "- Item novo: composições próprias devem usar SRAES-CP / SRAES-INS."
        ),
        "- Códigos oficiais conferidos em `validacao-codigos.md`.",
        f"- Planilha normalizada: `03-orcamento/{csv_norm.name}`.",
    ]
    (val / "relatorio-guardrails.md").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(
        f"{args.item}: {audit['status_geral']} | itens {len(plan.itens)} | bloqueios {len(audit['bloqueios'])} | ressalvas {len(audit['alertas'])} | relatórios em {val}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
