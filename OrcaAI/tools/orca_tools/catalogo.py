"""Catálogo único de agentes do ORCA-AI e geração das três projeções.

Fonte: ``OrcaAI/agents/catalogo.yaml``. Projeções:

- Claude Code: ``.claude/agents/*.md``, ``.claude/skills/<skill>/`` e um bloco
  delimitado em ``CLAUDE.md``.
- Codex: bloco delimitado em ``AGENTS.md`` e ``agents/openai.yaml`` dentro de
  cada skill marcada ``codex: true``.
- Antigravity: ``.agent/rules/GEMINI.md``, ``.agent/agents/``,
  ``.agent/subagents/``, ``.agent/skills/``, ``.agent/workflows/`` e
  ``.agent/ARCHITECTURE.md``.
- Fichas legíveis em ``OrcaAI/agents/fichas/``.

As pastas de projeção são apagadas e reescritas a cada geração; a pasta
``OrcaAI/agents/fichas/historico/`` é preservada.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import yaml

MARCA_INICIO = "<!-- orca:catalogo:inicio -->"
MARCA_FIM = "<!-- orca:catalogo:fim -->"
AVISO = "Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão."

PASTAS_PROJECAO = (
    ".claude/agents",
    ".claude/skills",
    ".agent/agents",
    ".agent/subagents",
    ".agent/skills",
    ".agent/workflows",
    "OrcaAI/agents/fichas",
)
PRESERVAR = {"OrcaAI/agents/fichas": {"historico"}}


# ----------------------------------------------------------------- leitura
def carregar(caminho: Path) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validar(cat: dict, raiz: Path) -> list[str]:
    erros: list[str] = []
    ids = [a["id"] for a in cat["agentes"]]
    if len(ids) != len(set(ids)):
        erros.append("ids de agentes repetidos")
    slugs = [a["slug"] for a in cat["agentes"]] + [s["slug"] for s in cat["subagentes"]]
    if len(slugs) != len(set(slugs)):
        erros.append("slugs repetidos entre agentes e subagentes")
    skills = {s["nome"]: s for s in cat["skills"]}
    canonico = raiz / "OrcaAI" / "agents" / "skills"
    for nome, s in skills.items():
        if s["situacao"] == "ativa" and not (canonico / nome / "SKILL.md").is_file():
            erros.append(f"skill ativa sem SKILL.md canônico: {nome}")
        for dona in s["dona"]:
            if dona not in ids:
                erros.append(f"skill {nome} aponta para agente inexistente {dona}")
    for a in cat["agentes"]:
        for sk in a.get("skills", []):
            if sk not in skills:
                erros.append(f"{a['id']} usa skill fora do catálogo: {sk}")
            elif skills[sk]["situacao"] != "ativa":
                erros.append(f"{a['id']} usa skill não ativa: {sk}")
        if a["plataforma"] not in cat["plataformas"]:
            erros.append(f"{a['id']} com plataforma desconhecida {a['plataforma']}")
    for s in cat["subagentes"]:
        for sk in s.get("skills", []):
            if sk not in skills:
                erros.append(f"subagente {s['slug']} usa skill fora do catálogo: {sk}")
    for w in cat["workflows"]:
        for alvo in w.get("aciona", []):
            if alvo not in ids and alvo not in slugs:
                erros.append(f"workflow /{w['comando']} aciona desconhecido {alvo}")
    return erros


# ----------------------------------------------------------------- utilitários
def _lista(itens, prefixo="- ") -> str:
    return "\n".join(f"{prefixo}{i}" for i in itens)


def _bloco(texto: str, conteudo: str) -> str:
    """Substitui ou acrescenta o bloco delimitado em um arquivo mantido à mão."""
    novo = f"{MARCA_INICIO}\n{conteudo.rstrip()}\n{MARCA_FIM}"
    if MARCA_INICIO in texto and MARCA_FIM in texto:
        padrao = re.compile(
            re.escape(MARCA_INICIO) + r".*?" + re.escape(MARCA_FIM), re.S
        )
        return padrao.sub(lambda _m: novo, texto)
    return texto.rstrip("\n") + "\n\n" + novo + "\n"


def _descricao_skill(caminho_skill: Path) -> str:
    """Primeira linha útil do campo description do SKILL.md."""
    texto = caminho_skill.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^description:\s*>?\s*(.*?)(?=^\S[^:]*:|^---)", texto, re.S | re.M)
    if not m:
        return ""
    return " ".join(m.group(1).split())[:240]


def _agente(cat: dict, ref: str) -> dict | None:
    for a in cat["agentes"]:
        if a["id"] == ref or a["slug"] == ref:
            return a
    return None


def _subagente(cat: dict, ref: str) -> dict | None:
    for s in cat["subagentes"]:
        if s["slug"] == ref:
            return s
    return None


def _nome_ref(cat: dict, ref: str) -> str:
    a = _agente(cat, ref)
    if a:
        return f"{a['id']} {a['nome']}"
    s = _subagente(cat, ref)
    return f"subagente `{s['slug']}`" if s else ref


# ----------------------------------------------------------------- blocos comuns
def _regras_comuns(cat: dict) -> str:
    p = cat["parametros_fixos"]
    g = "\n".join(
        f"| {x['id']} | {x['nome']} | {x['regra']} | {x['acao']} |"
        for x in cat["guardrails"]
    )
    return f"""## Regra de ouro

