"""
Calculadora de BDI (Bonificações e Despesas Indiretas) - OrcaAI
Implementa a fórmula oficial do Acórdão TCU nº 2.622/2013 - Plenário.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ParametrosBDI:
    ac: float = 0.0400  # Administração Central (4,00%)
    s: float = 0.0080  # Seguros (0,80%)
    r: float = 0.0120  # Riscos (1,20%)
    g: float = 0.0080  # Garantias (0,80%)
    df: float = 0.0120  # Despesas Financeiras (1,20%)
    lucro: float = 0.0740  # Lucro Operacional (7,40%)
    pis: float = 0.0065  # PIS (0,65%)
    cofins: float = 0.0300  # COFINS (3,00%)
    iss: float = 0.0500  # ISS Vitória/ES (5,00%)
    cprb: float = 0.0000  # CPRB se desonerado (0,00% se não desonerado)


def calcular_bdi(params: ParametrosBDI) -> Dict[str, Any]:
    """
    Calcula a taxa de BDI conforme a fórmula do TCU:
    BDI = [ ( (1 + AC + S + R + G) * (1 + DF) * (1 + L) ) / (1 - I) ] - 1
    """
    taxa_tributos = params.pis + params.cofins + params.iss + params.cprb
    denominador = 1.0 - taxa_tributos

    if denominador <= 0:
        raise ValueError("A soma dos tributos não pode ser maior ou igual a 100%.")

    numerador = (
        (1.0 + params.ac + params.s + params.r + params.g)
        * (1.0 + params.df)
        * (1.0 + params.lucro)
    )
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


BDI_SERVICO_MGI = 25.00
BDI_FORNECIMENTO_MGI = 14.02

# Decomposição oficial do BDI de 25,00% usada nos treze memoriais de justificativa
# do acervo (itens 01 a 12), regime DESONERADO: AC 3,38%; R 0,85%; S+G 0,48%;
# DF 0,85%; L 6,00%; I = ISS 5,00% + COFINS 3,00% + PIS 0,65% + CPRB 1,80% = 10,45%.
# Fonte: Justificativa_Tecnica_BDI_25_*.pdf e Composicao de BDI *.pdf em
# OrcaAI/projetos/*/03-orcamento (3º quartil do Acórdão TCU 2.622/2013).
PARAMETROS_SERVICO_MGI = ParametrosBDI(
    ac=0.0338,
    s=0.0048,
    r=0.0085,
    g=0.0000,
    df=0.0085,
    lucro=0.0600,
    pis=0.0065,
    cofins=0.0300,
    iss=0.0500,
    cprb=0.0180,
)


def obter_bdi_padrao_mgi(tipo: str = "servico") -> Dict[str, Any]:
    """
    Retorna o BDI institucional do MGI/SRA-ES.
    - 'servico': 25,00%, com a decomposição oficial dos memoriais do acervo
      (regime desonerado, CPRB 1,80%); o valor é calculado pela fórmula do TCU
      e confere com o memorial.
    - 'fornecimento': 14,02%, BDI diferenciado reduzido para fornecimento puro
      de materiais e equipamentos (faixa média do Acórdão TCU 2.622/2013, de
      11,10% a 18,45%). O acervo não possui memorial próprio com a decomposição
      desse percentual; o valor é devolvido como taxa fixa, sem decomposição.
    """
    if tipo == "servico":
        res = calcular_bdi(PARAMETROS_SERVICO_MGI)
        assert res["bdi_percentual"] == BDI_SERVICO_MGI, res
        res["tipo"] = "Serviços de Engenharia e Manutenção (BDI 25%, desonerado)"
        res["regime_encargos"] = "Desonerado"
        res["fonte"] = (
            "Memoriais Justificativa_Tecnica_BDI_25 do acervo (Acórdão TCU 2.622/2013, 3º quartil)"
        )
        return res
    if tipo == "fornecimento":
        return {
            "bdi_decimal": round(BDI_FORNECIMENTO_MGI / 100.0, 6),
            "bdi_percentual": BDI_FORNECIMENTO_MGI,
            "tipo": "Fornecimento de Bens e Equipamentos (BDI Diferenciado Reduzido)",
            "fonte": "Acórdão TCU 2.622/2013, faixa média para fornecimento; sem memorial próprio no acervo",
            "decomposicao": None,
        }
    raise ValueError("Tipo inválido. Use 'servico' ou 'fornecimento'.")


if __name__ == "__main__":
    bdi_serv = obter_bdi_padrao_mgi("servico")
    bdi_forn = obter_bdi_padrao_mgi("fornecimento")
    print(f"BDI Serviço MGI: {bdi_serv['bdi_percentual']}%")
    print(f"BDI Fornecimento MGI: {bdi_forn['bdi_percentual']}%")
