"""
Validador de Guardrails e Anti-Alucinação - OrcaAI
Executa os testes G-01 a G-10 antes da emissão de orçamentos e relatórios oficiais.
"""

import re
import unicodedata
from typing import List, Dict, Any


def _tokens(texto: str) -> set:
    """Palavras inteiras, sem acentos e em maiúsculas: 'Próprio' -> {'PROPRIO'}."""
    sem_acento = "".join(
        c
        for c in unicodedata.normalize("NFD", texto or "")
        if unicodedata.category(c) != "Mn"
    )
    return {t for t in re.split(r"[^A-Z0-9]+", sem_acento.upper()) if t}


def _fonte_oficial(fonte: str, oficiais: List[str]) -> bool:
    """Compara por palavra inteira: 'SINAPI-ES' e 'CPOS/CDHU' casam; 'DESCONHECIDA' não."""
    return any(f in _tokens(fonte) for f in oficiais)


def _fonte_propria(fonte: str) -> bool:
    return bool(_tokens(fonte) & {"PROPRIO", "PROPRIA", "PROPRIAS", "PROPRIOS", "CP"})


def auditar_orcamento(
    itens_orcamento: List[Dict[str, Any]],
    regime_encargos: str = "Desonerado",
    bdi_padrao_servico: float = 25.0,
    bdi_padrao_fornecimento: float = 14.02,
    series_historicas_toleradas: bool = False,
) -> Dict[str, Any]:
    """Audita G-01 e G-02.

    ``series_historicas_toleradas=True`` aplica a regra R-B6 da entrevista de
    maturidade (30/10/2026): nos itens já aprovados (2026-001 a 2026-012) as
    séries próprias históricas (SRAES-ELEV-, COMP-CAG-, SRA-ES-, ...) são
    conformidade documentada, não ressalva; nenhum item aprovado é reescrito.
    """
    relatorio = {
        "status_geral": "APROVADO",
        "bloqueios": [],
        "alertas": [],
        "conformidades": [],
    }

    # Bancos oficiais admitidos (cascata P0 a P3 do catálogo do ORCA-AI).
    fontes_oficiais = [
        "SINAPI",
        "IOPES",
        "DER",
        "SICRO",
        "ORSE",
        "SBC",
        "SUDECAP",
        "SETOP",
        "SICOR",
        "EMOP",
        "SCO",
        "SIURB",
        "CPOS",
        "CDHU",
        "FDE",
        "SEINFRA",
        "SEDOP",
        "AGESUL",
        "CAERN",
        "TPU",
    ]

    for idx, it in enumerate(itens_orcamento, start=1):
        cod = str(it.get("codigo", "")).strip()
        fonte = str(it.get("fonte", "")).strip().upper()
        bdi = float(it.get("bdi", 0.0))
        tipo = it.get("tipo", "servico").lower()

        # G-01: Validador de Código
        if not cod:
            relatorio["bloqueios"].append(
                f"Item {it.get('item', idx)}: Código referencial não informado."
            )
            relatorio["status_geral"] = "BLOQUEADO"
        elif (
            not _fonte_oficial(fonte, fontes_oficiais)
            and not cod.startswith("SRAES-CP-")
            and not cod.startswith("SRAES-INS-")
            and (
                cod.upper().startswith(("SRAES-", "SRA-ES-", "COMP-"))
                or _fonte_propria(fonte)
            )
        ):
            # Séries próprias históricas do acervo (SRAES-ELEV-, SRAES-FV-, ...):
            # têm a chancela SRAES-, mas o padrão novo é SRAES-CP/INS.
            if series_historicas_toleradas:
                relatorio["conformidades"].append(
                    f"G-01 (Série própria histórica tolerada, R-B6): Item {it.get('item', idx)} [{cod}] em item aprovado; não reescrever."
                )
            else:
                relatorio["alertas"].append(
                    f"G-01 (Série própria histórica): Item {it.get('item', idx)} ({cod}) usa série fora do padrão SRAES-CP/SRAES-INS; mapear na próxima revisão."
                )
        elif (
            not _fonte_oficial(fonte, fontes_oficiais)
            and not cod.startswith("SRAES-CP-")
            and not cod.startswith("SRAES-INS-")
        ):
            relatorio["bloqueios"].append(
                f"Item {it.get('item', idx)} ({cod}): Código não pertence a bases oficiais nem possui prefixo 'SRAES-CP-' / 'SRAES-INS-'."
            )
            relatorio["status_geral"] = "BLOQUEADO"
        else:
            relatorio["conformidades"].append(
                f"G-01 (Código Válido): Item {it.get('item', idx)} [{cod}]"
            )

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
            relatorio["conformidades"].append(
                f"G-02 (BDI Conforme): Item {it.get('item', idx)}"
            )

    if relatorio["bloqueios"]:
        relatorio["status_geral"] = "BLOQUEADO"
    elif relatorio["alertas"]:
        relatorio["status_geral"] = "RESSALVAS"

    return relatorio


if __name__ == "__main__":
    itens_teste = [
        {
            "item": "1.1",
            "codigo": "88316",
            "fonte": "SINAPI-ES",
            "bdi": 25.0,
            "tipo": "servico",
        },
        {
            "item": "1.2",
            "codigo": "SRAES-CP-001",
            "fonte": "PRÓPRIA",
            "bdi": 25.0,
            "tipo": "servico",
        },
        {
            "item": "1.3",
            "codigo": "XYZ_INVALIDO",
            "fonte": "DESCONHECIDA",
            "bdi": 30.0,
            "tipo": "servico",
        },
    ]
    res = auditar_orcamento(itens_teste)
    print(f"Status da Auditoria: {res['status_geral']}")
    print(f"Bloqueios: {res['bloqueios']}")
    print(f"Alertas: {res['alertas']}")
