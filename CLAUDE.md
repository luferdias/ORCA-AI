# Memória de trabalho do ORCA-AI

## Usuário e comunicação

- Nome: **Luis Fernando**, com **S**.
- Forma de tratamento solicitada: **engenheiro Luis Fernando**.
- Não usar “compadre”. A preferência explícita por S prevalece sobre grafias divergentes da transcrição.
- Responder em português, com linguagem clara e direta.
- Perfil: [memory/people/luis-fernando.md](memory/people/luis-fernando.md).

## Projeto acadêmico em andamento

- Aplicação de ML no ORCA-AI para a disciplina da UFG de aprendizado de máquina aplicado a dados estruturados.
- Fontes confirmadas: **SINAPI-ES** e **DER-ES/IOPES**; começar por SINAPI-ES, manter datasets e experimentos separados e comparar os resultados posteriormente.
- Escopo confirmado em 27/09/2026: **somente regressão, classificação e agrupamento**. Aprendizado por reforço fica para uma evolução futura.
- Entrega ao professor Ronaldo em 28/09/2026: PDF com links permanentes do GitHub em `OrcaAI/ufg/ml/entregas/professor_ronaldo_2026-09-28/relatorio.pdf`. O usuário autorizou explicitamente tornar `luferdias/ORCA-AI` público para leitura e download; visibilidade alterada e acesso anônimo verificado. Permissões de escrita permanecem restritas às contas autorizadas. A edição referencia o commit experimental `e20741b0214dff489147fa04739bb2a1ed44bc07` e preserva os resultados de 27/09/2026.
- Proposta alinhada às aulas: `LinearRegression`, `RandomForestClassifier` (comparadores árvore/KNN) e `KMeans`. Ver [proposta do projeto](OrcaAI/ufg/spec/proposta_projeto_ml_es.md).
- Três tarefas implementadas em Python para VS Code: [executar_estudo.py](OrcaAI/ufg/ml/executar_estudo.py), [executar_classificacao.py](OrcaAI/ufg/ml/executar_classificacao.py), [executar_agrupamento.py](OrcaAI/ufg/ml/executar_agrupamento.py) e [instruções](OrcaAI/ufg/ml/README.md). A regressão original continua em [executar_regressao.py](OrcaAI/ufg/ml/executar_regressao.py).
- Estudo confirmado de pintura e acabamentos: pintura, revestimentos/forros e pisos, somente m², snapshot maio/2026, 514 serviços SINAPI e 70 DER; três classes derivadas dos grupos oficiais, sem alegar homologação humana. Modelos e escalas separados por fonte. Plano: [consolidação](OrcaAI/ufg/spec/plano_consolidacao_acabamentos.md).
- Classificação seleciona por validação com grupos de variantes; na execução, a árvore venceu a validação nas duas fontes, ainda que RF tenha melhor F1 no teste. K-Means selecionou k=3 no SINAPI. No DER, nenhum k atendeu ao mínimo de quatro serviços por cluster: preservar diagnóstico k=2 identificado, sem tratá-lo como aprovado. A regressão nos três nichos não superou a persistência em MAPE.
- Apresentação didática da regressão: [relatório atual](OrcaAI/ufg/ml/APRESENTACAO_RESULTADOS.md), com HTML/PDF, 18 nichos e comparação em janela comum. O programa gera a apresentação automaticamente; `gerar_relatorio.py` refaz apenas os relatórios. Explicar ganhos e perdas frente à persistência, preservar extremos e identificar mudanças de serviço associadas ao mesmo código.
- Histórico coletado para regressão: SINAPI-ES 2025-01 a 2026-08 (20 competências); DER-ES 2025-01 a 2026-05 (17). Os datasets são separados; datas DER desconhecidas não são inferidas.
- Preservar os 12 projetos existentes e os arquivos originais. Trabalhar com dados derivados e versões identificadas. Desde a F2 (29/10/2026) os itens estão em `OrcaAI/projetos/2026-001-teto-elevadores` … `2026-012-reforma-suporte-cag`, estrutura `00-entrada` a `07-assinados`; validar com `OrcaAI/tools/cli/validar_estrutura.py`. Desde 30/10/2026 as etapas são **sob demanda** (regras R-E1 e R-E2 da entrevista de maturidade): `criar_projeto.py` cria controle e `00-entrada`; `--etapa` cria as demais; os itens históricos perderam as 44 etapas vazias e cada `projeto.md` lista as não aplicáveis. Respostas e regras da entrevista em `OrcaAI/knowledge/padroes/entrevista-maturidade-2026-10.md`.
- Materiais da disciplina: `/Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04 - Meus Documentos/GitHub/Machine Learning/`.
- ZIP SINAPI agosto/2026 obtido no site da CAIXA: `OrcaAI/bases/sinapi/2026-08/originais/`; conferir o manifesto antes de usar.
- **BDI do acervo:** os treze memoriais `Justificativa_Tecnica_BDI_25_*.pdf` (itens 01 a 12) usam regime **desonerado**, com AC 3,38%, R 0,85%, S+G 0,48%, DF 0,85%, L 6,00% e I 10,45% (ISS 5 + COFINS 3 + PIS 0,65 + CPRB 1,8), que a fórmula do TCU fecha em 25,00%. Em 30/10/2026 o engenheiro decidiu: **desonerado é o padrão** (R-B1); catálogo, spec, template de CPU e validador foram corrigidos. `orca_tools.bdi_calculator` reproduz a decomposição oficial; o BDI de fornecimento 14,02% não tem memorial no acervo e é tratado como taxa fixa.

