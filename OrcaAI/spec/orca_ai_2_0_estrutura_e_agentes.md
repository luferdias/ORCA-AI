---
title: "ORCA-AI 2.0 — Especificação técnica consolidada"
subtitle: "Estrutura, agentes, plataformas, aprendizado por demonstração e roteiro de migração"
author: "Engenheiro Luis Fernando · MGI / SRA-ES · com apoio do Claude Code"
date: "Versão 0.3 · 29/10/2026 · em execução"
lang: pt-BR
---

# ORCA-AI 2.0 — Especificação técnica consolidada

**Projeto:** ORCA-AI, Inteligência Artificial para Engenharia de Custos e Gestão Processual de Obras e Serviços de Engenharia.
**Órgão:** Ministério da Gestão e da Inovação em Serviços Públicos, Superintendência Regional de Administração no Espírito Santo (MGI / SRA-ES), Edifício Sede e Anexo, Vitória/ES.
**Responsável técnico:** engenheiro Luis Fernando.
**Versão:** 0.3, de 29/10/2026. Substitui as versões 0.1 e 0.2 do mesmo dia. **Status: em execução.** O engenheiro aprovou a proposta em 29/10/2026 e autorizou a execução contínua; o estado de cada fase está na seção 13.1.

---

## 0. Como ler este documento

Este documento consolida **tudo** o que o ORCA-AI já definiu, em três gerações de trabalho, e propõe a versão 2.0 sem descartar nada:

| Geração | Quando | Onde está | O que trouxe |
| --- | --- | --- | --- |
| **Central Orca** | julho/2026 | `Orca.zip` na raiz (128 entradas) | 12 agentes, 9 subagentes, 8 workflows, 33 skills, estrutura de projeto `00-entrada` a `07-assinados`, modelo de item orçamentário, templates, tutorial e comandos |
| **ORCA-AI** | agosto e setembro/2026 | `OrcaAI/` | 10 agentes numerados mais o Agente 5S, especificação do sistema, guardrails G-01 a G-10, protocolo LfD, protocolo de pesquisa de mercado, 12 contratações reais, acervo jurídico, bases SINAPI e DER-ES com manifestos |
| **Extensão ML/UFG** | setembro e outubro/2026 | `OrcaAI/ufg/spec/`, `OrcaAI/ufg/ml/`, `OrcaAI/knowledge/` | A11 e cinco subagentes de ML, cinco skills externas selecionadas, API Knowledge, estudo de regressão, classificação e agrupamento entregue à UFG, 223 testes, lint e hook |

A regra desta revisão, definida pelo engenheiro em 29/10/2026, é: **não cortar nada; melhorar o que já existe.** Por isso a seção 2 inventaria o que existe, a seção 3 diagnostica, as seções 4 a 12 propõem, e o Anexo A mostra, item a item, para onde cada coisa existente vai na versão 2.0.

Organização do documento:

1. Objetivo e premissas desta revisão
2. Inventário consolidado do ORCA-AI (o que existe hoje)
3. Diagnóstico 5S do repositório
4. Princípios da versão 2.0
5. Plataformas: Claude Code, Codex e Antigravity
6. Catálogo de agentes 2.0
7. Catálogo de skills e ferramentas 2.0
8. Workflows e comandos 2.0
9. Aprendizado por demonstração ampliado
10. Bases, conhecimento e API Knowledge
11. Extensão acadêmica de Machine Learning
12. Estrutura de pastas alvo
13. Roteiro de migração
14. Decisões que cabem ao engenheiro
15. Riscos e limites

- Anexo A. Mapa de preservação: de onde vem, para onde vai
- Anexo B. Referências internas

---

## 1. Objetivo e premissas desta revisão

O ORCA-AI já funciona. Produziu doze contratações reais para a SRA-ES, respondeu a parecer da AGU, tem protocolo de aprendizado por demonstração no Orçafascio e um estudo acadêmico de Machine Learning validado. Esta revisão faz quatro coisas:

1. **Inventaria** tudo o que o projeto já definiu, inclusive o que ficou na geração de julho e não migrou para a pasta atual.
2. **Diagnostica** o estado físico do repositório pela metodologia 5S e aponta o que está fora do lugar, duplicado, pesado ou inseguro.
3. **Define um catálogo único de agentes**, dizendo quantos são, o que cada um faz, qual plataforma executa cada um e como se comunicam.
4. **Propõe a estrutura de pastas alvo** e um roteiro de migração por fases, com critérios de conclusão e pontos de aprovação humana.

Premissas fixadas pelo engenheiro:

- Os papéis críticos de raciocínio técnico e governança rodam no **Claude Code**: orquestrador, arquiteto 5S, engenheiro civil sênior, auditor de dupla checagem e instrução processual.
- A produção em volume a partir de especificação clara vai para o **Codex**: descrições de serviços, composições de custo, planilhas, cronogramas, parsers e indexadores.
- A interação com navegador e o aprendizado por observação vão para o **Antigravity**: piloto do Orçafascio, observação do engenheiro, coleta de tabelas em portais governamentais, cotações.
- As três plataformas leem o mesmo catálogo de agentes.
- **Nenhuma credencial fica no sistema.** Quando um agente precisar do Orçafascio, ele abre o site e o engenheiro faz o login manualmente.
- O sistema deve aprender, observando o engenheiro, não só a busca de composições, mas também cronogramas, especificações, leitura de projetos (PDF, DWG, Revit) e composição de BDI.
- Os doze projetos existentes e os arquivos originais são preservados.

---

## 2. Inventário consolidado do ORCA-AI

Esta seção é o registro do que o projeto já definiu. Nada aqui é proposta; é o que vale hoje e continua valendo na 2.0, salvo onde a seção correspondente disser que melhora.

### 2.1 Identidade e contexto

- **Nome oficial:** Orca AI / ORCA-AI. O nome antigo do workspace, `Orcamento_de_Obra`, ainda aparece em caminhos absolutos de algumas fichas e deve ser eliminado (Seiketsu).
- **Órgão e local:** MGI / SRA-ES, Edifício Sede e Anexo, Vitória/ES. Praça de preços: Grande Vitória (Vitória, Vila Velha, Serra, Cariacica).
- **Paradigma:** aprendizado por demonstração (LfD). O engenheiro opera o Orçafascio; o sistema assimila e passa à operação autônoma supervisionada, com zero alucinação de códigos e preços.
- **Regra de ouro (Central Orca):** nenhum agente inventa código, preço, coeficiente ou fonte. Se a base oficial não resolver, registra pendência, pesquisa mercado e pede aprovação humana.
- **Ferramenta externa:** Orçafascio Web (`https://app.orcafascio.com/`), conta institucional `mgi.sra-es.serl@gestao.gov.br`, com mais de 30 bases ativas. Login manual pelo engenheiro.

### 2.2 Bases legais e normativas

| Norma | Aplicação |
| --- | --- |
| Lei Federal nº 14.133/2021 | Licitações e contratos; art. 46 para regime de execução |
| Decreto Federal nº 7.983/2013 | Elaboração de orçamento de obras e serviços de engenharia |
| IN SEGES/ME nº 65/2021 | Pesquisa de preços; art. 5º para requisitos da cotação |
| Acórdão TCU nº 2.622/2013 – Plenário | Fórmula e faixas de BDI |
| Acórdão TCU nº 2.371/2020 – Plenário | BDI diferenciado para fornecimento |
| Súmulas TCU 253/2010 e 258/2010 | Fundamentação em respostas a pareceres |
| Decreto nº 9.507/2018 | Atividades acessórias e complementares terceirizáveis |
| Portaria MS nº 3.523/1998, RE nº 09 ANVISA, NBR 14679:2012, NBR 15848:2010 | Climatização, PMOC e limpeza de HVAC |
| NBR 16690, NBR 16274, NBR 5410 | Instalações elétricas e fotovoltaicas |
| NR-10, NR-11, NR-12, NR-18, NR-35 | Segurança do trabalho |
| Diretrizes CREA-ES e CAU-ES | ART e RRT |

### 2.3 Parâmetros fixos do MGI/SRA-ES

**BDI.** Fórmula do Acórdão TCU 2.622/2013: BDI = [(1 + AC + S + R + G)(1 + DF)(1 + L) / (1 − I)] − 1.

- Serviços de engenharia e manutenção predial: **25,00%** (ISS Vitória 5%, PIS 0,65%, COFINS 3,00%, despesas indiretas do órgão).
- Fornecimento puro de materiais e equipamentos relevantes (painéis solares, grupos geradores, chillers): **14,02%**, faixa média do Acórdão (11,10% a 18,45%).
- O BDI do Orçafascio fica travado em 25% para serviços.

**Regime de encargos.** Não desonerado por padrão; desonerado quando solicitado. Nunca misturar regimes na mesma planilha (G-06).

**Codificação própria.** Serviços `SRAES-CP-001`, `SRAES-CP-002`...; insumos de mercado `SRAES-INS-001`...; proibido código genérico sem a chancela `SRAES-`. Códigos de skills anteriores (`SRAES-FV-001`, `COMP-HVAC-001`, `PR-01`) passam a ser aliases históricos mapeados para a série `SRAES-CP`.

**Cascata de bases oficiais** (consolidação das listas do Agente 2, do Agente 5, da spec do sistema e da Central Orca):