{cat["regra_de_ouro"]}

## Parâmetros fixos do MGI/SRA-ES

- BDI de serviços: {p["bdi_servico"]}
- BDI de fornecimento: {p["bdi_fornecimento"]}
- Regime de encargos: {p["regime_encargos"]}
- Códigos próprios: {p["codigos_proprios"]}
- Data-base: {p["data_base"]}
- Cascata de bases oficiais:
{_lista(p["cascata_bases"], "  - ")}
- Pesquisa de mercado: {p["cascata_mercado"]}

## Guardrails

| ID | Validador | Regra | Ação |
| --- | --- | --- | --- |
{g}

## Pausas obrigatórias (pedir o "De acordo" do engenheiro)

{_lista(cat["pausas_humanas"])}

Toda aprovação ou pendência: {cat["protocolo"]["decisoes"]}.

## Protocolo entre agentes

- Ordem de serviço: {cat["protocolo"]["ordem_de_servico"]}.
- Estados de um item: {" → ".join(cat["protocolo"]["estados_do_item"])}; registro em `{cat["protocolo"]["registro_de_estados"]}`.
- Estrutura de um item: `{"`, `".join(p["estrutura_item"]["etapas"])}` mais `{"`, `".join(p["estrutura_item"]["controle"])}`; nome {p["estrutura_item"]["nome"]}.
- Criação das etapas: {p["estrutura_item"]["criacao"]}.

## Orçafascio

URL `{cat["identidade"]["orcafascio"]["url"]}`, login institucional `{cat["identidade"]["orcafascio"]["login_institucional"]}`. Autenticação: {cat["identidade"]["orcafascio"]["autenticacao"]}.
"""


def _ficha_agente(cat: dict, a: dict, caminho_skills: str) -> str:
    plat = cat["plataformas"][a["plataforma"]]["nome"]
    skills = "\n".join(
        f"- [{s}]({caminho_skills}/{s}/SKILL.md)" for s in a.get("skills", [])
    )
    externas = ""
    if a.get("skills_externas"):
        externas = (
            "\n\nSkills externas a instalar: " + ", ".join(a["skills_externas"]) + "."
        )
    return f"""# {a["id"]} · {a["nome"]}

**Plataforma:** {plat} · **Camada:** {a["camada"]} · **Absorve:** {", ".join(a["absorve"])}

## Missão

{a["missao"]}

## Atribuições

{_lista(a["atribuicoes"])}

## Entradas

{_lista(a["entradas"])}

## Saídas

