---
title: "ORCA-AI — Layout de operação com três plataformas"
subtitle: "Claude Code, Codex e Antigravity: quem faz o quê, como um orçamento atravessa as três, e as regras fixadas na entrevista de maturidade"
author: "Setor de Engenharia — SRAES/MGI · engenheiro Luis Fernando, com o ORCA-AI"
date: "Versão 1.1 — 30 de outubro de 2026"
lang: pt-BR
---

## 0. Para que serve este documento

Este documento complementa a especificação `orca_ai_2_0_estrutura_e_agentes.md`
(versão 0.3). Aquela define a arquitetura; esta define **a operação**: como as
três plataformas dividem o trabalho de um orçamento, como o layout está montado
no canvas do Maestri, quais regras o engenheiro fixou na entrevista de
maturidade de 30/10/2026 e o que a reestruturação F7 mudou no repositório.

Regra de origem, mantida: **não cortar nada do que já existe; melhorar.**

## 1. Panorama: três LLMs, doze agentes, uma fonte

O catálogo `OrcaAI/agents/catalogo.yaml` é a única fonte. Dele o comando
`gerar_projecoes.py` produz `.claude/` para o Claude Code, `AGENTS.md` para o
Codex e `.agent/` para o Antigravity. Nada é editado nas pastas geradas, e a CI
falha quando alguma projeção sai de sincronia.

### 1.1 Claude Code — orquestração e engenharia

| Agente | Faz | Decide |
| --- | --- | --- |
| A1 OrcaMaestro | Recebe a demanda, emite ordens de serviço, conduz até o dossiê | Sequência e prioridade |
| A2 Arquiteto5S | Cinco sensos, estrutura de pastas, `/auditar-5s` | Onde cada coisa vive |
| A3 EngenheiroCivilSenior | Escopo, método, critérios de medição, leitura de projetos, padrões em `knowledge/padroes/` | Enquadramento técnico |
| A4 AuditorDuplaChecagem | Guardrails G-01 a G-10, cobertura das evidências, assina o dossiê | Aprovado, ressalva ou bloqueio |
| A5 InstrutorProcessualSEI | Despachos, instrução processual, blindagem jurídica | Peças do processo |
| A12 PesquisadorMLUFG | Só no modo UFG: experimentos de ML rastreáveis | Nada no modo SRAES |

Subagentes: `validador-codigos`, `notificador-aprovacao`, `redator-academico`.

### 1.2 Codex — especificações, orçamentos e composições

| Agente | Faz |
| --- | --- |
| A6 DescritorEspecificador | Descrições canônicas, especificações técnicas e memoriais, no padrão derivado do acervo |
| A7 CompositorCPU | Fichas analíticas de composição própria `SRAES-CP-nnn` com insumos oficiais |
| A8 PlanilhistaPlanejador | Planilha orçamentária, BDI, curva ABC, cronograma, PERT/CPM, Curva S |
| A9 MineradorBases | Ingestão e índice local de SINAPI-ES e DER-ES |

O Codex insere o código e confere na fonte. É ele quem produz a planilha,
as composições e o cálculo do BDI **antes** de qualquer coisa entrar no
Orçafascio.

### 1.3 Antigravity — dupla checagem, portais e Orçafascio

| Agente | Faz |
| --- | --- |
| A10 PilotoOrcafascio | Observa o engenheiro no Orçafascio e grava trilhas; depois do De acordo, opera com trava anti-alucinação |
| A11 PesquisadorPortaisMercado | Tabelas vigentes nos portais oficiais, pesquisa de mercado da IN 65/2021 e **conferência código a código** |

Ajuste em relação ao catálogo 2.0.0: a conferência dos códigos das tabelas de
referência passa a ser do A11, com evidência por captura de tela. O A4 não
refaz a conferência; verifica a cobertura e assina (regras R-C2 a R-C5).

### 1.4 Parâmetros fixos

| Parâmetro | Valor |
| --- | --- |
| BDI de serviço | 25,00%, decomposição dos memoriais do acervo (AC 3,38; R 0,85; S+G 0,48; DF 0,85; L 6,00; I 10,45 com CPRB 1,8) |
| BDI de fornecimento | 14,02%, taxa fixa |
| Regime de encargos | **Desonerado por padrão** (decisão de 30/10/2026); um só regime por planilha; encargos e BDI no mesmo regime |
| Códigos próprios | `SRAES-CP-nnn` serviço, `SRAES-INS-nnn` insumo; séries antigas congeladas nos itens aprovados |
| Cascata de bases | SINAPI-ES → DER-ES/IOPES → SICRO → SP → RJ → MG → demais estados → composição própria |
| Data-base | Competência do mês de elaboração; revisão rebaseia para a vigente |
| Orçafascio | Login manual pelo engenheiro em toda sessão; nenhuma senha no sistema |