| Nível | Bases | Uso |
| --- | --- | --- |
| P0 – Local | SINAPI-ES (Caixa/IBGE); IOPES / DER-ES (edificações, projetos e rodovias) | Primeira referência para serviços no ES |
| P1 – Sudeste | EMOP-RJ, SCO-Rio; CDHU, FDE, CPOS, SIURB-SP, DER-SP TPU; SUDECAP, SETOP-MG, SICOR-MG | Fallback regional com identificação de região, período e motivo |
| P2 – Infraestrutura e demais | SICRO3-ES (DNIT) para terraplenagem e pavimentação; ORSE-SE (CEHOP) como fallback consagrado pelo TCU; SEINFRA-CE; SBC nacional | Por tipo de objeto |
| P3 – Nuvem Orçafascio | Mais de 30 bases ativas na conta MGI-ES | Sincronização e conferência |
| Auxiliares | CUB-ES e ANP combustíveis | Indicadores, não catálogos |

A preferência operacional não é regra universal de precedência; o A1 e o A5 registram qual regra do projeto determina a referência. O catálogo em `bases/catalogo_fontes_referenciais.json` registra doze fontes verificadas em 27/09/2026 com condições de acesso.

**Cascata geográfica de pesquisa de mercado** (IN 65/2021), acionada só quando nenhuma base oficial cobre o item: Nível 1 Grande Vitória; Nível 2 Rio de Janeiro; Nível 3 São Paulo; Nível 4 Belo Horizonte. Cada cotação traz razão social, CNPJ ativo, endereço, telefone, e-mail, nome e cargo do vendedor, data (validade máxima de 180 dias), descrição com marca e modelo, frete CIF Vitória ou destacado, tributação e condições de pagamento. Mínimo de três propostas válidas; preço de referência pela mediana; descarte motivado de valores com desvio superior a 25% da média. Pausa obrigatória antes de integrar o valor à composição própria. Para bens e serviços comuns sem caracterização de engenharia, a skill `pesquisa-mercado-licitacoes` acrescenta Painel de Preços, BPS e contratações similares.

### 2.4 Peças, artefatos e planilha

**As sete peças do dossiê** (spec do sistema e POP do dossiê):

1. `01_Planilha_Orcamentaria_Analitica.xlsx` e `.pdf`
2. `02_Composicoes_Custos_Unitarios_Proprias.xlsx`
3. `03_Demonstrativo_e_Justificativa_BDI.pdf`
4. `04_Cronograma_Fisico_Financeiro.xlsx`
5. `05_Especificacao_Tecnica_e_Memorial_Descritivo.docx` / `.pdf`
6. `06_Mapa_Cotacoes_Pesquisa_Mercado.pdf`
7. `07_Relatorio_Conformidade_e_Auditoria_G01_G10.pdf`, acompanhado do dossiê de instrução processual SEI (TJTR, justificativa de preço global, declaração do Decreto 9.507/2018, notas técnicas de resposta à AGU/CGU)

**Artefatos obrigatórios por projeto** (Central Orca): `projeto.md`, `plano-execucao.md`, `log-decisoes.md`, planilha normalizada, memória de cálculo, demonstrativo de BDI, validação de códigos, relatório de guardrails, documento técnico, índice do dossiê, checklist final. A Fase 7 da Central acrescenta relatório de cotações, relatório de validação SINAPI/IOPES e PDF final para assinatura.

**Pasta de trabalho Excel do Agente 8**, com fórmulas dinâmicas e sem valores fixos: `01_Planilha_Orcamentaria`, `02_Composicoes_Proprias`, `03_Demonstrativo_BDI`, `04_Cronograma_PERT_CPM_Gantt` (precedências, tempos cedo e tarde, folgas total e livre, caminho crítico automático, Gantt reativo, Curva S em R$ e %) e `05_Curva_ABC` (A 80%, B 15%, C 5%). Ordenação construtiva da EAP em sete blocos: mobilização e preliminares; isolamento, proteções e demolições; infraestrutura e reforços; camadas principais e instalações; acabamentos e pintura; testes e comissionamento; desmobilização e limpeza.

**Modelo de dados mínimo do item** (Central Orca, `templates/planilhas/modelo-item-orcamentario.yaml`): número, código, sistema, descrição, unidade, quantidade, custo unitário sem BDI, BDI %, preço unitário com BDI, preço total, fonte (nome, data-base, arquivo de referência), validação (código encontrado, unidade e descrição compatíveis), observações. Marcadores obrigatórios: `[SEM FONTE]`, `[VALIDAR COEFICIENTE]`, `[PENDENTE DE MEDICAO]`.

### 2.5 Guardrails G-01 a G-10

| ID | Validador | Regra | Ação |
| --- | --- | --- | --- |
| G-01 | Código referencial válido | Código oficial existente (SINAPI, IOPES, SICRO, ORSE) ou `SRAES-CP` / `SRAES-INS` | Bloqueio imediato |
| G-02 | BDI por natureza | 25,00% serviços; 14,02% fornecimento puro | Alerta e recálculo |
| G-03 | Produtividade plausível | Coeficientes dentro das médias SINAPI/IOPES | Notificação |
| G-04 | Dupla contagem | O&M e limpeza não cobram manutenções já embutidas | Zera o item duplicado |
| G-05 | Curva ABC auditada | Faixa A com conferência documental e cotações robustas | Exige justificativa reforçada |
| G-06 | Encargos homogêneos | Um só regime por planilha | Bloqueio |
| G-07 | Data-base coerente | Mesma janela temporal e praça | Notificação |
| G-08 | Fundamentação legal | Citação da Lei 14.133, Decreto 7.983 e Acórdão 2.622 | Injeção das notas legais |
| G-09 | Regime jurídico declarado | Separação entre engenharia (Decreto 7.983) e comuns (IN 65) | Separação no TR |
| G-10 | Cotações válidas | Três propostas com CNPJ | Bloqueio |

A Central Orca acrescenta bloqueios críticos equivalentes: item sem fonte, código não validado, unidade divergente, BDI incorreto, pesquisa sem evidências, composição própria sem aprovação, item A sem revisão, documentos que contradizem a planilha. Saída: relatório com status `APROVADO`, `RESSALVAS` ou `BLOQUEADO`, achados com severidade e ação.

### 2.6 Pontos de aprovação humana

União das listas da spec do sistema, da Central Orca, do protocolo de mercado e do LfD. O fluxo para e pede o "De acordo" quando:

- não há base oficial para o item;
- será feita pesquisa de mercado ou cotação externa;
- será criada composição própria;
- será usada base de outro estado ou fallback regional;
- o BDI aplicado difere do padrão;
- há divergência de unidade ou de descrição entre planilha e base;
- há item relevante da curva ABC sem fonte robusta;
- o Orçafascio vai passar do modo observador ao modo autônomo;
- um código ou preço próprio será inserido no Orçafascio;
- o documento final está pronto para assinatura ou envio.

Toda aprovação ou pendência é registrada em `log-decisoes.md` com data, decisão, motivo, responsável e evidência.

### 2.7 Fluxos existentes

Quatro descrições do mesmo fluxo convivem e são compatíveis:

- **Oito fases da Central** (Fase 0 abertura, 1 planejamento, 2 leitura técnica e quantitativos, 3 bases oficiais, 4 composição, 5 mercado, 6 validação e guardrails, 7 documentos).
- **Quinze passos do fluxograma de operação** (criar projeto, entrada, `/novo-orcamento`, triagem, escopo e quantitativos, bases, compor custo ou pesquisar mercado com aprovação, BDI e memória, validar SINAPI/IOPES, guardrails e ABC, corrigir ou gerar documentos, dossiê, revisão final, pacote para assinatura).
- **Doze etapas do POP do dossiê**, com os agentes numerados.
- **Três fases do LfD** (co-piloto e gravação; assimilação e síntese; operação autônoma com trava).

**Oito comandos da Central Orca:** `/novo-orcamento`, `/orcafascio`, `/pesquisar-precos`, `/validar-orcamento`, `/gerar-documentos`, `/gerar-dossie`, `/status-orca`, `/revisar-final`. O tutorial de nove passos e os comandos de terminal do Windows (PowerShell) documentam o uso. A versão 2.0 mantém os oito e acrescenta outros (seção 8).

### 2.8 Catálogos de agentes existentes

| Catálogo | Agentes | Onde |
| --- | --- | --- |
| ORCA-AI (atual) | 1 OrcaMasterOrchestrator; 2 EngenheiroCustosSenior; 3 OrcafascioPilot; 4 PesquisadorMercado; 5 MineradorBasesOficiais; 6 CompositorCustosUnitarios; 7 EspecialistaEspecificacao; 8 EngenheiroPlanejamentoEConomico; 9 AuditorConformidade; 10 EspecialistaInstrucaoProcessualSEI; 5S Auditor5S_Organizacao | `OrcaAI/agents/` |
| Central Orca (julho) | central-orchestrator, intake-triage-agent, project-planner, engenheiro-orcamentista-publico, orcamentista-mgi-es, compositor-custos, pesquisador-bases-oficiais, pesquisador-mercado, validador-codigos, guardrail-controladoria, documentalista-tecnico, revisor-final | `Orca.zip` |
| Subagentes (julho) | browser-orcafascio, spreadsheet-normalizer, pdf-docx-extractor, quantity-takeoff, quotation-harvester, code-validator, bdi-calculator, document-renderer, approval-notifier | `Orca.zip` |
| Antigravity (atual) | orchestrator, project-planner, explorer-agent, documentation-writer, orcamentista-mgi, engenheiro-orcamentista, mais 14 agentes genéricos do kit | `.agent/agents/` |
| Extensão ML | A11 PesquisadorMLUFG; SA-ML-01 curadoria; SA-ML-02 conhecimento e busca; SA-ML-03 treinamento; SA-ML-04 integração e API; SA-ML-05 avaliação | `OrcaAI/ufg/spec/` |