{_lista(a["saidas"])}

## Skills

{skills}{externas}
"""


# ----------------------------------------------------------------- projeções
def gerar(cat: dict, raiz_origem: Path, raiz_destino: Path) -> dict[str, str]:
    """Produz todos os arquivos de projeção em ``raiz_destino``.

    Retorna o mapa caminho relativo → conteúdo dos arquivos de texto gerados.
    As cópias de skills são feitas diretamente em disco.
    """
    arquivos: dict[str, str] = {}
    canonico = raiz_origem / "OrcaAI" / "agents" / "skills"
    skills_cat = {s["nome"]: s for s in cat["skills"]}
    agentes_por_plat = {
        k: [a for a in cat["agentes"] if a["plataforma"] == k]
        for k in cat["plataformas"]
    }
    sub_por_plat = {
        k: [s for s in cat["subagentes"] if s["plataforma"] == k]
        for k in cat["plataformas"]
    }

    # --- fichas legíveis ------------------------------------------------
    linhas = [
        "# Fichas dos agentes ORCA-AI 2.0",
        "",
        AVISO,
        "",
        "| Id | Agente | Plataforma | Camada | Missão |",
        "| --- | --- | --- | --- | --- |",
    ]
    for a in cat["agentes"]:
        linhas.append(
            f"| {a['id']} | [{a['nome']}]({a['id']}-{a['slug']}.md) | {cat['plataformas'][a['plataforma']]['nome']} | {a['camada']} | {a['missao']} |"
        )
        arquivos[f"OrcaAI/agents/fichas/{a['id']}-{a['slug']}.md"] = (
            AVISO + "\n\n" + _ficha_agente(cat, a, "../skills")
        )
    linhas += [
        "",
        "## Subagentes",
        "",
        "| Subagente | Plataforma | Função | Origem |",
        "| --- | --- | --- | --- |",
    ]
    for s in cat["subagentes"]:
        linhas.append(
            f"| `{s['slug']}` | {cat['plataformas'][s['plataforma']]['nome']} | {s['funcao']} | {s['origem']} |"
        )
    linhas += [
        "",
        "## Subagentes de ML",
        "",
        "| Id | Nome | Reporta a | Skill externa | Função |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in cat["subagentes_ml"]:
        linhas.append(
            f"| {s['id']} | {s['nome']} | {s['reporta_a']} | {s['skill_externa']} | {s['funcao']} |"
        )
    linhas += [
        "",
        "## Equivalência com os catálogos anteriores",
        "",
        "| 2.0 | Absorve |",
        "| --- | --- |",
    ]
    for a in cat["agentes"]:
        linhas.append(f"| {a['id']} {a['nome']} | {', '.join(a['absorve'])} |")
    linhas += [
        "",
        "## Skills",
        "",
        "| Skill | Situação | Donos | Codex |",
        "| --- | --- | --- | --- |",
    ]
    for s in cat["skills"]:
        linhas.append(
            f"| {s['nome']} | {s['situacao']} | {', '.join(s['dona'])} | {'sim' if s.get('codex') else 'não'} |"
        )
    linhas += [
        "",
        "## Workflows",
        "",
        "| Comando | Plataforma | Aciona | Descrição |",
        "| --- | --- | --- | --- |",
    ]
    for w in cat["workflows"]:
        linhas.append(
            f"| `/{w['comando']}` | {w['plataforma']} | {', '.join(w['aciona']) or '—'} | {w['descricao']} |"
        )
    arquivos["OrcaAI/agents/fichas/README.md"] = "\n".join(linhas) + "\n"

    # --- Claude Code ----------------------------------------------------
    regras = _regras_comuns(cat)
    for a in agentes_por_plat["claude_code"]:
        corpo = _ficha_agente(cat, a, "../skills") + "\n" + regras
        arquivos[f".claude/agents/{a['slug']}.md"] = (
            f"---\nname: {a['slug']}\ndescription: {a['id']} {a['nome']} do ORCA-AI. {a['missao']} Use para: {a['camada']}.\n"
            f"tools: {', '.join(a['tools'])}\nmodel: inherit\n---\n\n<!-- {AVISO} -->\n\n"
            + corpo
        )
    for s in sub_por_plat["claude_code"]:
        arquivos[f".claude/agents/{s['slug']}.md"] = (
            f"---\nname: {s['slug']}\ndescription: Subagente ORCA-AI sem autonomia. {s['funcao']}\ntools: Read, Grep, Glob, Bash, Write, Edit\nmodel: inherit\n---\n\n"
            f"<!-- {AVISO} -->\n\n# Subagente `{s['slug']}`\n\n{s['funcao']}\n\nSkills: "
            + ", ".join(f"[{k}](../skills/{k}/SKILL.md)" for k in s["skills"])
            + f"\n\n{cat['regra_de_ouro']}\n"
        )
    skills_claude = sorted(
        {k for a in agentes_por_plat["claude_code"] for k in a.get("skills", [])}
        | {k for s in sub_por_plat["claude_code"] for k in s["skills"]}
    )
    tabela = "\n".join(
        f"| {a['id']} | {a['nome']} | {cat['plataformas'][a['plataforma']]['nome']} | {a['missao']} |"
        for a in cat["agentes"]
    )
    bloco_claude = f"""## Catálogo de agentes 2.0 ({cat["versao"]}, {cat["atualizado_em"]})

