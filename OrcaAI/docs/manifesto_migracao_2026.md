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
