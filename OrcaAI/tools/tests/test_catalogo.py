import subprocess
import sys
from pathlib import Path

from orca_tools.catalogo import carregar, validar

RAIZ = Path(__file__).resolve().parents[3]


def test_catalogo_valido():
    cat = carregar(RAIZ / "OrcaAI" / "agents" / "catalogo.yaml")
    assert validar(cat, RAIZ) == []
    assert len(cat["agentes"]) == 12
    assert {a["plataforma"] for a in cat["agentes"]} == {
        "claude_code",
        "codex",
        "antigravity",
    }


def test_projecoes_sincronizadas():
    r = subprocess.run(
        [
            sys.executable,
            str(RAIZ / "OrcaAI" / "tools" / "cli" / "gerar_projecoes.py"),
            "--verificar",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