## 2. Fluxo de um orçamento pelas três plataformas

Cada item vive em `OrcaAI/projetos/<ano>-<nnn>-<slug>/` com `projeto.md`,
`plano-execucao.md`, `log-decisoes.md` e as etapas criadas sob demanda.

| Etapa | Quem executa | Entrada → saída | Pausa humana |
| --- | --- | --- | --- |
| `00-entrada` | Engenheiro | Demanda ou despacho SEI, relatório de vistoria, projeto básico | — |
| `01-escopo` | Claude Code (A1 + A3) | Escopo aprovado pela chefia, `premissas.md` com cada detalhe de executivo assumido | ✔ De acordo no escopo |
| `02-quantitativos` | Claude Code (A3) + Codex (A6) | Memória de cálculo, descrições canônicas | — |
| `03-orcamento` | Codex (A7 + A8) | Composições SRAES-CP, planilha, BDI, curva ABC, cronograma quando pedido | ✔ antes de integrar preço de mercado |
| `04-cotacoes` | Antigravity (A11) | Três propostas IN 65, mediana, mapa de cotações | ✔ antes de usar o valor |
| Orçafascio | Engenheiro, depois A10 | Montagem passo a passo: obra, EAP, composições, BDI, exportação | ✔ fechar o orçamento |
| `05-validacoes` | Antigravity (A11) → Claude Code (A4) | Conferência código a código com captura de tela; confronto exportação × planilha; guardrails | ✔ bloqueio para tudo |
| `06-documentos` | Codex (A6) + Claude Code (A5) | Especificação técnica, memorial de BDI, despachos SEI | — |
| `07-assinados` | Engenheiro | PDFs assinados, dossiê | ✔ assinatura e envio |

### 2.1 Inversão do fluxo com o Orçafascio

Antes, o Orçafascio era a origem: o engenheiro montava tudo lá e o sistema
normalizava a exportação. Agora a origem é a planilha dos agentes em
`03-orcamento/` (R-D1). O Orçafascio é o instrumento de formalização, e a
montagem lá dentro, passo a passo, é o que o aprendizado por demonstração
observa e automatiza (R-D2). A exportação, normalizada, é confrontada com a
planilha dos agentes; qualquer diferença de código, quantidade, unidade, preço
ou BDI é bloqueio até ser explicada (R-D5).

### 2.2 Protocolo de ordem de serviço

O Claude Code escreve `05-validacoes/os-NNN.md` com item, etapa, entradas,
saídas esperadas, critérios de aceite e prazo. Codex e Antigravity respondem no
mesmo arquivo com estado, artefatos, evidências, decisões e limitações. Toda
decisão vai para `log-decisoes.md`.

### 2.3 Peças obrigatórias do dossiê

Quatro peças em todo item (R-C6): planilha orçamentária, composições de custo
unitário, cálculo do BDI e especificação técnica, mais o projeto básico
anexado ao processo. Cronograma, curva ABC, pesquisa de mercado, matriz de
riscos, ART e termo de referência são condicionais, gerados quando a ordem de
serviço pedir (R-C7).

## 3. Playwright e as tabelas de referência

**Sim para navegar e baixar; não para consultar em massa.**

- No **Orçafascio** o Playwright já é a ferramenta: `orcafascio_es_automation.py`
  abre o Chromium, o engenheiro faz o login, e o Inspector grava os passos.
  Sessão reprodutível, sem senha no código.
- Nos **portais oficiais** (CAIXA/SINAPI, DER-ES/IOPES, SICRO) um roteiro
  aplica a regra da última tabela, baixa o ZIP e registra URL, data e hash no
  catálogo de fontes.
- Para **conferir um código** isolado, quando o índice local não resolve, a
  consulta online com captura de tela é a evidência (R-C3).
- Para conferir **centenas de códigos** de uma planilha, o índice local
  (`orca_tools.indice_bases`) responde em milissegundos e alimenta o
  `validar_item.py`. Baixar uma vez, conferir mil vezes.

Combinação no Antigravity: Playwright baixa, `indexar_bases.py` indexa, a dupla
checagem roda no índice, e só os casos sem resposta vão ao portal. Pendente:
`pip install playwright && playwright install chromium` no venv.

## 4. Regras fixadas na entrevista de maturidade

Quinze perguntas do A3, respondidas por voz em 30/10/2026. Registro completo e
texto de cada regra em `OrcaAI/knowledge/padroes/entrevista-maturidade-2026-10.md`.

