# Fichas dos agentes ORCA-AI 2.0

Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão.

| Id | Agente | Plataforma | Camada | Missão |
| --- | --- | --- | --- | --- |
| A1 | [OrcaMaestro](A1-orca-maestro.md) | Claude Code | governança e engenharia | Conduzir a demanda da leitura do escopo até o dossiê de contratação pública. |
| A2 | [Arquiteto5S](A2-arquiteto-5s.md) | Claude Code | governança e engenharia | Guardião dos cinco sensos e da arquitetura do repositório. |
| A3 | [EngenheiroCivilSenior](A3-engenheiro-civil-senior.md) | Claude Code | governança e engenharia | Autoridade técnica de engenharia civil e de custos. |
| A4 | [AuditorDuplaChecagem](A4-auditor-dupla-checagem.md) | Claude Code | governança e engenharia | Última linha de defesa: guardrails, dupla checagem e revisão final. |
| A5 | [InstrutorProcessualSEI](A5-instrutor-processual-sei.md) | Claude Code | governança e engenharia | Blindagem jurídica e instrução processual no SEI. |
| A6 | [DescritorEspecificador](A6-descritor-especificador.md) | Codex | produção | Descrições canônicas, especificações técnicas e memoriais. |
| A7 | [CompositorCPU](A7-compositor-cpu.md) | Codex | produção | Fichas analíticas de composição própria SRAES-CP com insumos oficiais. |
| A8 | [PlanilhistaPlanejador](A8-planilhista-planejador.md) | Codex | produção | Planilha orçamentária, BDI, curva ABC, cronograma, PERT/CPM e Curva S. |
| A9 | [MineradorBases](A9-minerador-bases.md) | Codex | produção | Ingestão, normalização e índice local das bases oficiais. |
| A10 | [PilotoOrcafascio](A10-piloto-orcafascio.md) | Antigravity | navegador e aprendizado | Observar o engenheiro no Orçafascio e, após o De acordo, operar com trava anti-alucinação. |
| A11 | [PesquisadorPortaisMercado](A11-pesquisador-portais-mercado.md) | Antigravity | navegador e aprendizado | Tabelas vigentes nos portais oficiais e pesquisa de mercado da IN 65/2021. |
| A12 | [PesquisadorMLUFG](A12-pesquisador-ml-ufg.md) | Claude Code | governança e engenharia | Extensão acadêmica de Machine Learning, com experimentos rastreáveis. |

## Subagentes

| Subagente | Plataforma | Função | Origem |
| --- | --- | --- | --- |
| `extrator-pdf-docx` | Codex | Texto, tabelas e OCR de PDF e DOCX; salva 01-escopo/extracao-documentos.md. | pdf-docx-extractor-subagent |
| `extrator-quantitativos-cad` | Codex | DXF via ezdxf e IFC via ifcopenshell; quadro de quantitativos com fonte e confiança; quantitativo estimado é premissa, nunca medição confirmada. | quantity-takeoff-subagent (ampliado) |
| `normalizador-planilhas` | Codex | XLSX, CSV e exportações do Orçafascio para o modelo único; salva 03-orcamento/planilha-normalizada.*. | spreadsheet-normalizer-subagent |
| `calculador-bdi` | Codex | Confere BDI de serviço, obra e fornecimento; salva 03-orcamento/demonstrativo-bdi.md. | bdi-calculator-subagent |
| `renderizador-documentos` | Codex | Markdown para DOCX e PDF com os templates; editáveis em 06-documentos, finais em 07-assinados. | document-renderer-subagent |
| `validador-codigos` | Claude Code | Executa check-sinapi-iopes-codes/scripts/validate_codes.py; salva 05-validacoes/validacao-codigos.md e JSON. | code-validator-subagent |
| `navegador-orcafascio` | Antigravity | Seleção de projeto, busca de composições e insumos, exportação de relatórios e evidência visual; login manual do engenheiro; não insere preço próprio sem aprovação registrada. | browser-orcafascio-subagent |
| `navegador-portais` | Antigravity | Navegação, download e captura de tela datada em portais oficiais (CAIXA, DER-ES, DNIT, ORSE e regionais). | novo |
| `coletor-cotacoes` | Antigravity | Organiza cotações e evidências de fornecedores; salva 04-cotacoes/relatorio-cotacoes.md. | quotation-harvester-subagent |
| `notificador-aprovacao` | Claude Code | Pausa o fluxo nos gatilhos de aprovação humana e registra a decisão em log-decisoes.md. | approval-notifier-subagent |
| `redator-academico` | Claude Code | Relatórios e demonstrações da extensão ML/UFG a partir dos artefatos executados. | documentation-writer |