Atribuições relevantes que cada ficha trouxe e que a 2.0 preserva estão incorporadas na seção 6.

### 2.9 Skills existentes

**Atuais em `.agent/skills` (24):** bdi-servicos-es, behavioral-modes, brainstorming, check-sinapi-iopes-codes (com `scripts/validate_codes.py`, `references/source-layout.md` e `agents/openai.yaml`), clean-code, descritor-servicos-sinapi, documentation-templates, documentos-tecnicos-fv (com referências), documentos-tecnicos-gerador, documentos-tecnicos-hvac, engenheiro-civil-senior, guardrails-orcamento-publico, intelligent-routing, master-skill, orcafascio-integration, orcafascio-mgi-automation, orcamento-gerador-es, orcamento-limpeza-fv-es, orcamento-limpeza-hvac-es, pesquisa-mercado-licitacoes, pesquisa-mercado-vitoria, plan-writing, systematic-debugging, vitoria-cost-engineering (com `scripts/compositor.py`).

**Presentes só no `Orca.zip` (9), a recuperar:** auditoria-fontes-precos, cronograma-fisico-financeiro, curva-abc-sobrepreco, dossie-licitacao-publica, extracao-quantitativos-engenharia, matriz-riscos-contratacao, medicao-e-aditivo-contratual, normalizacao-planilhas-orcamento, termo-referencia-obras-servicos. São exatamente as nove "skills novas recomendadas" do documento de arquitetura da Central; elas foram escritas em julho e perdidas na migração de pasta.

**Selecionadas para ML (5), ainda não instaladas:** analyze-data-quality, scikit-learn, ml-pipeline-workflow, embedding-strategies, qdrant-clients-sdk. Reservas: qdrant-hybrid-search, rag-implementation.

**Módulos Python em `OrcaAI/skills` (4):** `bdi_calculator.py` (fórmula TCU, `ParametrosBDI`, `calcular_bdi`, `obter_bdi_padrao_mgi`), `cronograma_generator.py`, `excel_budget_generator.py` (abas coordenadas), `code_guardrail_validator.py` (`auditar_orcamento`, G-01 a G-10).

### 2.10 Templates, documentos, scripts, bases e acervo

- **Templates (11):** `modelo_composicao_propria_cpu.md`, `modelo_especificacao_tecnica.md`, `modelo_justificativa_bdi.md`, `modelo_pesquisa_mercado.md`; e os da Central: `bdi/demonstrativo-bdi.md`, `especificacoes/especificacao-tecnica.md`, `memoriais/memoria-calculo.md`, `planilhas/modelo-item-orcamentario.yaml`, `planilhas/modelo-planilha-orcamentaria.csv`, `relatorios/indice-dossie.md`, `relatorios/relatorio-validacao.md`. Modelos de projeto no zip: `_modelo/projeto.md`, `plano-execucao.md`, `log-decisoes.md`.
- **Workflows POP (2):** `pipeline_aprendizado_orcafascio.md`, `pipeline_geracao_dossie_completo.md`.
- **Docs (10):** tutorial, comandos de terminal, fluxograma, arquitetura da central, auditoria de bases de 27/09, viabilidade de ML, sincronização de 28/09, e três documentos da reforma da CAG (`projeto.md`, `plano_de_execucao.md`, `logs_de_decisoes.md`).
- **Scripts (14):** `criar_projeto_orca.py`, `validar_estrutura_orca.py`, `gerar_indice_dossie.py`, `orcafascio_es_automation.py`, geradores de despacho e entregáveis (`generate_despacho.py`, `build_despacho_24_58.py`, `build_despacho_engenharia_v2.py`, `build_entregavel3.py`, `generate_pdf_reportlab.py`, `update_docx.py`) e quatro `.ps1` de conversão no Windows.
- **Bases:** SINAPI-ES com 20 competências (2025-01 a 2026-08) e DER-ES com 17 (2025-01 a 2026-05), ZIPs originais intocados e manifestos SHA-256; pastas `iopes`, `sicro`, `orcafascio-export` e `outras-bases` criadas e vazias; catálogo de 12 fontes.
- **Knowledge:** datasets derivados `custos_historicos.csv` para SINAPI-ES e DER-ES, com relatório e curadoria.
- **Acervo de projetos (12):** Item 01 teto dos elevadores; 02 limpeza robotizada de dutos (PMOC); 03 lavagem de fachada envidraçada; 04 juntas de dilatação; 05 pintura de gradis; 06 película de controle solar; 07 pintura externa; 08 impermeabilização de cisterna; 09 O&M de usina fotovoltaica; 10 manutenção de gerador e subestação; 11 impermeabilização de marquise; 12 reforma do suporte da CAG. Mais `Projetos Básicos` (plantas DWG e PDF dos itens 01 a 11, calçada cidadã, estacionamento, anexo Vila Rubim) e `_governanca_sei_agu_cgu` (pareceres AGU, termos de justificativas globais, respostas e notas técnicas, despachos SEI, memória de BDI e ABC consolidada, plantas gerais).
- **Estrutura de projeto** (Item 12 e `_modelo`): `00-entrada`, `01-escopo`, `02-quantitativos`, `03-orcamento`, `04-cotacoes`, `05-validacoes`, `06-documentos`, `07-assinados`, `projeto.md`, `plano-execucao.md`, `log-decisoes.md`.

### 2.11 Extensão ML/UFG e API Knowledge

- Escopo confirmado em 27/09/2026: regressão, classificação e agrupamento; aprendizado por reforço fica para evolução futura.
- Estudo de pintura e acabamentos (pintura, revestimentos e forros, pisos, só m²), snapshot maio/2026, 514 serviços SINAPI e 70 DER, três classes derivadas dos grupos oficiais sem homologação humana, modelos e escalas separados por fonte. Resultados de 27/09: árvore de decisão vence a validação nas duas fontes; K-Means seleciona k=3 no SINAPI e nenhum k elegível no DER (diagnóstico k=2 preservado); a regressão nos três nichos não supera a persistência em MAPE. Regressão dos 18 nichos com comparação em janela comum.
- Entrega ao professor Ronaldo em 28/09/2026 com links permanentes ao commit `e20741b`. Em 29/10/2026 o ambiente subiu para pandas 3.1.0 e numpy 2.5.4 e reproduziu os resultados.
- Protocolo de avaliação em oito passos (congelar; separar por projeto e duplicatas; verificar classes; comparar com referência; ajustar só no treino; registrar completo; avaliar recuperação à parte com Recall@5 e MRR@5; documentar limites). Registro mínimo de exemplo com identificação, fonte, entrada, rótulo e versão.
- API Knowledge, contrato inicial: `GET /context/{context_id}`, `GET /models/latest`, `POST /insights`; configuração `KNOWLEDGE_PATH`, `VECTOR_DB=qdrant`, `QDRANT_URL`; sete critérios de verificação. Serviço não implementado.

### 2.12 Qualidade de código e memória

Ruff 0.17.3 configurado em `pyproject.toml`, hook de pre-commit com varredura de segredos e lint, 223 testes no módulo ML, `CLAUDE.md` e `AGENTS.md` com as preferências do engenheiro e a memória do projeto.

---

## 3. Diagnóstico 5S do repositório (29/10/2026)

### 3.1 Segurança — concluído em 29/10/2026

A senha institucional do Orçafascio estava em texto claro em 23 arquivos versionados (skill do Antigravity, ficha do Agente 3 e 21 scripts de automação do Item 07), em repositório público desde 28/09/2026. Princípio adotado: **nenhuma credencial fica no sistema; o engenheiro faz o login manualmente em cada sessão.** Executado no commit `3354d3f`: senha removida dos 23 arquivos, URL e login mantidos, hook de pre-commit com varredura de segredos, `.env` ignorado. Pendente do engenheiro: trocar a senha no Orçafascio (ela permanece no histórico do Git até a decisão D3).

### 3.2 Seiri — o que está no repositório sem precisar estar

| Item | Tamanho ou quantidade | Situação |
| --- | --- | --- |
| `OrcaAI/ufg/ml/outputs/` | 3,8 GB, 4.046 `.joblib`, 476 imagens | Dezessete execuções; quatro cópias idênticas de 547 MB; sete repetições do mesmo CSV de 82 MB. O `.git` tem 579 MB. |
| `Item 07/automation_script/node_modules/` | 3.164 arquivos JS/TS/map | Dependências de Node dentro de pasta de obra |
| Logs do Chrome, `.bak` de DWG, zip duplicado dos projetos básicos | 6 arquivos | Lixo de execução e duplicação |
| `Orca.zip` na raiz | 120 KB | Geração de julho, com 9 skills, 9 subagentes e 8 workflows que precisam ser recuperados antes de arquivá-lo |
| `relatorio_regressao.pdf`, `Organograma ORCA-AI.png` na raiz | 2 arquivos | Pertencem a `OrcaAI/ufg/ml/entregas` e `OrcaAI/ufg/spec` |
| `.temp_ag_kit/`, `.sixth/`, `.venv/` da raiz (layout Windows) | pastas | Já ignoradas; ocupam a raiz |
| `Projetos/` na raiz | 13 `.gitkeep` | Estrutura experimental nunca usada; README descreve links simbólicos removidos |

### 3.3 Seiton — o que está no lugar errado ou duplicado