{AVISO}

| Id | Agente | Plataforma | Missão |
| --- | --- | --- | --- |
{tabela}

- Agentes do Claude Code em `.claude/agents/` (A1, A2, A3, A4, A5, A12 e subagentes `{"`, `".join(s["slug"] for s in sub_por_plat["claude_code"])}`); skills em `.claude/skills/`.
- Codex lê `AGENTS.md`; Antigravity lê `.agent/`. Fichas completas em `OrcaAI/agents/fichas/`. Fonte: `OrcaAI/agents/catalogo.yaml`.
- Regra de ouro: {cat["regra_de_ouro"]}
- Orçafascio: {cat["identidade"]["orcafascio"]["autenticacao"]}.
- Comandos: {", ".join("`/" + w["comando"] + "`" for w in cat["workflows"])}."""
    arquivos["CLAUDE.md"] = _bloco(
        (raiz_origem / "CLAUDE.md").read_text(encoding="utf-8"), bloco_claude
    )

    # --- Codex ----------------------------------------------------------
    partes = [
        f"## Agentes do Codex no ORCA-AI 2.0 ({cat['versao']}, {cat['atualizado_em']})",
        "",
        AVISO,
        "",
        f"Você atua como um dos agentes de produção do ORCA-AI para o {cat['identidade']['orgao']}. Responsável técnico: {cat['identidade']['responsavel']}. Tratamento: {cat['identidade']['tratamento']}.",
        "",
        f"**Responsável por:** {cat['plataformas']['codex']['responsavel_por']}.",
        "",
        f"**Não deve fazer:** {cat['plataformas']['codex']['nao_deve']}. Toda saída é auditada pelo A4 (Claude Code) antes de entrar no dossiê.",
        "",
    ]
    for a in agentes_por_plat["codex"]:
        partes += [
            f"### {a['id']} · {a['nome']}",
            "",
            f"**Missão:** {a['missao']}",
            "",
            "Atribuições:",
            "",
            _lista(a["atribuicoes"]),
            "",
            "Skills (ler o SKILL.md indicado antes de produzir): "
            + ", ".join(
                f"`OrcaAI/agents/skills/{k}/SKILL.md`" for k in a.get("skills", [])
            ),
            "",
            "Entradas: "
            + "; ".join(a["entradas"])
            + ". Saídas: "
            + "; ".join(a["saidas"])
            + ".",
            "",
        ]
    partes += [
        "### Subagentes do Codex",
        "",
        _lista(
            f"`{s['slug']}`: {s['funcao']} Skills: "
            + ", ".join(f"`OrcaAI/agents/skills/{k}/SKILL.md`" for k in s["skills"])
            for s in sub_por_plat["codex"]
        ),
        "",
    ]
    partes += [
        "### Ferramentas e testes",
        "",
        "- Pacote Python `OrcaAI/tools/orca_tools` (BDI, cronograma, planilha Excel, guardrails, estrutura de item); testes com `cd OrcaAI/tools && ../ml/.venv/bin/python -m pytest -q`.",
        "- Lint: `ruff check .` e `ruff format .` na raiz; o hook de pre-commit bloqueia segredos e erros de lint.",
        "- Nunca gravar credenciais em arquivo, variável ou prompt.",
        "",
        regras,
    ]
    arquivos["AGENTS.md"] = _bloco(
        (raiz_origem / "AGENTS.md").read_text(encoding="utf-8"), "\n".join(partes)
    )

    # --- Antigravity ----------------------------------------------------
    for a in agentes_por_plat["antigravity"]:
        arquivos[f".agent/agents/{a['slug']}.md"] = (
            f"---\nname: {a['slug']}\ndescription: {a['id']} {a['nome']} do ORCA-AI. {a['missao']}\n"
            f"tools: {', '.join(a['tools'])}\nmodel: inherit\nskills: {', '.join(a.get('skills', []))}\n---\n\n<!-- {AVISO} -->\n\n"
            + _ficha_agente(cat, a, "../skills")
            + "\n"
            + regras
        )
    for s in sub_por_plat["antigravity"]:
        arquivos[f".agent/subagents/{s['slug']}.md"] = (
            f"---\nname: {s['slug']}\ndescription: Subagente ORCA-AI sem autonomia. {s['funcao']}\ntools: browser_subagent, read_file, write_file\nmodel: inherit\nskills: {', '.join(s['skills'])}\n---\n\n"
            f"<!-- {AVISO} -->\n\n# Subagente `{s['slug']}`\n\n{s['funcao']}\n\n{cat['regra_de_ouro']}\n\nOrçafascio: {cat['identidade']['orcafascio']['autenticacao']}.\n"
        )
    skills_ag = sorted(
        {k for a in agentes_por_plat["antigravity"] for k in a.get("skills", [])}
        | {k for s in sub_por_plat["antigravity"] for k in s["skills"]}
    )
    for w in cat["workflows"]:
        arg = f" {w['argumento']}" if w.get("argumento") else ""
        regras_w = (
            ("\n## Regras\n\n" + _lista(w["regras"]) + "\n") if w.get("regras") else ""
        )
        arquivos[f".agent/workflows/{w['comando']}.md"] = (
            f"---\ndescription: {w['descricao']}\n---\n\n<!-- {AVISO} -->\n\n# /{w['comando']}{arg}\n\n$ARGUMENTS\n\n"
            f"**Plataforma:** {w['plataforma']} · **Aciona:** {', '.join(_nome_ref(cat, r) for r in w['aciona']) or '—'}\n\n## Objetivo\n\n{w['descricao']}\n\n## Fluxo\n\n"
            + "\n".join(f"{i}. {p}" for i, p in enumerate(w["fluxo"], 1))
            + "\n\n## Saída\n\n"
            + _lista(w["saida"])
            + "\n"
            + regras_w
        )
    classif = "\n".join(
        f"| `/{w['comando']}` | {w['descricao']} |" for w in cat["workflows"]
    )
    gemini = f"""---
