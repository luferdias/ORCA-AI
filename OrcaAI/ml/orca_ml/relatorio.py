"""Relatório didático auditável: apresentação não altera treino nem seleção de modelos."""
from __future__ import annotations

import base64
import hashlib
import html
import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

FONTES = {"sinapi_es": "SINAPI-ES", "der_es": "DER-ES / IOPES"}


def validar_periodos(resumos: dict) -> None:
    if not resumos:
        raise ValueError("Nenhuma execução disponível para o relatório")
    for campo in ("competencias_validacao", "competencias_teste"):
        janelas = {tuple(r[campo]) for r in resumos.values()}
        if len(janelas) != 1 or not next(iter(janelas)):
            raise ValueError("A comparação exige o mesmo período de validação e teste nas fontes")


def validar_csv(raw: pd.DataFrame, resumo: dict, fonte: str) -> None:
    if set(raw.fonte.unique()) != {fonte}:
        raise ValueError(f"A fonte do CSV não corresponde à pasta {fonte}")
    for fase, campo in (("validacao", "competencias_validacao"), ("teste", "competencias_teste")):
        reais = set(raw.loc[raw.fase == fase, "competencia_alvo"].unique())
        declaradas = set(resumo[campo])
        confere = reais == declaradas if fase == "teste" else bool(reais) and reais <= declaradas
        if not confere:
            raise ValueError(f"As competências do CSV em {fase} diferem do resumo de {fonte}")


def selecionar_exemplos(avaliacao: pd.DataFrame, historicos: dict) -> dict:
    """Priorize pintura de paredes e preço mediano anterior ao teste, nunca o erro."""
    escolhidos = {}
    for fonte, hist in historicos.items():
        candidatos = avaliacao[(avaliacao.fonte == fonte) & (avaliacao.nicho_id == "pintura")]
        if candidatos.empty:
            continue
        paredes = candidatos[candidatos.grupo.str.contains("Pintura Interna|Pintura Externa|SOBRE PAREDES E FORROS", regex=True)]
        if not paredes.empty:
            candidatos = paredes
        inicio = candidatos.competencia_alvo.min()
        passado = hist[hist.competencia < inicio].copy()
        keys = ["fonte", "grupo", "unidade", "codigo"]
        elegiveis = candidatos[keys].drop_duplicates()
        passado = passado.merge(elegiveis, on=keys, how="inner", validate="many_to_one")
        if passado.empty:
            continue
        # Um único recorte e unidade: maior número de códigos antes do teste.
        cobertura = passado.groupby(["grupo", "unidade"]).codigo.nunique().sort_values(ascending=False, kind="stable")
        grupo, unidade = cobertura.index[0]
        passado = passado[(passado.grupo == grupo) & (passado.unidade == unidade)]
        cobertura = passado.groupby("codigo").competencia.nunique()
        codigos = cobertura[cobertura == cobertura.max()].index
        ultimos = passado[passado.codigo.isin(codigos)].sort_values(["competencia", "codigo"]).groupby("codigo").tail(1).copy()
        ultimos["distancia_mediana"] = (ultimos.custo - ultimos.custo.median()).abs()
        escolhido = ultimos.sort_values(["distancia_mediana", "codigo"]).iloc[0]
        escolhidos[fonte] = {"codigo": str(escolhido.codigo), "grupo": grupo, "unidade": unidade,
                            "competencia_selecao": escolhido.competencia, "custo_selecao": float(escolhido.custo),
                            "criterio": "Pintura de paredes, quando disponível; recorte com mais códigos, maior cobertura histórica e preço anterior ao teste mais próximo da mediana; empate pelo código. Disponibilidade na avaliação exigida; erros de teste não são usados."}
    return escolhidos


def numero(valor, casas=2):
    if pd.isna(valor):
        return "não definido"
    return f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def periodo(meses):
    meses = sorted(meses)
    return " a ".join(m[5:] + "/" + m[:4] for m in (meses[0], meses[-1]))


