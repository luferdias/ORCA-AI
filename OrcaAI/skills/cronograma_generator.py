"""
Gerador de Cronograma Físico-Financeiro - OrcaAI
Estrutura a distribuição temporal de desembolsos financeiros e avanço físico das obras.
"""

from typing import List, Dict, Any


def gerar_cronograma_fisico_financeiro(
    itens_macro: List[Dict[str, Any]], 
    num_meses: int = 3,
    distribuicoes: Dict[str, List[float]] = None
) -> Dict[str, Any]:
    """
    Gera o cronograma físico-financeiro com base nos macro-itens e percentuais por mês.
    
    itens_macro: Lista de dicionários no formato:
      [
        {"item": "1.0", "descricao": "Serviços Preliminares", "valor_total": 5000.0},
        {"item": "2.0", "descricao": "Execução Estrutural", "valor_total": 45000.0}
      ]
    distribuicoes: Mapeamento de item -> lista de percentuais decimais por mês somando 1.0 (100%).
      Ex: {"1.0": [0.60, 0.40, 0.0], "2.0": [0.20, 0.50, 0.30]}
    """
    valor_global = sum(it["valor_total"] for it in itens_macro)
    linhas_cronograma = []
    totais_por_mes_rs = [0.0] * num_meses
    
    for it in itens_macro:
        chave_item = it["item"]
        v_total = it["valor_total"]
        
        # Se não houver distribuição explícita, distribui linearmente
        if distribuicoes and chave_item in distribuicoes:
            perc_meses = distribuicoes[chave_item]
        else:
            perc_meses = [1.0 / num_meses] * num_meses
            
        desembolsos_rs = [v_total * p for p in perc_meses]
        for i, val in enumerate(desembolsos_rs):
            totais_por_mes_rs[i] += val
            
        linhas_cronograma.append({
            "item": it["item"],
            "descricao": it["descricao"],
            "valor_total": v_total,
            "peso_percentual_global": round((v_total / valor_global) * 100.0, 2) if valor_global > 0 else 0.0,
            "distribuicao_percentual": [round(p * 100.0, 2) for p in perc_meses],
            "desembolso_rs": [round(d, 2) for d in desembolsos_rs]
        })
        
    totais_por_mes_perc = [(tot / valor_global) * 100.0 if valor_global > 0 else 0.0 for tot in totais_por_mes_rs]
    
    # Cálculo do acumulado
    acumulado_rs = []
    acumulado_perc = []
    soma_rs = 0.0
    for t_rs in totais_por_mes_rs:
        soma_rs += t_rs
        acumulado_rs.append(round(soma_rs, 2))
        acumulado_perc.append(round((soma_rs / valor_global) * 100.0, 2) if valor_global > 0 else 0.0)
        
    return {
        "valor_global": round(valor_global, 2),
        "num_meses": num_meses,
        "linhas": linhas_cronograma,
        "totais_mensais_rs": [round(t, 2) for t in totais_por_mes_rs],
        "totais_mensais_perc": [round(p, 2) for p in totais_por_mes_perc],
        "acumulado_rs": acumulado_rs,
        "acumulado_perc": acumulado_perc
    }


if __name__ == "__main__":
    itens_exemplo = [
        {"item": "1.0", "descricao": "Serviços Preliminares", "valor_total": 10000.0},
        {"item": "2.0", "descricao": "Tratamento e Vedação", "valor_total": 50000.0},
        {"item": "3.0", "descricao": "Limpeza Final e Desmobilização", "valor_total": 5000.0}
    ]
    dist = {
        "1.0": [0.80, 0.20, 0.00],
        "2.0": [0.20, 0.50, 0.30],
        "3.0": [0.00, 0.30, 0.70]
    }
    cron = gerar_cronograma_fisico_financeiro(itens_exemplo, num_meses=3, distribuicoes=dist)
    print(f"Total da Obra: R$ {cron['valor_global']}")
    print(f"Desembolso por mês (R$): {cron['totais_mensais_rs']}")
    print(f"Avanço Acumulado (%): {cron['acumulado_perc']}")
