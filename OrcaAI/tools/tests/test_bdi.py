import pytest

from orca_tools.bdi_calculator import ParametrosBDI, calcular_bdi, obter_bdi_padrao_mgi


def test_bdi_padrao_servico_e_25_por_cento_pela_formula_do_tcu():
    r = obter_bdi_padrao_mgi("servico")
    assert r["bdi_percentual"] == 25.0
    assert r["total_tributos_percentual"] == 10.45
    assert r["regime_encargos"] == "Desonerado"


def test_decomposicao_oficial_dos_memoriais_reproduz_25():
    from orca_tools.bdi_calculator import PARAMETROS_SERVICO_MGI

    assert calcular_bdi(PARAMETROS_SERVICO_MGI)["bdi_percentual"] == 25.0


def test_bdi_padrao_fornecimento_e_14_02_por_cento_taxa_fixa():
    r = obter_bdi_padrao_mgi("fornecimento")
    assert r["bdi_percentual"] == 14.02
    assert r["decomposicao"] is None


def test_formula_tcu_com_parametros_nulos_da_zero():
    zero = ParametrosBDI(ac=0, s=0, r=0, g=0, df=0, lucro=0, pis=0, cofins=0, iss=0)
    assert calcular_bdi(zero)["bdi_percentual"] == 0.0


def test_tributos_de_100_por_cento_sao_rejeitados():
    with pytest.raises(ValueError):
        calcular_bdi(ParametrosBDI(pis=0.5, cofins=0.5, iss=0.0))


def test_tipo_invalido():
    with pytest.raises(ValueError):
        obter_bdi_padrao_mgi("obra")