- **Quatro catálogos de agentes sem ponte** (seção 2.8). Nenhum é gerado a partir do outro.
- **Fichas citam skills que não existem na pasta atual:** `guardrails-orcamento-publico` existe, mas `parallel-agents`, `dossie-licitacao-publica`, `extracao-quantitativos-engenharia` e outras só existem no zip. As fichas trazem caminhos absolutos do nome antigo do projeto.
- **Scripts apontam para estrutura inexistente:** `criar_projeto_orca.py` copia `projetos/_modelo`, que só existe no zip; `validar_estrutura_orca.py` exige `.agent/subagents`, `novo-orcamento.md` e `central-orchestrator.md`, que só existem no zip.
- **Acervo com dois padrões:** Itens 01 a 11 planos; Item 12 com estrutura numerada, duplicado em duas pastas `2026-001` (uma com nove arquivos a mais).
- **Documentos de um projeto na documentação do sistema:** os três documentos da CAG em `docs/`.
- **"Skills" com dois significados:** módulos Python em `OrcaAI/skills/` e instruções de prompt em `.agent/skills/`.
- **Scripts de uso único ao lado de ferramentas**, e `.ps1` do Windows em ambiente Mac.
- **Agente 7 cita "Agente 11 (CompositorCustosUnitarios)"**, numeração antiga; o compositor é o Agente 6.

### 3.4 O que já está certo e deve ser replicado

`bases/` com ZIPs intocados e manifestos; `ml/` com testes, lint, hook e manifestos de execução; `spec/orca_ai_system_spec.md` com os parâmetros fixos; `_governanca_sei_agu_cgu/` separado; o modelo de item orçamentário da Central; o protocolo de avaliação da extensão ML.

---

## 4. Princípios da versão 2.0

1. **Uma fonte, três projeções.** `OrcaAI/agents/catalogo.yaml` é a fonte única de agentes, subagentes, skills e workflows. Dele se geram `CLAUDE.md` e `.claude/agents/` (Claude Code), `AGENTS.md` (Codex) e `.agent/` (Antigravity). Nenhuma projeção é editada à mão.
2. **Plataforma segue o tipo de trabalho.** Decisão técnica, legal ou de governança: Claude Code. Produção repetitiva com especificação clara: Codex. Navegador, observação e portais: Antigravity.
3. **Nenhuma credencial no sistema.** Login manual pelo engenheiro; agentes não guardam, pedem nem digitam senhas; o hook bloqueia padrões de senha e chave.
4. **Artefato pesado fora do Git.** Resultados de execução, modelos e dependências instaladas ficam fora, com manifesto de hash dentro.
5. **Toda contratação tem a mesma anatomia** `00-entrada` a `07-assinados`; o acervo migra sem perder nenhum original.
6. **Nenhum agente inventa código, preço, coeficiente ou fonte.** Regra de ouro herdada da Central Orca.
7. **Nada se apaga sem registro.** Cada movimentação da migração gera linha em `docs/manifesto_migracao_2026.md` com origem, destino e hash.
8. **Pausas humanas são parte do fluxo** (seção 2.6).
9. **Documento e planilha contam a mesma história.** O documento final é gerado dos mesmos dados da planilha.

---

## 5. Plataformas e divisão de trabalho

| Plataforma | Modelo | Ponto de entrada (gerado) | Responsável por | Não deve fazer |
| --- | --- | --- | --- | --- |
| **Claude Code** | Claude 5 | `CLAUDE.md`, `.claude/agents/*.md`, `.claude/skills/` | Orquestração; arquitetura e 5S; engenharia civil sênior e decisões técnicas; auditoria e dupla checagem; instrução processual; pesquisa ML/UFG; geração das projeções | Preencher telas; baixar portais em massa |
| **Codex** | GPT | `AGENTS.md` na raiz, com uma seção por agente, mais `agents/openai.yaml` dentro das skills | Descrições canônicas; composições próprias; planilhas `.xlsx` com fórmulas; cronograma PERT/CPM, Gantt e Curva S; curva ABC; parsers e índices de bases; normalização de planilhas antigas; conversão DOCX/PDF | Decidir BDI, regime ou enquadramento; publicar sem auditoria |
| **Antigravity** | Gemini | `.agent/rules/GEMINI.md`, `.agent/agents/`, `.agent/subagents/`, `.agent/skills/`, `.agent/workflows/` | Piloto do Orçafascio com `browser_subagent`; observação e registro das ações do engenheiro; portais oficiais; captura de cotações e evidências; leitura multimodal de pranchas | Inserir código ou preço sem validação do auditor; guardar credenciais |

**Regra de passagem de bastão.** Trabalho que cruza plataformas passa por arquivo no repositório, nunca por copiar e colar. O orquestrador escreve uma **ordem de serviço** `os-NNN.md` em `projetos/<item>/05-validacoes/` com solicitante, destinatário, plataforma, objetivo, entradas, critério de aceite, dependências; o destinatário responde no mesmo arquivo com estado, artefatos, evidências, decisões, limitações e próximo responsável. É o "contrato de uma delegação" da extensão ML, generalizado.

---

## 6. Catálogo de agentes 2.0

**Doze agentes principais** em três camadas, **onze subagentes utilitários** e **cinco subagentes de ML**. Cada agente 2.0 absorve integralmente as atribuições das fichas anteriores listadas na coluna "Absorve". A numeração antiga fica válida por tabela de equivalência (decisão D1).

### 6.1 Camada de governança e engenharia — Claude Code

**A1 · OrcaMaestro** — absorve Agente 1 OrcaMasterOrchestrator, central-orchestrator, intake-triage-agent, project-planner, orchestrator.
Missão: conduzir a demanda da leitura do escopo até o dossiê. Atribuições: triagem (objeto, local, unidade, finalidade entre estimativa, licitação, TR, aditivo, medição ou parecer; arquivos recebidos; pendências); criar a pasta do item e `projeto.md`, `plano-execucao.md`, `log-decisoes.md`; classificar o serviço e as skills obrigatórias; despachar ordens de serviço; coordenar o ciclo LfD e autorizar a transição à autonomia; bloquear a esteira nas pausas da seção 2.6; submeter o pacote ao A4 antes da emissão; consolidar pendências e dossiê; apresentar ata de decisões e relatório executivo. Perguntas mínimas quando faltar informação: objeto e local; finalidade; quais arquivos são oficiais. Skills: intelligent-routing, plan-writing, brainstorming, guardrails-orcamento-publico, dossie-licitacao-publica.

**A2 · Arquiteto5S** — absorve Agente 5S Auditor5S_Organizacao, explorer-agent, documentation-writer (parte de estrutura).
Missão: guardião dos cinco sensos e da arquitetura. Seiri: elimina temporários, logs, `.bak`, imagens de OCR, pastas legadas migradas. Seiton: um lugar para cada coisa (regras da seção 12). Seiso: raiz limpa. Seiketsu: identidade única "Orca AI", prefixos padronizados, UTF-8 NFC. Shitsuke: relatório de conformidade 5S, bloqueio de implementações com violação crítica. Na 2.0 acrescenta: manter `catalogo.yaml` e o gerador das três projeções; manter hooks, lint, testes e CI; manter o manifesto de migração; validar estrutura de cada item (`validar_estrutura`). Skills: clean-code, documentation-templates, plan-writing.

**A3 · EngenheiroCivilSenior** — absorve Agente 2 EngenheiroCustosSenior, engenheiro-orcamentista-publico, engenheiro-orcamentista, orcamentista-mgi-es (parte decisória), Agente 6 (parte decisória: quando cabe CPU e quais insumos).
Missão: autoridade técnica. Interpreta projetos (PDF, DWG convertido em DXF ou PDF, Revit exportado em IFC), memoriais e vistorias; extrai áreas, volumes, extensões, pesos; aplica perdas e critérios de medição dos cadernos SINAPI; define método construtivo e EAP; valida unidade de pagamento; enquadra cada serviço na cascata P0 a P3; declara premissas; decide quando o serviço é atípico e exige composição própria, desdobrando em material, mão de obra e equipamento e repassando os insumos sem tabela ao A11; separa quantitativo medido de estimado (`[PENDENTE DE MEDICAO]`); aprende com as trilhas de demonstração (seção 9) e escreve os padrões. Skills: engenheiro-civil-senior, vitoria-cost-engineering, extracao-quantitativos-engenharia, bdi-servicos-es, descritor-servicos-sinapi, orcamento-limpeza-hvac-es, orcamento-limpeza-fv-es, orcamento-gerador-es.

**A4 · AuditorDuplaChecagem** — absorve Agente 9 AuditorConformidade, guardrail-controladoria, validador-codigos, revisor-final.
Missão: última linha de defesa. Executa G-01 a G-10; roda `validate_codes.py` e `auditar_orcamento` contra as bases locais; confere data-base, regime, BDI, unidade e descrição; curva ABC e risco de sobrepreço; auditoria de fontes de preço (todo item tem fonte, toda fonte tem data-base, Orçafascio exportado ou registrado); matriz de riscos; dupla checagem independente de quantitativos e preços; conferência com os portais, por meio do A11, de que a tabela usada é a vigente; valida o código antes de o A10 gravar no Orçafascio; revisão final (escopo e planilha coincidem, quantitativos com fonte, bases e data-base declaradas, BDI demonstrado, validações executadas, pendências resolvidas, arquivos no lugar). Emite `relatorio-guardrails.md`, `validacao-codigos.md`, `curva-abc.md`, `checklist-final.md` em `05-validacoes`, com status `APROVADO`, `RESSALVAS` ou `BLOQUEADO`. Skills: guardrails-orcamento-publico, check-sinapi-iopes-codes, curva-abc-sobrepreco, auditoria-fontes-precos, matriz-riscos-contratacao, dossie-licitacao-publica, engenheiro-civil-senior.