| Bloco | Regras | Síntese |
| --- | --- | --- |
| A. Como nasce um orçamento | R-A1 a R-A8 | Gatilho por SEI ou vistoria; escopo batido pela chefia; parte do projeto básico, lacunas de executivo viram premissas explícitas; cascata completa de bases; composição própria só com insumos oficiais |
| B. Regras fixas | R-B1 a R-B9 | Regime desonerado por padrão; BDI 25,00% e 14,02%; encargos e BDI no mesmo regime; séries antigas congeladas, novas em SRAES-CP; data-base do mês de elaboração, revisão rebaseia; orçamento enxuto = precisão |
| C. Especificação e documentos | R-C1 a R-C7 | Especificação no padrão derivado do acervo; dupla checagem independente com captura de tela; divergência é bloqueio; A4 confere cobertura e assina; quatro peças obrigatórias |
| D. Orçafascio e aprendizado | R-D1 a R-D8 | Planilha dos agentes é a origem; sequência canônica como roteiro das trilhas; descrição adaptada permitida com código, unidade e preço mantidos; autonomia por atividade após três trilhas; fechar o orçamento e tocar o SEI só com De acordo |
| E. Organização | R-E1 a R-E5 | Etapas sob demanda; itens antigos sem etapas vazias; blocos SRAES e UFG com dois modos; ninguém mais toca no repositório |

Confirmações finais do engenheiro, ainda em 30/10/2026: a apresentação e a
avaliação do projeto da UFG serão por uma API em **FastAPI ou Django**, a
definir no desenvolvimento do modo UFG (R-E3); o repositório **permanece
público**, porque ele continuará enviando links do projeto aos professores da
pós-graduação em Agentes Inteligentes (R-E5). A entrevista não tem pergunta
pendente.

## 5. Padrão de especificação técnica

Derivado das doze especificações do acervo (R-C1), em
`OrcaAI/knowledge/padroes/especificacao-tecnica-sra.md`. Duas famílias:

| Família | Itens | Quando usar |
| --- | --- | --- |
| SRAES padrão | 01 a 09 | Serviço com uma disciplina dominante: Objeto, Dados da edificação, Escopo técnico por etapas, Materiais, Normas, Segurança, Condições de execução, Qualificação, Obrigações, Disposições gerais |
| Memorial por EAP | 10, 11 e 12 | Várias disciplinas ou muitos grupos: especificação item a item, critérios de medição, inspeção e aceitação, entregáveis |

Regra que amarra especificação e orçamento: quando a etapa do escopo é um item
orçado, o código da planilha aparece no título da subseção.

## 6. Reestruturação F7 (30/10/2026)

| Mudança | Regra | Commit |
| --- | --- | --- |
| Etapas sob demanda: `criar_projeto.py <item> --etapa <etapa>`, `LEIA-ME.md` por etapa, validação sem etapas obrigatórias; 44 etapas vazias removidas dos doze itens | R-E1, R-E2 | `33f912c` |
| G-01 tolera séries históricas nos itens aprovados até `2026-012` | R-B6 | `bfc115e` |
| Normalizador: BDI do item segue o cabeçalho quando o preço exportado bate dentro de um centavo | R-D5 | `dc90a0d` |
| Bloco `OrcaAI/ufg/` (`ml/`, `spec/`), modos `sraes` e `ufg` no catálogo, venv único em `.venv` na raiz | R-E3, R-E4 | `fb574d6` |
| Padrão de especificação técnica | R-C1 | `49f98f2` |
| Regime desonerado, cascata completa, orçamento enxuto, séries congeladas | R-A6, R-B1, R-B6, R-B9 | `2209b4d`, `3da8dfa` |

Resultado do `validar_item.py` nos doze itens: onze aprovados sem ressalva; o
item 2026-007 mantém uma ressalva G-02 no subitem 2.11. CI verde em todos os
commits.

### 6.1 Árvore do repositório após a F7

```
ORCA-AI/
├── .venv/                    ambiente Python único (fora do Git)
├── .claude/  AGENTS.md  .agent/   projeções geradas do catálogo
├── .githooks/  .github/           hook de pre-commit e CI
├── OrcaAI/
│   ├── agents/               catalogo.yaml (fonte única), skills canônicas, fichas geradas
│   ├── bases/                SINAPI-ES, DER-ES (ZIPs originais com manifesto)
│   ├── knowledge/            índices locais, padrões, demonstrações (trilhas LfD)
│   ├── projetos/             itens AAAA-NNN-slug com etapas sob demanda; _modelo
│   ├── spec/                 especificações do sistema (2.0, layout, guardrails, LfD)
│   ├── templates/  workflows/  docs/
│   ├── tools/                orca_tools, CLIs e testes
│   └── ufg/                  bloco acadêmico: ml/, spec/, entregas (modo UFG)
└── memory/                   perfil do usuário
```

