"""Estrutura única de um item de orçamento do ORCA-AI.

Cada item fica em ``OrcaAI/projetos/<AAAA-NNN-slug>/`` com as oito etapas
``00-entrada`` a ``07-assinados`` e os três arquivos de controle
``projeto.md``, ``plano-execucao.md`` e ``log-decisoes.md``.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

ETAPAS = (
    "00-entrada",
    "01-escopo",
    "02-quantitativos",
    "03-orcamento",
    "04-cotacoes",
    "05-validacoes",
    "06-documentos",
    "07-assinados",
)
ARQUIVOS_CONTROLE = ("projeto.md", "plano-execucao.md", "log-decisoes.md")
PADRAO_SLUG = re.compile(r"^\d{4}-\d{3}-[a-z0-9]+(-[a-z0-9]+)*$")
PASTAS_ESPECIAIS = ("_modelo", "_governanca_sei_agu_cgu", "_projetos_basicos")


def raiz_orcaai(inicio: Path | None = None) -> Path:
    """Sobe a partir de ``inicio`` até encontrar a pasta ``OrcaAI`` (com ``projetos/``)."""
    atual = (inicio or Path(__file__)).resolve()
    for candidato in (atual, *atual.parents):
        if candidato.name == "OrcaAI" and (candidato / "projetos").is_dir():
            return candidato
    raise FileNotFoundError("pasta OrcaAI não encontrada acima de " + str(atual))


@dataclass
class ResultadoValidacao:
    item: str
    faltantes: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.faltantes


def validar_item(pasta: Path) -> ResultadoValidacao:
    r = ResultadoValidacao(item=pasta.name)
    if not PADRAO_SLUG.match(pasta.name):
        r.avisos.append("nome fora do padrão AAAA-NNN-slug")
    for etapa in ETAPAS:
        if not (pasta / etapa).is_dir():
            r.faltantes.append(etapa + "/")
    for arquivo in ARQUIVOS_CONTROLE:
        if not (pasta / arquivo).is_file():
            r.faltantes.append(arquivo)
    for solto in pasta.iterdir():
        if (
            solto.is_file()
            and solto.name not in ARQUIVOS_CONTROLE
            and solto.name != "indice-dossie.md"
        ):
            r.avisos.append(f"arquivo solto na raiz do item: {solto.name}")
        if solto.is_dir() and solto.name not in ETAPAS:
            r.avisos.append(f"pasta fora das etapas: {solto.name}/")
    return r


def validar_projetos(raiz_projetos: Path) -> list[ResultadoValidacao]:
    itens = sorted(
        p for p in raiz_projetos.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    return [validar_item(p) for p in itens]


def criar_item(raiz_projetos: Path, slug: str, modelo: Path | None = None) -> Path:
    if not PADRAO_SLUG.match(slug):
        raise ValueError(f"slug inválido: {slug!r}; use AAAA-NNN-slug em minúsculas")
    destino = raiz_projetos / slug
    if destino.exists():
        raise FileExistsError(f"já existe: {destino}")
    modelo = modelo or (raiz_projetos / "_modelo")
    shutil.copytree(modelo, destino)
    return destino
