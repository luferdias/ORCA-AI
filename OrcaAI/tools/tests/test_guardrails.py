from orca_tools.code_guardrail_validator import auditar_orcamento


def item(codigo, fonte, bdi=25.0, tipo="servico", n="1.1"):
    return {"item": n, "codigo": codigo, "fonte": fonte, "bdi": bdi, "tipo": tipo}


def test_codigo_oficial_com_bdi_padrao_aprova():
    r = auditar_orcamento([item("88316", "SINAPI-ES")])
    assert r["status_geral"] == "APROVADO"
    assert not r["bloqueios"] and not r["alertas"]


def test_codigo_proprio_sraes_e_aceito():
    r = auditar_orcamento(
        [item("SRAES-CP-001", "PRÓPRIA"), item("SRAES-INS-007", "MERCADO", n="1.2")]
    )
    assert r["status_geral"] == "APROVADO"


def test_codigo_arbitrario_bloqueia():
    r = auditar_orcamento([item("XYZ", "DESCONHECIDA")])
    assert r["status_geral"] == "BLOQUEADO"
    assert "SRAES-CP-" in r["bloqueios"][0]


def test_codigo_vazio_bloqueia():
    assert auditar_orcamento([item("", "SINAPI")])["status_geral"] == "BLOQUEADO"


def test_bdi_divergente_gera_ressalva():
    r = auditar_orcamento([item("88316", "SINAPI-ES", bdi=30.0)])
    assert r["status_geral"] == "RESSALVAS"
    r2 = auditar_orcamento([item("1234", "SINAPI", bdi=14.02, tipo="fornecimento")])
    assert r2["status_geral"] == "APROVADO"


def test_serie_propria_historica_gera_ressalva_e_nao_bloqueio():
    r = auditar_orcamento([item("SRAES-ELEV-001", "Próprio")])
    assert r["status_geral"] == "RESSALVAS"
    assert "SRAES-CP" in r["alertas"][0]


def test_composicao_propria_com_serie_comp_gera_ressalva():
    r = auditar_orcamento([item("COMP-HVAC-001", "Próprio")])
    assert r["status_geral"] == "RESSALVAS"


def test_fonte_desconhecida_nao_casa_por_substring():
    assert (
        auditar_orcamento([item("4939", "DESCONHECIDA")])["status_geral"] == "BLOQUEADO"
    )
    assert (
        auditar_orcamento([item("4939", "ORSE - 02/2026 - Sergipe")])["status_geral"]
        == "APROVADO"
    )


def test_serie_historica_tolerada_em_item_aprovado():
    r = auditar_orcamento(
        [item("SRAES-ELEV-001", "Próprio")], series_historicas_toleradas=True
    )
    assert r["status_geral"] == "APROVADO" and not r["alertas"]
    assert "R-B6" in r["conformidades"][0]
    r2 = auditar_orcamento(
        [item("XYZ", "DESCONHECIDA")], series_historicas_toleradas=True
    )
    assert r2["status_geral"] == "BLOQUEADO"