**A5 · InstrutorProcessualSEI** — absorve Agente 10 EspecialistaInstrucaoProcessualSEI, documentalista-tecnico (parte processual).
Missão: blindagem jurídica e instrução no SEI. Respostas ponto a ponto a pareceres AGU/CJU e apontamentos CGU/TCU com Súmulas 253 e 258, Acórdão 2.622, Lei 14.133 e Decreto 7.983; DFD alinhado ao PCA; termo de abertura; despachos à equipe de licitação; atas de alinhamento; TJTR; justificativa de empreitada por preço global (art. 46); declaração do Decreto 9.507/2018; termo de referência e projeto básico (estrutura de treze seções); medição, reajuste, reequilíbrio e aditivos; gestão do acervo `_governanca_sei_agu_cgu`. Skills: guardrails-orcamento-publico, engenheiro-civil-senior, documentation-templates, termo-referencia-obras-servicos, medicao-e-aditivo-contratual, dossie-licitacao-publica.

**A12 · PesquisadorMLUFG** — absorve A11 da extensão ML. Missão e limites conforme `agentes_e_subagentes.md`: conduz experimentos rastreáveis; delega a SA-ML-01 a SA-ML-04; não altera o acervo, não promove modelo nem toma decisões de orçamento; o parecer independente vem de SA-ML-05 via A4. Skills: plan-writing, documentation-templates, ml-pipeline-workflow, scikit-learn.

### 6.2 Camada de produção — Codex

**A6 · DescritorEspecificador** — absorve Agente 7 EspecialistaEspecificacao, documentalista-tecnico (parte técnica).
Descrição canônica com a sintaxe `[AÇÃO] + [ELEMENTO E SUBSTRATO] + [MATERIAIS] + [MÉTODO E FERRAMENTAL] + [CONDICIONANTES] + [AF_MÊS/ANO]`, mesmo a partir de demanda sumarizada; especificação técnica e memorial com as sete seções obrigatórias (objeto e local; justificativa; normas; metodologia; materiais; critérios de medição e pagamento; obrigações, ART/RRT, EPIs, resíduos e garantias); cadernos de encargos; documentos setoriais de HVAC, fotovoltaico e gerador; parecer técnico, laudo com registro fotográfico, minutas de ART/RRT. Regra: o documento não contradiz a planilha. Skills: descritor-servicos-sinapi, documentos-tecnicos-hvac, documentos-tecnicos-fv, documentos-tecnicos-gerador, documentation-templates, termo-referencia-obras-servicos.

**A7 · CompositorCPU** — absorve Agente 6 CompositorCustosUnitarios (parte executiva), compositor-custos.
Recebe a descrição do A6 e o enquadramento do A3; define a unidade; decompõe em mão de obra (códigos oficiais, por exemplo SINAPI 88316 servente e 88309 pedreiro, encargos de Vitória), materiais (perdas de 3% a 10% dos cadernos SINAPI; `SRAES-INS-XXX` quando sem tabela) e equipamentos (horas produtivas e improdutivas); calibra produtividade por cadernos SINAPI, TCPO e composições análogas IOPES/ORSE, documentando a justificativa; emite a ficha analítica `SRAES-CP-XXX` (tipo, código, banco, descrição, unidade, coeficiente, preço, total, custo direto sem BDI). Marca `[VALIDAR COEFICIENTE]` em estimativas. Skills: descritor-servicos-sinapi, orcafascio-integration, normalizacao-planilhas-orcamento, bdi-servicos-es, vitoria-cost-engineering.

**A8 · PlanilhistaPlanejador** — absorve Agente 8 EngenheiroPlanejamentoEConomico, bdi-calculator-subagent, spreadsheet-normalizer (parte de saída).
Gera a pasta de trabalho de cinco abas da seção 2.4 com fórmulas dinâmicas; aplica o BDI decidido pelo A3 e demonstra pela fórmula TCU; curva ABC; cronograma físico-financeiro com etapas, percentuais mensais e critérios de medição (soma 100%); PERT/CPM, Gantt e Curva S reativos; mantém `bdi_calculator`, `cronograma_generator` e `excel_budget_generator`. Skills: bdi-servicos-es, cronograma-fisico-financeiro, curva-abc-sobrepreco, normalizacao-planilhas-orcamento, vitoria-cost-engineering.

**A9 · MineradorBases** — absorve Agente 5 MineradorBasesOficiais (ingestão e indexação), pesquisador-bases-oficiais (consulta).
Ingere SINAPI-ES, IOPES/DER-ES, SICRO, ORSE e exportações do Orçafascio: parsers, normalização de códigos (zeros iniciais, valor bruto), unidades, grupos, regime; índice local de consulta em milissegundos; retorna para cada item código, fonte, data-base, descrição, unidade, custo e decomposição material, mão de obra e equipamento; monitora datas-base e garante a mesma data-base no lote; emite declaração formal de inexistência e passa o bastão ao A11. Saída padrão: tabela item, descrição buscada, base, código, unidade, data-base, observação. Skills: vitoria-cost-engineering, descritor-servicos-sinapi, orcafascio-integration, check-sinapi-iopes-codes, clean-code.

### 6.3 Camada de navegador e aprendizado — Antigravity

**A10 · PilotoOrcafascio** — absorve Agente 3 OrcafascioPilot, browser-orcafascio-subagent, orcamentista-mgi (parte operacional).
Modo observador: registra base, praça, termo de busca, código escolhido, tipo (sintética ou analítica), quantidade, ajustes de produtividade ou perdas, BDI aplicado. Modo autônomo, após o "De acordo": insere os itens restantes, submetendo cada código ao A4 antes de gravar; nunca insere código inexistente; se a busca não retornar o item com 100% de confiança, suspende e aciona o A1; exporta planilhas sintéticas e analíticas para `bases/orcafascio-export/`; captura evidência visual. Autenticação: abre a URL e aguarda o engenheiro fazer o login; não preenche senha. Skills: orcafascio-mgi-automation, orcafascio-integration.

**A11 · PesquisadorPortaisMercado** — absorve Agente 4 PesquisadorMercado, Agente 5 (parte de coleta), pesquisador-mercado, quotation-harvester-subagent.
Portais: localiza e baixa a edição vigente de cada fonte do catálogo seguindo a regra da última tabela (seção 10), com URL, data de publicação e hash; atualiza o catálogo. Mercado: cascata Vitória, RJ, SP, BH; três propostas válidas com todos os campos da IN 65; mediana; descarte motivado; `04-cotacoes/relatorio-cotacoes.md` e mapa de cotações; pausa obrigatória antes de integrar à CPU; para bens comuns usa Painel de Preços e BPS. Skills: pesquisa-mercado-vitoria, pesquisa-mercado-licitacoes, auditoria-fontes-precos, vitoria-cost-engineering.

### 6.4 Subagentes utilitários (sem autonomia; chamados por um agente principal)

| Subagente | Plataforma | Função e saída | Origem |
| --- | --- | --- | --- |
| `extrator-pdf-docx` | Codex | Texto, tabelas e OCR de PDF e DOCX; `01-escopo/extracao-documentos.md` | pdf-docx-extractor-subagent |
| `extrator-quantitativos-cad` | Codex | DXF via `ezdxf`, IFC via `ifcopenshell`; quadro de quantitativos com fonte e confiança | quantity-takeoff-subagent, ampliado |
| `normalizador-planilhas` | Codex | XLSX, CSV e exportações para o modelo único; `03-orcamento/planilha-normalizada.*` | spreadsheet-normalizer-subagent |
| `calculador-bdi` | Codex | Confere BDI por tipo; `03-orcamento/demonstrativo-bdi.md` | bdi-calculator-subagent |
| `renderizador-documentos` | Codex | Markdown para DOCX e PDF com templates; editáveis em `06-documentos`, finais em `07-assinados` | document-renderer-subagent |
| `validador-codigos` | Claude Code ou Codex | `validate_codes.py`; `05-validacoes/validacao-codigos.md` e JSON | code-validator-subagent |
| `navegador-orcafascio` | Antigravity | Seleção de projeto, busca, exportação, evidência visual; login manual | browser-orcafascio-subagent |
| `navegador-portais` | Antigravity | Download e captura de tela datada em portais oficiais | novo |
| `coletor-cotacoes` | Antigravity | Organiza cotações e evidências; `04-cotacoes/relatorio-cotacoes.md` | quotation-harvester-subagent |
| `notificador-aprovacao` | Claude Code | Pausa o fluxo nos gatilhos da seção 2.6; registra em `log-decisoes.md` | approval-notifier-subagent |
| `redator-academico` | Claude Code | Relatórios e demonstrações da extensão ML | documentation-writer |

### 6.5 Subagentes de ML (reportam ao A12; SA-ML-05 reporta ao A4)

SA-ML-01 curadoria de dados (analyze-data-quality); SA-ML-02 conhecimento e busca documental (embedding-strategies, Qdrant); SA-ML-03 treinamento (scikit-learn, ml-pipeline-workflow); SA-ML-04 integração e API Knowledge (qdrant-clients-sdk); SA-ML-05 avaliação experimental (scikit-learn), com parecer `reproduzível`, `inconclusivo` ou `inválido`. Responsabilidades e limites conforme `agentes_e_subagentes.md`, preservados integralmente.

