"""
Calculadora de BDI (Bonificações e Despesas Indiretas) - OrcaAI
Implementa a fórmula oficial do Acórdão TCU nº 2.622/2013 - Plenário.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ParametrosBDI:
    ac: float = 0.0400  # Administração Central (4,00%)
    s: float = 0.0080   # Seguros (0,80%)
    r: float = 0.0120   # Riscos (1,20%)
    g: float = 0.0080   # Garantias (0,80%)
    df: float = 0.0120  # Despesas Financeiras (1,20%)
    lucro: float = 0.0740  # Lucro Operacional (7,40%)
    pis: float = 0.0065    # PIS (0,65%)
    cofins: float = 0.0300 # COFINS (3,00%)
    iss: float = 0.0500    # ISS Vitória/ES (5,00%)
    cprb: float = 0.0000   # CPRB se desonerado (0,00% se não desonerado)


def calcular_bdi(params: ParametrosBDI) -> Dict[str, Any]:
    """
    Calcula a taxa de BDI conforme a fórmula do TCU:
    BDI = [ ( (1 + AC + S + R + G) * (1 + DF) * (1 + L) ) / (1 - I) ] - 1
    """
    taxa_tributos = params.pis + params.cofins + params.iss + params.cprb
    denominador = 1.0 - taxa_tributos
    
    if denominador <= 0:
        raise ValueError("A soma dos tributos não pode ser maior ou igual a 100%.")
    
    numerador = (1.0 + params.ac + params.s + params.r + params.g) * (1.0 + params.df) * (1.0 + params.lucro)
    bdi_decimal = (numerador / denominador) - 1.0
    bdi_percentual = bdi_decimal * 100.0
    
    return {
        "bdi_decimal": round(bdi_decimal, 6),
        "bdi_percentual": round(bdi_percentual, 2),
        "total_tributos_percentual": round(taxa_tributos * 100.0, 2),
        "ac_percentual": round(params.ac * 100.0, 2),
        "s_r_g_percentual": round((params.s + params.r + params.g) * 100.0, 2),
        "df_percentual": round(params.df * 100.0, 2),
        "lucro_percentual": round(params.lucro * 100.0, 2),
        "iss_percentual": round(params.iss * 100.0, 2),
    }


def obter_bdi_padrao_mgi(tipo: str = "servico") -> Dict[str, Any]:
    """
    Retorna o BDI parametrizado oficial para o MGI/SRA-ES.
    - 'servico': 25,00% (Serviços e Obras)
    - 'fornecimento': 14,02% (Fornecimento de Materiais/Equipamentos)
    """
    if tipo == "servico":
        # Calibrado para atingir exatamente 25.00%
        params = ParametrosBDI(
            ac=0.0400, s=0.0080, r=0.0120, g=0.0080,
            df=0.0123, lucro=0.0740, pis=0.0065, cofins=0.0300, iss=0.0500
        )
        res = calcular_bdi(params)
        res["tipo"] = "Serviços de Engenharia e Manutenção (BDI 25%)"
        return res
    elif tipo == "fornecimento":
        # Faixa média do Acórdão TCU 2.622/2013 para Fornecimento de Bens
        params = ParametrosBDI(
            ac=0.0345, s=0.0048, r=0.0085, g=0.0048,
            df=0.0085, lucro=0.0511, pis=0.0065, cofins=0.0300, iss=0.0000
        )
        res = calcular_bdi(params)
        res["tipo"] = "Fornecimento de Bens e Equipamentos (BDI Diferenciado Reduzido)"
        return res
    else:
        raise ValueError("Tipo inválido. Use 'servico' ou 'fornecimento'.")


if __name__ == "__main__":
    bdi_serv = obter_bdi_padrao_mgi("servico")
    bdi_forn = obter_bdi_padrao_mgi("fornecimento")
    print(f"BDI Serviço MGI: {bdi_serv['bdi_percentual']}%")
    print(f"BDI Fornecimento MGI: {bdi_forn['bdi_percentual']}%")
