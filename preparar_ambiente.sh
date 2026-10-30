#!/bin/sh
# Prepara um clone do ORCA-AI no macOS ou Linux: venv na raiz, dependências,
# hook de pre-commit, fileMode e, com --indices, os índices locais das bases.
# Uso: sh preparar_ambiente.sh [--indices]
set -e
cd "$(dirname "$0")"

py=""
for c in python3.12 python3; do
    if command -v "$c" >/dev/null 2>&1; then py="$c"; break; fi
done
[ -n "$py" ] || { echo "Python 3.12 não encontrado. Instale em https://www.python.org/downloads/ e repita."; exit 1; }

if [ ! -x .venv/bin/python ]; then
    echo "==> criando .venv com $py"
    "$py" -m venv .venv
fi
echo "==> instalando dependências"
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r OrcaAI/ufg/ml/requirements-dev.txt

echo "==> configurando o clone"
git config core.hooksPath .githooks
git config core.fileMode false      # OneDrive e Windows alteram permissões

if [ "$1" = "--indices" ]; then
    echo "==> reconstruindo índices locais das bases"
    .venv/bin/python OrcaAI/tools/cli/indexar_bases.py --todas 2026-04 || true
fi

echo "==> verificando"
.venv/bin/ruff check . && .venv/bin/ruff format --check . >/dev/null
.venv/bin/python OrcaAI/tools/cli/validar_estrutura.py | tail -1
.venv/bin/python OrcaAI/tools/cli/gerar_projecoes.py --verificar
(cd OrcaAI/tools && ../../.venv/bin/python -m pytest -q | tail -1)
echo "Ambiente pronto. Ferramentas externas opcionais: pandoc e Google Chrome (PDF), Playwright (Orçafascio)."
