"""Estrutura única de um item de orçamento do ORCA-AI.

Cada item fica em ``OrcaAI/projetos/<AAAA-NNN-slug>/`` com os três arquivos de
controle ``projeto.md``, ``plano-execucao.md`` e ``log-decisoes.md`` e as
etapas ``00-entrada`` a ``07-assinados``.

Desde 30/10/2026 (entrevista de maturidade, regras R-E1 e R-E2) as etapas são
criadas **sob demanda**: ``criar_item`` gera os arquivos de controle e
``00-entrada``; as demais nascem por ``criar_etapa`` quando a ordem de serviço
as aciona, já com um ``LEIA-ME.md`` que diz o que a etapa recebe e entrega.
Itens históricos têm só as etapas aplicáveis; ``validar_item`` exige apenas os
arquivos de controle e aceita qualquer subconjunto das etapas conhecidas.
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
ETAPAS_DESCRICAO = {
    "00-entrada": (
        "Recebe: demanda ou despacho do SEI, relatório de vistoria quando houve, "
        "projeto básico e demais arquivos recebidos (R-A3). "
        "Entrega: nada; é a origem do item."
    ),
    "01-escopo": (
        "Recebe: entrada e decisão da chefia sobre o escopo (R-A2). "
        "Entrega: escopo aprovado, premissas.md com cada detalhe de executivo "
        "assumido (R-A4) e lista de serviços."
    ),
    "02-quantitativos": (
        "Recebe: escopo aprovado e projeto. "
        "Entrega: memória de cálculo por serviço e descrições canônicas (A3 e A6)."
    ),
    "03-orcamento": (
        "Recebe: quantitativos e índices das bases. "
        "Entrega: planilha orçamentária, composições SRAES-CP, BDI, itens.yaml; "
        "é a fonte do orçamento (R-D1)."
    ),
    "04-cotacoes": (
        "Recebe: insumos sem base oficial. "
        "Entrega: três propostas IN 65/2021, mediana, mapa e relatório de cotações (A11)."
    ),
    "05-validacoes": (
        "Recebe: planilha, composições e exportação do Orçafascio. "
        "Entrega: validacao-codigos, relatorio-guardrails, ordens de serviço os-NNN.md "
        "e confronto com a exportação (R-C2, R-D5)."
    ),
    "06-documentos": (
        "Recebe: planilha validada e escopo. "
        "Entrega: especificação técnica, memorial de BDI, despachos SEI e demais "
        "peças, em Markdown e renderizadas (R-C6)."
    ),
    "07-assinados": (
        "Recebe: peças finais aprovadas pelo engenheiro. "
        "Entrega: PDFs assinados e dossiê de contratação."
    ),
}
ETAPAS_INICIAIS = ("00-entrada",)
ARQUIVOS_CONTROLE = ("projeto.md", "plano-execucao.md", "log-decisoes.md")
ARQUIVOS_RAIZ_ACEITOS = ARQUIVOS_CONTROLE + ("indice-dossie.md",)
ARQUIVOS_ESTRUTURA = ("LEIA-ME.md", ".gitkeep")
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
    etapas: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.faltantes


def etapa_vazia(pasta: Path) -> bool:
    """Verdadeiro quando a etapa só tem arquivos de estrutura (LEIA-ME, .gitkeep)."""
    return not any(
        p for p in pasta.rglob("*") if p.is_file() and p.name not in ARQUIVOS_ESTRUTURA
    )


def validar_item(pasta: Path) -> ResultadoValidacao:
    r = ResultadoValidacao(item=pasta.name)
    if not PADRAO_SLUG.match(pasta.name):
        r.avisos.append("nome fora do padrão AAAA-NNN-slug")
    for arquivo in ARQUIVOS_CONTROLE:
        if not (pasta / arquivo).is_file():
            r.faltantes.append(arquivo)
    for solto in sorted(pasta.iterdir()):
        if solto.name == ".DS_Store":
            continue
        if solto.is_file() and solto.name not in ARQUIVOS_RAIZ_ACEITOS:
            r.avisos.append(f"arquivo solto na raiz do item: {solto.name}")
        if solto.is_dir():
            if solto.name in ETAPAS:
                r.etapas.append(solto.name)
            else:
                r.avisos.append(f"pasta fora das etapas: {solto.name}/")
    return r


def validar_projetos(raiz_projetos: Path) -> list[ResultadoValidacao]:
    itens = sorted(
        p for p in raiz_projetos.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    return [validar_item(p) for p in itens]


def criar_etapa(item: Path, etapa: str, modelo: Path | None = None) -> Path:
    """Cria uma etapa sob demanda, com o LEIA-ME do modelo ou o texto padrão.

    Idempotente: se a etapa já existe, apenas a devolve.
    """
    if etapa not in ETAPAS:
        raise ValueError(
            f"etapa desconhecida: {etapa!r}; use uma de {', '.join(ETAPAS)}"
        )
    destino = item / etapa
    if destino.is_dir():
        return destino
    destino.mkdir(parents=True)
    leia_me = (modelo / etapa / "LEIA-ME.md") if modelo else None
    if leia_me and leia_me.is_file():
        shutil.copy2(leia_me, destino / "LEIA-ME.md")
    else:
        (destino / "LEIA-ME.md").write_text(
            f"# {etapa}\n\n{ETAPAS_DESCRICAO[etapa]}\n", encoding="utf-8"
        )
    return destino


def criar_item(raiz_projetos: Path, slug: str, modelo: Path | None = None) -> Path:
    """Cria um item com os arquivos de controle e as etapas iniciais (R-E1)."""
    if not PADRAO_SLUG.match(slug):
        raise ValueError(f"slug inválido: {slug!r}; use AAAA-NNN-slug em minúsculas")
    destino = raiz_projetos / slug
    if destino.exists():
        raise FileExistsError(f"já existe: {destino}")
    modelo = modelo or (raiz_projetos / "_modelo")
    destino.mkdir(parents=True)
    for arquivo in ARQUIVOS_CONTROLE:
        origem = modelo / arquivo
        if origem.is_file():
            shutil.copy2(origem, destino / arquivo)
        else:
            (destino / arquivo).write_text(f"# {arquivo[:-3]}\n", encoding="utf-8")
    for etapa in ETAPAS_INICIAIS:
        criar_etapa(destino, etapa, modelo)
    return destino
