# Prepara um clone do ORCA-AI no Windows (PowerShell): venv na raiz,
# dependências, hook de pre-commit e, com -Indices, os índices locais das bases.
# Uso, na raiz do clone:  powershell -ExecutionPolicy Bypass -File .\preparar_ambiente.ps1 [-Indices]
param([switch]$Indices)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = $null
foreach ($c in @("py -3.12", "python3.12", "python")) {
    try { & cmd /c "$c --version" 2>$null | Out-Null; if ($LASTEXITCODE -eq 0) { $py = $c; break } } catch {}
}
if (-not $py) { Write-Error "Python 3.12 não encontrado. Instale em https://www.python.org/downloads/ e marque 'Add to PATH'."; exit 1 }

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "==> criando .venv com $py"
    & cmd /c "$py -m venv .venv"
}
Write-Host "==> instalando dependências"
& .venv\Scripts\python.exe -m pip install -q --upgrade pip
& .venv\Scripts\python.exe -m pip install -q -r OrcaAI\ufg\ml\requirements-dev.txt

Write-Host "==> configurando o clone"
git config core.hooksPath .githooks     # o Git for Windows executa o hook com o seu próprio sh
git config core.fileMode false
git config core.autocrlf false          # .gitattributes já decide o fim de linha por tipo de arquivo

if ($Indices) {
    Write-Host "==> reconstruindo índices locais das bases"
    & .venv\Scripts\python.exe OrcaAI\tools\cli\indexar_bases.py --todas 2026-04
}

Write-Host "==> verificando"
& .venv\Scripts\ruff.exe check .
& .venv\Scripts\python.exe OrcaAI\tools\cli\validar_estrutura.py | Select-Object -Last 1
& .venv\Scripts\python.exe OrcaAI\tools\cli\gerar_projecoes.py --verificar
Push-Location OrcaAI\tools; & ..\..\.venv\Scripts\python.exe -m pytest -q | Select-Object -Last 1; Pop-Location
Write-Host "Ambiente pronto. Opcionais: pandoc (winget install JohnMacFarlane.Pandoc) e Google Chrome para PDF; Playwright para o Orçafascio."