## Subagentes de ML

| Id | Nome | Reporta a | Skill externa | Função |
| --- | --- | --- | --- | --- |
| SA-ML-01 | Curadoria de dados | A12 | analyze-data-quality | Inventário, extrações, dicionário de campos, candidatos a rótulos e relatório de qualidade, com ligação a arquivo, página, aba ou linha e projeto de origem. |
| SA-ML-02 | Conhecimento e busca documental | A12 | embedding-strategies | Divisão em trechos, embeddings para português técnico, manifesto do índice, consultas de referência; sem fonte suficiente, devolve resultado insuficiente. |
| SA-ML-03 | Treinamento de modelos | A12 | scikit-learn, ml-pipeline-workflow | Compara referência simples com modelos; ajusta pré-processamento só no treino; registra configurações, versões, candidatos e previsões. |
| SA-ML-04 | Integração e API Knowledge | A12 | qdrant-clients-sdk | Conexão com Qdrant, consulta a contextos, registro de modelos e gravação de insights; testes de contrato. |
| SA-ML-05 | Avaliação experimental | A4 | scikit-learn | Verifica isolamento entre projetos, duplicatas, cobertura dos rótulos e comparação com baseline; parecer reproduzível, inconclusivo ou inválido. |

## Equivalência com os catálogos anteriores

| 2.0 | Absorve |
| --- | --- |
| A1 OrcaMaestro | Agente 1 OrcaMasterOrchestrator, central-orchestrator, intake-triage-agent, project-planner, orchestrator |
| A2 Arquiteto5S | Agente 5S Auditor5S_Organizacao, explorer-agent, documentation-writer (estrutura) |
| A3 EngenheiroCivilSenior | Agente 2 EngenheiroCustosSenior, engenheiro-orcamentista-publico, engenheiro-orcamentista, orcamentista-mgi-es (decisão), Agente 6 (decisão) |
| A4 AuditorDuplaChecagem | Agente 9 AuditorConformidade, guardrail-controladoria, validador-codigos, revisor-final |
| A5 InstrutorProcessualSEI | Agente 10 EspecialistaInstrucaoProcessualSEI, documentalista-tecnico (processual) |
| A6 DescritorEspecificador | Agente 7 EspecialistaEspecificacao, documentalista-tecnico (técnico), documentation-writer |
| A7 CompositorCPU | Agente 6 CompositorCustosUnitarios (execução), compositor-custos |
| A8 PlanilhistaPlanejador | Agente 8 EngenheiroPlanejamentoEConomico, bdi-calculator-subagent |
| A9 MineradorBases | Agente 5 MineradorBasesOficiais (indexação), pesquisador-bases-oficiais |
| A10 PilotoOrcafascio | Agente 3 OrcafascioPilot, browser-orcafascio-subagent, orcamentista-mgi (operação) |
| A11 PesquisadorPortaisMercado | Agente 4 PesquisadorMercado, Agente 5 (coleta), pesquisador-mercado, quotation-harvester-subagent |
| A12 PesquisadorMLUFG | A11 da extensão ML/UFG |

## Skills

