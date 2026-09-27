"""Classificação temática para apresentar resultados sem alterar os modelos.

O mapa mantém cada par (fonte, grupo nativo) em um único nicho. Um nicho
compartilhado entre bases não comprova equivalência técnica de seus serviços.
As decisões sobre grupos mistos e demais limites ficam no JSON versionado.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


CAMINHO_PADRAO = Path(__file__).resolve().parents[1] / "configs" / "grupos_didaticos.json"


def _objeto_sem_duplicatas(pares: list[tuple[str, Any]]) -> dict:
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Chave JSON duplicada: {chave!r}. Cada grupo deve ter um único nicho.")
        objeto[chave] = valor
    return objeto


def _validar_config(config: dict) -> dict[str, str]:
    if not isinstance(config, dict):
        raise ValueError("O mapa deve ser um objeto com 'nichos' e 'mapeamento'.")
    nichos = config.get("nichos")
    mapeamento = config.get("mapeamento")
    if not isinstance(nichos, list) or not nichos:
        raise ValueError("O mapa deve conter uma lista não vazia de 'nichos'.")
    if not isinstance(mapeamento, dict) or not mapeamento:
        raise ValueError("O mapa deve conter um 'mapeamento' por fonte e grupo.")

    nomes: dict[str, str] = {}
    ordens = set()
    for nicho in nichos:
        if not isinstance(nicho, dict):
            raise ValueError("Cada nicho deve conter id, nome, ordem e descricao.")
        for campo in ("id", "nome", "descricao"):
            if not isinstance(nicho.get(campo), str) or not nicho[campo].strip():
                raise ValueError(f"Campo {campo!r} inválido no nicho: {nicho!r}.")
        if nicho["id"] in nomes:
            raise ValueError(f"Identificador de nicho duplicado: {nicho['id']!r}.")
        ordem = nicho.get("ordem")
        if isinstance(ordem, bool) or not isinstance(ordem, int) or ordem < 1:
            raise ValueError(f"Ordem inválida para o nicho {nicho['id']!r}; use inteiro positivo.")
        if ordem in ordens:
            raise ValueError(f"Ordem de nicho duplicada: {ordem}.")
        nomes[nicho["id"]] = nicho["nome"]
        ordens.add(ordem)

    for fonte, grupos in mapeamento.items():
        if not isinstance(fonte, str) or not fonte.strip() or not isinstance(grupos, dict):
            raise ValueError("Cada fonte deve ter um dicionário de grupos nativos.")
        for grupo, nicho_id in grupos.items():
            if not isinstance(grupo, str) or not grupo.strip():
                raise ValueError(f"Nome de grupo vazio ou inválido na fonte {fonte!r}.")
            if not isinstance(nicho_id, str) or nicho_id not in nomes:
                raise ValueError(f"O grupo {fonte!r} / {grupo!r} aponta para nicho inexistente: {nicho_id!r}.")
    return nomes


def carregar_mapa(path: str | Path | None = None) -> dict:
    """Lê e valida o JSON, rejeitando inclusive chaves duplicadas no arquivo.

    O caminho padrão independe do diretório corrente. O retorno também contém
    ``limitacoes`` e ``observacoes_mapeamento`` para exibição no relatório.
    """
    caminho = CAMINHO_PADRAO if path is None else Path(path)
    with caminho.open(encoding="utf-8") as arquivo:
        config = json.load(arquivo, object_pairs_hook=_objeto_sem_duplicatas)
    _validar_config(config)
    return config


def adicionar_nichos(frame: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Devolve uma cópia com ``nicho_id`` e ``nicho``, sem mudar as linhas.

    Preserva a fonte, os grupos, unidades, códigos, índices e ordem originais.
    Não consulta preços, erros nem resultados dos modelos. Grupos desconhecidos
    exigem revisão explícita do mapa, inclusive quando há um nicho de outros.
    """
    if config is None:
        config = carregar_mapa()
    nomes = _validar_config(config)
    faltantes = {"fonte", "grupo"} - set(frame.columns)
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes para o mapa de nichos: {', '.join(sorted(faltantes))}.")
    existentes = {"nicho_id", "nicho"} & set(frame.columns)
    if existentes:
        raise ValueError(f"As colunas de nicho já existem: {', '.join(sorted(existentes))}. Remova-as explicitamente antes de remapear.")
    if frame[["fonte", "grupo"]].isna().any().any():
        raise ValueError("Valores vazios em fonte ou grupo; revise o dataset antes de mapear os nichos.")
    if any(not isinstance(x, str) or not x.strip() for x in frame["fonte"]) or any(
        not isinstance(x, str) or not x.strip() for x in frame["grupo"]
    ):
        raise ValueError("Valores vazios ou não textuais em fonte ou grupo; preserve os nomes nativos.")

    pares = list(zip(frame["fonte"], frame["grupo"]))
    mapa = config["mapeamento"]
    desconhecidos = sorted({(fonte, grupo) for fonte, grupo in pares if grupo not in mapa.get(fonte, {})})
    if desconhecidos:
        detalhes = "; ".join(f"{fonte}: {grupo}" for fonte, grupo in desconhecidos)
        raise ValueError(f"Grupos ou fontes não mapeados: {detalhes}. Revise configs/grupos_didaticos.json e registre a decisão; não há categoria automática.")

    resultado = frame.copy(deep=True)
    ids = [mapa[fonte][grupo] for fonte, grupo in pares]
    # Listas mantêm a atribuição posicional mesmo quando o índice é duplicado.
    resultado["nicho_id"] = ids
    resultado["nicho"] = [nomes[nicho_id] for nicho_id in ids]
    return resultado


def unidade_legivel(unidade: str) -> str:
    """Formata o rótulo; não converte valores nem prova equivalência de serviço.

    Abreviações não verificadas são preservadas, por exemplo ``ms`` no DER.
    ``CHP`` e ``CHI`` permanecem distintos de hora simples.
    """
    rotulos = {
        "M": "m", "M2": "m²", "M²": "m²", "M3": "m³", "M³": "m³",
        "CM": "cm", "UN": "un", "UND": "un", "KG": "kg", "T": "t",
        "L": "L", "H": "h", "MES": "mês", "MÊS": "mês", "CJ": "cj",
        "PT": "pt", "VB": "vb", "CHP": "CHP", "CHI": "CHI",
        "KGXKM": "kg·km", "LXKM": "L·km", "M2XKM": "m²·km",
        "M3XKM": "m³·km", "MXKM": "m·km", "UNXKM": "un·km", "TXKM": "t·km",
    }
    return rotulos.get(str(unidade).strip().upper(), str(unidade))