## Qualidade de código

- Lint e formatação com **ruff 0.17.3**, configurado em `pyproject.toml` na raiz (regras padrão E4, E7, E9, F; Python 3.12; largura 88). Versão pinada em `OrcaAI/ufg/ml/requirements-dev.txt` e instalada no `.venv` da raiz do repositório.
- Rodar `ruff check .` e `ruff format .` a partir da raiz antes de commitar. Em 29/10/2026 todo o repositório passou a estar limpo e formatado.
- Hook versionado em `.githooks/pre-commit` roda `ruff check` e `ruff format --check` nos arquivos Python preparados e bloqueia o commit em caso de erro. Ativado neste clone com `git config core.hooksPath .githooks`; em outro clone é preciso repetir o comando.
- `core.fileMode false` está ativo neste clone porque o OneDrive altera permissões dos arquivos. O OneDrive também não preserva links simbólicos: não criar symlinks no repositório.
- **Vários lugares e sistemas (30/10/2026):** o engenheiro usa Mac e Windows, VS Code, a nuvem do Claude Code e o Maestri. Tudo o que define o sistema viaja no Git; um clone novo fica pronto com `sh preparar_ambiente.sh` (macOS/Linux) ou `preparar_ambiente.ps1` (Windows), que criam o `.venv`, ativam o hook e configuram o clone. `.gitattributes` fixa LF em scripts; `.maestri/` fica fora do Git. Regra: `git pull` antes de editar, um único clone dentro do OneDrive. Seção 6 do `README.md`.
- Documentação para o usuário: seção 5 do `README.md` da raiz e seção "Qualidade de código" de `OrcaAI/ufg/ml/README.md`.
- Em 29/10/2026 o venv (hoje `.venv` na raiz) subiu para pandas 3.1.0, numpy 2.5.4, reportlab 5.1.0 e pytest 9.2.0. O estudo de acabamentos e a regressão dos 18 nichos foram reexecutados e reproduziram as métricas, seleções e previsões de 27/09/2026; as únicas diferenças são no último dígito de ponto flutuante. As pastas em `OrcaAI/ufg/ml/outputs` não foram regeneradas e continuam sendo a referência entregue. Desde a F1 (29/10/2026) `ml/outputs` fica fora do Git, no disco local, com `MANIFESTO.json` e `MANIFESTO_arquivos.tsv` versionados; os links permanentes da entrega apontam para `e20741b`.

## ORCA-AI 2.0 (revisão de estrutura e agentes)

