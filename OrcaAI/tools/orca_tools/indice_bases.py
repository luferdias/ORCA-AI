"""Índice local das bases oficiais (A9 MineradorBases).

Lê os ZIPs originais de ``OrcaAI/bases/<fonte>/<competencia>/originais/`` com
os leitores já validados do módulo de ML (``OrcaAI/ufg/ml``) (``orca_ml.sinapi`` e ``orca_ml.der``)
e grava um índice tabular em ``OrcaAI/knowledge/indices/<fonte>/<competencia>/``:

- ``servicos.csv``: fonte, competencia, codigo, descricao, unidade, grupo,
  custo, regime, publicado_em, arquivo_sha256, localizador. No SINAPI, cada
  serviço aparece nos dois regimes: ``sem_desoneracao`` (aba CSD, lida pelo
  leitor validado do ML) e ``com_desoneracao`` (aba CCD, lida aqui; R-B1).
- ``manifesto.json``: origem (ZIP e SHA-256), contagens e data de geração.

O índice é ignorado pelo Git; o manifesto pode ser versionado. A consulta por
código é O(1) depois de carregado; a busca textual é por termos normalizados.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from orca_tools.estrutura_projeto import raiz_orcaai

COLUNAS = [
    "fonte",
    "competencia",
    "codigo",
    "descricao",
    "unidade",
    "grupo",
    "custo",
    "regime",
    "publicado_em",
    "arquivo_sha256",
    "localizador",
]
FONTES = {"sinapi_es": "sinapi", "der_es": "der_es"}


def _ml_no_path() -> None:
    ml = raiz_orcaai() / "ufg" / "ml"
    if str(ml) not in sys.path:
        sys.path.insert(0, str(ml))


def _zip_da_competencia(fonte: str, competencia: str) -> Path:
    pasta = raiz_orcaai() / "bases" / FONTES[fonte] / competencia / "originais"
    zips = sorted(pasta.glob("*.zip"))
    if len(zips) != 1:
        raise FileNotFoundError(f"esperado um ZIP em {pasta}; encontrados {len(zips)}")
    return zips[0]


def _publicado_em(pasta: Path) -> str:
    for m in pasta.glob("manifesto*.json"):
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for k in ("publicacao_exibida_no_portal", "publicado_em", "data_publicacao"):
            if d.get(k):
                return str(d[k])[:10]
    return ""


def construir(fonte: str, competencia: str, destino_raiz: Path | None = None) -> Path:
    """Constrói o índice de uma fonte/competência e devolve a pasta gerada."""
    _ml_no_path()
    origem = _zip_da_competencia(fonte, competencia)
    publicado = _publicado_em(origem.parent)
    t0 = time.time()
    if fonte == "sinapi_es":
        from orca_ml.sinapi import ler_zip_sinapi

        frame = ler_zip_sinapi(origem, competencia, publicado)
        linhas = frame[COLUNAS].to_dict("records")
        relatorio = dict(frame.attrs.get("relatorio", {}))
        desonerados, excluidos_ccd = _ler_servicos_ccd(origem, competencia, publicado)
        linhas += desonerados
        relatorio["servicos_com_desoneracao"] = len(desonerados)
        relatorio["excluidos_ccd"] = excluidos_ccd
        insumos = _ler_insumos_sinapi(origem, competencia)
    elif fonte == "der_es":
        from orca_ml.der import parse_der_zip

        linhas = [
            {c: r.get(c, "") for c in COLUNAS}
            for r in parse_der_zip(origem, competencia, publicado)
        ]
        relatorio = {"servicos_lidos": len(linhas)}
        insumos = []
    else:
        raise ValueError(f"fonte desconhecida: {fonte}")
    destino = (
        (destino_raiz or raiz_orcaai() / "knowledge" / "indices") / fonte / competencia
    )
    destino.mkdir(parents=True, exist_ok=True)
    with open(destino / "servicos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        for r in linhas:
            w.writerow({c: r.get(c, "") for c in COLUNAS})
    if insumos:
        with open(destino / "insumos.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLUNAS_INSUMOS)
            w.writeheader()
            w.writerows(insumos)
    sha_csv = hashlib.sha256((destino / "servicos.csv").read_bytes()).hexdigest()
    manifesto = {
        "fonte": fonte,
        "competencia": competencia,
        "publicado_em": publicado,
        "origem_zip": str(origem.relative_to(raiz_orcaai().parent)),
        "origem_sha256": hashlib.sha256(origem.read_bytes()).hexdigest(),
        "servicos": len(linhas),
        "servicos_por_regime": {
            r: sum(1 for x in linhas if x.get("regime") == r)
            for r in sorted({x.get("regime", "") for x in linhas})
        },
        "insumos": len(insumos),
        "servicos_csv_sha256": sha_csv,
        "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "duracao_s": round(time.time() - t0, 1),
        "relatorio_leitura": {k: v for k, v in relatorio.items() if k != "exclusoes"},
    }
    (destino / "manifesto.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return destino


def _ler_servicos_ccd(
    zip_path: Path, competencia: str, publicado_em: str
) -> tuple[list[dict], int]:
    """Serviços do SINAPI com desoneração (aba CCD), coluna ES.

    Mesmas verificações de cabeçalho do leitor CSD (competência, regime, coluna
    ES única, custo e %AS); custo ausente, hífen ou zero é excluído e contado.
    """
    import io
    import unicodedata
    import zipfile

    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
    from orca_ml.sinapi import _codigo_csd, _decimal, _normalizado, _texto

    raw = zip_path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    esperado = f"SINAPI_Referência_{competencia.replace('-', '_')}.xlsx"
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        nome = [
            n
            for n in z.namelist()
            if unicodedata.normalize("NFC", Path(n).name) == esperado
        ][0]
        wb = load_workbook(io.BytesIO(z.read(nome)), read_only=True, data_only=False)
    try:
        if "CCD" not in wb.sheetnames:
            return [], 0
        it = wb["CCD"].iter_rows(values_only=True)
        cab = [next(it) for _ in range(10)]
        ano, mes = competencia.split("-")
        if _texto(cab[2][1]) != f"{mes}/{ano}":
            raise ValueError(f"Competência divergente em CCD; esperado {competencia}")
        if "com desoneracao" not in _normalizado(cab[1][0]):
            raise ValueError("Regime com desoneração não confirmado em CCD")
        pos = [i for i, v in enumerate(cab[8]) if _texto(v).upper() == "ES"]
        if len(pos) != 1 or _normalizado(cab[9][pos[0]]) != "custo (r$)":
            raise ValueError("Coluna de custo do ES não identificada em CCD")
        col = pos[0]
        linhas, excluidos = [], 0
        for n, row in enumerate(it, 11):
            if all(v is None for v in row):
                continue
            codigo = _codigo_csd(row[1], f"CCD!B{n}")
            valor = row[col]
            if _texto(valor) in {"", "-", "–", "—"} or _decimal(valor, f"CCD!{n}") == 0:
                excluidos += 1
                continue
            custo = _decimal(valor, f"CCD!{get_column_letter(col + 1)}{n}")
            if custo < 0:
                raise ValueError(f"Custo negativo em CCD linha {n}")
            linhas.append(
                {
                    "fonte": "sinapi_es",
                    "competencia": competencia,
                    "codigo": codigo,
                    "descricao": _texto(row[2]),
                    "unidade": _texto(row[3]),
                    "grupo": _texto(row[0]),
                    "custo": float(custo),
                    "regime": "com_desoneracao",
                    "publicado_em": publicado_em,
                    "arquivo_sha256": sha,
                    "localizador": f"{nome}!CCD!{get_column_letter(col + 1)}{n}",
                }
            )
    finally:
        wb.close()
    return linhas, excluidos


COLUNAS_INSUMOS = [
    "fonte",
    "competencia",
    "codigo",
    "classificacao",
    "descricao",
    "unidade",
    "origem_preco",
    "preco",
    "regime",
    "localizador",
]


def _ler_insumos_sinapi(zip_path: Path, competencia: str) -> list[dict]:
    """Insumos do SINAPI (abas ISD sem desoneração e ICD com desoneração), coluna ES."""
    import io
    import unicodedata
    import zipfile

    from openpyxl import load_workbook

    esperado = f"SINAPI_Referência_{competencia.replace('-', '_')}.xlsx"
    with zipfile.ZipFile(zip_path) as z:
        nome = [
            n
            for n in z.namelist()
            if unicodedata.normalize("NFC", Path(n).name) == esperado
        ][0]
        wb = load_workbook(io.BytesIO(z.read(nome)), read_only=True, data_only=True)
    linhas: list[dict] = []
    try:
        for aba, regime in (("ISD", "sem_desoneracao"), ("ICD", "com_desoneracao")):
            if aba not in wb.sheetnames:
                continue
            ws = wb[aba]
            it = ws.iter_rows(values_only=True)
            cab = None
            for n, row in enumerate(it, 1):
                vals = [
                    str(v).replace("\n", " ").strip() if v is not None else ""
                    for v in row
                ]
                if cab is None:
                    if (
                        len(vals) > 4
                        and vals[1].lower().startswith("código do")
                        and "ES" in vals
                    ):
                        cab = vals
                        col_es = vals.index("ES")
                    continue
                codigo = vals[1]
                if not codigo or not codigo.isdigit():
                    continue
                preco = row[col_es] if col_es < len(row) else None
                linhas.append(
                    {
                        "fonte": "sinapi_es",
                        "competencia": competencia,
                        "codigo": codigo,
                        "classificacao": vals[0],
                        "descricao": vals[2],
                        "unidade": vals[3],
                        "origem_preco": vals[4],
                        "preco": "" if preco in (None, "") else preco,
                        "regime": regime,
                        "localizador": f"{aba}!B{n}",
                    }
                )
            if cab is None:
                raise ValueError(f"cabeçalho de insumos não encontrado na aba {aba}")
    finally:
        wb.close()
    return linhas


def _norm(texto: str) -> str:
    s = unicodedata.normalize("NFD", str(texto or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


REGIME_PADRAO = "com_desoneracao"


@dataclass
class Indice:
    fonte: str
    competencia: str
    por_codigo: dict[str, dict]
    linhas: list[dict]

    regime: str = REGIME_PADRAO

    @classmethod
    def carregar(
        cls,
        fonte: str,
        competencia: str,
        raiz_indices: Path | None = None,
        regime: str = REGIME_PADRAO,
    ) -> "Indice":
        """Carrega o índice; ``regime`` é o preferido (desonerado por padrão, R-B1).

        Quando o código existe no regime preferido, é essa linha que ``codigo``
        e ``buscar`` devolvem; se só existir no outro regime (bases antigas ou
        DER-ES), a linha disponível é devolvida, e o campo ``regime`` diz qual.
        """
        pasta = (
            (raiz_indices or raiz_orcaai() / "knowledge" / "indices")
            / fonte
            / competencia
        )
        with open(pasta / "servicos.csv", encoding="utf-8") as f:
            linhas = list(csv.DictReader(f))
        if (pasta / "insumos.csv").exists():
            with open(pasta / "insumos.csv", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    r["tipo"] = "insumo"
                    linhas.append(r)
        for r in linhas:
            r.setdefault("tipo", "servico")
            r["_busca"] = _norm(r["descricao"])
        linhas.sort(key=lambda r: r.get("regime") != regime)
        por_codigo: dict[str, dict] = {}
        preferidas: list[dict] = []
        vistos: set[tuple[str, str]] = set()
        for r in linhas:
            chave = (r["tipo"], r["codigo"])
            if chave in vistos:
                continue
            vistos.add(chave)
            preferidas.append(r)
            por_codigo.setdefault(r["codigo"], r)
        return cls(fonte, competencia, por_codigo, preferidas, regime)

    def codigo(self, codigo: str) -> dict | None:
        return self.por_codigo.get(str(codigo).strip())

    def buscar(self, termos: str, limite: int = 10) -> list[dict]:
        toks = [t for t in _norm(termos).split() if len(t) > 2]
        if not toks:
            return []
        pont = []
        for r in self.linhas:
            n = sum(1 for t in toks if t in r["_busca"])
            if n:
                pont.append((n, r))
        pont.sort(key=lambda x: (-x[0], x[1]["codigo"]))
        return [r for _, r in pont[:limite]]