### 6.6 Tabela de equivalência

| 2.0 | ORCA-AI atual | Central Orca (julho) | Antigravity atual |
| --- | --- | --- | --- |
| A1 OrcaMaestro | Agente 1 | central-orchestrator, intake-triage-agent, project-planner | orchestrator, project-planner |
| A2 Arquiteto5S | Agente 5S | — | explorer-agent |
| A3 EngenheiroCivilSenior | Agente 2 (+ decisões do 6) | engenheiro-orcamentista-publico, orcamentista-mgi-es | engenheiro-orcamentista |
| A4 AuditorDuplaChecagem | Agente 9 | guardrail-controladoria, validador-codigos, revisor-final | — |
| A5 InstrutorProcessualSEI | Agente 10 | documentalista-tecnico (processual) | — |
| A6 DescritorEspecificador | Agente 7 | documentalista-tecnico (técnico) | documentation-writer |
| A7 CompositorCPU | Agente 6 (execução) | compositor-custos | — |
| A8 PlanilhistaPlanejador | Agente 8 | bdi-calculator-subagent | — |
| A9 MineradorBases | Agente 5 (indexação) | pesquisador-bases-oficiais | — |
| A10 PilotoOrcafascio | Agente 3 | browser-orcafascio-subagent | orcamentista-mgi |
| A11 PesquisadorPortaisMercado | Agente 4, Agente 5 (coleta) | pesquisador-mercado, quotation-harvester | — |
| A12 PesquisadorMLUFG | A11 da extensão ML | — | — |

### 6.7 Protocolo entre agentes

- **Ordem de serviço** (seção 5).
- **Estados de um item:** `rascunho` → `enquadrado` (A3) → `composto` (A7 ou código oficial via A9) → `precificado` (A8 ou A10) → `auditado` (A4) → `aprovado` (engenheiro) → `emitido`. Registro em `03-orcamento/itens.yaml`, no modelo de dados da seção 2.4.
- **Pausas** da seção 2.6, operadas pelo `notificador-aprovacao`.
- **Fluxo padrão** (o mesmo dos POPs, com os ids novos): A1 triagem e plano → A3 escopo, quantitativos e enquadramento → A9 bases ou A10 Orçafascio → se faltar base, A11 mercado com pausa → A6 descrição → A7 CPU → A8 planilha, BDI e cronograma → A4 auditoria → correção ou A6 documentos e A5 instrução → A1 dossiê → revisão final (A4) e assinatura.

---

## 7. Catálogo de skills e ferramentas 2.0

Skills de prompt ficam em `OrcaAI/agents/skills/<nome>/SKILL.md` com `agents/openai.yaml` quando a skill for usada pelo Codex, e são projetadas para `.claude/skills` e `.agent/skills`. Ferramentas Python ficam no pacote `OrcaAI/tools/orca_tools`.

| Skill | Situação | Dona | Plataforma |
| --- | --- | --- | --- |
| engenheiro-civil-senior | ativa | A3 | Claude Code |
| vitoria-cost-engineering (+ compositor.py) | ativa | A3, A7, A8, A9, A11 | todas |
| bdi-servicos-es | ativa | A3, A7, A8 | Claude Code, Codex |
| descritor-servicos-sinapi | ativa | A6, A7, A9 | Codex |
| guardrails-orcamento-publico | ativa | A1, A4, A5 | Claude Code |
| check-sinapi-iopes-codes (+ validate_codes.py) | ativa | A4, A9 | Claude Code, Codex |
| orcafascio-integration | ativa | A7, A9, A10 | Codex, Antigravity |
| orcafascio-mgi-automation | ativa, sem credenciais | A10 | Antigravity |
| pesquisa-mercado-vitoria | ativa | A11 | Antigravity |
| pesquisa-mercado-licitacoes | ativa | A11 | Antigravity |
| orcamento-limpeza-hvac-es | ativa | A3, A7 | Claude Code, Codex |
| orcamento-limpeza-fv-es | ativa | A3, A7 | Claude Code, Codex |
| orcamento-gerador-es | ativa | A3, A7 | Claude Code, Codex |
| documentos-tecnicos-hvac | ativa | A6 | Codex |
| documentos-tecnicos-fv (+ references) | ativa | A6 | Codex |
| documentos-tecnicos-gerador | ativa | A6 | Codex |
| plan-writing, brainstorming, intelligent-routing, documentation-templates, clean-code, behavioral-modes, systematic-debugging | ativas (kit) | A1, A2 | todas |
| master-skill | ativa; passa a instalar só o que o ORCA usa | A2 | Antigravity |
| auditoria-fontes-precos | **recuperar do zip** | A4, A11 | Claude Code |
| curva-abc-sobrepreco | **recuperar do zip** | A4, A8 | Claude Code, Codex |
| matriz-riscos-contratacao | **recuperar do zip** | A4, A5 | Claude Code |
| dossie-licitacao-publica | **recuperar do zip** | A1, A4, A5 | Claude Code |
| extracao-quantitativos-engenharia | **recuperar do zip** | A3 | Claude Code, Codex |
| normalizacao-planilhas-orcamento | **recuperar do zip** | A7, A8 | Codex |
| cronograma-fisico-financeiro | **recuperar do zip** | A8 | Codex |
| termo-referencia-obras-servicos | **recuperar do zip** | A5, A6 | Claude Code, Codex |
| medicao-e-aditivo-contratual | **recuperar do zip** | A5 | Claude Code |
| analyze-data-quality, scikit-learn, ml-pipeline-workflow, embedding-strategies, qdrant-clients-sdk | **instalar** (externas, com licença conferida) | A12, SA-ML | Claude Code |
| qdrant-hybrid-search, rag-implementation | reservas | SA-ML-02 | — |
| leitura-projetos-cad (nova) | **criar**: DXF e IFC, camadas, cotas, conferência com prancha | A3 | Claude Code, Codex |
| aprendizado-por-demonstracao (nova) | **criar**: formato das trilhas, síntese de padrões, validação | A3, A4, A10 | todas |

Skills genéricas do Antigravity Kit sem uso no ORCA (frontend, mobile, jogos, SEO, segurança ofensiva etc.) saem de `.agent` e ficam disponíveis em `.temp_ag_kit` para reinstalação (decisão D6).

**Ferramentas Python (`orca_tools`)**: `bdi` (de `bdi_calculator.py`), `cronograma`, `planilha_excel`, `guardrails` (de `code_guardrail_validator.py`), `validar_codigos` (de `validate_codes.py`), `compositor` (de `compositor.py`), `manifestos` (hash e manifesto de migração), `indice_dossie`, `projeto` (criar e validar estrutura), `extrair_cad` (novo), `trilhas_lfd` (novo). CLIs em `tools/cli/`. Scripts de uso único de um item vão para a pasta do item em `05-validacoes/scripts/`; `.ps1` ficam em `tools/windows/` com nota de que o ambiente principal é macOS.

---

## 8. Workflows e comandos 2.0

Os oito comandos da Central Orca são mantidos com os mesmos nomes. Cinco são acrescentados. Cada comando declara em qual plataforma roda e quais agentes aciona.

| Comando | Plataforma | Aciona | Saída |
| --- | --- | --- | --- |
| `/novo-orcamento <slug>` | Claude Code | A1, A3 | pasta do item, `projeto.md`, `plano-execucao.md`, pendências |
| `/observar-orcafascio` (novo) | Antigravity | A10 em modo observador | trilha LfD em `knowledge/demonstracoes/` |
| `/orcafascio` | Antigravity | A10 em modo autônomo, A4 na trava | itens inseridos, exportação, evidências |
| `/pesquisar-precos` | Antigravity | A11, coletor-cotacoes, pausa | `04-cotacoes/relatorio-cotacoes.md` |
| `/atualizar-bases` (novo) | Antigravity + Codex | A11 portais, A9 ingestão | ZIP original, manifesto, índice |
| `/validar-orcamento` | Claude Code | A4, validador-codigos | `validacao-codigos.md`, `relatorio-guardrails.md`, `curva-abc.md` |
| `/gerar-documentos` | Codex | A6, renderizador-documentos | especificação, memorial, TR, demonstrativo de BDI, relatório de cotações |
| `/instruir-sei` (novo) | Claude Code | A5 | despachos, notas técnicas, TJTR, DFD |
| `/gerar-dossie` | Claude Code | A1, A4 | `indice-dossie.md`, `checklist-final.md`, lista de finais |
| `/revisar-final` | Claude Code | A4 | status aprovado, com ressalvas ou bloqueado |
| `/status-orca` | qualquer | leitura das oito pastas | fase atual, pendências, próximo comando |
| `/auditar-5s` (novo) | Claude Code | A2 | relatório de conformidade 5S |
| `/experimento-ml` (novo) | Claude Code | A12, SA-ML | execução com manifesto e relatório |

As regras globais do Antigravity (`GEMINI.md` da Central Orca) são mantidas e atualizadas: classificação de pedido, nove regras técnicas, pastas padrão `00` a `07`, pontos de parada, e a seção de credenciais passa a dizer apenas "login manual pelo engenheiro".

---

## 9. Aprendizado por demonstração ampliado

O protocolo atual (três fases: co-piloto e gravação; assimilação e síntese; operação autônoma com trava) cobre a busca e inserção de composições no Orçafascio. A 2.0 mantém o protocolo e amplia o escopo para cronogramas, especificações, leitura de projetos e composição de BDI.

