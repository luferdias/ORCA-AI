# Manifesto de migração — ORCA-AI 2.0 (2026)

Registro de toda remoção, movimentação e recuperação executada nas fases da especificação `spec/orca_ai_2_0_estrutura_e_agentes.md`. Nenhum arquivo é apagado sem linha aqui. Hashes SHA-256 permitem conferir o conteúdo contra o histórico do Git ou contra cópias externas.

## F1 — Recuperação do Orca.zip (29/10/2026, commit f1db3ed)

| Ação | Origem | Destino | Conferência |
| --- | --- | --- | --- |
| Extração integral | `Orca.zip` (128 entradas, 101 arquivos) | `OrcaAI/docs/historico/orca_central_2026-07/` | 101 arquivos extraídos, fins de linha normalizados, variável de senha removida do `.env.example`, `COMANDOS_TERMINAL.md` e `TUTORIAL.md` |
| Arquivamento | `Orca.zip` na raiz | `OrcaAI/docs/historico/Orca-2026-07.zip` | `git mv`, conteúdo idêntico |
| Recuperação | 9 skills do zip | `.agent/skills/` | auditoria-fontes-precos, cronograma-fisico-financeiro, curva-abc-sobrepreco, dossie-licitacao-publica, extracao-quantitativos-engenharia, matriz-riscos-contratacao, medicao-e-aditivo-contratual, normalizacao-planilhas-orcamento, termo-referencia-obras-servicos |
| Recuperação | 9 subagentes do zip | `.agent/subagents/` | `browser-orcafascio` ajustado para login manual |
| Recuperação | 8 workflows do zip | `.agent/workflows/` | `/orcafascio` ajustado para login manual |
| Recuperação | regras `GEMINI.md` do zip | `.agent/rules/orca-central.md` | seção de credenciais substituída por login manual |
| Recuperação | `projetos/_modelo` do zip | `OrcaAI/projetos/_modelo/` | 8 pastas com `.gitkeep` e 3 arquivos |

## F1 — Seiri (29/10/2026)

| Ação | Caminho | Tamanho / hash | Motivo e destino |
| --- | --- | --- | --- |
| Remoção (Git e disco) | `Item 07/automation_script/node_modules/` | 3164 arquivos, 31.8 MB | Dependências instaladas; reinstaláveis por `package.json` e `package-lock.json`, mantidos |
| Remoção | `Item 07/chrome_stdout.log`, `chrome_stderr.log` | 0 bytes cada (hash do vazio `e3b0c442…`) | Logs de execução vazios |
| Remoção | `Item 12/projetos_executivos_dwg/Reforço da estrutura da CAG.bak` | 22714792 bytes, `b592bde2803bb532…` | Backup automático do AutoCAD; o `.dwg` correspondente permanece |
| Remoção após extração | `projetos/Projetos Básicos dos itens 01 a 11.zip` | 21688001 bytes, `f3b6773c82072370…` | 17 dos 18 arquivos já existiam na pasta com hash idêntico; `Itens_01_a_11_assinado.pdf` (4.116.693 bytes) foi extraído para a pasta antes da remoção |
| Remoção | `Projetos/` na raiz | 13 arquivos `.gitkeep`, sem conteúdo | Estrutura experimental nunca usada; conceito absorvido por `OrcaAI/knowledge/` |
| Movimentação | `relatorio_regressao.pdf` (raiz) | `OrcaAI/ml/entregas/relatorio_regressao_didatico_2026-09-27.pdf` | 209875 bytes, `34ccb4f6d1fe2eb2…`; idêntico a `ml/outputs/relatorio_final_2026-09-27/relatorio.pdf` |
| Movimentação | `Organograma ORCA-AI.png` (raiz) | `OrcaAI/spec/ml_ufg/organograma.png` | `git mv` |
| Remoção local (não versionados) | `.sixth/` (vazia) e `.venv/` da raiz (layout Windows) | — | Inúteis no macOS; o ambiente real é `OrcaAI/ml/.venv` |
| Mantidos | `_governanca/plantas_e_projetos_gerais/*.bak` (2 arquivos) | — | Não há `.dwg` correspondente; podem ser a única cópia do desenho. Avaliar na F2 |
| Mantido | `.temp_ag_kit/` (ignorado) | — | Original do Antigravity Kit, para reinstalação (decisão D6) |

