"""Cria um item de orçamento, ou uma etapa dentro de um item existente.

Uso, a partir de qualquer pasta:
    python OrcaAI/tools/cli/criar_projeto.py 2026-013-nome-do-servico
    python OrcaAI/tools/cli/criar_projeto.py 2026-013-nome-do-servico --etapa 03-orcamento

O item nasce com projeto.md, plano-execucao.md, log-decisoes.md e 00-entrada.
As demais etapas são criadas sob demanda com --etapa (regra R-E1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orca_tools.estrutura_projeto import (  # noqa: E402
    ETAPAS,
    criar_etapa,
    criar_item,
    raiz_orcaai,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cria um item de orçamento ou uma etapa de um item existente."
    )
    parser.add_argument("slug", help="Nome da pasta, ex.: 2026-013-limpeza-hvac")
    parser.add_argument(
        "--etapa",
        choices=ETAPAS,
        help="Cria esta etapa dentro do item (que deve existir) em vez de criar o item.",
    )
    args = parser.parse_args()
    projetos = raiz_orcaai() / "projetos"
    try:
        if args.etapa:
            item = projetos / args.slug
            if not item.is_dir():
                print(f"item não encontrado: {item}")
                return 1
            destino = criar_etapa(item, args.etapa, projetos / "_modelo")
            print(f"Etapa pronta: {destino}")
            return 0
        destino = criar_item(projetos, args.slug)
    except (ValueError, FileExistsError) as erro:
        print(erro)
        return 1
    print(f"Item criado: {destino}")
    print("Coloque os arquivos recebidos em 00-entrada e preencha projeto.md.")
    print("Crie as próximas etapas com --etapa quando a ordem de serviço as acionar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