- Especificação consolidada em `OrcaAI/spec/orca_ai_2_0_estrutura_e_agentes.md` (PDF ao lado), versão 0.2 de 29/10/2026, rascunho para decisão. Regra fixada pelo engenheiro: **não cortar nada do que já existe; melhorar**. Doze agentes em três camadas (Claude Code: A1 maestro, A2 arquiteto 5S, A3 engenheiro civil sênior, A4 auditor de dupla checagem, A5 instrução SEI, A12 ML/UFG; Codex: A6 descritor, A7 compositor de CPU, A8 planilhista, A9 minerador de bases; Antigravity: A10 piloto do Orçafascio, A11 portais e mercado), onze subagentes utilitários e cinco de ML. Catálogo único em `agents/catalogo.yaml` gera `CLAUDE.md`, `AGENTS.md` e `.agent/`.
- F1 executada em 29/10/2026 (commits `f1db3ed`, `4fa127b` e seguinte): conteúdo do `Orca.zip` recuperado (9 skills, 9 subagentes em `.agent/subagents`, 8 workflows, `projetos/_modelo`, regras em `.agent/rules/orca-central.md`) e arquivado em `OrcaAI/docs/historico/`; Seiri com `node_modules`, logs, backup, zip duplicado e `Projetos/` removidos; `ml/outputs` fora do Git. F2 executada em 29/10/2026: doze itens na estrutura única, `scripts/` e `skills/` viraram `OrcaAI/tools/` (pacote `orca_tools` com testes), fichas e docs corrigidos. F3 executada em 29/10/2026: `OrcaAI/agents/catalogo.yaml` é a fonte única; `OrcaAI/tools/cli/gerar_projecoes.py` regenera `.claude/`, `AGENTS.md`, `.agent/` e as fichas; `--verificar` garante sincronia. Skills canônicas em `OrcaAI/agents/skills/`. Registro completo em `OrcaAI/docs/manifesto_migracao_2026.md`. F4 executada em 29/10/2026: `orca_tools` ganhou `indice_bases`, `normalizar_planilha` e `renderizar`; `tools/cli/validar_item.py` valida um item de ponta a ponta e foi rodado nos doze itens (nenhum bloqueio; ressalvas pelas séries próprias históricas). Índices locais em `OrcaAI/knowledge/indices/` (só manifestos versionados). F5 preparada (trilhas em `orca_tools.trilhas_lfd`, padrões em `OrcaAI/knowledge/padroes/`) e F6 preparada (CI em `.github/workflows/ci.yml`). Spec na versão 0.3 com a seção 13.1 de estado. Pendentes do engenheiro: trocar a senha do Orçafascio, gravar sessões reais no Antigravity, decidir D2 e D3.
- **F7 (30/10/2026), reestruturação após a entrevista de maturidade** (`OrcaAI/knowledge/padroes/entrevista-maturidade-2026-10.md`, regras R-A1 a R-E5): etapas sob demanda e 44 etapas vazias removidas do acervo; G-01 tolera séries históricas nos itens aprovados (R-B6) e o normalizador deixou de gerar ressalvas G-02 por arredondamento (onze dos doze itens aprovados sem ressalva); bloco acadêmico em `OrcaAI/ufg/` (`ml/`, `spec/`) com os modos `sraes` (padrão) e `ufg` declarados no catálogo; venv único em `.venv` na raiz; padrão de especificação técnica derivado do acervo em `knowledge/padroes/especificacao-tecnica-sra.md`; layout das três plataformas no Maestri (maestro **Engenheiro Chefe** para governança e construção do sistema; terminais de produção Batuta, Prumo e Sextante; os dois Claude Code são mantidos de propósito, ver seção 8.1 da spec do layout; partitura "ORCA-AI · Layout" salva com o Batuta como maestro). Decisões confirmadas em 30/10: regime desonerado por padrão (R-B1), cascata completa (R-A6), orçamento enxuto (R-B9) e séries antigas congeladas com composições novas em SRAES-CP (R-B6). Também confirmados: apresentação/avaliação do curso por API em FastAPI ou Django, a definir no modo UFG (R-E3), e repositório **mantido público** porque o engenheiro envia links aos professores da pós (R-E5). Entrevista sem pendências.
- Spec de operação do layout com as três plataformas: `OrcaAI/spec/orca_ai_layout_tres_plataformas.md` (PDF ao lado), versão 1.4 de 30/10/2026: panorama, fluxo de um orçamento, Playwright, regras da entrevista, F7, modos e canvas do Maestri.
- Credenciais do Orçafascio: **login manual pelo engenheiro em cada sessão; nenhuma senha no sistema**. Senha removida de 23 arquivos no commit `3354d3f`; o hook de pre-commit bloqueia segredos. Pendente: trocar a senha no Orçafascio e decidir a reescrita do histórico (D3).
- Decisões abertas D1 a D6 e D8 na seção 14 da spec (D7 decidida; D8 executada na prática pela F1).

