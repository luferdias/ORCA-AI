"""Comparação do orçamento nos dois regimes de encargos (regra R-B10, A8).

O padrão é o regime desonerado (R-B1), mas a escolha precisa ser fundamentada
em cada processo: o A8 calcula o orçamento nos dois regimes, cada um com o seu
BDI, e registra qual resultou no menor preço global.

- Desonerado: custo SINAPI da aba CCD e BDI de 25,00% (memoriais do acervo,
  com CPRB 1,80%).
- Não desonerado: custo SINAPI da aba CSD e BDI de 22,54%, a mesma decomposição
  sem a CPRB. É uma estimativa derivada: o acervo não tem memorial próprio para
  esse BDI.
- DER-ES/IOPES: a tabela do DER-ES só é publicada sem desoneração (leis sociais
  de 157,27% para horista e 73,85% para mensalista, maio/2026). O mesmo custo
  entra nos dois cenários, com o BDI de cada um, e o item é sinalizado (R-B11).
- Composição própria e outras bases: o custo depende dos encargos dos insumos
  de mão de obra e não é recalculado aqui. Esses itens ficam fora dos totais
  comparados (só trocar o BDI favoreceria artificialmente o não desonerado), e
  o relatório informa a cobertura: a parcela do orçamento que foi comparada.
  Abaixo de 80% de cobertura, o resultado é inconclusivo até as composições
  próprias serem recalculadas no outro regime.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from orca_tools.bdi_calculator import PARAMETROS_SERVICO_MGI, calcular_bdi
from orca_tools.indice_bases import Indice

BDI_DESONERADO = calcular_bdi(PARAMETROS_SERVICO_MGI)["bdi_percentual"]
BDI_NAO_DESONERADO = calcular_bdi(replace(PARAMETROS_SERVICO_MGI, cprb=0.0))[
    "bdi_percentual"
]
SISTEMAS_DER = {"IOPES", "DER", "DER-ES", "DER_ES"}
COBERTURA_MINIMA = 0.80


@dataclass
class ResultadoRegimes:
    total_desonerado: float = 0.0
    total_nao_desonerado: float = 0.0
    total_orcamento: float = 0.0
    valor_fora: float = 0.0
    itens_sinapi: int = 0
    itens_der: list[str] = field(default_factory=list)
    itens_sem_comparacao: list[str] = field(default_factory=list)
    sinapi_sem_par: list[str] = field(default_factory=list)

    @property
    def cobertura(self) -> float:
        if not self.total_orcamento:
            return 0.0
        return 1 - self.valor_fora / self.total_orcamento

    @property
    def conclusivo(self) -> bool:
        return self.cobertura >= COBERTURA_MINIMA

    @property
    def vencedor(self) -> str:
        if not self.conclusivo:
            return "inconclusivo"
        if round(self.total_desonerado, 2) <= round(self.total_nao_desonerado, 2):
            return "desonerado"
        return "nao_desonerado"

    @property
    def diferenca(self) -> float:
        return round(self.total_nao_desonerado - self.total_desonerado, 2)


def comparar(itens: list[dict], indice_sinapi: Indice | None) -> ResultadoRegimes:
    """Compara os regimes para as linhas de serviço de uma planilha normalizada.

    Cada item precisa de ``item``, ``codigo``, ``sistema``, ``quantidade`` e
    ``custo_unitario_sem_bdi`` (colunas de ``planilha-normalizada.csv``).
    """
    res = ResultadoRegimes()
    fd, fn = 1 + BDI_DESONERADO / 100, 1 + BDI_NAO_DESONERADO / 100
    for it in itens:
        if it.get("tipo_item", "servico") == "grupo" or not it.get("quantidade"):
            continue
        q = float(it["quantidade"])
        custo = float(it.get("custo_unitario_sem_bdi") or 0)
        sistema = (it.get("sistema") or "").upper()
        rotulo = f"{it.get('item', '?')} {sistema} {it.get('codigo', '')}".strip()
        custo_d = custo_n = custo
        preco_padrao = round(custo * fd, 2) * q
        res.total_orcamento += preco_padrao
        if sistema == "SINAPI" and indice_sinapi is not None:
            custos = indice_sinapi.custos_por_regime(it.get("codigo", ""))
            if {"com_desoneracao", "sem_desoneracao"} <= custos.keys():
                custo_d = custos["com_desoneracao"]
                custo_n = custos["sem_desoneracao"]
                res.itens_sinapi += 1
            else:
                res.sinapi_sem_par.append(rotulo)
                res.valor_fora += preco_padrao
                continue
        elif sistema in SISTEMAS_DER:
            res.itens_der.append(rotulo)
        else:
            res.itens_sem_comparacao.append(rotulo)
            res.valor_fora += preco_padrao
            continue
        res.total_desonerado += round(custo_d * fd, 2) * q
        res.total_nao_desonerado += round(custo_n * fn, 2) * q
    res.total_orcamento = round(res.total_orcamento, 2)
    res.valor_fora = round(res.valor_fora, 2)
    res.total_desonerado = round(res.total_desonerado, 2)
    res.total_nao_desonerado = round(res.total_nao_desonerado, 2)
    return res


def _brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _conclusao(res: ResultadoRegimes) -> str:
    if res.vencedor == "inconclusivo":
        return (
            f"**Inconclusivo:** a parcela comparada ({res.cobertura:.1%}) é menor que "
            f"{COBERTURA_MINIMA:.0%}. Para decidir, recalcular as composições próprias "
            "com os insumos de mão de obra no regime não desonerado. Até lá, vale o "
            "padrão desonerado (R-B1)."
        )
    venc = "desonerado" if res.vencedor == "desonerado" else "não desonerado"
    return (
        f"**Menor preço nos itens comparados: regime {venc}** "
        f"(diferença de {_brl(abs(res.diferenca))})."
    )


def relatorio_markdown(res: ResultadoRegimes, titulo: str, competencia: str) -> str:
    """Texto para ``05-validacoes/comparacao-regimes.md`` e para o log."""
    linhas = [
        f"# Comparação de regimes — {titulo}",
        "",
        f"Competência SINAPI: {competencia}. Regra R-B10 (A8).",
        "",
        f"Parcela comparada: {res.cobertura:.1%} do orçamento "
        f"({_brl(res.total_orcamento - res.valor_fora)} de {_brl(res.total_orcamento)}"
        ", pelo preço desonerado).",
        "",
        "| Cenário (itens comparados) | BDI | Total com BDI |",
        "| --- | ---: | ---: |",
        f"| Desonerado (padrão, R-B1) | {BDI_DESONERADO:.2f}% | {_brl(res.total_desonerado)} |",
        f"| Não desonerado | {BDI_NAO_DESONERADO:.2f}% (estimativa sem memorial) | {_brl(res.total_nao_desonerado)} |",
        "",
        _conclusao(res),
        "",
        f"- Itens SINAPI comparados nos dois regimes: {res.itens_sinapi}.",
    ]
    if res.itens_der:
        linhas.append(
            "- Itens DER-ES/IOPES (tabela publicada só sem desoneração; mesmo custo "
            f"nos dois cenários, R-B11): {', '.join(res.itens_der)}."
        )
    if res.itens_sem_comparacao:
        linhas.append(
            "- Fora da comparação (composições próprias e outras bases; os encargos "
            "dos insumos de mão de obra não foram recalculados): "
            f"{', '.join(res.itens_sem_comparacao)}."
        )
    if res.sinapi_sem_par:
        linhas.append(
            "- Códigos SINAPI sem os dois regimes no índice: "
            f"{', '.join(res.sinapi_sem_par)}."
        )
    linhas += [
        "",
        "Se o não desonerado vencer, a escolha do regime volta ao engenheiro "
        "antes de fechar a planilha, e a decisão vai para `log-decisoes.md`.",
    ]
    return "\n".join(linhas) + "\n"