### 9.1 O que é gravado

Cada sessão observada gera uma **trilha** em `knowledge/demonstracoes/<item>/<data>-<atividade>.jsonl`. Cada linha é um evento: instante; aplicação (Orçafascio, Excel, Word, visualizador de PDF ou CAD); tela ou aba; ação (busca, seleção, digitação, cálculo, filtro); entrada do engenheiro; resultado observado; justificativa dita ou digitada, quando houver; captura da tela (HTML ou imagem) quando a ação for no navegador. No Orçafascio, os campos são os já definidos no protocolo: base, praça, termo, código, tipo, quantidade, ajuste de produtividade ou perdas, BDI. Para Excel e Word, o engenheiro trabalha no arquivo dentro da pasta do item e o A2 registra as diferenças entre versões salvas.

### 9.2 Como vira conhecimento

1. O A3 lê as trilhas e escreve **padrões** em `knowledge/padroes/<atividade>.md`, por exemplo: "em pintura externa de fachada, buscar família 88xxx, preferir composição com andaime incluso, cronograma em três parcelas de 30%, 40% e 30%". A matriz de calibração do protocolo atual (famílias preferenciais, regime, BDI travado) é o primeiro padrão.
2. O A4 confere cada padrão contra os parâmetros fixos (seção 2.3) e marca `validado` ou `pendente`.
3. Só padrões validados entram nas instruções dos agentes de produção, por regeneração do catálogo pelo A2.
4. Cada padrão guarda a trilha de origem; prática nova substitui o padrão, com histórico.
5. A transição à autonomia continua exigindo entre três e cinco itens observados e a mensagem de prontidão com o "De acordo".

### 9.3 Leitura de projetos

Nenhum modelo lê DWG nativo com confiabilidade. Caminho determinístico, em caráter assistido até validação em três itens do acervo:

- **DWG:** converter para DXF com o ODA File Converter e extrair entidades com `ezdxf`; o A3 confere camadas; o `extrator-quantitativos-cad` calcula áreas e comprimentos.
- **Revit:** exportar IFC; `ifcopenshell` extrai elementos com quantidades.
- **PDF de prancha:** leitura multimodal pelo Antigravity para localizar cotas e tabelas, sempre conferida pelo A3 contra DXF ou IFC quando existir.
- Até a validação, o quantitativo final é do engenheiro; o sistema produz a memória de cálculo para conferência. Quantitativo estimado é premissa, nunca medição confirmada.

### 9.4 Segurança da sessão

O A10 abre o site e aguarda o login do engenheiro. Não preenche senha, não a solicita, não a armazena. Só opera em modo autônomo depois que o A4 confirma que a tela corresponde à versão aprendida.

---

## 10. Bases, conhecimento e API Knowledge

- **Regra da última tabela** (sete passos, preservada): abrir a pesquisa do projeto; consultar o publicador; confirmar o arquivo; conferir o conteúdo; guardar a edição original com hash; fixar as referências do orçamento; atualizar com rastreabilidade. Portal indisponível gera `atualidade_nao_confirmada`.
- **Entidades:** fonte, edição, serviço/composição, insumo, composição analítica, exemplo revisado; chave de serviço inclui base e código; versão inclui edição, UF, regime e revisão; campos adicionais `descricao_oficial`, `descricao_normalizada`, `unidade_original`, `unidade_normalizada`, `grupo_nativo`, `classe_revisada`, `source_locator`, `regime_encargos`, `bdi_incluso`, `bdi_percentual`, `preco_status`.
- **Caminho de coleta:** `bases/<fonte>/<uf>/<competencia>/<revisao>/originais/` com manifesto; a estrutura atual `bases/sinapi/<competencia>/originais/` é compatível e migra sem mover ZIPs.
- **Índices locais** em `knowledge/indices/`, gerados pelo A9, ignorados pelo Git, com manifesto versionado.
- **API Knowledge:** contrato preservado (três rotas, configuração, critérios). Implementação em `OrcaAI/api/` quando a Fase F4 chegar; Qdrant local na porta 6333.

---

## 11. Extensão acadêmica de Machine Learning

Preservada na íntegra: proposta alinhada às aulas (LinearRegression, RandomForest com árvore e KNN, KMeans), plano de consolidação de acabamentos, protocolo de avaliação, registro mínimo de exemplo, pacote acadêmico de um experimento, cinco skills selecionadas e duas reservas, organograma. Mudanças na 2.0: A11 passa a A12 na numeração; `OrcaAI/ufg/ml/outputs` sai do Git com manifesto e release das três execuções entregues; o estudo ganha o comando `/experimento-ml`. Aprendizado por reforço continua fora do escopo.

---

## 12. Estrutura de pastas alvo

```text
ORCA-AI/
├── README.md                 # apresentação; aponta para OrcaAI/README.md
├── CLAUDE.md                 # gerado do catálogo (Claude Code)
├── AGENTS.md                 # gerado do catálogo (Codex)
├── pyproject.toml            # ruff, pytest, pacote orca_tools
├── .githooks/pre-commit      # segredos + ruff
├── .claude/
│   ├── agents/               # gerado: A1–A5, A12, subagentes Claude
│   └── skills/               # projeção das skills usadas pelo Claude Code
├── .agent/                   # Antigravity, só o que o ORCA usa
│   ├── rules/GEMINI.md       # gerado
│   ├── agents/               # gerado: A10, A11
│   ├── subagentes/           # gerado: navegador-orcafascio, navegador-portais, coletor-cotacoes
│   ├── skills/               # projeção das skills do Antigravity
│   └── workflows/            # os treze comandos da seção 8
└── OrcaAI/
    ├── README.md
    ├── agents/
    │   ├── catalogo.yaml     # FONTE ÚNICA
    │   ├── fichas/           # uma ficha por agente e subagente
    │   └── skills/           # 33 skills + novas, com agents/openai.yaml onde couber
    ├── spec/                 # sistema, guardrails, LfD, mercado, esta spec, ml_ufg/
    ├── docs/                 # tutorial, comandos, fluxograma, auditorias, manifesto de migração
    ├── workflows/            # POPs
    ├── templates/            # os 11 templates + _modelo de projeto
    ├── bases/                # ZIPs originais + manifestos + catálogo
    ├── knowledge/
    │   ├── indices/          # gerado pelo A9 (ignorado; manifesto versionado)
    │   ├── demonstracoes/    # trilhas LfD
    │   ├── padroes/          # padrões validados
    │   ├── datasets/         # derivados para ML
    │   ├── documentos/       # derivados e identificados para busca
    │   └── embeddings/       # manifestos do índice vetorial
    ├── api/                  # API Knowledge (futuro)
    ├── tools/
    │   ├── orca_tools/       # pacote Python com testes
    │   ├── cli/
    │   ├── windows/          # .ps1
    │   └── tests/
    ├── ml/                   # como hoje; outputs/ ignorado com MANIFESTO.json
    └── projetos/
        ├── _modelo/
        ├── _governanca_sei_agu_cgu/
        ├── _projetos_basicos/
        ├── 2025-001-teto-elevadores/ ... 2025-011-impermeabilizacao-marquise/
        └── 2026-001-reforma-cag/
```

Regras de nome: item como `AAAA-NNN-slug`, número antigo em `projeto.md`; peças com prefixo `01_` a `07_`; sem espaços nem acentos em nomes novos; originais recebidos mantêm o nome em `00-entrada`; UTF-8 NFC.

O que sai do Git: `ml/outputs` (OneDrive `ORCA-AI-artefatos/ml-outputs/` com `MANIFESTO.json` e release das três execuções entregues); `node_modules`, logs, `.bak`, zip duplicado, `.temp_ag_kit`, `.sixth`, `.venv` da raiz; `Projetos/` da raiz. `Orca.zip` é arquivado em `docs/historico/` depois que seu conteúdo útil for recuperado.

---

## 13. Roteiro de migração

Nenhuma fase apaga arquivo sem registrar hash e destino em `docs/manifesto_migracao_2026.md`.

| Fase | Nome | Executor | O que acontece | Pronto quando |
| --- | --- | --- | --- | --- |
| **F0** | Segurança | Engenheiro + A2 | Troca da senha no Orçafascio (pendente); remoção da senha (feito); login manual (feito); varredura no hook (feito) | `git grep` sem credenciais; hook bloqueia senha falsa |
| **F1** | Seiri e recuperação | A2 (Claude Code) | Recuperar do `Orca.zip` as 9 skills, 9 subagentes, 8 workflows e `_modelo`; sair `ml/outputs`, `node_modules`, logs, `.bak`, zips e pastas vazias; `.gitignore`; manifesto | Repositório abaixo de 600 MB sem `.git`; nada do zip perdido |
| **F2** | Seiton | A2 + `normalizador-planilhas` (Codex) | `_modelo`; migrar itens 01 a 11 para `00`–`07`; unificar o item 12; mover documentos da CAG; `tools/orca_tools` com testes; corrigir fichas (skills inexistentes, caminhos antigos, "Agente 11") | `validar_estrutura` passa em 12 itens; conferência por hash |
| **F3** | Catálogo | A2 (Claude Code) | `catalogo.yaml`; gerador das três projeções; `.agent` reduzido; `AGENTS.md` por agente; `openai.yaml` nas skills do Codex | `diff` vazio após regenerar |
| **F4** | Produção | A6, A7, A8, A9 (Codex) | Indexador de bases; normalização das planilhas antigas; renderizador; API Knowledge inicial | Um item refeito de ponta a ponta e aprovado pelo A4 |
| **F5** | LfD ampliado | A10, A11 (Antigravity) + A3, A4 | `/observar-orcafascio`; trilhas; padrões validados; `/atualizar-bases` | Três sessões gravadas; cinco padrões validados; catálogo de fontes com hash |
| **F6** | Shitsuke | A2 | CI no GitHub (hook, `validar_estrutura`, testes); relatório 5S mensal; `/auditar-5s` | CI verde no `main`; relatório sem violação crítica |

