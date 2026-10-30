"""Renderização de documentos (subagente renderizador-documentos).

Markdown → HTML (pandoc, com folha de estilo institucional) → PDF (Chrome em
modo headless) e Markdown → DOCX (pandoc). Ferramentas externas são detectadas
em tempo de execução; a ausência de uma delas gera ``RuntimeError`` com a
instrução de instalação, nunca um PDF vazio.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

CHROMES = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/chromium-browser"),
)
CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #1a1a1a; line-height: 1.42; }
h1 { font-size: 16pt; color: #1b365d; border-bottom: 1px solid #1b365d; padding-bottom: 3pt; }
h2 { font-size: 12.5pt; color: #1b365d; margin-top: 16pt; }
h3 { font-size: 11pt; color: #2d4a7a; }
table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 8pt 0; }
thead { display: table-header-group; }
th { background: #e8edf4; color: #1b365d; border: 1px solid #c5ccd8; padding: 3pt 5pt; text-align: left; }
td { border: 1px solid #d5dae3; padding: 3pt 5pt; vertical-align: top; }
tr { break-inside: avoid; }
code { font-family: Menlo, monospace; font-size: 0.9em; background: #f1f3f6; padding: 0 2pt; }
pre { font-size: 8.2pt; background: #f6f7f9; border: 1px solid #dfe3ea; padding: 7pt 9pt; white-space: pre-wrap; }
"""


def _exigir(nome: str, caminho: str | None, dica: str) -> str:
    if not caminho:
        raise RuntimeError(f"{nome} não encontrado. {dica}")
    return caminho


def markdown_para_html(md: Path, html: Path, titulo: str | None = None) -> Path:
    pandoc = _exigir(
        "pandoc",
        shutil.which("pandoc"),
        "Instale com: brew install pandoc (macOS) ou winget install JohnMacFarlane.Pandoc (Windows)",
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".css", delete=False, encoding="utf-8"
    ) as css:
        css.write(CSS)
        css_path = css.name
    args = [
        pandoc,
        str(md),
        "-f",
        "markdown",
        "-t",
        "html5",
        "-s",
        "--metadata",
        "lang=pt-BR",
        "-c",
        css_path,
        "--embed-resources",
        "-o",
        str(html),
    ]
    if titulo:
        args += ["--metadata", f"title={titulo}"]
    subprocess.run(args, check=True)
    return html


def html_para_pdf(html: Path, pdf: Path) -> Path:
    chrome = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chrome")
        or next((str(c) for c in CHROMES if c.exists()), None)
    )
    chrome = _exigir(
        "Google Chrome",
        chrome,
        "Instale o Chrome (macOS, Windows ou Linux) ou use pandoc com wkhtmltopdf.",
    )
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf}",
            f"file://{html.resolve()}",
        ],
        check=True,
        capture_output=True,
    )
    if not pdf.exists() or pdf.stat().st_size < 1000:
        raise RuntimeError(f"PDF não gerado ou vazio: {pdf}")
    return pdf


def markdown_para_pdf(md: Path, pdf: Path, titulo: str | None = None) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        html = markdown_para_html(md, Path(tmp) / "doc.html", titulo)
        return html_para_pdf(html, pdf)


def markdown_para_docx(md: Path, docx: Path, modelo: Path | None = None) -> Path:
    pandoc = _exigir(
        "pandoc",
        shutil.which("pandoc"),
        "Instale com: brew install pandoc (macOS) ou winget install JohnMacFarlane.Pandoc (Windows)",
    )
    args = [pandoc, str(md), "-f", "markdown", "-t", "docx", "-o", str(docx)]
    if modelo:
        args += ["--reference-doc", str(modelo)]
    subprocess.run(args, check=True)
    return docx