GLOSSARIO = [
    ("O que está sendo previsto?", "O custo referencial de um serviço na competência seguinte. A regressão simples usa o último custo; a múltipla usa os três últimos custos. A persistência repete o último custo. O estudo não estima o custo total real de uma obra."),
    ("Erro percentual absoluto (APE)", "100 × |previsto - observado| / observado. Exemplo ilustrativo: observado R$ 100,00 e previsto R$ 103,00 resultam em erro absoluto R$ 3,00 e APE de 3%. Todos os alvos usados são positivos."),
    ("MAPE: média dos erros percentuais", "É a média dos APEs de cada serviço-mês. Menor é melhor. Cada observação tem o mesmo peso; serviços presentes em mais meses contribuem mais. Custos pequenos podem gerar percentuais altos. Não é economia nem acurácia de classificação."),
    ("Mediana, P90 e dispersão", "A mediana (MdAPE) descreve o erro típico: metade dos erros está abaixo dela. P90 resume a cauda: aproximadamente 90% dos erros ficam até esse valor. Média maior que mediana sugere influência de erros altos. São estatísticas descritivas, não intervalos de confiança."),
    ("Dentro de 5%", "Proporção das previsões cujo erro absoluto percentual foi no máximo 5%. O limite de 5% foi escolhido para leitura didática; não representa tolerância contratual ou critério oficial de orçamento."),
    ("MAE, RMSE e MSE", "MAE é a média do erro absoluto em R$/unidade. RMSE penaliza mais os erros altos e conserva R$/unidade. MSE é a média do erro ao quadrado, em (R$/unidade)². Esses valores são apresentados por grupo nativo e unidade, sem somar moedas de unidades diferentes."),
    ("R² e viés", "R² compara o erro quadrático com a dispersão dos valores observados; pode ser negativo e fica indefinido quando o observado é constante. R² alto não garante ganho sobre persistência. Viés percentual é a média de 100 × (previsto - observado) / observado: positivo indica superestimação média."),
    ("Como os modelos foram escolhidos?", "O MSE da validação escolhe regressão simples ou múltipla por grupo nativo e unidade. O modelo é reajustado antes do teste e avaliado mês a mês. A apresentação em MAPE não muda essa escolha nem elimina resultados desfavoráveis."),
    ("Como comparar SINAPI e IOPES?", "O período de teste é comum e as fontes permanecem separadas. Os nichos organizam assuntos semelhantes, mas não provam equivalência técnica entre composições. Diferenças de catálogo e de cobertura impedem concluir que uma fonte é mais barata ou superior apenas pelos erros."),
    ("Qual é o alcance da evidência?", "O teste contém poucas competências e várias observações compartilham o mesmo serviço e as mesmas variações mensais. Não foram calculados p-valores nem intervalos de confiança que tratem todas as linhas como independentes. O resultado é descritivo deste histórico."),
    ("Quais limites dos dados permanecem?", "As tabelas atuais incluem revisões históricas. SINAPI tem controle das datas conhecidas; DER tem publicação desconhecida e assinatura técnica parcial de descrição/unidade. Mudanças técnicas no alvo são mantidas; mudanças de unidade são registradas e excluídas da comparação monetária."),
]


def _tabela(frame: pd.DataFrame, colunas: dict) -> str:
    shown = frame[list(colunas)].rename(columns=colunas).copy()
    for col in shown:
        if pd.api.types.is_float_dtype(shown[col]):
            shown[col] = shown[col].map(numero)
    return shown.to_html(index=False, border=0, escape=True, classes="dados")


