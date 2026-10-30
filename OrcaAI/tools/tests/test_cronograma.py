import pytest

from orca_tools.cronograma_generator import gerar_cronograma_fisico_financeiro

ITENS = [
    {"item": "1.0", "descricao": "Preliminares", "valor_total": 10000.0},
    {"item": "2.0", "descricao": "Execução", "valor_total": 50000.0},
    {"item": "3.0", "descricao": "Limpeza final", "valor_total": 5000.0},
]


def test_distribuicao_linear_fecha_em_100():
    c = gerar_cronograma_fisico_financeiro(ITENS, num_meses=3)
    assert c["valor_global"] == 65000.0
    assert c["acumulado_perc"][-1] == pytest.approx(100.0)
    assert sum(c["totais_mensais_rs"]) == pytest.approx(65000.0)


def test_distribuicao_explicita():
    dist = {"1.0": [0.8, 0.2, 0.0], "2.0": [0.2, 0.5, 0.3], "3.0": [0.0, 0.3, 0.7]}
    c = gerar_cronograma_fisico_financeiro(ITENS, num_meses=3, distribuicoes=dist)
    assert c["totais_mensais_rs"] == [18000.0, 28500.0, 18500.0]
    assert c["linhas"][0]["distribuicao_percentual"] == [80.0, 20.0, 0.0]


def test_sem_itens_nao_divide_por_zero():
    c = gerar_cronograma_fisico_financeiro([], num_meses=2)
    assert c["valor_global"] == 0.0
    assert c["acumulado_perc"] == [0.0, 0.0]
