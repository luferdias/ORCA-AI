"""Regenera as projeções do catálogo único de agentes.

Uso, a partir de qualquer pasta:
    OrcaAI/ml/.venv/bin/python OrcaAI/tools/cli/gerar_projecoes.py [--verificar]

Com --verificar, gera em pasta temporária e compara com o repositório; sai com
código 1 se houver diferença (uso em CI e no comando /auditar-5s).
"""

from __future__ import annotations

import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.catalogo import PASTAS_PROJECAO, carregar, gerar, validar  # noqa: E402


def raiz_repo() -> Path:
    return Path(__file__).resolve().parents[3]


def _diferencas(a: Path, b: Path, rel: str) -> list[str]:
    difs: list[str] = []
    da, db = a / rel, b / rel
    if not da.exists() or not db.exists():
        return [rel] if da.exists() != db.exists() else []
    cmp = filecmp.dircmp(da, db, ignore=["historico", "__pycache__", ".DS_Store"])
    pilha = [(cmp, rel)]
    while pilha:
        c, base = pilha.pop()
        difs += [f"{base}/{x}" for x in c.left_only + c.right_only + c.diff_files]
        pilha += [(sub, f"{base}/{nome}") for nome, sub in c.subdirs.items()]
    return difs


def main() -> int:
    raiz = raiz_repo()
    cat = carregar(raiz / "OrcaAI" / "agents" / "catalogo.yaml")
    erros = validar(cat, raiz)
    if erros:
        print("catálogo inválido:")
        for e in erros:
            print("  -", e)
        return 1
    if "--verificar" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            for arq in ("CLAUDE.md", "AGENTS.md"):
                (destino / arq).write_text(
                    (raiz / arq).read_text(encoding="utf-8"), encoding="utf-8"
                )
            arquivos = gerar(cat, raiz, destino)
            difs: list[str] = []
            for rel in PASTAS_PROJECAO + (".agent/rules", ".agent/ARCHITECTURE.md"):
                if (raiz / rel).is_file():
                    if (raiz / rel).read_text(encoding="utf-8") != (
                        destino / rel
                    ).read_text(encoding="utf-8"):
                        difs.append(rel)
                else:
                    difs += _diferencas(raiz, destino, rel)
            for arq in ("CLAUDE.md", "AGENTS.md"):
                if arquivos[arq] != (raiz / arq).read_text(encoding="utf-8"):
                    difs.append(arq)
        if difs:
            print("projeções desatualizadas; rode gerar_projecoes.py:")
            for d in sorted(set(difs)):
                print("  -", d)
            return 1
        print("projeções sincronizadas com o catálogo")
        return 0
    arquivos = gerar(cat, raiz, raiz)
    print(
        f"{len(arquivos)} arquivos de texto gerados; skills copiadas para .claude/skills e .agent/skills"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
