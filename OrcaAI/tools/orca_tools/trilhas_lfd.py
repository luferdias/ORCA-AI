"""Trilhas de aprendizado por demonstração (LfD) — formato e utilitários.

Uma trilha é um arquivo JSONL em
``OrcaAI/knowledge/demonstracoes/<item>/<AAAA-MM-DD>-<atividade>.jsonl``.
Cada linha é um evento observado enquanto o engenheiro trabalha:

    {"instante": "2026-10-29T14:03:11", "aplicacao": "orcafascio",
     "tela": "busca de composições", "acao": "busca",
     "entrada": "pintura latex acrilica parede", "resultado": "104642 selecionado",
     "campos": {"base": "SINAPI", "praca": "ES", "codigo": "104642", "tipo": "analitica",
                "quantidade": 120.5, "bdi": 25.0},
     "justificativa": "composição com andaime incluso"}

Quem grava: o A10 (Antigravity) no navegador; o A2 para Excel e Word por
diferença entre versões salvas. Quem lê: o A3, para escrever os padrões em
``OrcaAI/knowledge/padroes/<atividade>.md``, validados pelo A4.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

APLICACOES = ("orcafascio", "excel", "word", "pdf", "cad", "outro")
ACOES = (
    "busca",
    "selecao",
    "digitacao",
    "calculo",
    "filtro",
    "exportacao",
    "observacao",
)


@dataclass
class Evento:
    aplicacao: str
    acao: str
    entrada: str = ""
    resultado: str = ""
    tela: str = ""
    campos: dict = field(default_factory=dict)
    justificativa: str = ""
    instante: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%S"))

    def validar(self) -> list[str]:
        erros = []
        if self.aplicacao not in APLICACOES:
            erros.append(f"aplicacao inválida: {self.aplicacao}")
        if self.acao not in ACOES:
            erros.append(f"acao inválida: {self.acao}")
        if "senha" in json.dumps(self.campos, ensure_ascii=False).lower():
            erros.append("campos não podem conter senha")
        return erros


class Trilha:
    def __init__(self, caminho: Path):
        self.caminho = caminho
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.jsonl$", caminho.name)
        if not m:
            raise ValueError("nome deve ser AAAA-MM-DD-<atividade>.jsonl")
        self.data, self.atividade = m.group(1), m.group(2)
        self.item = caminho.parent.name

    def registrar(self, evento: Evento) -> None:
        erros = evento.validar()
        if erros:
            raise ValueError("; ".join(erros))
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(self.caminho, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(evento), ensure_ascii=False) + "\n")

    def eventos(self) -> list[Evento]:
        if not self.caminho.exists():
            return []
        with open(self.caminho, encoding="utf-8") as f:
            return [Evento(**json.loads(linha)) for linha in f if linha.strip()]

    def resumo(self) -> dict:
        """Contagens que o A3 usa como ponto de partida para escrever um padrão."""
        evs = self.eventos()
        bases = Counter(e.campos.get("base") for e in evs if e.campos.get("base"))
        familias = Counter(
            str(e.campos.get("codigo"))[:2] for e in evs if e.campos.get("codigo")
        )
        bdis = Counter(
            e.campos.get("bdi") for e in evs if e.campos.get("bdi") is not None
        )
        return {
            "item": self.item,
            "data": self.data,
            "atividade": self.atividade,
            "eventos": len(evs),
            "acoes": dict(Counter(e.acao for e in evs)),
            "bases": dict(bases),
            "familias_de_codigo": dict(familias),
            "bdi": dict(bdis),
            "justificativas": [e.justificativa for e in evs if e.justificativa],
        }


def listar_trilhas(raiz_demonstracoes: Path) -> list[Trilha]:
    return [Trilha(p) for p in sorted(raiz_demonstracoes.glob("*/*.jsonl"))]