## F1 — Execuções de ML fora do Git (29/10/2026)

`OrcaAI/ml/outputs/` (17 execuções, 5069 arquivos, 3.58 GB) saiu do controle de versão com `git rm --cached`. Os arquivos **permanecem no disco**, na pasta sincronizada pelo OneDrive, e os links relativos dos documentos do módulo continuam válidos localmente. Versionados: `MANIFESTO.json` (digest por execução) e `MANIFESTO_arquivos.tsv` (SHA-256 de cada arquivo). Cópia em `ORCA-AI-artefatos/` no OneDrive e release no GitHub das três execuções entregues dependem da decisão D2.

| Execução | Arquivos | MB | Digest | Status registrado |
| --- | ---: | ---: | --- | --- |
| `20260927T184724_638519Z` | 0 | 0 | `e3b0c44298fc1c14…` | — |
| `20260927T184801_695117Z` | 0 | 0 | `e3b0c44298fc1c14…` | — |
| `20260927T185450_466046Z` | 214 | 246 | `081e22b9df72d5a4…` | — |
| `20260927T211131_310095Z` | 759 | 572 | `822dcad6e944b353…` | — |
| `20260927T211258_775620Z` | 759 | 572 | `fa07aed3386e964a…` | — |
| `20260927T211358_192111Z` | 761 | 572 | `2df73a9b8f2fefc9…` | — |
| `apresentacao_2026-09-27` | 759 | 572 | `8a25ed1a499d3b20…` | — |
| `entrega_ufg_acabamentos_2026-09-27` | 144 | 29 | `0a32beeea4b97b6d…` | concluido |
| `entrega_ufg_acabamentos_2026-09-27_previa_layout` | 144 | 29 | `f3c16f1b8942bdcf…` | concluido |
| `estudo_acabamentos_2026-09-27` | 83 | 20 | `cddd382e01fc1a13…` | erro |
| `estudo_acabamentos_final_2026-09-27` | 144 | 29 | `319c08a7239f9a5c…` | concluido |
| `janela_comum_2026-05` | 348 | 242 | `d3ed98f867fcff2b…` | — |
| `regressao_2026-09-27` | 344 | 286 | `d43578b6d0b08677…` | — |
| `regressao_validada_2026-09-27` | 344 | 286 | `1b66bb9cbbfe1311…` | — |
| `relatorio_didatico_2026-09-27` | 67 | 44 | `1e8e87341178d1da…` | — |
| `relatorio_final_2026-09-27` | 67 | 44 | `e6c898778a5e264f…` | — |
| `verificacao_der_inicial` | 132 | 35 | `73735ce6fdc8cde0…` | — |
## F2 — Seiton: acervo de projetos (29/10/2026, commit 3e6c752)

319 arquivos movidos com `git mv`; conferência por SHA-256 de todos os arquivos de `projetos/` antes e depois: nenhum perdido. Regras de distribuição: `assinado` → `07-assinados`; especificações → `06-documentos`; orçamentos, BDI, cronogramas e memórias → `03-orcamento`; propostas de fornecedores e pesquisa IN 65 → `04-cotacoes`; projetos recebidos e DWG → `00-entrada`; scripts de automação → `05-validacoes/scripts`.