<!-- orca:catalogo:inicio -->
## Catálogo de agentes 2.0 (2.0.0, 2026-10-29)

Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão.

| Id | Agente | Plataforma | Missão |
| --- | --- | --- | --- |
| A1 | OrcaMaestro | Claude Code | Conduzir a demanda da leitura do escopo até o dossiê de contratação pública. |
| A2 | Arquiteto5S | Claude Code | Guardião dos cinco sensos e da arquitetura do repositório. |
| A3 | EngenheiroCivilSenior | Claude Code | Autoridade técnica de engenharia civil e de custos. |
| A4 | AuditorDuplaChecagem | Claude Code | Última linha de defesa: guardrails, dupla checagem e revisão final. |
| A5 | InstrutorProcessualSEI | Claude Code | Blindagem jurídica e instrução processual no SEI. |
| A6 | DescritorEspecificador | Codex | Descrições canônicas, especificações técnicas e memoriais. |
| A7 | CompositorCPU | Codex | Fichas analíticas de composição própria SRAES-CP com insumos oficiais. |
| A8 | PlanilhistaPlanejador | Codex | Planilha orçamentária, BDI, curva ABC, cronograma, PERT/CPM e Curva S. |
| A9 | MineradorBases | Codex | Ingestão, normalização e índice local das bases oficiais. |
| A10 | PilotoOrcafascio | Antigravity | Observar o engenheiro no Orçafascio e, após o De acordo, operar com trava anti-alucinação. |
| A11 | PesquisadorPortaisMercado | Antigravity | Tabelas vigentes nos portais oficiais e pesquisa de mercado da IN 65/2021. |
| A12 | PesquisadorMLUFG | Claude Code | Extensão acadêmica de Machine Learning, com experimentos rastreáveis. |

- Agentes do Claude Code em `.claude/agents/` (A1, A2, A3, A4, A5, A12 e subagentes `validador-codigos`, `notificador-aprovacao`, `redator-academico`); skills em `.claude/skills/`.
- Codex lê `AGENTS.md`; Antigravity lê `.agent/`. Fichas completas em `OrcaAI/agents/fichas/`. Fonte: `OrcaAI/agents/catalogo.yaml`.
- Regra de ouro: Nenhum agente inventa código, preço, coeficiente ou fonte. Se a base oficial não resolver, registra pendência, pesquisa mercado e pede aprovação humana.
- Orçafascio: manual, pelo engenheiro, no início de cada sessão; nenhum agente armazena, solicita ou digita a senha.
- Comandos: `/novo-orcamento`, `/observar-orcafascio`, `/orcafascio`, `/pesquisar-precos`, `/atualizar-bases`, `/validar-orcamento`, `/gerar-documentos`, `/instruir-sei`, `/gerar-dossie`, `/revisar-final`, `/status-orca`, `/auditar-5s`, `/experimento-ml`.
<!-- orca:catalogo:fim -->

## Sincronização com o GitHub — premissa multiplataforma (decisor, 30/10/2026)

Este projeto é trabalhado no **Antigravity, VS Code, Codex e Claude Code**, no **Mac (casa) e no Windows (trabalho)**.
**GitHub = fonte da verdade; OneDrive = só backup de arquivos.** A sincronização é automática
(`git-autosync`: serviço do sistema a cada 15 min + hooks do Claude Code — ver `VOLT-AI/docs/git-autosync/LEIA-ME.md`),
mas todo agente, em qualquer plataforma, segue a mesma regra, porque Codex e Antigravity não têm hooks:

1. **Ao começar:** `git fetch origin` e, na branch principal com árvore limpa, `git pull --ff-only origin <principal>`.
2. **Ao terminar (ou a cada marco):** `git add -A` (nunca arquivos de credencial), `git commit` em português imperativo, `git push origin <branch>`.
3. Nunca `push --force`; divergência resolve-se com `git pull --rebase` e, se falhar, para e avisa.
4. O `.git` de cada máquina vive **fora** do OneDrive (`~/.gitdirs/<nome>.git` no Mac, `C:\Users\luis.fernando\.gitdirs\<nome>.git` no Windows); a pasta sincronizada tem só o ponteiro `.git` (arquivo). Não criar pastas `.git` dentro do OneDrive.
5. Se a árvore "sumir" sem mtime nas pastas (OneDrive re-enumerando, M-52 do VOLT-AI): não restaurar nem commitar — esperar e reconferir `git status`.
