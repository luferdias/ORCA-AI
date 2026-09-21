import os
from playwright.sync_api import sync_playwright

def carregar_env():
    """Carrega as variáveis do arquivo .env manualmente para não depender de pacotes externos."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.exists(env_path):
        print(f"Arquivo não encontrado: {env_path}")
        return
    
    with open(env_path, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                os.environ[chave.strip()] = valor.strip()

def automatizar_orcafascio():
    carregar_env()
    
    login = os.environ.get("ORCAFASCIO_LOGIN")
    senha = os.environ.get("ORCAFASCIO_PASSWORD")
    
    if not login or not senha:
        print("Erro: As credenciais ORCAFASCIO_LOGIN e ORCAFASCIO_PASSWORD não foram encontradas no .env.")
        return

    print("Iniciando a automação assistida do Orçafascio...")
    
    with sync_playwright() as p:
        # headless=False para você ver a tela
        # slow_mo ajuda a ver a digitação e os cliques acontecendo
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        
        print("Acessando a página de login...")
        page.goto("https://app.orcafascio.com/")
        
        # O Orçafascio costuma ter os campos com name ou id específicos.
        # Vamos tentar usar seletores flexíveis.
        print("Preenchendo credenciais...")
        try:
            page.fill("input[type='email'], input[name='login'], input[name='email']", login)
            page.fill("input[type='password'], input[name='password']", senha)
            
            # Clicando no botão de login
            page.click("button[type='submit'], input[type='submit'], text='Entrar', text='Login'")
            
            print("Login submetido. Aguardando o carregamento da página inicial...")
            page.wait_for_load_state("networkidle")
            
        except Exception as e:
            print(f"Houve um desvio no login automático: {e}")
            print("Você pode fazer o login manualmente agora na tela.")
            
        print("\n--- ATENÇÃO ---")
        print("O script foi pausado! A partir daqui, você já está logado.")
        print("Você pode usar a janela do navegador para me guiar e acessar as bases do Espírito Santo.")
        print("Quando quiser encerrar, basta fechar o navegador ou o Inspetor do Playwright.")
        print("-----------------\n")
        
        # Pausa a execução e abre o inspetor.
        # Você pode usar a interface do navegador livremente.
        page.pause()
        
        browser.close()

if __name__ == "__main__":
    automatizar_orcafascio()
