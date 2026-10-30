from __future__ import annotations

from pathlib import Path


REQUIRED_DIRS = [
    ".agent/agents",
    ".agent/subagents",
    ".agent/skills",
    ".agent/workflows",
    ".agent/rules",
    "bases/sinapi",
    "bases/iopes",
    "bases/sicro",
    "bases/orcafascio-export",
    "templates/planilhas",
    "templates/especificacoes",
    "templates/memoriais",
    "templates/relatorios",
    "projetos",
    "scripts",
]

REQUIRED_FILES = [
    "README.md",
    "FLUXOGRAMA_OPERACAO.md",
    ".agent/ARCHITECTURE.md",
    ".agent/rules/GEMINI.md",
    ".agent/agents/central-orchestrator.md",
    ".agent/workflows/novo-orcamento.md",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = []

    for item in REQUIRED_DIRS:
        if not (root / item).is_dir():
            missing.append(item)

    for item in REQUIRED_FILES:
        if not (root / item).is_file():
            missing.append(item)

    if missing:
        print("Estrutura incompleta:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Estrutura Orca OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

