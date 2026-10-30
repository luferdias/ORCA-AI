"""Normalização de planilhas orçamentárias para o modelo único (A8 / normalizador-planilhas).

Formato de entrada reconhecido: exportação "Orçamento Sintético" do Orçafascio,
como a usada nos doze itens do acervo:

    linha 1: Obra | Bancos | B.D.I. | Encargos Sociais
    linha 2: <obra> | SINAPI - 04/2026 - Espírito Santo | 25,0% | Desonerado: ...
    linha N: Item | Código | Banco | Descrição | Und | Quant. | Valor Unit | Valor Unit com BDI | Total | Peso (%)
    linhas seguintes: grupos (sem código) e itens (com código)

Saída: linhas com as colunas de ``templates/planilhas/modelo-planilha-orcamentaria.csv``
mais ``grupo`` e ``tipo_item`` (``servico`` ou ``fornecimento``, inferido como
``servico`` por padrão) e um dicionário de metadados da obra.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import openpyxl

COLUNAS_MODELO = [
    "item",
    "codigo",
    "sistema",
    "descricao",
    "unidade",
    "quantidade",
    "custo_unitario_sem_bdi",
    "bdi_percentual",
    "preco_unitario_com_bdi",
    "preco_total_com_bdi",
    "fonte",
    "data_base",
    "observacoes",
    "grupo",
    "tipo_item",
]


def _norm(v) -> str:
    s = unicodedata.normalize("NFD", str(v if v is not None else ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def _num(v) -> float | None:
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("%", "").replace("R$", "").strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


@dataclass
class PlanilhaNormalizada:
    obra: str = ""
    bancos: str = ""
    bdi_percentual: float | None = None
    encargos: str = ""
    data_base: str = ""
    linhas: list[dict] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def itens(self) -> list[dict]:
        return [r for r in self.linhas if r["codigo"]]


def _data_base_dos_bancos(bancos: str) -> str:
    m = re.search(r"(\d{2})/(\d{4})", bancos)
    return f"{m.group(2)}-{m.group(1)}" if m else ""


def _sistema(banco: str, codigo: str) -> str:
    b = _norm(banco)
    if "sinapi" in b:
        return "SINAPI"
    if "iopes" in b or "der" in b:
        return "IOPES"
    if "sicro" in b:
        return "SICRO"
    if "orse" in b:
        return "ORSE"
    if "propri" in b or codigo.upper().startswith("SRAES-"):
        return "PROPRIA"
    return banco.strip().upper() or "DESCONHECIDO"


def normalizar_orcafascio_sintetico(
    caminho: Path, aba: str | None = None
) -> PlanilhaNormalizada:
    wb = openpyxl.load_workbook(caminho, data_only=True)
    ws = wb[aba] if aba else wb.worksheets[0]
    linhas = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    out = PlanilhaNormalizada()
    # cabeçalho da obra
    for i, r in enumerate(linhas[:6]):
        cab = [_norm(c) for c in r]
        if "obra" in cab and i + 1 < len(linhas):
            dados = linhas[i + 1]
            out.obra = str(dados[cab.index("obra")] or "").strip()
            if "bancos" in cab:
                out.bancos = str(dados[cab.index("bancos")] or "").strip()
            for k in cab:
                if k.startswith("b.d.i") or k == "bdi":
                    out.bdi_percentual = _num(dados[cab.index(k)])
                if "encargos" in k:
                    out.encargos = str(dados[cab.index(k)] or "").strip()
            break
    out.data_base = _data_base_dos_bancos(out.bancos)
    # linha de cabeçalho das colunas
    idx = None
    for i, r in enumerate(linhas):
        cab = [_norm(c) for c in r]
        if "item" in cab and ("codigo" in cab) and any("descri" in c for c in cab):
            idx = i
            break
    if idx is None:
        raise ValueError(f"cabeçalho de colunas não encontrado em {caminho.name}")
    cab = [_norm(c) for c in linhas[idx]]

    def col(*nomes):
        for n in nomes:
            for j, c in enumerate(cab):
                if c == n or c.startswith(n):
                    return j
        return None

    c_item, c_cod, c_banco, c_desc = (
        col("item"),
        col("codigo"),
        col("banco"),
        col("descri"),
    )
    c_und, c_qtd, c_unit = col("und", "unidade"), col("quant"), col("valor unit")
    c_unit_bdi = next(
        (j for j, c in enumerate(cab) if "com bdi" in c or "com b.d.i" in c), None
    )
    c_total = col("total")
    grupo_atual = ""
    for r in linhas[idx + 1 :]:
        item = str(r[c_item] or "").strip() if c_item is not None else ""
        desc = str(r[c_desc] or "").strip() if c_desc is not None else ""
        if not item or not desc:
            if desc.lower().startswith("total"):
                break
            continue
        codigo = str(r[c_cod] or "").strip() if c_cod is not None else ""
        if not codigo:
            grupo_atual = f"{item} {desc}"
            out.linhas.append(
                {c: "" for c in COLUNAS_MODELO}
                | {
                    "item": item,
                    "descricao": desc,
                    "grupo": grupo_atual,
                    "tipo_item": "grupo",
                }
            )
            continue
        banco = str(r[c_banco] or "").strip() if c_banco is not None else ""
        unit = _num(r[c_unit]) if c_unit is not None else None
        unit_bdi = _num(r[c_unit_bdi]) if c_unit_bdi is not None else None
        bdi = out.bdi_percentual
        if unit and unit_bdi:
            implicito = round((unit_bdi / unit - 1.0) * 100.0, 2)
            # O Orçafascio arredonda o preço com BDI a centavos; em preços
            # pequenos isso desloca o BDI implícito (24,74% em vez de 25%).
            # Se o preço exportado bate com o BDI do cabeçalho dentro de um
            # centavo, o BDI do item é o do cabeçalho; senão, o implícito.
            cab = out.bdi_percentual
            if (
                cab is not None
                and abs(unit_bdi - round(unit * (1 + cab / 100), 2)) <= 0.01
            ):
                bdi = cab
            else:
                bdi = implicito
        out.linhas.append(
            {
                "item": item,
                "codigo": codigo,
                "sistema": _sistema(banco, codigo),
                "descricao": desc,
                "unidade": str(r[c_und] or "").strip() if c_und is not None else "",
                "quantidade": _num(r[c_qtd]) if c_qtd is not None else None,
                "custo_unitario_sem_bdi": unit,
                "bdi_percentual": bdi,
                "preco_unitario_com_bdi": unit_bdi,
                "preco_total_com_bdi": _num(r[c_total])
                if c_total is not None
                else None,
                "fonte": banco
                or ("PRÓPRIA" if codigo.upper().startswith("SRAES-") else ""),
                "data_base": out.data_base,
                "observacoes": "",
                "grupo": grupo_atual,
                "tipo_item": "servico",
            }
        )
    if not out.itens:
        out.avisos.append("nenhum item com código encontrado")
    return out


def gravar_csv(plan: PlanilhaNormalizada, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS_MODELO)
        w.writeheader()
        for r in plan.linhas:
            w.writerow(
                {c: ("" if r.get(c) is None else r.get(c)) for c in COLUNAS_MODELO}
            )
    return destino
