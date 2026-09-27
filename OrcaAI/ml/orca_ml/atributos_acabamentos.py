"""Atributos tabulares e grupos conservadores para o estudo de acabamentos.

As classes vêm dos grupos oficiais. O agrupamento de variantes é uma proteção
experimental, não uma certificação de equivalência técnica entre serviços.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata

import numpy as np
import pandas as pd

from .grupos import adicionar_nichos

NICHOS = ("pintura", "revestimentos_forros", "pisos")
CATEGORIAS = ("mao_obra", "material", "equipamento", "outros")
ATRIBUTOS = ([f"fracao_{c}" for c in CATEGORIAS]
             + [f"n_{c}" for c in CATEGORIAS]
             + ["horas_mao_obra", "horas_equipamento"])


def _exigir(frame, columns):
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")


def _texto(value):
    return " ".join(unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower().split())


def selecionar_recorte(historico: pd.DataFrame, competencia: str | None = None) -> pd.DataFrame:
    """Filtre cada linha por seu próprio nicho/unidade; não selecione sobreviventes."""
    _exigir(historico, ["fonte", "competencia", "codigo", "grupo", "unidade"])
    if historico.duplicated(["fonte", "competencia", "codigo"]).any():
        raise ValueError("Serviço/competência duplicado no histórico")
    dados = adicionar_nichos(historico.drop(columns=["nicho", "nicho_id", "classe"], errors="ignore"))
    unidades = dados.unidade.astype(str).str.strip().str.lower().str.replace("²", "2", regex=False)
    mask = dados.nicho_id.isin(NICHOS) & unidades.eq("m2")
    if competencia is not None:
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", competencia):
            raise ValueError("Competência deve usar YYYY-MM")
        mask &= dados.competencia.eq(competencia)
    result = dados.loc[mask].copy()
    result["classe"] = result.nicho_id
    return result.reset_index(drop=True)


def _normalizar_descricao(value: str) -> str:
    text = _texto(value)
    text = re.sub(r"\baf[_\s]*\d+[\/_]\d+", "", text)
    text = re.sub(r"\b(um|uma|dois|duas|tres|quatro|cinco|seis)\b", "#", text)
    text = re.sub(r"\d+(?:[.,/]\d+)*", "#", text)
    return " ".join(re.sub(r"[^a-z#]+", " ", text).split())


def agrupar_variantes(servicos: pd.DataFrame, recursos: pd.DataFrame) -> pd.DataFrame:
    """Una suportes de folhas iguais OU descrições sem medidas/demãos, transitivamente."""
    _exigir(servicos, ["codigo", "descricao"])
    _exigir(recursos, ["codigo_servico", "codigo_recurso", "categoria", "unidade_recurso"])
    data = servicos.copy()
    data["codigo"] = data.codigo.astype(str)
    if data.codigo.duplicated().any():
        raise ValueError("Código duplicado no catálogo de variantes")
    codes = sorted(data.codigo)
    parent = {code: code for code in codes}

    def find(code):
        while parent[code] != code:
            parent[code] = parent[parent[code]]
            code = parent[code]
        return code

    def union(a, b):
        a, b = find(a), find(b)
        parent[max(a, b)] = min(a, b)

    fingerprints = {}
    for code, group in recursos.groupby("codigo_servico", sort=True):
        code = str(code)
        if code not in parent:
            continue
        leaves = sorted(set(tuple(map(str, row)) for row in group[["categoria", "codigo_recurso", "unidade_recurso"]].itertuples(index=False, name=None)))
        fingerprints[code] = hashlib.sha256(repr(leaves).encode()).hexdigest()
    if set(fingerprints) != set(codes):
        raise ValueError("Serviço sem recursos não pode formar um grupo de variantes")
    data["assinatura_recursos"] = data.codigo.map(fingerprints)
    data["descricao_normalizada"] = data.descricao.map(_normalizar_descricao)
    for column in ("assinatura_recursos", "descricao_normalizada"):
        for value, group in data.groupby(column, sort=True):
            if not value:
                continue
            members = sorted(group.codigo)
            for code in members[1:]:
                union(members[0], code)
    components = {}
    for code in codes:
        components.setdefault(find(code), []).append(code)
    names = {root: "v_" + hashlib.sha256("|".join(members).encode()).hexdigest()[:16]
             for root, members in components.items()}
    data["grupo_particao"] = data.codigo.map(lambda code: names[find(code)])
    return data


def preparar_atributos(servicos: pd.DataFrame, recursos: pd.DataFrame) -> pd.DataFrame:
    """Prepare somente composições conciliadas, com ausência de categoria igual a zero.

    Frações calculadas sobre custos-folha antes dos truncamentos hierárquicos;
    não são porcentagens publicadas na tabela. O total oficial fica como metadata.
    """
    _exigir(servicos, ["fonte", "competencia", "codigo", "descricao", "custo", "status_composicao"])
    _exigir(recursos, ["codigo_servico", "codigo_recurso", "categoria", "unidade_recurso", "coeficiente", "custo_folha_sem_truncamento", "horas_mao_obra", "horas_equipamento"])
    if servicos.fonte.nunique() != 1 or servicos.competencia.nunique() != 1:
        raise ValueError("Prepare uma fonte e uma competência por vez")
    if not servicos.status_composicao.isin(["ok", "excluido"]).all():
        raise ValueError("Status de composição desconhecido")
    if servicos.codigo.duplicated().any():
        raise ValueError("Código duplicado no snapshot")
    rows = recursos.copy()
    rows["codigo_servico"] = rows.codigo_servico.astype(str)
    rows["codigo_recurso"] = rows.codigo_recurso.astype(str)
    if rows.duplicated(["codigo_servico", "codigo_recurso"]).any():
        raise ValueError("Recurso duplicado no mesmo serviço")
    if not set(rows.codigo_servico).issubset(set(servicos.codigo.astype(str))):
        raise ValueError("Recurso ligado a serviço desconhecido")
    if not rows.categoria.isin(CATEGORIAS).all():
        raise ValueError("Categoria desconhecida de recurso")
    numeric = ["coeficiente", "custo_folha_sem_truncamento", "horas_mao_obra", "horas_equipamento"]
    rows[numeric] = rows[numeric].apply(pd.to_numeric, errors="raise")
    values = rows[numeric].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Coeficientes, custos e horas devem ser finitos e não negativos")
    data = selecionar_recorte(servicos)
    data = data.loc[data.status_composicao.eq("ok")].copy()
    if data.empty:
        raise ValueError("Nenhuma composição conciliada no recorte")
    data["codigo"] = data.codigo.astype(str)
    rows = rows.loc[rows.codigo_servico.isin(data.codigo)].copy()
    records = []
    for code, group in rows.groupby("codigo_servico", sort=True):
        total = float(group.custo_folha_sem_truncamento.sum())
        if total <= 0:
            raise ValueError(f"Custo de folhas não positivo no serviço {code}")
        record = {"codigo": code, "custo_folhas_sem_truncamento": total}
        for category in CATEGORIAS:
            sub = group.loc[group.categoria.eq(category)]
            record[f"fracao_{category}"] = float(sub.custo_folha_sem_truncamento.sum() / total)
            record[f"n_{category}"] = int(sub.codigo_recurso.nunique())
        record["horas_mao_obra"] = float(group.horas_mao_obra.sum())
        record["horas_equipamento"] = float(group.horas_equipamento.sum())
        record["n_recursos"] = int(group.codigo_recurso.nunique())
        record["n_recursos_preco_sp"] = int(group.uf_preco.eq("SP").sum()) if "uf_preco" in group else 0
        records.append(record)
    if set(data.codigo) != set(record["codigo"] for record in records):
        raise ValueError("Composição conciliada sem recursos-folha")
    data = data.merge(pd.DataFrame(records), on="codigo", validate="one_to_one")
    if not np.isfinite(data.custo.astype(float)).all() or data.custo.le(0).any():
        raise ValueError("Custo oficial deve ser positivo e finito")
    data["diferenca_folhas_pct"] = 100 * (data.custo_folhas_sem_truncamento - data.custo) / data.custo
    return agrupar_variantes(data, rows).sort_values("codigo").reset_index(drop=True)