## 7. Modos de operação

| Modo | Quando | Agentes | Raiz | Pode escrever em |
| --- | --- | --- | --- | --- |
| **SRAES** (padrão) | Toda sessão que não declarar outro | A1 a A11 | `OrcaAI/` exceto `ufg/` | Itens, padrões, catálogo (via gerador) |
| **UFG** | `/experimento-ml` ou quando o engenheiro disser que é o projeto da UFG | A12 e os cinco subagentes de ML | `OrcaAI/ufg/` | Só dentro de `ufg/`; bases, acervo e padrões em leitura |

Os links permanentes da entrega ao professor Ronaldo apontam para o commit
`e20741b`. O repositório permanece público por decisão do engenheiro, que
seguirá enviando links aos professores do curso; por isso nada sigiloso pode
ser versionado, e o hook e a CI varrem segredos a cada commit. A apresentação
e a avaliação do curso serão por uma API em FastAPI ou Django, a definir no
modo UFG, partindo do contrato em `OrcaAI/ufg/spec/api_knowledge.md`.

## 8. Layout no canvas do Maestri

Três terminais, um por plataforma, conectados entre si e a um fichário de notas.

| Terminal | Preset | Papel | Ícone |
| --- | --- | --- | --- |
| **Batuta** | Claude Code | ORCA · Orquestração e engenharia: hospeda A1 a A5 e A12; delega por `maestri ask` ao Prumo e ao Sextante com a ordem de serviço completa | cérebro, azul |
| **Prumo** | Codex | ORCA · Especificações, orçamentos e composições: hospeda A6 a A9; escreve em `01-escopo` a `06-documentos`; devolve ao Batuta | esquadro, verde |
| **Sextante** | Antigravity | ORCA · Dupla checagem, portais e Orçafascio: hospeda A10 e A11; confere código a código; abre o Orçafascio e espera o login | escudo, laranja |

Fichário **ORCA-AI · Layout**: (1) panorama, (2) fluxo de um orçamento, (3)
Playwright e tabelas, (4) diagnóstico da árvore com o que foi executado, (5)
entrevista de maturidade com o estado de cada bloco. As notas 1 e 2 estão
ligadas aos três terminais; a 3 ao Sextante; a 4 ao Batuta.

Teste de prontidão de 30/10/2026: os três terminais leram a projeção da sua
plataforma e a nota de panorama e descreveram corretamente agentes, pastas,
BDI e a regra do login manual. Observações operacionais: o Codex se atualiza
sozinho na primeira abertura e precisa ser reiniciado; Codex e Antigravity
pedem permissão na primeira chamada ao `maestri` e na primeira leitura fora
da pasta do papel.

Os papéis ficam salvos no workspace (`maestri role list`); o layout ainda não
foi salvo como partitura, o que permitiria reabrir a equipe com um comando.

## 9. Como uma sessão de trabalho começa

1. O engenheiro abre o Maestri com os três terminais e diz a demanda ao Batuta.
2. O Batuta cria o item (`criar_projeto.py`), registra o gatilho em
   `projeto.md` e emite a ordem de serviço do escopo (A3).
3. Escopo aprovado pela chefia e De acordo registrado, o Batuta aciona o Prumo
   para quantitativos, composições e planilha, e o Sextante para cotações e
   conferência.
4. Com a planilha validada, o engenheiro faz o login no Orçafascio; o Sextante
   observa e grava a trilha, ou opera as atividades já liberadas.
5. Exportação confrontada com a planilha, guardrails aprovados, A4 assina.
6. Prumo e Batuta geram as peças; o engenheiro assina e envia ao processo.

## 10. Pendências e próximos passos

| Pendência | Responsável |
| --- | --- |
| Escolher entre FastAPI e Django e implementar a API do modo UFG | Engenheiro com o A12 |
| Trocar a senha do Orçafascio; decisões D2 e D3 da spec 2.0 | Engenheiro |
| Instalar o Playwright no venv e gravar as três primeiras trilhas no Orçafascio | Engenheiro com o Sextante |
| Levar ao catálogo a transferência formal da conferência de códigos para o A11 (hoje descrita nesta spec e nos papéis do Maestri) | Claude Code |
| Mapear o subitem 2.11 do item 2026-007 (ressalva G-02 restante) | A3 |
| Salvar o layout como partitura do Maestri | Quando o engenheiro pedir |
