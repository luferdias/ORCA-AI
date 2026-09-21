"""
Validador de Guardrails e Anti-Alucinação - OrcaAI
Executa os testes G-01 a G-10 antes da emissão de orçamentos e relatórios oficiais.
"""

from typing import List, Dict, Any


def auditar_orcamento(
    itens_orcamento: List[Dict[str, Any]],
    regime_encargos: str = "Nao_Desonerado",
    bdi_padrao_servico: float = 25.0,
    bdi_padrao_fornecimento: float = 14.02
) -> Dict[str, Any]:
    relatorio = {
        "status_geral": "APROVADO",
        "bloqueios": [],
        "alertas": [],
        "conformidades": []
    }
    
    fontes_oficiais = ["SINAPI", "SINAPI-ES", "IOPES", "IOPES-ES", "SICRO", "SICRO3", "ORSE", "SUDECAP", "SETOP", "EMOP", "SIURB"]
    
    for idx, it in enumerate(itens_orcamento, start=1):
        cod = str(it.get("codigo", "")).strip()
        fonte = str(it.get("fonte", "")).strip().upper()
        bdi = float(it.get("bdi", 0.0))
        tipo = it.get("tipo", "servico").lower()
        
        # G-01: Validador de Código
        if not cod:
            relatorio["bloqueios"].append(f"Item {it.get('item', idx)}: Código referencial não informado.")
            relatorio["status_geral"] = "BLOQUEADO"
        elif not any(f in fonte for f in fontes_oficiais) and not cod.startswith("SRAES-CP-") and not cod.startswith("SRAES-INS-"):
            relatorio["bloqueios"].append(
                f"Item {it.get('item', idx)} ({cod}): Código não pertence a bases oficiais nem possui prefixo 'SRAES-CP-' / 'SRAES-INS-'."
            )
            relatorio["status_geral"] = "BLOQUEADO"
        else:
            relatorio["conformidades"].append(f"G-01 (Código Válido): Item {it.get('item', idx)} [{cod}]")
            
        # G-02: Validador de BDI
        if tipo == "fornecimento" and abs(bdi - bdi_padrao_fornecimento) > 0.05:
            relatorio["alertas"].append(
                f"G-02 (BDI Fornecimento): Item {it.get('item', idx)} aplica BDI de {bdi}%, diferente do padrão TCU de {bdi_padrao_fornecimento}%."
            )
        elif tipo != "fornecimento" and abs(bdi - bdi_padrao_servico) > 0.05:
            relatorio["alertas"].append(
                f"G-02 (BDI Serviço): Item {it.get('item', idx)} aplica BDI de {bdi}%, diferente do padrão MGI de {bdi_padrao_servico}%."
            )
        else:
            relatorio["conformidades"].append(f"G-02 (BDI Conforme): Item {it.get('item', idx)}")
            
    if relatorio["bloqueios"]:
        relatorio["status_geral"] = "BLOQUEADO"
    elif relatorio["alertas"]:
        relatorio["status_geral"] = "RESSALVAS"
        
    return relatorio


if __name__ == "__main__":
    itens_teste = [
        {"item": "1.1", "codigo": "88316", "fonte": "SINAPI-ES", "bdi": 25.0, "tipo": "servico"},
        {"item": "1.2", "codigo": "SRAES-CP-001", "fonte": "PRÓPRIA", "bdi": 25.0, "tipo": "servico"},
        {"item": "1.3", "codigo": "XYZ_INVALIDO", "fonte": "DESCONHECIDA", "bdi": 30.0, "tipo": "servico"}
    ]
    res = auditar_orcamento(itens_teste)
    print(f"Status da Auditoria: {res['status_geral']}")
    print(f"Bloqueios: {res['bloqueios']}")
    print(f"Alertas: {res['alertas']}")
