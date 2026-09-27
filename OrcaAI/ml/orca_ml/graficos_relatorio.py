"""Figuras com valores, amostras e legendas; saídas PNG, SVG e PDF vetorial."""
from __future__ import annotations

import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

from .relatorio import FONTES, numero
from .estatisticas_relatorio import resumir_avaliacao
from .grupos import unidade_legivel

AZUL = "#1765ad"
LARANJA = "#ae6414"
TEXTO = "#163047"
CINZA = "#526677"
FUNDO = "#f0f5f9"
NOMES_CURTOS = {"hidrossanitarias": "Hidráulica e sanitária", "eletricas": "Elétrica e comunicação",
                "urbanizacao_infraestrutura": "Urbanização e infraestrutura", "gas_incendio": "Gás e incêndio"}


def _base(titulo, subtitulo, size=(13.6, 9.3)):
    fig = plt.figure(figsize=size, facecolor="white")
    fig.text(.045, .963, "ORCA-AI  /  UFG", color=AZUL, fontsize=10, weight="bold", va="top")
    fig.text(.045, .92, titulo, color=TEXTO, fontsize=20 if len(titulo) > 62 else 23, weight="bold", va="top")
    fig.text(.045, .865, subtitulo, color=CINZA, fontsize=12, va="top")
    return fig


def _eixo(ax, ylabel=None):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#b3c2cd")
    ax.spines["bottom"].set_color("#b3c2cd")
    ax.grid(axis="y", alpha=.18, zorder=0)
    ax.set_axisbelow(True)
    if ylabel:
        ax.set_ylabel(ylabel, color=TEXTO, fontsize=11)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: numero(x, 1)))


