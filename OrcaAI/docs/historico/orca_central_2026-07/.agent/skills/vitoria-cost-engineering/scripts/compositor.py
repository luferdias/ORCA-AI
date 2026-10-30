import argparse
import sys
from statistics import mean

def calcular_media_cotacoes(cotacoes):
    """Calcula a média aritmética de uma lista de cotações"""
    if len(cotacoes) < 3:
        print("AVISO: A regra de fallback exige NO MÍNIMO 3 cotações do mercado da Grande Vitória.")
    return mean(cotacoes)

def gerar_composicao_mock(servico, is_iopess=True):
    # This is a scaffold. Eventually, it could parse a real CSV 
    # of SINAPI or IOPES if the user drops the file in this folder.
    print(f"Buscando referências para '{servico}' no Espírito Santo...")
    print("---------------------------------------------------------")
    print(f"Fonte Prioritária simulada: {'IOPES/SINAPI-ES' if is_iopess else 'Média de Cotações Vitória'}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utilitário de Orçamento para a Grande Vitória")
    parser.add_argument("--cotacao", nargs="+", type=float, help="Passe valores para calcular a média (min. 3)")
    parser.add_argument("--servico", type=str, help="Serviço para testar a busca")

    args = parser.parse_args()

    if args.cotacao:
        media = calcular_media_cotacoes(args.cotacao)
        print(f"Cotações obtidas: {args.cotacao}")
        print(f"Preço adotado (Média Aritmética): R$ {media:.2f}")

    if args.servico:
        gerar_composicao_mock(args.servico)

    if len(sys.argv) == 1:
        parser.print_help()