| Pasta anterior | Pasta nova | Etapa | Arquivos |
| --- | --- | --- | ---: |
| `Item 01 - teto_elevadores` | `2026-001-teto-elevadores` | `(raiz)` | 1 |
| `Item 01 - teto_elevadores` | `2026-001-teto-elevadores` | `00-entrada` | 2 |
| `Item 01 - teto_elevadores` | `2026-001-teto-elevadores` | `03-orcamento` | 11 |
| `Item 01 - teto_elevadores` | `2026-001-teto-elevadores` | `06-documentos` | 2 |
| `Item 01 - teto_elevadores` | `2026-001-teto-elevadores` | `07-assinados` | 2 |
| `Item 02 - Limpeza_robotizada_AC` | `2026-002-limpeza-robotizada-ac` | `(raiz)` | 1 |
| `Item 02 - Limpeza_robotizada_AC` | `2026-002-limpeza-robotizada-ac` | `03-orcamento` | 10 |
| `Item 02 - Limpeza_robotizada_AC` | `2026-002-limpeza-robotizada-ac` | `06-documentos` | 2 |
| `Item 02 - Limpeza_robotizada_AC` | `2026-002-limpeza-robotizada-ac` | `07-assinados` | 2 |
| `Item 03 - Lavagem_envidracada` | `2026-003-lavagem-fachada-envidracada` | `03-orcamento` | 10 |
| `Item 03 - Lavagem_envidracada` | `2026-003-lavagem-fachada-envidracada` | `06-documentos` | 2 |
| `Item 03 - Lavagem_envidracada` | `2026-003-lavagem-fachada-envidracada` | `07-assinados` | 2 |
| `Item 04 - Junta_dilatacao` | `2026-004-juntas-dilatacao` | `03-orcamento` | 10 |
| `Item 04 - Junta_dilatacao` | `2026-004-juntas-dilatacao` | `06-documentos` | 2 |
| `Item 04 - Junta_dilatacao` | `2026-004-juntas-dilatacao` | `07-assinados` | 2 |
| `Item 05 - Pintura_grade` | `2026-005-pintura-grades` | `03-orcamento` | 10 |
| `Item 05 - Pintura_grade` | `2026-005-pintura-grades` | `06-documentos` | 2 |
| `Item 05 - Pintura_grade` | `2026-005-pintura-grades` | `07-assinados` | 2 |
| `Item 06 - insulfilm` | `2026-006-pelicula-controle-solar` | `03-orcamento` | 10 |
| `Item 06 - insulfilm` | `2026-006-pelicula-controle-solar` | `06-documentos` | 2 |
| `Item 06 - insulfilm` | `2026-006-pelicula-controle-solar` | `07-assinados` | 2 |
| `Item 07 - Pintura_externa_MGIES` | `2026-007-pintura-externa` | `03-orcamento` | 17 |
| `Item 07 - Pintura_externa_MGIES` | `2026-007-pintura-externa` | `05-validacoes` | 57 |
| `Item 07 - Pintura_externa_MGIES` | `2026-007-pintura-externa` | `06-documentos` | 6 |
| `Item 07 - Pintura_externa_MGIES` | `2026-007-pintura-externa` | `07-assinados` | 4 |
| `Item 08 - impermeabilizacao_cisterna` | `2026-008-impermeabilizacao-cisterna` | `03-orcamento` | 10 |
| `Item 08 - impermeabilizacao_cisterna` | `2026-008-impermeabilizacao-cisterna` | `06-documentos` | 2 |
| `Item 08 - impermeabilizacao_cisterna` | `2026-008-impermeabilizacao-cisterna` | `07-assinados` | 2 |
| `Item 09 - limpeza_FV` | `2026-009-limpeza-fotovoltaica` | `03-orcamento` | 12 |
| `Item 09 - limpeza_FV` | `2026-009-limpeza-fotovoltaica` | `06-documentos` | 2 |
| `Item 09 - limpeza_FV` | `2026-009-limpeza-fotovoltaica` | `07-assinados` | 2 |
| `Item 10 - MNT_gerador_subestacao` | `2026-010-manutencao-gerador-subestacao` | `03-orcamento` | 12 |
| `Item 10 - MNT_gerador_subestacao` | `2026-010-manutencao-gerador-subestacao` | `04-cotacoes` | 5 |
| `Item 10 - MNT_gerador_subestacao` | `2026-010-manutencao-gerador-subestacao` | `06-documentos` | 4 |
| `Item 10 - MNT_gerador_subestacao` | `2026-010-manutencao-gerador-subestacao` | `07-assinados` | 2 |
| `Item 11 - Impermeabilizacao_Marquise` | `2026-011-impermeabilizacao-marquise` | `00-entrada` | 1 |
| `Item 11 - Impermeabilizacao_Marquise` | `2026-011-impermeabilizacao-marquise` | `03-orcamento` | 10 |
| `Item 11 - Impermeabilizacao_Marquise` | `2026-011-impermeabilizacao-marquise` | `06-documentos` | 3 |
| `Item 11 - Impermeabilizacao_Marquise` | `2026-011-impermeabilizacao-marquise` | `07-assinados` | 2 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `(raiz)` | 3 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `00-entrada` | 12 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `02-quantitativos` | 6 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `03-orcamento` | 23 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `05-validacoes` | 2 |
| `Item 12 - Reforma_Suporte_CAG (duas subpastas 2026-001 unificadas)` | `2026-012-reforma-suporte-cag` | `06-documentos` | 13 |
| `Projetos Básicos` | `_projetos_basicos` | `(raiz)` | 18 |

