# OrcaAI - Inteligência Artificial para Orçamento de Obras Públicas
## MGI / SRA-ES - Superintendência Regional de Administração no Espírito Santo

---

## 📋 1. Visão Geral

O **OrcaAI** é uma plataforma modular de agentes inteligentes especializada em Engenharia de Custos, Orçamentação Pública e Instrução Processual de Obras e Serviços de Engenharia conforme a **Lei Federal nº 14.133/2021**, o **Decreto Federal nº 7.983/2013**, o **Acórdão TCU nº 2.622/2013** e a **IN SEGES/ME nº 65/2021**.

O sistema foi desenhado sob o paradigma de **Aprendizado por Demonstração (*Learning from Demonstration - LfD*)**: o engenheiro opera a plataforma [Orçafascio](https://app.orcafascio.com/), enquanto o OrcaAI aprende e assimila as escolhas técnicas, avançando subsequentemente para a **operação autônoma supervisionada**, com **zero alucinações de códigos e preços**.

```mermaid
graph TD
    Demanda([Demanda de Engenharia / Termo de Abertura SEI]) --> A1[Agente 1: OrcaMasterOrchestrator]
    
    subgraph "Engenharia de Custos, Bases & Modelagem"
        A1 --> A2[Agente 2: EngenheiroCustosSenior]
        A1 --> A3[Agente 3: OrcafascioPilot]
        A1 --> A4[Agente 4: PesquisadorMercado]
        A1 --> A5[Agente 5: MineradorBasesOficiais]
        A1 --> A6[Agente 6: CompositorCustosUnitarios]
    end

    subgraph "Especificação, Planejamento & Finanças"
        A1 --> A7[Agente 7: EspecialistaEspecificacao]
        A1 --> A8[Agente 8: EngenheiroPlanejamentoEConomico]
    end

    subgraph "Instrução Processual & Governança Jurídica"
        A1 --> A10[Agente 10: EspecialistaInstrucaoProcessualSEI]
    end

    subgraph "Auditoria, Guardrails & Dossiê"
        A2 & A3 & A4 & A5 & A6 & A7 & A8 & A10 --> A9[Agente 9: AuditorConformidade]
        A9 --> Dossie([Dossiê Completo de Contratação Pública])
    end
```

---

## 🤖 2. Matriz dos 10 Agentes Especialistas do OrcaAI

| Agente | Identificador | Função Primária | Entregáveis Gerados |
| :--- | :--- | :--- | :--- |
| **Agente 1** | `OrcaMasterOrchestrator` | Gestão mestre da árvore de projetos, triagem de demandas e ciclo LfD. | Plano de execução, ata de decisões e relatório executivo. |
| **Agente 2** | `EngenheiroCustosSenior` | Estruturação da EAP, levantamento de quantitativos e método construtivo. | EAP detalhada e pré-planilha referencial de engenharia. |
| **Agente 3** | `OrcafascioPilot` | Captura de ações humanas (LfD) e navegação autônoma no Orçafascio Web. | Sincronização e exportação de orçamentos no Orçafascio. |
| **Agente 4** | `PesquisadorMercado` | Pesquisa de preços escalonada: **Vitória $\rightarrow$ RJ $\rightarrow$ SP $\rightarrow$ BH** (IN 65/2021). | Mapa de cotações, 3 propostas válidas e preço de referência. |
| **Agente 5** | `MineradorBasesOficiais` | Mineração e indexação em alta velocidade de tabelas oficiais (SINAPI, IOPES, etc.). | Banco indexado local, consulta em ms e atualização mensal. |
| **Agente 6** | `CompositorCustosUnitarios` | Criação analítica de CPUs Próprias com produtividade técnica e insumos oficiais. | Ficha analítica de CPU (`SRAES-CP-XXX`) com insumos SINAPI/IOPES. |
| **Agente 7** | `EspecialistaEspecificacao` | Descrição técnica padronizada (padrão SINAPI/EMOP), especificações e TRs. | Descrição padronizada para CPU, Caderno Técnico e Memorial. |
| **Agente 8** | `EngenheiroPlanejamentoEConomico` | Planilhas `.xlsx` dinâmicas, BDI (TCU 2.622/2013), PERT/CPM, Curva S e Curva ABC. | Arquivo `.xlsx` com EAP sequenciada, BDI justificado e Gantt responsivo. |
| **Agente 9** | `AuditorConformidade` | Validação de guardrails (G-01 a G-10), rastreabilidade e anti-alucinação. | Relatório de Conformidade Legal e Auditoria de Códigos. |
| **Agente 10** | `EspecialistaInstrucaoProcessualSEI` | Instrução processual SEI, respostas a Pareceres AGU/CGU, TJTR e notas legais. | Notas Técnicas de resposta à AGU, Despachos SEI e TJTRs. |
| **Agente 5S** | `Auditor5S_Organizacao` | Guardião da metodologia 5S, governança estrutural e higienização contínua. | Relatório de Conformidade 5S e auditoria de diretórios. |

---

## 📁 3. Estrutura do Diretório `OrcaAI/`

```text
OrcaAI/
├── README.md                                  # Este documento de visão geral
├── spec/                                      # Especificações Técnicas e Diretrizes Oficiais
│   ├── orca_ai_system_spec.md                 # Spec Geral do Sistema OrcaAI
│   ├── lfd_learning_protocol.md               # Protocolo de Aprendizado por Demonstração (LfD)
│   ├── market_research_protocol.md            # Estratégia de Pesquisa de Mercado Escalonada
│   └── guardrails_validation_spec.md          # Validadores G-01 a G-10
├── agents/                                    # Catálogo único e projeções
│   ├── catalogo.yaml                          # FONTE ÚNICA: agentes, subagentes, skills, workflows
│   ├── fichas/                                # Fichas 2.0 geradas (A1 a A12) + historico/ (AGENTE_01 a 10 e 5S)
│   └── skills/                                # 33 skills canônicas (copiadas para .claude/skills e .agent/skills)
├── tools/                                     # Pacote Python orca_tools, CLIs e testes
│   ├── orca_tools/                            # bdi_calculator, cronograma_generator, excel_budget_generator, code_guardrail_validator, estrutura_projeto
│   ├── cli/                                   # criar_projeto, validar_estrutura, gerar_indice_dossie, orcafascio_es_automation
│   └── tests/
├── templates/                                 # Modelos Formais de Peças Técnicas
│   ├── modelo_especificacao_tecnica.md
│   ├── modelo_justificativa_bdi.md
│   ├── modelo_composicao_propria_cpu.md
│   └── modelo_pesquisa_mercado.md
├── workflows/                                 # Procedimentos Operacionais Padrão (POP)
│   ├── pipeline_aprendizado_orcafascio.md
│   └── pipeline_geracao_dossie_completo.md
└── projetos/                                  # 📁 Acervo de Projetos e Demandas Orçamentárias
    ├── 2026-001-teto-elevadores/             # Recuperação do teto da casa de máquinas
    ├── 2026-002-limpeza-robotizada-ac/       # Limpeza robotizada de dutos e PMOC
    ├── 2026-003-lavagem-fachada-envidracada/         # Lavagem técnica de pele de vidro/fachada
    ├── 2026-004-juntas-dilatacao/             # Tratamento e calafetação de juntas
    ├── 2026-005-pintura-grades/               # Pintura e proteção anticorrosiva de gradis
    ├── 2026-006-pelicula-controle-solar/                   # Aplicação de película de controle solar
    ├── 2026-007-pintura-externa/       # Pintura predial externa
    ├── 2026-008-impermeabilizacao-cisterna/  # Impermeabilização de reservatório inferior
    ├── 2026-009-limpeza-fotovoltaica/                  # O&M e limpeza de módulos fotovoltaicos
    ├── 2026-010-manutencao-gerador-subestacao/      # Manutenção de gerador e subestação abrigada
    ├── 2026-011-impermeabilizacao-marquise/  # Impermeabilização da marquise frontal
    ├── 2026-012-reforma-suporte-cag/         # Reforma estrutural do suporte dos chillers
    ├── _projetos_basicos/                     # Plantas DWG/PDF e arquivos de engenharia
    ├── _modelo/                               # Modelo de item (00-entrada a 07-assinados)
    └── _governanca_sei_agu_cgu/               # Acervo Processual, Pareceres AGU, CGU e TJTR
```