trigger: always_on
---

# Regras globais do ORCA-AI para o Antigravity

<!-- {AVISO} -->

Este workspace é o ORCA-AI, {cat["identidade"]["orgao"]}. Responsável técnico: {cat["identidade"]["responsavel"]}. Tratamento: {cat["identidade"]["tratamento"]}.

O Antigravity é responsável por: {cat["plataformas"]["antigravity"]["responsavel_por"]}. Não deve: {cat["plataformas"]["antigravity"]["nao_deve"]}.

## Classificação de pedido

| Pedido | Ação |
| --- | --- |
| Pergunta simples | Responder direto, sem criar arquivos. |
{classif}

## Agentes deste workspace

{_lista(f"`{a['slug']}` ({a['id']} {a['nome']}): {a['missao']} Ficha em `.agent/agents/{a['slug']}.md`." for a in agentes_por_plat["antigravity"])}

Subagentes em `.agent/subagents/`: {", ".join("`" + s["slug"] + "`" for s in sub_por_plat["antigravity"])}. Os demais agentes (A1 a A9 e A12) rodam no Claude Code e no Codex; a passagem de trabalho é por ordem de serviço em arquivo.

## Credenciais

Nenhuma credencial fica no sistema. Para o Orçafascio, abrir `{cat["identidade"]["orcafascio"]["url"]}` e aguardar o engenheiro fazer o login manualmente. Nunca preencher, solicitar ou armazenar a senha.