Documentos da CAG que estavam em `docs/` (`projeto.md`, `plano_de_execucao.md`, `logs_de_decisoes.md`) voltaram ao item `2026-012`: plano e log substituem os modelos em branco; `projeto.md` ficou em `05-validacoes/historico/projeto_docs_2026-07.md`, ao lado de `projeto_variante_2026-001.md`. Cada item 01 a 11 recebeu `projeto.md`, `plano-execucao.md` e `log-decisoes.md` novos, com o nome da pasta anterior registrado.

## F2 — Seiton: ferramentas Python (29/10/2026)

| Origem | Destino |
| --- | --- |
| `OrcaAI/skills/{bdi_calculator,cronograma_generator,excel_budget_generator,code_guardrail_validator}.py` | `OrcaAI/tools/orca_tools/` (pacote, com `estrutura_projeto.py` novo e 18 testes) |
| `OrcaAI/scripts/criar_projeto_orca.py`, `validar_estrutura_orca.py` | `OrcaAI/tools/cli/criar_projeto.py`, `validar_estrutura.py` (reescritos para a estrutura real) |
| `OrcaAI/scripts/gerar_indice_dossie.py`, `orcafascio_es_automation.py` | `OrcaAI/tools/cli/` (o segundo reescrito para login manual, sem `.env`) |
| `OrcaAI/scripts/*.ps1` (4) | `OrcaAI/tools/windows/` |
| `build_despacho_24_58.py`, `build_despacho_engenharia_v2.py`, `generate_despacho.py`, `update_docx.py` | `projetos/_governanca_sei_agu_cgu/scripts/` (uso único, documentos SEI) |
| `build_entregavel3.py`, `generate_pdf_reportlab.py` | `docs/historico/entregavel_3_scripts/` (Entregável 3 TRL e PI, cujos produtos não estão no repositório) |
| Fichas `AGENTE_01` (link absoluto) e `AGENTE_07` ("Agente 11") | corrigidas no lugar |


## F3 — Catálogo único e projeções (29/10/2026)