| Skill | Situação | Donos | Codex |
| --- | --- | --- | --- |
| engenheiro-civil-senior | ativa | A3, A4, A5 | não |
| vitoria-cost-engineering | ativa | A3, A7, A8, A9, A11 | sim |
| bdi-servicos-es | ativa | A3, A7, A8 | sim |
| descritor-servicos-sinapi | ativa | A6, A7, A9 | sim |
| guardrails-orcamento-publico | ativa | A1, A4, A5 | não |
| check-sinapi-iopes-codes | ativa | A4, A9 | sim |
| orcafascio-integration | ativa | A7, A9, A10 | sim |
| orcafascio-mgi-automation | ativa | A10 | não |
| pesquisa-mercado-vitoria | ativa | A11 | não |
| pesquisa-mercado-licitacoes | ativa | A11 | não |
| orcamento-limpeza-hvac-es | ativa | A3, A7 | sim |
| orcamento-limpeza-fv-es | ativa | A3, A7 | sim |
| orcamento-gerador-es | ativa | A3, A7 | sim |
| documentos-tecnicos-hvac | ativa | A6 | sim |
| documentos-tecnicos-fv | ativa | A6 | sim |
| documentos-tecnicos-gerador | ativa | A6 | sim |
| plan-writing | ativa | A1, A2, A12 | não |
| brainstorming | ativa | A1 | não |
| intelligent-routing | ativa | A1 | não |
| documentation-templates | ativa | A2, A5, A6, A12 | sim |
| clean-code | ativa | A2, A9 | sim |
| behavioral-modes | ativa | A1 | não |
| systematic-debugging | ativa | A2 | não |
| master-skill | ativa | A2 | não |
| auditoria-fontes-precos | ativa | A4, A11 | não |
| curva-abc-sobrepreco | ativa | A4, A8 | sim |
| matriz-riscos-contratacao | ativa | A4, A5 | não |
| dossie-licitacao-publica | ativa | A1, A4, A5 | não |
| extracao-quantitativos-engenharia | ativa | A3 | sim |
| normalizacao-planilhas-orcamento | ativa | A7, A8 | sim |
| cronograma-fisico-financeiro | ativa | A8 | sim |
| termo-referencia-obras-servicos | ativa | A5, A6 | sim |
| medicao-e-aditivo-contratual | ativa | A5 | não |
| analyze-data-quality | instalar | A12 | não |
| scikit-learn | instalar | A12 | não |
| ml-pipeline-workflow | instalar | A12 | não |
| embedding-strategies | instalar | A12 | não |
| qdrant-clients-sdk | instalar | A12 | não |
| leitura-projetos-cad | criar | A3 | sim |
| aprendizado-por-demonstracao | criar | A3, A4, A10 | não |

## Workflows

| Comando | Plataforma | Aciona | Descrição |
| --- | --- | --- | --- |
| `/novo-orcamento` | claude_code | A1, A3 | Abre um item de orçamento e conduz triagem, planejamento e extração inicial de escopo. |
| `/observar-orcafascio` | antigravity | A10 | Grava uma sessão do engenheiro no Orçafascio como trilha de demonstração. |
| `/orcafascio` | antigravity | A10, A4 | Opera o Orçafascio em modo autônomo supervisionado, com trava anti-alucinação. |
| `/pesquisar-precos` | antigravity | A11, coletor-cotacoes | Pesquisa de mercado para itens sem base oficial, com três cotações e aprovação humana. |
| `/atualizar-bases` | antigravity | A11, A9 | Baixa a edição vigente das tabelas oficiais e reconstrói o índice local. |
| `/validar-orcamento` | claude_code | A4, validador-codigos | Valida planilha, códigos, fontes, BDI, curva ABC e riscos antes dos documentos finais. |
| `/gerar-documentos` | codex | A6, renderizador-documentos | Gera especificação, memorial, TR, demonstrativo de BDI e relatórios a partir da planilha validada. |
| `/instruir-sei` | claude_code | A5 | Peças de instrução processual: despachos, notas técnicas, TJTR e DFD. |
| `/gerar-dossie` | claude_code | A1, A4 | Monta o pacote final com índice, checklist, planilha, memória, validações, documentos e pendências. |
| `/revisar-final` | claude_code | A4 | Revisão final de coerência entre escopo, orçamento, memória, documentos e dossiê. |
| `/status-orca` | qualquer | — | Mostra a fase atual de um item, pendências e próximo comando. |
| `/auditar-5s` | claude_code | A2 | Relatório de conformidade 5S do repositório. |
| `/experimento-ml` | claude_code | A12 | Executa um experimento da extensão ML/UFG com manifesto e relatório. |