{regras}
## Protocolo de skills

Ao ativar um agente, ler sua ficha, depois o `SKILL.md` de cada skill listada (apenas as seções pertinentes ao pedido). Prioridade: estas regras > ficha do agente > SKILL.md.
"""
    arquivos[".agent/rules/GEMINI.md"] = gemini
    arquivos[".agent/ARCHITECTURE.md"] = (
        f"# Arquitetura do ORCA-AI no Antigravity\n\n<!-- {AVISO} -->\n\n## Agentes\n\n"
        + _lista(
            f"`{a['slug']}` — {a['id']} {a['nome']}"
            for a in agentes_por_plat["antigravity"]
        )
        + "\n\n## Subagentes\n\n"
        + _lista(f"`{s['slug']}`" for s in sub_por_plat["antigravity"])
        + "\n\n## Skills\n\n"
        + _lista(f"`{k}`" for k in skills_ag)
        + "\n\n## Workflows\n\n"
        + _lista(f"`/{w['comando']}` ({w['plataforma']})" for w in cat["workflows"])
        + "\n\nFonte única: `OrcaAI/agents/catalogo.yaml`. Fichas completas: `OrcaAI/agents/fichas/`.\n"
    )

    # openai.yaml nas skills do Codex (escrito na fonte canônica, só se faltar)
    if raiz_destino == raiz_origem:
        for nome, s in skills_cat.items():
            if s.get("codex") and s["situacao"] == "ativa":
                alvo = canonico / nome / "agents" / "openai.yaml"
                if not alvo.exists():
                    alvo.parent.mkdir(parents=True, exist_ok=True)
                    desc = _descricao_skill(canonico / nome / "SKILL.md") or nome
                    alvo.write_text(
                        "interface:\n"
                        f'  display_name: "{nome}"\n'
                        f'  short_description: "{desc[:120]}"\n'
                        f'  default_prompt: "Leia SKILL.md desta skill e aplique-a ao pedido, respeitando a regra de ouro do ORCA-AI: nunca inventar código, preço, coeficiente ou fonte."\n',
                        encoding="utf-8",
                    )
    # --- escrita --------------------------------------------------------
    for rel in PASTAS_PROJECAO:
        destino = raiz_destino / rel
        if destino.exists():
            for filho in destino.iterdir():
                if filho.name in PRESERVAR.get(rel, set()):
                    continue
                shutil.rmtree(filho) if filho.is_dir() else filho.unlink()
        destino.mkdir(parents=True, exist_ok=True)
    for rel, conteudo in arquivos.items():
        p = raiz_destino / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding="utf-8")
    for nome in skills_claude:
        if skills_cat[nome]["situacao"] == "ativa":
            shutil.copytree(
                canonico / nome,
                raiz_destino / ".claude" / "skills" / nome,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
    for nome in skills_ag:
        if skills_cat[nome]["situacao"] == "ativa":
            shutil.copytree(
                canonico / nome,
                raiz_destino / ".agent" / "skills" / nome,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
    return arquivos
