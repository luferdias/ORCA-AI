# Orca AI — Inteligência Artificial para Engenharia de Custos e Gestão Processual
## Ministério da Gestão e da Inovação em Serviços Públicos (MGI / SRA-ES)

---

## 🏛️ 1. Visão Geral do Projeto Orca AI

O **Orca AI** é a plataforma agêntica unificada de Engenharia de Custos, Planejamento Físico-Financeiro (PERT/CPM), Orçamentação Pública e Instrução Processual Administrativa (SEI / AGU / CGU) da Superintendência Regional de Administração no Espírito Santo (**SRA-ES / MGI**).

O sistema opera com uma esteira de **10 Agentes Especialistas** e **1 Agente Guardião do 5S**, regidos pela **Lei Federal nº 14.133/2021**, o **Decreto nº 7.983/2013**, o **Acórdão TCU nº 2.622/2013** e a **IN SEGES/ME nº 65/2021**.

---

## 📂 2. Estrutura Canônica do Repositório (Metodologia 5S)

Todo o ecossistema ativo está estruturado dentro do núcleo [`OrcaAI/`](file:///Users/luisfdias/Library/CloudStorage/OneDrive-Pessoal/04%20-%20Meus%20Documentos/GitHub/Orcamento_de_Obra/OrcaAI):

```text
Orca_AI/
├── README.md                                  # Este documento de apresentação
├── OrcaAI/                                    # 🧠 NÚCLEO OPERACIONAL DO ORCA AI
│   ├── README.md                              # Documentação executiva completa do sistema
│   ├── spec/                                  # Especificações Técnicas (System, LfD, Market, Guardrails)
│   ├── agents/                                # Fichas Técnicas dos 10 Agentes + Agente 5S
│   ├── skills/                                # Módulos Python de cálculo e automação
│   ├── scripts/                               # Ferramentas e geradores de despachos e planilhas
│   ├── templates/                             # Modelos formais de peças técnicas e SEI
│   ├── workflows/                             # Procedimentos Operacionais Padrão (POPs)
│   ├── docs/                                  # Manuais, Tutoriais e Fluxogramas operacionais
│   ├── bases/                                 # Tabelas oficiais indexadas (SINAPI, IOPES, SICRO)
│   └── projetos/                              # 📁 Acervo de Projetos e Contratações Reais
│       ├── Item 01 - teto_elevadores/         # Recuperação estrutural do teto dos elevadores
│       ├── Item 02 - Limpeza_robotizada_AC/   # Limpeza robotizada de dutos (PMOC)
│       ├── Item 03 - Lavagem_envidracada/     # Lavagem técnica de pele de vidro
│       ├── Item 04 - Junta_dilatacao/         # Tratamento de juntas de dilatação
│       ├── Item 05 - Pintura_grade/           # Pintura e proteção de gradis metálicos
│       ├── Item 06 - insulfilm/               # Película de controle solar
│       ├── Item 07 - Pintura_externa_MGIES/   # Pintura externa predial
│       ├── Item 08 - impermeabilizacao_cisterna/ # Impermeabilização de reservatório
│       ├── Item 09 - limpeza_FV/              # O&M de usina solar fotovoltaica
│       ├── Item 10 - MNT_gerador_subestacao/  # Manutenção de gerador e subestação
│       ├── Item 11 - Impermeabilizacao_Marquise/ # Impermeabilização de marquise
│       ├── Item 12 - Reforma_Suporte_CAG/     # Reforma do suporte dos chillers (CAG)
│       ├── Projetos Básicos/                  # Plantas DWG/PDF e arquivos de engenharia
│       └── _governanca_sei_agu_cgu/           # ⚖️ Pareceres AGU, CGU, Respostas e TJTR
└── .agent/                                    # Configuração Antigravity / Regras Globais
```

---

### Área de projetos de IA

A pasta `Projetos/`, na raiz do repositório, organiza as três áreas abaixo:

```text
Projetos/
├── ORCA-AI/
│   ├── agents/
│   ├── prompts/
│   ├── workflows/
│   ├── shared -> ../Shared-Knowledge/
│   └── outputs/
├── Machine-Learning/
│   ├── models/
│   ├── datasets/
│   ├── notebooks/
│   ├── shared -> ../Shared-Knowledge/
│   └── outputs/
└── Shared-Knowledge/
    ├── docs/
    ├── specs/
    ├── embeddings/
    ├── vector_db/
    └── api/
```

`Projetos/ORCA-AI/` reúne agentes, prompts, fluxos e resultados; `Machine-Learning/` reúne modelos, dados e experimentos; `Shared-Knowledge/` reúne o conhecimento compartilhado. As subpastas começam vazias, com arquivos `.gitkeep` para inclusão no Git. O conteúdo operacional existente continua em `OrcaAI/`.

Os links simbólicos `shared` dão aos dois projetos acesso à mesma pasta `Shared-Knowledge/`.

---

## 🤖 3. Equipe de Agentes Especialistas do Orca AI

1. **Agente 1 (`OrcaMasterOrchestrator`)**: Maestro geral, gestão da árvore de projetos e ciclo LfD.
2. **Agente 2 (`EngenheiroCustosSenior`)**: Estruturação de EAP, quantitativos e métodos construtivos.
3. **Agente 3 (`OrcafascioPilot`)**: Piloto autômato e integração em nuvem com o Orçafascio Web.
4. **Agente 4 (`PesquisadorMercado`)**: Cotações sob a IN 65/2021 na cascata Vitória $\rightarrow$ RJ $\rightarrow$ SP $\rightarrow$ BH.
5. **Agente 5 (`MineradorBasesOficiais`)**: Garimpagem e indexação rápida em milissegundos de SINAPI-ES e IOPES.
6. **Agente 6 (`CompositorCustosUnitarios`)**: Elaboração de CPUs analíticas próprias com produtividades técnicas.
7. **Agente 7 (`EspecialistaEspecificacao`)**: Descritor canônico no padrão SINAPI/EMOP e cadernos de encargos.
8. **Agente 8 (`EngenheiroPlanejamentoEConomico`)**: Planilhas `.xlsx` dinâmicas, BDI (TCU 2.622/2013), PERT/CPM e Curva S.
9. **Agente 9 (`AuditorConformidade`)**: Validador de guardrails (G-01 a G-10), anti-alucinação e consistência legal.
10. **Agente 10 (`EspecialistaInstrucaoProcessualSEI`)**: Instrução processual SEI, respostas a Pareceres AGU/CGU e TJTR.
11. **Agente 5S (`Auditor5S_Organizacao`)**: Guardião da metodologia 5S, limpeza contínua e integridade de pastas.

## 4. Aplicação acadêmica de Machine Learning — UFG

A primeira etapa, **regressão**, está implementada no [módulo Python para VS Code](OrcaAI/ml/README.md). O [arquivo principal](OrcaAI/ml/executar_regressao.py) executa SINAPI-ES e DER-ES/IOPES separadamente, com datasets reais, avaliação temporal e comparação com o último custo conhecido. Classificação e agrupamento seguem como próximas etapas.

A [proposta atual do trabalho](OrcaAI/spec/ml_ufg/proposta_projeto_ml_es.md) define Regressão Linear, Random Forest e K-Means, a partir dos materiais da disciplina. Prevê execução em Python no VS Code, primeiro no SINAPI-ES e depois no DER-ES/IOPES, com comparação dos resultados. Aprendizado por reforço fica para uma evolução futura, conforme decisão do engenheiro Luis Fernando.

A [estrutura agêntica proposta para ML/UFG](OrcaAI/spec/ml_ufg/README.md) mantém o orquestrador central, aproveita os especialistas e as skills existentes e define uma extensão acadêmica com cinco subagentes de apoio. O pacote inclui o organograma, a seleção de cinco skills externas, os critérios de dados e avaliação e o contrato inicial da API Knowledge.

Os 12 projetos de orçamento permanecem em `OrcaAI/projetos/`. A API Knowledge e os novos papéis agênticos continuam especificados para etapas posteriores; as skills externas selecionadas ainda não foram instaladas.

A [auditoria de bases oficiais de 27/09/2026](OrcaAI/docs/auditoria_bases_referenciais_2026-09-27.md) registra competências localizadas, arquivos amostrados e pendências de acesso. O [catálogo de fontes](OrcaAI/bases/catalogo_fontes_referenciais.json) e o [protocolo de atualização por projeto](OrcaAI/spec/ml_ufg/bases_servicos_e_atualizacao.md) orientam a pesquisa com prioridade no Espírito Santo.

O [relatório preliminar de viabilidade](OrcaAI/docs/viabilidade_ml_dados_estruturados_es_2026-09-27.md) registra a análise anterior à leitura das aulas. A seleção de modelos e o escopo vigente estão na proposta atual.