def _escrever_html(output, figuras, resumo, nichos, recortes, cobertura, exemplos, inventario, janela, config, textos_nichos, extremos):
    def img(nome, alt):
        data = base64.b64encode((output / "graficos" / f"{nome}.png").read_bytes()).decode()
        return f'<img loading="lazy" src="data:image/png;base64,{data}" alt="{html.escape(alt)}">'

    cards = []
    for row in resumo.to_dict("records"):
        cards.append(f'<article class="card"><div class="eyebrow">{FONTES[row["fonte"]]}</div><div class="big">{numero(row["dentro_5_pct"],1)}%</div><b>das previsões com erro de até 5%</b><p>Mediana: {numero(row["mdape"])}% · P90: {numero(row["p90"])}%</p><p>Média: {numero(row["mape"])}% · Média da persistência: {numero(row["mape_persistencia"])}%</p><p>{numero(row["n"],0)} previsões de {numero(row["n_servicos"],0)} serviços · {row["n_meses"]} meses</p><small>Limite de 5% usado para leitura didática.</small></article>')
    sections = []
    for item in sorted(config["nichos"], key=lambda x: x["ordem"]):
        nid = item["id"]
        covered = cobertura[cobertura.nicho_id == nid]
        if covered.empty:
            continue
        detail = recortes[recortes.nicho_id == nid].copy()
        detail["fonte"] = detail.fonte.map(FONTES)
        note = textos_nichos[nid]
        title = html.escape(item["nome"])
        if f"nicho_{nid}" in figuras:
            figure = img(f"nicho_{nid}", f"{item['nome']}: erro percentual por mês, modelos e tamanhos das amostras.")
        else:
            figure = '<p class="alert">Este nicho não possui recortes com amostra suficiente para avaliação.</p>'
        table = _tabela(detail, {"fonte":"Fonte", "grupo":"Grupo original", "unidade":"Unidade", "n":"Previsões", "n_servicos":"Serviços", "mape":"MAPE %", "mape_persistencia":"Persistência %", "mae":"MAE R$/un", "rmse":"RMSE R$/un", "r2":"R²"}) if not detail.empty else ""
        missing = covered[covered.status != "avaliado"]
        # A classificação é temática. Os nomes e unidades originais continuam visíveis.
        sections.append(f'<section id="{nid}" class="nicho" data-search="{html.escape(item["nome"].lower())}"><h2>{title}</h2><p>{html.escape(item["descricao"])}</p><p class="leitura">{html.escape(note)}</p>{figure}<details><summary>Ver todos os {len(detail)} recortes avaliados deste nicho e seus valores</summary><div class="table-scroll">{table}</div></details><details><summary>Ver os {len(missing)} recortes sem avaliação e os motivos</summary><div class="table-scroll">{_tabela(missing, {"fonte":"Fonte", "grupo":"Grupo original", "unidade":"Unidade", "status":"Situação", "motivo":"Motivo"})}</div></details></section>')
    deep = "".join(img(name, "Pintura: histórico observado, previsão, persistência e tabela com erros reais do serviço identificado.") for name in figuras if name.startswith("pintura_"))
    selection = "".join(f'<li>{FONTES[f]}: código <b>{html.escape(x["codigo"])}</b>, grupo {html.escape(x["grupo"])}. Preço usado na escolha: R$ {numero(x["custo_selecao"])} em {x["competencia_selecao"]}.</li>' for f, x in exemplos.items())
    glossary = "".join(f'<details><summary>{html.escape(title)}</summary><p>{html.escape(body)}</p></details>' for title, body in GLOSSARIO)
    links = "".join(f'<a href="#{x["id"]}">{html.escape(x["nome"])}</a>' for x in sorted(config["nichos"], key=lambda x: x["ordem"]) if x["id"] in set(cobertura.nicho_id))
    overview = "".join(img(name, "Todos os nichos: mediana do erro percentual da regressão e da persistência, com valores e tamanho de amostra.") for name in figuras if name.startswith("visao_"))
    trocas = extremos[(extremos.fonte == "der_es") & extremos.mudanca_tecnica_alvo & (extremos.descricao != extremos.descricao_alvo)]
    if not trocas.empty:
        t = trocas.iloc[0]
        diagnostico = f'Exemplo DER: o código {t.codigo}, em {t.competencia_alvo}, apresenta alteração de descrição. Antes: “{t.descricao}”. No alvo: “{t.descricao_alvo}”. A mudança de identidade precisa ser verificada; não interpretar automaticamente a diferença de custo como queda de preço do mesmo serviço.'
    else:
        diagnostico = "Custos observados de poucos centavos ampliam os percentuais. Mudanças técnicas, quando presentes, estão identificadas e precisam ser conferidas antes de interpretar uma variação de preço."
    total_catalogo = len(cobertura[["fonte", "grupo"]].drop_duplicates())
    total_periodo = len(cobertura.loc[cobertura.status != "fora_do_historico", ["fonte", "grupo"]].drop_duplicates())
    cobertura_texto = f"O catálogo organiza {total_catalogo} grupos originais: {total_periodo} têm registros no período comparado. Os demais aparecem nas tabelas de cobertura como fora do histórico."
    page = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ORCA-AI · Regressão explicada</title><style>
    :root{{--ink:#153047;--muted:#4d6373;--blue:#1765ad;--amber:#b36713;--line:#dbe3e9;--paper:#fff;--bg:#f3f6f8}}
    *{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}header{{background:#112d43;color:white;padding:60px max(5vw,24px) 44px}}header>div,main{{max-width:1250px;margin:auto}}h1{{font-size:clamp(32px,4vw,54px);line-height:1.15;max-width:1000px}}h2{{font-size:29px;line-height:1.25;margin:0 0 16px}}h3{{font-size:21px}}.eyebrow{{text-transform:uppercase;letter-spacing:2px;font-size:13px;font-weight:700}}header p{{color:#d4e2ed;max-width:930px}}main{{padding:30px 22px 60px}}section{{background:white;border:1px solid var(--line);border-radius:14px;padding:28px;margin:25px 0;scroll-margin-top:20px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px}}.card{{background:white;padding:26px;border-radius:12px;border:1px solid var(--line)}}.big{{font-size:48px;font-weight:750;color:var(--blue);line-height:1.4}}p{{margin:12px 0}}a{{color:#115794}}header a{{color:white}}.buttons a{{display:inline-block;padding:10px 18px;border:1px solid #a8c7df;border-radius:8px;text-decoration:none;margin:5px 10px 0 0}}img{{display:block;width:100%;height:auto;margin:20px 0;background:white}}.leitura{{border-left:4px solid var(--blue);background:#eef5fb;padding:16px 20px}}.alert{{background:#fff5e8;padding:18px;border-radius:8px}}.table-scroll{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:13px;line-height:1.45}}th,td{{padding:11px 10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}}th{{background:#eaf0f5;position:sticky;top:0}}tbody tr:nth-child(even){{background:#f7f9fb}}td:nth-child(2){{min-width:250px;max-width:430px}}details{{border:1px solid var(--line);border-radius:8px;padding:14px;margin:12px 0}}summary{{cursor:pointer;font-weight:650}}nav{{display:flex;flex-wrap:wrap;gap:9px}}nav a{{padding:7px 12px;border-radius:20px;background:#eaf1f6;text-decoration:none;font-size:14px}}label{{display:block;font-weight:650}}input{{padding:12px 16px;border:1px solid #aebeca;border-radius:8px;width:100%;font:inherit;margin:10px 0}}footer{{font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:20px}}small{{font-size:13px}}@media print{{header{{background:white;color:#153047;padding:20px}}header p,header a{{color:#153047}}.buttons,nav,#busca{{display:none}}section{{break-inside:avoid}}details{{break-inside:auto}}main{{padding:0}}}}
    </style></head><body><header><div><div class="eyebrow">ORCA-AI / UFG · Aprendizado de máquina</div><h1>Regressão de custos,<br>explicada por etapa da obra</h1><p>Engenheiro Luis Fernando · SINAPI-ES e DER-ES / IOPES<br>Teste comum: {html.escape(janela)} · Custos sem desoneração</p><div class="buttons"><a href="relatorio.pdf">Abrir relatório em PDF</a><a href="#nichos">Explorar grupos</a><a href="#estatistica">Entender a estatística</a></div></div></header><main>
    <div class="cards">{''.join(cards)}</div>
    <section><h2>Como ler este resultado</h2><p>O modelo tenta estimar o custo da competência seguinte. Comparamos a regressão com uma alternativa simples: repetir o último custo conhecido, chamada <b>persistência</b>. Em todos os gráficos de erro, <b>menor é melhor</b>.</p><p>O panorama abaixo reúne percentuais calculados serviço a serviço. Não compara preços médios de catálogos diferentes. Um nicho combina grupos por tema; a comparação técnica de serviços equivalentes é uma etapa própria.</p><p class="alert">Resultados positivos são mostrados junto aos casos em que a persistência é melhor. Um erro pequeno pode ser útil como aproximação e, ainda assim, não representar melhoria sobre essa referência.</p>{_tabela(inventario, {"fonte":"Fonte", "inicio":"Histórico usado", "fim":"Até", "registros":"Registros", "codigos":"Códigos", "recortes_avaliados":"Recortes avaliados", "recortes_insuficientes":"Sem amostra", "validacao_efetiva":"Validação efetiva"})}<p>A validação usa apenas meses com dados admissíveis. As retificações podem remover competências da avaliação quando o alvo já era conhecido na origem.</p></section>
    <section><h2>1. Panorama de todos os nichos</h2><p>Barras azuis: regressão selecionada na validação. Barras listradas: persistência. Os números ao lado das barras são as <b>medianas dos erros percentuais</b>: o erro típico. O tamanho de cada catálogo é informado em cada linha. Média e P90 aparecem nas análises detalhadas.</p>{overview}</section>
    <section><h2>2. Em quantas previsões o erro foi pequeno?</h2><p>As faixas incluem todas as previsões avaliadas, inclusive os erros altos. Elas mostram a distribuição dos erros, enquanto a média resume um único valor.</p>{img('distribuicao', 'Distribuição completa do erro percentual absoluto por fonte e método, com percentuais por faixa.')}</section>
    <section><h2>Por que média e mediana são diferentes?</h2>{img('extremos', 'Maiores erros percentuais por fonte, com código, mês, custo observado, previsto e flag de mudança técnica.')}<p class="alert">{html.escape(diagnostico)}</p><p>O arquivo <a href="diagnostico_extremos.csv">diagnóstico dos extremos</a> apresenta descrições anteriores e do alvo, custos e localizadores oficiais. Os registros permanecem na avaliação. A mediana e o P90 complementam a média; nenhum indicador isolado resume o catálogo.</p></section>
    <section id="exemplos_pintura"><h2>3. Pintura: do gráfico ao valor em reais</h2><p>O serviço ilustrativo de cada fonte foi escolhido por cobertura histórica e preço próximo da mediana <b>antes do teste</b>, priorizando paredes. A disponibilidade de resultados é necessária para desenhar o exemplo; o tamanho do erro não participou da escolha. São exemplos independentes, sem pareamento técnico entre códigos.</p><ul>{selection}</ul>{deep or '<p>Não há exemplo de pintura avaliável nesta execução.</p>'}</section>
    <section id="nichos"><h2>4. Explorar por etapa da obra</h2><p>{cobertura_texto} Abra as tabelas para ler cada grupo original, unidade e resultado. A busca aceita tanto o nome do nicho quanto o nome de um grupo original.</p><nav>{links}</nav><div id="busca"><label for="filtro">Buscar grupo ou etapa</label><input id="filtro" type="search" placeholder="Ex.: fundações, alvenaria, pintura, hidráulica" aria-describedby="contagem"><small id="contagem" aria-live="polite">Todos os nichos estão visíveis.</small></div></section>
    {''.join(sections)}
    <section id="estatistica"><h2>5. A estatística, em linguagem direta</h2>{glossary}<p>Não há faixas de confiança inferenciais neste estudo. P90 e variação mensal descrevem o histórico observado e não são garantias para próximos meses.</p></section>
    <section><h2>6. Dados para conferência e continuidade</h2><ul><li><a href="estatisticas_nichos.csv">Estatísticas por nicho e fonte</a></li><li><a href="estatisticas_recortes.csv">Todos os grupos originais e unidades: métricas completas</a></li><li><a href="cobertura_recortes.csv">Cobertura e motivos dos recortes sem avaliação</a></li><li><a href="previsoes_pareadas.csv">Observado, regressão e persistência nas mesmas linhas</a></li><li><a href="mapeamento_grupos.csv">Mapa auditável dos grupos originais para nichos</a></li><li><a href="manifesto_relatorio.json">Manifesto de fontes, arquivos e critérios de seleção</a></li></ul><p>Próximas melhorias técnicas: ampliar o histórico, verificar datas de publicação DER e validar pares de composições equivalentes. Os grupos em que a persistência vence são candidatos a investigação, sem trocar o modelo depois de olhar o teste.</p></section>
    <footer>Fontes de dados: <a href="https://www.caixa.gov.br/site/Paginas/downloads.aspx#categoria_888">SINAPI / CAIXA</a> e <a href="https://der.es.gov.br/referencial-de-precos-edificacoes">DER-ES Edificações</a>. Referência técnica: <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics">métricas de regressão do scikit-learn</a>. Relatório gerado a partir dos dados locais identificados no manifesto. Resultados de regressão; classificação e agrupamento seguem em etapas posteriores.</footer></main><script>
    const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();document.getElementById('filtro').addEventListener('input',e=>{{let count=0;document.querySelectorAll('.nicho').forEach(s=>{{const visible=norm(s.textContent).includes(norm(e.target.value));s.hidden=!visible;if(visible)count++}});document.getElementById('contagem').textContent=count+' nichos encontrados.'}});
    </script></body></html>'''
    (output / "relatorio.html").write_text(page, encoding="utf-8")


def gerar_relatorio(execucao_dir: Path, historicos: dict[str, pd.DataFrame], saida: Path | None = None) -> dict:
    """Gere HTML autônomo e PDF a partir de uma avaliação com janela comum."""
    from .estatisticas_relatorio import preparar_avaliacao, resumir_avaliacao, resumir_recortes
    from .grupos import carregar_mapa, adicionar_nichos
    from .graficos_relatorio import gerar_figuras

    source = Path(execucao_dir).resolve()
    output = Path(saida).resolve() if saida else source / "relatorio_didatico"
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"A pasta de relatório já contém arquivos: {output}")
    resumos, dados, hashes = {}, [], {}
    for fonte in FONTES:
        path = source / fonte / "previsoes_avaliacao.csv"
        if path.is_file():
            resumos[fonte] = json.loads((path.parent / "resumo.json").read_text())
            raw = pd.read_csv(path, dtype={"codigo": str}, keep_default_na=False)
            validar_csv(raw, resumos[fonte], fonte)
            resumos[fonte]["competencias_validacao_efetivas"] = sorted(raw.loc[raw.fase == "validacao", "competencia_alvo"].unique())
            dados.append(preparar_avaliacao(raw))
            hashes[str(path.relative_to(source))] = hashlib.sha256(path.read_bytes()).hexdigest()
    validar_periodos(resumos)
    if any(fonte not in historicos for fonte in resumos):
        raise ValueError("Os históricos de todas as fontes são necessários")
    config = carregar_mapa()
    avaliacao = adicionar_nichos(pd.concat(dados, ignore_index=True), config)
    common_end = next(iter(resumos.values()))["competencias_teste"][-1]
    historicos = {f: df[df.competencia <= common_end].copy() for f, df in historicos.items() if f in resumos}
    target = pd.concat([h[["fonte", "codigo", "competencia", "descricao", "custo", "localizador"]] for h in historicos.values()]).rename(columns={"competencia": "competencia_alvo", "descricao": "descricao_alvo", "custo": "custo_alvo_conferido", "localizador": "localizador_alvo"})
    avaliacao = avaliacao.merge(target, on=["fonte", "codigo", "competencia_alvo"], how="left", validate="many_to_one")
    if avaliacao.custo_alvo_conferido.isna().any() or not np.allclose(avaliacao.custo_observado, avaliacao.custo_alvo_conferido, rtol=0, atol=1e-8):
        raise ValueError("Os custos observados não correspondem aos históricos fornecidos")
    resumo = resumir_avaliacao(avaliacao, ["fonte"])
    nichos = resumir_avaliacao(avaliacao, ["fonte", "nicho_id", "nicho"])
    recortes = adicionar_nichos(resumir_recortes(avaliacao), config)
    rows = [{"fonte": f, **g} for f, s in resumos.items() for g in s["recortes"]]
    original_recortes = pd.concat([h[["fonte", "grupo", "unidade"]] for h in historicos.values()]).drop_duplicates()
    mapping = adicionar_nichos(pd.DataFrame([{"fonte": f, "grupo": g} for f in historicos for g in config["mapeamento"][f]]), config)
    existentes = set(zip(original_recortes.fonte, original_recortes.grupo))
    mapping["presente_no_historico"] = [(f,g) in existentes for f,g in zip(mapping.fonte,mapping.grupo)]
    ausentes = mapping.loc[~mapping.presente_no_historico, ["fonte", "grupo"]].assign(unidade="—")
    original_recortes = pd.concat([original_recortes, ausentes], ignore_index=True)
    cobertura = adicionar_nichos(original_recortes.merge(pd.DataFrame(rows), on=["fonte", "grupo", "unidade"], how="left", validate="one_to_one"), config)
    sem_janela = cobertura.status.isna()
    cobertura.loc[sem_janela, "status"] = "sem_janela_modelavel"
    if "motivo" not in cobertura:
        cobertura["motivo"] = ""
    cobertura["motivo"] = cobertura.motivo.fillna("")
    cobertura.loc[sem_janela, "motivo"] = "Sem sequência histórica elegível para construir as entradas e o alvo."
    fora = cobertura.unidade.eq("—")
    cobertura.loc[fora, "status"] = "fora_do_historico"
    cobertura.loc[fora, "motivo"] = "Grupo do catálogo geral sem registros no período desta execução."
    exemplos = selecionar_exemplos(avaliacao, historicos)
    inventario = pd.DataFrame([{"fonte": FONTES[f], "inicio": h.competencia.min(), "fim": h.competencia.max(),
        "registros": len(h), "codigos": h.codigo.nunique(), "recortes_avaliados": sum(g["status"] == "avaliado" for g in resumos[f]["recortes"]),
        "recortes_insuficientes": sum(g["status"] != "avaliado" for g in resumos[f]["recortes"]),
        "validacao_efetiva": ", ".join(resumos[f]["competencias_validacao_efetivas"])} for f, h in historicos.items()])
    janela = periodo(next(iter(resumos.values()))["competencias_teste"])
    textos = {}
    for nid in cobertura.nicho_id.unique():
        lines = []
        for row in nichos[nichos.nicho_id == nid].to_dict("records"):
            direction = "menor" if row["mape"] < row["mape_persistencia"] else "maior" if row["mape"] > row["mape_persistencia"] else "igual"
            lines.append(f'{FONTES[row["fonte"]]}: erro médio de {numero(row["mape"])}% na regressão e {numero(row["mape_persistencia"])}% na persistência; a regressão teve erro {direction}. Mediana {numero(row["mdape"])}% e P90 {numero(row["p90"])}%, em {numero(row["n"],0)} previsões de {numero(row["n_servicos"],0)} serviços.')
        textos[nid] = " ".join(lines) or "Sem recortes com amostra suficiente para avaliação."
    output.mkdir(parents=True, exist_ok=True)
    (output / "graficos").mkdir()
    for name, frame in {"estatisticas_fontes": resumo, "estatisticas_nichos": nichos, "estatisticas_recortes": recortes,
                        "cobertura_recortes": cobertura, "previsoes_pareadas": avaliacao}.items():
        frame.to_csv(output / f"{name}.csv", index=False, encoding="utf-8-sig")
    mapping.to_csv(output / "mapeamento_grupos.csv", index=False, encoding="utf-8-sig")
    extremos = pd.concat([avaliacao[avaliacao.fonte == f].nlargest(5, "ape") for f in resumos])
    extremos[["fonte", "codigo", "competencia_alvo", "descricao", "descricao_alvo", "unidade", "custo_t", "custo_observado", "custo_previsto", "ape", "mudanca_tecnica_alvo", "localizador", "localizador_alvo", "arquivo_sha256_alvo"]].to_csv(output / "diagnostico_extremos.csv", index=False, encoding="utf-8-sig")
    figuras = gerar_figuras(output, avaliacao, resumo, nichos, cobertura, exemplos, historicos, janela, config, GLOSSARIO, textos)
    _escrever_html(output, figuras, resumo, nichos, recortes, cobertura, exemplos, inventario, janela, config, textos, extremos)
    markdown = ["# Regressão de custos: relatório didático", "", "Engenheiro Luis Fernando · ORCA-AI / UFG", "", f"Teste comum: **{janela}**. Fontes sem desoneração.", "", "[Abrir relatório visual completo](relatorio.html) · [PDF para apresentação](relatorio.pdf)", "", "## Panorama", ""]
    for row in resumo.to_dict("records"):
        markdown.append(f'- **{FONTES[row["fonte"]]}:** MAPE {numero(row["mape"])}% na regressão e {numero(row["mape_persistencia"])}% na persistência; mediana {numero(row["mdape"])}%, P90 {numero(row["p90"])}%; {numero(row["n"],0)} previsões de {numero(row["n_servicos"],0)} serviços.')
    markdown += ["", "Os nichos aproximam assuntos, sem declarar equivalência técnica de serviços ou comparar preços entre catálogos. Cada observação serviço-mês pesa igualmente no MAPE. Os resultados desfavoráveis permanecem incluídos.", ""]
    for item in config["nichos"]:
        if item["id"] in textos:
            markdown += [f'## {item["nome"]}', "", textos[item["id"]], ""]
    markdown += ["## Validação efetiva", "", *[f"- {FONTES[f]}: {', '.join(r['competencias_validacao_efetivas'])}." for f,r in resumos.items()], "", "A validação usa somente meses cujos alvos ainda eram desconhecidos na origem, conforme as datas disponíveis. No teste, as duas fontes compartilham as competências indicadas.", "", "## Estatística e limites", ""]
    for title, body in GLOSSARIO:
        markdown += [f"### {title}", "", body, ""]
    markdown += ["## Fontes e reprodução", "", "As métricas foram recalculadas das mesmas linhas do teste; as previsões permanecem intactas. Consulte `manifesto_relatorio.json`, `previsoes_pareadas.csv` e `mapeamento_grupos.csv`.", "", "Referência: [métricas de regressão do scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)."]
    (output / "RELATORIO.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    manifesto = {"gerado_em_utc": datetime.now(timezone.utc).isoformat(), "execucao_origem": str(source),
        "janela_teste": next(iter(resumos.values()))["competencias_teste"], "sha256_previsoes": hashes,
        "validacao_efetiva": {f:s["competencias_validacao_efetivas"] for f,s in resumos.items()},
        "sha256_taxonomia": hashlib.sha256(json.dumps(config, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        "sha256_codigo_relatorio": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), Path(__file__).with_name("graficos_relatorio.py"), Path(__file__).with_name("estatisticas_relatorio.py"), Path(__file__).with_name("grupos.py")]},
        "exemplos": exemplos, "figuras": figuras, "n_previsoes_pareadas": len(avaliacao),
        "nichos": nichos.to_dict("records"), "limites": [body for _, body in GLOSSARIO[-3:]],
        "criterio_modelos": "Escolhidos pelo MSE de validação, sem seleção por resultados de teste ou de apresentação."}
    # Séries numéricas podem produzir NaN apenas em métricas indefinidas.
    manifesto = json.loads(json.dumps(manifesto, ensure_ascii=False, default=lambda x: x.item() if hasattr(x, "item") else str(x)))
    def limpar(value):
        if isinstance(value, float) and not np.isfinite(value):
            return None
        if isinstance(value, dict):
            return {k: limpar(v) for k, v in value.items()}
        if isinstance(value, list):
            return [limpar(v) for v in value]
        return value
    (output / "manifesto_relatorio.json").write_text(json.dumps(limpar(manifesto), ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return {"html": str(output / "relatorio.html"), "pdf": str(output / "relatorio.pdf"), "markdown": str(output / "RELATORIO.md")}
