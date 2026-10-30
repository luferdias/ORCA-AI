"""Sessão assistida no Orçafascio Web com login manual.

Abre o navegador na página do Orçafascio e para, com o Inspector do
Playwright aberto, para que o engenheiro faça o login e conduza a sessão.
Nenhuma credencial é lida de arquivo, variável de ambiente ou prompt.

Uso:
    OrcaAI/ml/.venv/bin/python -m pip install playwright && playwright install chromium
    python OrcaAI/tools/cli/orcafascio_es_automation.py
"""

from playwright.sync_api import sync_playwright

URL = "https://app.orcafascio.com/"


def sessao_assistida() -> None:
    print("Abrindo o Orçafascio. Faça o login manualmente na janela do navegador.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.goto(URL)
        print("\n--- ATENÇÃO ---")
        print("O script está pausado. Faça o login na tela e navegue livremente.")
        print("Use o Inspector do Playwright para gravar ações quando quiser.")
        print("Quando terminar, feche o navegador ou o Inspector.")
        print("-----------------\n")
        page.pause()
        browser.close()


if __name__ == "__main__":
    sessao_assistida()