def _tabela(fig, linhas, cabecalhos, box, fontsize=11.5, widths=None):
    ax = fig.add_axes(box)
    ax.axis("off")
    table = ax.table(cellText=linhas, colLabels=cabecalhos, loc="center", cellLoc="center", colWidths=widths, bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#d5e0e8")
        cell.set_linewidth(.6)
        cell.set_text_props(color=TEXTO)
        cell.set_facecolor("#e6eef5" if r == 0 else "white" if r % 2 else "#f6f9fb")
        if r == 0:
            cell.set_text_props(weight="bold")
    return table


def _paragrafo(fig, text, x, y, width=112, fontsize=12, color=TEXTO):
    wrapped = "\n".join(textwrap.wrap(text, width=width))
    fig.text(x, y, wrapped, fontsize=fontsize, color=color, va="top", linespacing=1.5)
    return y - (wrapped.count("\n") + 1) * (fontsize * 1.5 / (72 * fig.get_figheight()))


def gerar_figuras(output, avaliacao, resumo, nichos, cobertura, exemplos, historicos, janela, config, glossario, textos):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.labelsize": 11,
                         "axes.titlesize": 15, "legend.fontsize": 10, "pdf.fonttype": 42, "svg.fonttype": "none", "text.parse_math": False})
    nomes = []
    metadados = {x["id"]: x for x in config["nichos"]}
    fontes = [f for f in FONTES if f in set(avaliacao.fonte)]
    pdf_path = output / "relatorio.pdf"
    with PdfPages(pdf_path, metadata={"Title": "ORCA-AI | Regressão explicada por etapa da obra", "Author": "Engenheiro Luis Fernando | ORCA-AI", "Subject": f"SINAPI e DER-ES/IOPES - teste {janela}"}) as pdf:
        def salvar(fig, nome, nota="Dados oficiais coletados localmente · Custos sem desoneração · Estudo retrospectivo"):
            fig.text(.045, .04, nota, fontsize=9.2, color=CINZA, va="bottom")
            fig.text(.956, .02, f"{len(nomes)+1:02}", fontsize=9, color=CINZA, ha="right")
            pdf.savefig(fig)
            fig.savefig(output / "graficos" / f"{nome}.png", dpi=160, facecolor="white")
            fig.savefig(output / "graficos" / f"{nome}.svg", facecolor="white")
            nomes.append(nome)
            plt.close(fig)

        fig = _base("Quanto a regressão erra ao estimar o próximo mês?", f"Engenheiro Luis Fernando · SINAPI-ES e DER-ES / IOPES · Teste comum: {janela}")
        y = .79
        for row in resumo.to_dict("records"):
            fig.text(.055, y, FONTES[row["fonte"]], fontsize=17, color=TEXTO, weight="bold")
            fig.text(.055, y-.075, f'{numero(row["dentro_5_pct"],1)}%', fontsize=35, color=AZUL, weight="bold")
            fig.text(.26, y-.06, "das previsões tiveram erro até 5%", fontsize=17, color=TEXTO)
            fig.text(.26, y-.099, f'{numero(row["n"],0)} previsões · {numero(row["n_servicos"],0)} serviços · {row["n_meses"]} meses', fontsize=12, color=CINZA)
            fig.text(.055, y-.151, f'Erro típico (mediana): {numero(row["mdape"])}%  |  P90: {numero(row["p90"])}%  |  Média: {numero(row["mape"])}%', fontsize=13)
            fig.text(.055, y-.19, f'Persistência: mediana {numero(row["mdape_persistencia"])}% e média {numero(row["mape_persistencia"])}%', fontsize=12, color=LARANJA)
            y -= .27
        _paragrafo(fig, "Leitura: erro pequeno é uma medida de aproximação. O ganho do aprendizado só aparece quando ele também supera a persistência, que repete o último preço. O limite de 5% é didático; não representa tolerância oficial.", .055, .22, width=128)
        _paragrafo(fig, "A média é sensível a poucos custos próximos de zero. Por isso mostramos também mediana, P90, erros por mês e os casos extremos, mantendo todas as observações.", .055, .125, width=128, fontsize=11.5)
        salvar(fig, "resumo", f"Teste {janela} · Mesmas observações para regressão e persistência · Estatística descritiva")

        # Mediana em escala linear: poucos auxiliares com custo quase zero não achatam todo o catálogo.
        ordem = [x["id"] for x in sorted(config["nichos"], key=lambda x: x["ordem"])]
        max_med = max(nichos.mdape.max(), nichos.mdape_persistencia.max())
        for fonte in fontes:
            sub = nichos[nichos.fonte == fonte].set_index("nicho_id").reindex([n for n in ordem if n in set(nichos[nichos.fonte == fonte].nicho_id)])
            fig = _base(f"{FONTES[fonte]}: o erro típico em cada etapa", f"Mediana do erro percentual absoluto (MdAPE) · Teste {janela} · Menor é melhor", size=(13.6, 11.2))
            ax = fig.add_axes([.30, .12, .62, .68])
            yy = np.arange(len(sub))
            one = ax.barh(yy-.17, sub.mdape, height=.29, color=AZUL, label="Regressão selecionada")
            two = ax.barh(yy+.17, sub.mdape_persistencia, height=.29, color="#f3dec8", edgecolor=LARANJA, hatch="///", linewidth=.8, label="Último preço (persistência)")
            for bars in (one, two):
                ax.bar_label(bars, labels=[numero(b.get_width())+"%" for b in bars], padding=4, fontsize=10)
            labels = [NOMES_CURTOS.get(n, metadados[n]["nome"]) + f'\n{numero(row.n_servicos,0)} serviços · {numero(row.n,0)} previsões' for n, row in sub.iterrows()]
            ax.set_yticks(yy, labels, fontsize=10)
            ax.invert_yaxis()
            ax.set_xlim(0, max(.1, max_med)*1.27)
            ax.set_xlabel("Erro típico (%) — metade das previsões tem erro até esse valor", labelpad=12)
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: numero(x, 1)+"%"))
            ax.legend(loc="lower left", bbox_to_anchor=(0, 1.012), frameon=False, ncols=2)
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(axis="x", alpha=.18)
            ax.set_axisbelow(True)
            salvar(fig, f"visao_{fonte}", "Nichos temáticos; composições não pareadas entre fontes. Média, P90 e recortes completos acompanham o relatório.")

        fig = _base("A distribuição mostra o que a média esconde", f"Erro absoluto percentual por faixa · Todas as previsões do teste {janela}")
        ax = fig.add_axes([.25, .27, .69, .49])
        palette = ["#1765ad", "#69a5d3", "#b6d3e8", "#e6b66b", "#914f0b"]
        labels = ["Até 1%", ">1% a 3%", ">3% a 5%", ">5% a 10%", "Acima de 10%"]
        data_rows = []
        ticklabels = []
        for fonte in fontes:
            f = avaliacao[avaliacao.fonte == fonte]
            for method, col in [("Regressão", "ape"), ("Persistência", "ape_persistencia")]:
                vals = pd.cut(f[col], bins=[-np.inf, 1, 3, 5, 10, np.inf], labels=False).value_counts().reindex(range(5), fill_value=0).to_numpy()
                data_rows.append(vals / len(f) * 100)
                ticklabels.append(f"{FONTES[fonte]}\n{method} · n={numero(len(f),0)}")
        data_rows = np.array(data_rows)
        left = np.zeros(len(data_rows))
        for i, label in enumerate(labels):
            ax.barh(range(len(data_rows)), data_rows[:, i], left=left, color=palette[i], label=label, height=.56, edgecolor="white")
            for j, val in enumerate(data_rows[:, i]):
                if val >= 4:
                    ax.text(left[j]+val/2, j, numero(val,1)+"%", ha="center", va="center", fontsize=11, color="white" if i in (0,4) else TEXTO)
            left += data_rows[:, i]
        ax.set_yticks(range(len(data_rows)), ticklabels, fontsize=11)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Participação nas previsões avaliadas (%)")
        ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.04), ncols=3, frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
        _tabela(fig, [[ticklabels[i].replace("\n", " / ")] + [numero(x,1)+"%" for x in row] for i, row in enumerate(data_rows)], ["Fonte / método", *labels], [.055, .085, .89, .14], fontsize=10, widths=[.36,.128,.128,.128,.128,.128])
        salvar(fig, "distribuicao", "Faixas fechadas à direita. Percentuais podem diferir de 100% por arredondamento; extremos foram mantidos.")

        # Os maiores erros ficam visíveis e identificados, inclusive quando apontam mudança técnica.
        fig = _base("Por que a média pode ficar tão alta?", "Custos observados próximos de zero ampliam o erro percentual; os registros permanecem na análise")
        extreme = pd.concat([avaliacao[avaliacao.fonte == f].nlargest(3, "ape") for f in fontes])
        table_rows = [[FONTES[r.fonte], r.codigo, r.competencia_alvo, r.unidade, numero(r.custo_observado), numero(r.custo_previsto), numero(r.ape,1)+"%", "Sim" if r.mudanca_tecnica_alvo else "Não"] for r in extreme.itertuples()]
        _tabela(fig, table_rows, ["Fonte", "Código", "Mês", "Unidade", "Observado\nR$/un", "Previsto\nR$/un", "Erro\npercentual", "Mudança\ntécnica"], [.055, .46, .89, .30], fontsize=11, widths=[.15,.10,.11,.08,.12,.12,.12,.10])
        _paragrafo(fig, "Um custo observado de poucos centavos pode produzir erro percentual enorme mesmo sem um erro absoluto elevado. A média reflete essa cauda; a mediana descreve o centro. Nenhum desses indicadores substitui a inspeção da composição e da unidade.", .055, .39, width=125)
        _paragrafo(fig, "Mudança técnica identifica alteração observável no mês-alvo. Se um código passa a descrever outro serviço, isso é quebra de identidade; não significa queda de preço do mesmo serviço. Descrições anteriores e novas, custos e referências oficiais estão em diagnostico_extremos.csv.", .055, .255, width=125)
        _paragrafo(fig, "Esses casos indicam uma demanda concreta do ORCA-AI: revisão de valores muito baixos e de alterações de composição antes do uso em orçamento. Sua presença não foi usada para excluir previsões depois de observar o teste.", .055, .12, width=125, fontsize=11.5)
        salvar(fig, "extremos", "Exemplos selecionados pelos maiores erros apenas para diagnóstico; não são usados para escolher modelos.")

        for fonte, choice in exemplos.items():
            code, group, unit = choice["codigo"], choice["grupo"], choice["unidade"]
            unit_label = unidade_legivel(unit)
            sub = avaliacao[(avaliacao.fonte == fonte) & (avaliacao.codigo == code) & (avaliacao.grupo == group) & (avaliacao.unidade == unit)].sort_values("competencia_alvo")
            hist = historicos[fonte]
            hist = hist[(hist.codigo == code) & (hist.grupo == group) & (hist.unidade == unit)].sort_values("competencia").tail(9)
            description = str(sub.iloc[0].descricao)
            fig = _base(f"Pintura em valores reais: {FONTES[fonte]}", f"Código {code} · Unidade {unit_label} · Grupo {group}")
            _paragrafo(fig, description, .055, .81, width=128, fontsize=11)
            ax = fig.add_axes([.09, .35, .84, .31])
            months = sorted(set(hist.competencia) | set(sub.competencia_alvo))
            xpos = {m:i for i,m in enumerate(months)}
            ax.axvspan(xpos[sub.competencia_alvo.min()]-.4, len(months)-.7, color="#eaf2f8", label="Período de teste")
            ax.plot([xpos[x] for x in hist.competencia], hist.custo, "o-", color=TEXTO, lw=2, markersize=6, label="Custo oficial observado")
            ax.plot([xpos[x] for x in sub.competencia_alvo], sub.custo_previsto, "X--", color=AZUL, lw=2, markersize=8, label="Previsão da regressão")
            ax.plot([xpos[x] for x in sub.competencia_alvo], sub.previsto_persistencia, "s:", color=LARANJA, lw=2, markersize=6, label="Último preço (persistência)")
            ax.set_xticks(range(len(months)), [x[5:]+"/"+x[2:4] for x in months], fontsize=10)
            ax.set_xlabel("Competência de referência")
            _eixo(ax, f"Custo referencial (R$/{unit_label})")
            ax.margins(y=.24)
            ax.legend(loc="upper left", bbox_to_anchor=(0, 1.21), ncols=2, frameon=False, fontsize=9.5)
            rows = [[r.competencia_alvo, numero(r.custo_observado), numero(r.custo_previsto), numero(r.previsto_persistencia), numero(r.erro_abs), numero(r.ape)+"%"] for r in sub.itertuples()]
            _tabela(fig, rows, ["Competência", "Observado\nR$/un", "Regressão\nR$/un", "Persistência\nR$/un", "Erro absoluto\nregressão R$/un", "Erro %\nregressão"], [.055, .15, .89, .14], fontsize=11)
            first = sub.iloc[0]
            _paragrafo(fig, f'Exemplo aproximado: |{numero(first.custo_previsto,4)} - {numero(first.custo_observado,4)}| = {numero(first.erro_abs,4)} R$/{unit_label}; dividido por {numero(first.custo_observado)} e × 100 resulta em {numero(first.ape)}%.', .055, .11, width=132, fontsize=11)
            salvar(fig, f"pintura_{fonte}", "Escolha por cobertura e preço mediano antes do teste; não pelo erro. Códigos das fontes não são equivalentes confirmados.")

        for nid in ordem:
            stats = nichos[nichos.nicho_id == nid]
            if stats.empty:
                continue
            name = metadados[nid]["nome"]
            fig = _base(name + ": como o erro variou por mês", f"Média do erro percentual absoluto (MAPE) · Teste {janela} · Menor é melhor")
            monthly = resumir_avaliacao(avaliacao[avaliacao.nicho_id == nid], ["fonte", "competencia_alvo"])
            maxval = max(monthly.mape.max(), monthly.mape_persistencia.max(), .05)
            monthlyrows = []
            for i, fonte in enumerate(fontes):
                left = .07 + i * (.89/len(fontes))
                ax = fig.add_axes([left, .49, .79/len(fontes), .25])
                f = monthly[monthly.fonte == fonte].sort_values("competencia_alvo")
                ax.set_title(FONTES[fonte], color=TEXTO, weight="bold", fontsize=14)
                if f.empty:
                    ax.text(.5, .5, "Sem amostra suficiente", transform=ax.transAxes, ha="center")
                    ax.set_axis_off()
                    continue
                xs = np.arange(len(f))
                ax.plot(xs, f.mape, "o-", color=AZUL, label="Regressão", lw=2, markersize=7)
                ax.plot(xs, f.mape_persistencia, "s--", color=LARANJA, label="Persistência", lw=2, markersize=6)
                ax.set_ylim(0, maxval*1.30)
                ax.set_xticks(xs, [m[5:]+"/"+m[:4] for m in f.competencia_alvo])
                _eixo(ax, "Erro médio (%)")
                ax.legend(loc="upper left", bbox_to_anchor=(0, 1.28), ncols=2, frameon=False)
                for x, r in zip(xs, f.itertuples()):
                    offset = -17 if r.mape < r.mape_persistencia and r.mape > maxval*.12 else 9
                    ax.annotate(numero(r.mape)+"%", (x,r.mape), xytext=(0,offset), textcoords="offset points", ha="center", fontsize=10, color=AZUL,
                                bbox={"facecolor":"white", "edgecolor":"none", "alpha":.85, "pad":.5})
                    monthlyrows.append([FONTES[fonte], r.competencia_alvo, numero(r.n,0), numero(r.mape)+"%", numero(r.mape_persistencia)+"%"])
            _tabela(fig, monthlyrows, ["Fonte", "Mês", "Previsões", "Regressão MAPE", "Persistência MAPE"], [.055, .24, .89, .18], fontsize=10.5)
            lines = []
            for r in stats.itertuples():
                lines.append(f'{FONTES[r.fonte]}: {numero(r.n_servicos,0)} serviços; mediana {numero(r.mdape)}%; P90 {numero(r.p90)}%; {numero(r.dentro_5_pct,1)}% das previsões até 5%.')
            y = .19
            for line in lines:
                y = _paragrafo(fig, line, .055, y, width=140, fontsize=11.5) - .018
            if nid == "apoio_producao":
                fig.text(.055, .086, "Atenção: a média é dominada por extremos e mudanças de serviço. Consulte mediana/P90 e a página de diagnóstico.", fontsize=10.5, color=LARANJA, weight="bold")
            salvar(fig, f"nicho_{nid}", "Mesma escala nos painéis. Média recalculada das linhas do mês; tamanho da amostra pode variar. Grupos temáticos não pareados.")

        for offset in range(0, len(glossario), 4):
            chunk = glossario[offset:offset+4]
            fig = _base("Entender a estatística", "Definições, interpretação e limites do experimento")
            y = .79
            for title, body in chunk:
                fig.text(.055, y, title, color=AZUL, fontsize=15, weight="bold", va="top")
                y = _paragrafo(fig, body, .055, y-.039, width=129, fontsize=12) - .05
            salvar(fig, f"estatistica_{offset//4+1}", "Referência: scikit-learn.org/stable/modules/model_evaluation.html · Registros e critérios no manifesto do relatório")
    return nomes