Ordem: F0 hoje; F1 e F2 só com Claude Code; F3 antes de F4; F5 depois de F3.

### 13.1 Estado de execução em 29/10/2026

| Fase | Estado | Commits | O que foi feito | O que falta |
| --- | --- | --- | --- | --- |
| F0 | parcial | `3354d3f` | Senha removida de 23 arquivos; login manual como regra; varredura de segredos no hook e na CI | Troca da senha no Orçafascio, só o engenheiro pode fazer |
| F1 | concluída | `f1db3ed`, `4fa127b`, `5ff4efc` | Conteúdo do `Orca.zip` recuperado e arquivado; `node_modules`, logs, backup, zip duplicado e `Projetos/` removidos; `ml/outputs` fora do Git com manifestos | Cópia externa e release das execuções entregues (D2) |
| F2 | concluída | `3e6c752`, `0f4557a` | Doze itens na estrutura única; `tools/orca_tools` com testes; fichas e docs corrigidos; BDI do acervo reproduzido pela fórmula | — |
| F3 | concluída | `734687d` | `catalogo.yaml` como fonte única; gerador e verificador das três projeções; skills canônicas; kit genérico arquivado | — |
| F4 | concluída, exceto API | `3853cca` | Índices de bases, normalizador, renderizador, validação de ponta a ponta nos doze itens | API Knowledge (depende de Qdrant); leitura da planilha analítica do Orçafascio |
| F5 | preparada | este commit | Formato e utilitários das trilhas; primeiro padrão derivado do acervo; comandos `/observar-orcafascio` e `/orcafascio` gerados | Sessões reais gravadas pelo engenheiro no Antigravity; padrões a partir de trilhas |
| F6 | preparada | este commit | CI no GitHub: ruff, segredos, estrutura dos itens, projeções, testes de ferramentas e de ML | Relatório 5S mensal; reescrita do histórico (D3) |
| F7 | Reestruturação após a entrevista de maturidade | **Executada em 30/10/2026**: etapas sob demanda; G-01 tolera séries históricas nos itens aprovados; bloco `OrcaAI/ufg/` com modos `sraes` e `ufg`; venv na raiz; padrão de especificação técnica do acervo. Ver F7 do manifesto de migração. |

---

## 14. Decisões que cabem ao engenheiro

| Id | Decisão | Opções | Recomendação |
| --- | --- | --- | --- |
| D1 | Numeração dos agentes | Manter 1–10 e 5S; ou A1–A12 com equivalência | A1–A12 com equivalência |
| D2 | Onde guardar `ml/outputs` | OneDrive fora do repositório; Git LFS; release | OneDrive com manifesto, mais release das três execuções entregues |
| D3 | Reescrever o histórico do Git (senha e 3,8 GB) | Sim, uma vez, com `git filter-repo`; ou não | Sim, logo após F1; refazer os links da entrega UFG para o commit equivalente |
| D4 | Renomear itens 01 a 11 para `AAAA-NNN-slug` | Sim; ou manter o nome e só criar a estrutura interna | Sim |
| D5 | Pacote `orca_tools` no lugar de `scripts` e `skills` | Sim; ou manter | Sim |
| D6 | Remover o kit genérico do Antigravity de `.agent` | Remover; ou manter em pasta separada | Remover; `.temp_ag_kit` guarda o original |
| D7 | Credenciais do Orçafascio | **Decidido em 29/10/2026: login manual; nenhuma credencial armazenada** | Mantido |
| D8 | Recuperar as 9 skills, 9 subagentes e 8 workflows do `Orca.zip` | Sim; ou reescrever | Sim, na F1, revisando o texto de cada um |

---

## 15. Riscos e limites

- **Antigravity e Orçafascio:** a automação depende da interface; toda trilha guarda a versão da tela; o modo autônomo só roda com tela conferida pelo A4.
- **Codex sem contexto de decisão:** a ordem de serviço tem critério de aceite obrigatório; o A4 audita toda saída do Codex antes do dossiê.
- **Leitura de projetos:** assistida até validação em três itens; sem promessa de quantitativo automático.
- **Reescrita de histórico:** invalida clones e links permanentes; faz parte da decisão D3.
- **Skills externas de ML:** licenças e dependências a conferir antes de instalar, conforme `skills_selecionadas.md`.
- **Fichas descrevem papéis:** a presença de uma ficha não significa serviço autônomo em execução; o que roda é o que a plataforma executa quando acionada.

---

## Anexo A. Mapa de preservação: de onde vem, para onde vai

| Existente | Destino na 2.0 |
| --- | --- |
| `OrcaAI/agents/AGENTE_01` a `AGENTE_10`, `AGENTE_5S` | Absorvidos em A1 a A12 (seção 6.6); fichas antigas arquivadas em `agents/fichas/historico/` |
| 12 agentes da Central Orca (zip) | Absorvidos em A1, A3, A4, A5, A6, A7, A9, A10, A11 |
| 9 subagentes da Central Orca (zip) | Mantidos com nomes em português (seção 6.4) |
| 8 workflows da Central Orca (zip) | Mantidos com os mesmos nomes, mais cinco novos (seção 8) |
| `GEMINI.md` da Central Orca (zip) | Base do `GEMINI.md` gerado; credenciais viram login manual |
| 24 skills atuais | Mantidas em `agents/skills/` e projetadas |
| 9 skills só no zip | Recuperadas na F1 |
| 5 skills de ML e 2 reservas | Instaladas na F4, com licença conferida |
| `OrcaAI/skills/*.py` (4) e `compositor.py`, `validate_codes.py` | Pacote `tools/orca_tools` |
| `scripts/criar_projeto_orca.py`, `validar_estrutura_orca.py`, `gerar_indice_dossie.py`, `orcafascio_es_automation.py` | `tools/cli/`, corrigidos para a estrutura real |
| Geradores de despacho e entregáveis de uso único | `projetos/<item>/05-validacoes/scripts/` do item correspondente |
| `.ps1` | `tools/windows/` |
| 11 templates + `_modelo` do zip | `templates/` e `projetos/_modelo/` |
| POPs de LfD e dossiê | `workflows/`, atualizados com os ids novos |
| Spec do sistema, guardrails, mercado, LfD | Mantidas; esta spec as referencia e não as substitui |
| Docs de tutorial, comandos, fluxograma, arquitetura da central | Mantidos em `docs/`; tutorial ganha os comandos novos e versão macOS |
| Três documentos da CAG em `docs/` | `projetos/2026-001-reforma-cag/` |
| Auditoria de bases, viabilidade de ML, sincronização | `docs/` |
| Bases SINAPI (20) e DER-ES (17) com manifestos; catálogo de 12 fontes | `bases/`, sem mover ZIPs |
| `knowledge/datasets` | `knowledge/datasets` |
| Extensão ML: spec, código, testes, entregas | `ufg/spec/`, `ufg/ml/`, `ufg/ml/entregas/` (bloco UFG desde 30/10/2026) |
| `ml/outputs` (17 execuções) | OneDrive com manifesto; release das três entregues |
| 12 itens, projetos básicos, governança | `projetos/` na estrutura única; originais preservados em `00-entrada` ou na subpasta de origem |
| `Item 07/automation_script` (sem `node_modules`) | `projetos/2025-007-pintura-externa/05-validacoes/scripts/`; `package.json` mantido |
| `Orca.zip` | `docs/historico/Orca-2026-07.zip` após recuperação |
| `Organograma ORCA-AI.png`, `relatorio_regressao.pdf` | `ufg/spec/` e `ufg/ml/entregas/` |
| `Projetos/` da raiz | Removida; conceito absorvido por `knowledge/` |
| `CLAUDE.md`, `AGENTS.md` | Gerados do catálogo; preferências do engenheiro preservadas em bloco fixo |
| `pyproject.toml`, hook, ruff, 223 testes | Mantidos; CI na F6 |

## Anexo B. Referências internas

- Especificação do sistema: `OrcaAI/spec/orca_ai_system_spec.md`
- Guardrails: `OrcaAI/spec/guardrails_validation_spec.md`
- Protocolo LfD: `OrcaAI/spec/lfd_learning_protocol.md`
- Protocolo de mercado: `OrcaAI/spec/market_research_protocol.md`
- Arquitetura da Central Orca: `OrcaAI/docs/central-orcamento-publico-agentes-arquitetura.md` e `Orca.zip`
- Extensão ML/UFG: `OrcaAI/ufg/spec/` (README, proposta, plano, agentes e subagentes, skills, dados e avaliação, bases, API Knowledge)
- Fichas atuais: `OrcaAI/agents/`
- Fluxos: `OrcaAI/workflows/`, `OrcaAI/docs/FLUXOGRAMA_OPERACAO.md`, `OrcaAI/docs/TUTORIAL.md`, `OrcaAI/docs/COMANDOS_TERMINAL.md`
- Qualidade: `pyproject.toml`, `.githooks/pre-commit`, `OrcaAI/ufg/ml/README.md`