| Ação | Origem | Destino | Observação |
| --- | --- | --- | --- |
| Fonte única | — | `OrcaAI/agents/catalogo.yaml` | 12 agentes, 11 subagentes, 5 subagentes de ML, 40 skills, 13 workflows, parâmetros fixos, guardrails, pausas e protocolo |
| Gerador | — | `OrcaAI/tools/orca_tools/catalogo.py`, `OrcaAI/tools/cli/gerar_projecoes.py` | `--verificar` compara as projeções com o catálogo; teste `test_projecoes_sincronizadas` |
| Skills canônicas | `.agent/skills/` (33) | `OrcaAI/agents/skills/` | `git mv`; `.agent/skills` e `.claude/skills` passam a ser cópias geradas (6 e 21 skills); skills do Codex ganham `agents/openai.yaml` |
| Fichas antigas | `OrcaAI/agents/AGENTE_01…10.md`, `AGENTE_5S.md` | `OrcaAI/agents/fichas/historico/` | preservadas; fichas 2.0 geradas em `OrcaAI/agents/fichas/` |
| Claude Code | — | `.claude/agents/` (6 agentes + 3 subagentes), `.claude/skills/`, bloco em `CLAUDE.md` | gerados |
| Codex | — | bloco em `AGENTS.md` | preferências do engenheiro preservadas fora do bloco |
| Antigravity | — | `.agent/rules/GEMINI.md`, `.agent/agents/` (A10, A11), `.agent/subagents/` (3), `.agent/skills/`, `.agent/workflows/` (13), `.agent/ARCHITECTURE.md` | gerados |
| Kit genérico do Antigravity | `.agent/workflows/` (11), `.agent/scripts/` (4), `mcp_config.json`, `ARCHITECTURE.md`, `rules/GEMINI.md`, `agents/` (6) | `OrcaAI/docs/historico/antigravity_2026-10/` | decisão D6; `.agent/.shared/ui-ux-pro-max` (560 KB) removido, cópia em `.temp_ag_kit/.agent/.shared` |
| Subagentes e workflows do zip | `.agent/subagents/` (9), `.agent/workflows/` (8), `.agent/rules/orca-central.md` | removidos das pastas ativas | substituídos pelos gerados; originais em `docs/historico/orca_central_2026-07/` e `antigravity_2026-10/rules/` |

## F4 — Linha de produção (29/10/2026)

| Entrega | Onde | Observação |
| --- | --- | --- |
| Indexador de bases (A9) | `orca_tools/indice_bases.py`, `tools/cli/indexar_bases.py` | Reusa os leitores validados do módulo de ML; `knowledge/indices/<fonte>/<competencia>/servicos.csv` (SINAPI: também `insumos.csv` das abas ISD e ICD, coluna ES) ignorados pelo Git; `manifesto.json` versionado. Construídos: SINAPI-ES 2026-02, 2026-04 e 2026-06; DER-ES 2026-02 e 2026-04 (não há ZIP DER de 2026-06 no acervo) |
| Normalizador de planilhas (A8) | `orca_tools/normalizar_planilha.py` | Lê a exportação "Orçamento Sintético" do Orçafascio usada nos doze itens; grava `03-orcamento/planilha-normalizada.csv` no modelo único |
| Renderizador (subagente) | `orca_tools/renderizar.py` | Markdown para DOCX (pandoc) e PDF (pandoc + Chrome) |
| Validação de ponta a ponta (A4) | `tools/cli/validar_item.py` | Normaliza, audita G-01 e G-02, confere códigos SINAPI/IOPES contra o índice da data-base declarada e grava `05-validacoes/relatorio-guardrails.md`, `validacao-codigos.md`, `validacao-codigos.json` e `codigos-oficiais.csv`. Executado nos doze itens |
| Guardrail G-01 refinado | `orca_tools/code_guardrail_validator.py` | Bancos oficiais da cascata completa, comparação por palavra inteira sem acento; séries próprias históricas (`SRAES-ELEV-`, `SRAES-LIMP-`, `SRAES-GER-`, `SRAES-SUB-`, `SRA-ES-`, `COMP-HVAC-`, `COMP-CAG-`) viram ressalva com pedido de mapeamento para `SRAES-CP` |
| Achados do acervo | `projetos/*/05-validacoes/` | Todos os doze itens passam sem bloqueio; dez ficam em RESSALVAS pelas séries próprias históricas; itens 05 e 08 APROVADOS em G-01 e G-02. Validação de códigos: Item 07 com 12 códigos consistentes e 5 descrições reescritas pelo engenheiro (a conferir pelo A4); Item 05 com 2 códigos não encontrados no índice de 2026-02 (a investigar). A planilha analítica do Orçafascio não tem valores em cache e fica para leitura futura |
| API Knowledge | — | Não iniciada; depende de Qdrant (fase posterior) |
