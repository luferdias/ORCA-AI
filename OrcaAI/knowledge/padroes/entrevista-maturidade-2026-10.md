# Entrevista de maturidade — outubro de 2026

Registro das respostas do engenheiro Luis Fernando às quinze perguntas do A3
(engenheiro civil sênior), feitas em 30/10/2026 no canvas do Maestri. As
respostas chegaram por voz; o texto abaixo é a interpretação, e cada regra
derivada aponta a resposta que a sustenta. Regras marcadas **a confirmar**
dependem de um ponto ambíguo na transcrição.

Estado: cinco blocos respondidos em 30/10/2026. Confirmados em seguida: R-A6 (ordem completa da cascata), R-B1 (regime desonerado) e R-B9 (orçamento enxuto). Confirmado também R-B6 (séries antigas congeladas; novas composições em SRAES-CP). R-E3 e R-E5 confirmados em seguida (FastAPI ou Django, a definir; repositório público). Nenhuma pergunta pendente.

## Bloco A — Como nasce um orçamento na SRA

### Pergunta 1 — gatilho e definição do escopo

**Resposta.** O pedido chega por vistoria ou por demanda no SEI; depende do
caso. Quem bate o martelo sobre o escopo inicial é a chefia.

**Regras derivadas.**

- R-A1. Toda demanda nasce de um dos dois gatilhos: processo SEI ou vistoria.
  O item registra em `projeto.md` qual foi o gatilho e, quando houver, o
  número do processo SEI.
- R-A2. O escopo inicial é decisão da chefia. `01-escopo` guarda o escopo tal
  como aprovado por ela, e qualquer alteração posterior entra em
  `log-decisoes.md` com data e quem decidiu.
- R-A3. `00-entrada` recebe, no mínimo: a demanda ou o despacho do SEI, o
  relatório de vistoria quando ela existiu, e o projeto recebido.

### Pergunta 2 — entradas disponíveis e lacunas

**Resposta.** Em geral o projeto em si vem com a demanda. O que costuma faltar
é o detalhamento de projeto executivo; o orçamento parte do projeto básico, e
é preciso cuidado com o escopo por causa disso.

**Regras derivadas.**

- R-A4. O nível de referência do orçamento é o **projeto básico**. O sistema
  não presume detalhes de executivo: cada detalhe assumido vira uma premissa
  explícita em `01-escopo/premissas.md`, com a justificativa e o impacto no
  quantitativo.
- R-A5. O A3 abre a etapa de escopo listando as lacunas de executivo
  encontradas no projeto recebido. Lacuna sem premissa aprovada bloqueia o
  avanço para `02-quantitativos`.

### Pergunta 3 — ordem de tentativa quando falta código

**Resposta.** Na descrição de serviço procura-se primeiro a base do Espírito
Santo e também o SICRO do Espírito Santo. Se não houver, parte-se para
composição própria, montada com toda a base de conhecimento e todas as tabelas
de referência disponíveis, principalmente os insumos e os materiais
especificados.

**Regras derivadas.**

- R-A6. Cascata de bases para o serviço, confirmada em detalhe pelo
  engenheiro: SINAPI-ES → DER-ES/IOPES → SICRO → São Paulo → Rio de Janeiro →
  Minas Gerais → demais estados, "e assim pelo Brasil todo" → composição
  própria SRAES-CP. O catálogo (`parametros_fixos.cascata_bases`) foi
  reordenado nessa sequência em 30/10/2026.
- R-A7. Composição própria é montada com insumos de bases oficiais (SINAPI
  insumos ES, SICRO-ES, DER-ES) e com os materiais tal como especificados no
  projeto. Pesquisa de mercado entra apenas para o insumo sem base oficial,
  e só após a pausa humana.
- R-A8. A descrição canônica do serviço (A6) deve nascer da base oficial
  escolhida; a composição própria herda a descrição e a unidade dessa base
  quando existe serviço análogo.

## Bloco B — Regras fixas que o sistema deve obedecer

### Pergunta 4 — BDI e regime

**Resposta.** O padrão passa a ser o regime dos memoriais do acervo, e as
fichas devem ser corrigidas para esse regime. Há casos de orçamento "bem
enxuto" em que o tratamento pode ser diferente.

**Confirmação do engenheiro (30/10/2026).** "O regime é desonerado." O
"orçamento bem enxuto" não é um BDI diferente: é um orçamento feito com muita
atenção, mais preciso, em que tanto os códigos quanto as descrições dos
serviços representam o que realmente será executado na obra. Catálogo, spec,
template de composição própria e validador foram corrigidos para "desonerado
por padrão".

**Regras derivadas.**

- R-B1. BDI de serviço padrão: 25,00% pela decomposição dos memoriais
  (AC 3,38; R 0,85; S+G 0,48; DF 0,85; L 6,00; I 10,45 com CPRB 1,8), regime
  desonerado. BDI de fornecimento: 14,02%, taxa fixa.
- R-B2. Fichas, spec e `catalogo.yaml` passam a dizer "desonerado por padrão"
  assim que a leitura de R-B1 for confirmada; `bdi_calculator` já reproduz a
  decomposição.
- R-B3. Qualquer BDI fora do padrão exige memorial próprio em
  `06-documentos/` e registro em `log-decisoes.md`.
- R-B9. Orçamento enxuto: o critério de qualidade é a precisão, não o
  tamanho. Cada código deve ser o que melhor representa o serviço executado,
  e cada descrição deve dizer exatamente o que será feito (liga-se a R-D3,
  descrição adaptada à obra). O A4 verifica isso item a item antes de
  aprovar.

### Pergunta 5 — encargos sociais

**Resposta.** Encargos sociais do SINAPI-ES, regime desonerado.

**Regras derivadas.**

- R-B4. Planilhas e composições usam a tabela SINAPI-ES **desonerada**. O
  normalizador e o `validar_item.py` apontam divergência quando a exportação
  do Orçafascio vier "Não desonerado".
- R-B5. Regime de encargos e regime do BDI são o mesmo em todo o item; a
  mistura é bloqueio (guardrail), não ressalva.

### Pergunta 6 — séries antigas de códigos próprios

**Resposta.** Os itens já aprovados não são congelados; as séries seguem.

**Confirmação do engenheiro (30/10/2026).** "Novas composições em SRAES-CP;
as antigas ficam congeladas." As séries antigas (`SRAES-ELEV-`, `COMP-CAG-`,
`SRA-ES-` e outras) permanecem nos itens já aprovados, sem migração; nenhuma
composição nova as utiliza.

**Regras derivadas.**

- R-B6. Nenhum item aprovado é reescrito por causa de código próprio. O
  guardrail G-01 deixa de emitir ressalva para as séries históricas nos
  itens de 2026-001 a 2026-012.
- R-B7. Para composições novas, o padrão é sempre `SRAES-CP-nnn` (serviço) e
  `SRAES-INS-nnn` (insumo). Em item novo, série antiga é bloqueio G-01, não
  ressalva; a tolerância de R-B6 vale só para os itens até `2026-012`.

### Pergunta 7 — data-base e virada de tabela

**Resposta.** A data-base é a tabela do mês da elaboração. Quando o orçamento
atravessa a virada de tabela ou é revisado dois ou três meses depois, a
revisão adota a tabela vigente e atualiza os preços.

**Regras derivadas.**

- R-B8. Data-base = competência vigente no mês de elaboração, registrada em
  `projeto.md`. Toda revisão posterior ao fechamento rebaseia o orçamento
  para a competência vigente na data da revisão, gera nova versão da
  planilha e registra a mudança em `log-decisoes.md`; o A11 garante o índice
  da competência nova antes da revisão.

## Bloco C — Especificação técnica e documentos

### Pergunta 8 — estrutura da especificação técnica

**Resposta.** Vale o modelo que já foi usado nos orçamentos dos itens 01 a 12,
não um modelo genérico.

**Regras derivadas.**

- R-C1. A estrutura canônica da especificação técnica da SRA é a dos
  documentos do acervo (itens 2026-001 a 2026-012). O A3 deriva dela o
  padrão `knowledge/padroes/especificacao-tecnica-sra.md`, e o A6 só escreve
  nessa estrutura. O modelo genérico de `templates/` passa a ser
  subordinado ao padrão derivado.

### Pergunta 9 — dupla checagem e evidência

**Resposta.** A evidência é a captura de tela. O foco principal do sistema é
a parte dos códigos das tabelas de referência: quem elabora o orçamento, o
Codex, insere o código e verifica se os materiais estão corretos; é o ponto
crítico do orçamento. Os códigos têm de estar 100% alinhados com as
referências, nesta ordem: SINAPI, depois DER, depois SICRO, depois outras
tabelas.

**Regras derivadas.**

- R-C2. Quem insere o código (A7/A8 no Codex) já confere na fonte e anota a
  evidência; quem faz a dupla checagem (A11 no Antigravity) confere de novo,
  de forma independente, código a código, e grava `05-validacoes/`.
- R-C3. Evidência mínima por código: captura de tela da fonte (portal ou
  Orçafascio) com data visível, mais a linha do índice local quando existir.
  O hash do ZIP cobre a competência, não o código.
- R-C4. Código, descrição, unidade e preço divergentes da referência são
  **bloqueio**, não ressalva: o item não avança para `06-documentos`.
- R-C5. O A4 (Claude Code) não refaz a conferência; recebe o relatório do
  A11, verifica a cobertura (todo código tem evidência) e assina.

### Pergunta 10 — documentos do dossiê

**Resposta.** Quatro peças básicas em todo orçamento: planilha orçamentária,
planilha de composições de custo unitário, cálculo do BDI e especificação
técnica. O projeto básico também é anexado ao processo.

**Regras derivadas.**

- R-C6. Obrigatórios em todo item: `03-orcamento/planilha-orcamentaria`,
  `03-orcamento/composicoes`, `06-documentos/memorial-bdi` e
  `06-documentos/especificacao-tecnica`, mais o projeto básico recebido em
  `00-entrada` e anexado ao processo.
- R-C7. Condicionais, gerados só quando a ordem de serviço pedir:
  cronograma físico-financeiro, curva ABC, pesquisa de mercado (IN 65),
  matriz de riscos, ART/RRT, termo de referência. `validar_estrutura.py`
  exige apenas R-C6.

## Bloco D — Orçafascio e aprendizado por demonstração

### Pergunta 11 — sequência no Orçafascio e onde se perde tempo

**Resposta.** A sequência é a descrita: cria a obra, monta a EAP, insere as
composições, aplica o BDI, exporta. Quando o serviço existe na tabela de
referência, entra como está. Quando não bate exatamente, adapta-se a
descrição ao serviço da obra que será executada, mantendo a referência da
tabela; ou faz-se a composição própria, e ela é registrada. Perde-se tempo
fazendo tudo isso à mão. A ideia agora é inverter: os agentes já fazem a
planilha, as composições e o cálculo do BDI, buscando os códigos nos sites
das tabelas (DER e as outras); dentro do Orçafascio só se monta o orçamento,
passo a passo, e é essa montagem que o aprendizado por demonstração vai
observar e automatizar.

**Regras derivadas.**

- R-D1. A fonte do orçamento é a planilha produzida pelos agentes em
  `03-orcamento/` (A7 e A8, com os índices locais e a conferência do A11).
  O Orçafascio não é a origem dos dados; é o instrumento de formalização.
- R-D2. Sequência canônica no Orçafascio, usada como roteiro das trilhas
  LfD: (1) criar a obra com bancos, praça e data-base; (2) montar a EAP
  igual à planilha; (3) inserir as composições pelo código; (4) aplicar o
  BDI do item; (5) exportar sintético e analítico. Cada passo é um evento
  da trilha (`orca_tools.trilhas_lfd`).
- R-D3. Descrição adaptada: é permitido alterar a descrição do serviço no
  Orçafascio para refletir a obra, desde que código, unidade e preço da
  referência sejam mantidos e a planilha normalizada guarde as duas
  descrições, a de referência e a da obra. Divergência de descrição
  **registrada** é ressalva documentada; divergência **não registrada**
  continua bloqueio (refina R-C4).
- R-D4. Serviço sem referência vira composição própria SRAES-CP antes de
  entrar no Orçafascio, nunca uma composição "inventada" lá dentro.
- R-D5. Fechamento do ciclo: a exportação do Orçafascio, normalizada, é
  comparada com a planilha dos agentes. Qualquer diferença de código,
  quantidade, unidade, preço ou BDI é bloqueio até ser explicada em
  `log-decisoes.md`. Esse confronto é a segunda dupla checagem do item.

### Pergunta 12 — autonomia e De acordo

**Resposta.** Depois de observar o engenheiro três vezes, o sistema pode
executar sozinho a montagem no Orçafascio. O que nunca faz sem o De acordo:
concluir o orçamento e levá-lo ao processo. Essa conclusão é do engenheiro.

**Regras derivadas.**

- R-D6. Autonomia por atividade: cada atividade da sequência R-D2 só é
  liberada para execução autônoma do A10 depois de três trilhas LfD
  válidas da mesma atividade, com padrão escrito pelo A3 em
  `knowledge/padroes/` e validado pelo A4. Antes disso, o A10 apenas
  observa e sugere.
- R-D7. Gatilhos de pausa obrigatória no Orçafascio: concluir ou fechar o
  orçamento, gerar os documentos finais, e qualquer ação ligada ao processo
  SEI. O notificador-aprovacao registra o De acordo em `log-decisoes.md`.
- R-D8. O login continua manual em toda sessão (regra fixa do sistema). A
  autonomia de R-D6 começa depois do login e termina antes de R-D7.

## Bloco E — Organização do projeto

### Pergunta 13 — etapas e itens antigos

**Resposta.** As etapas são criadas sob demanda, e cada etapa criada vem com
a estrutura completa. Os itens antigos podem perder as etapas que não se
aplicam.

**Regras derivadas.**

- R-E1. `criar_projeto.py` cria só os arquivos de controle (`projeto.md`,
  `plano-execucao.md`, `log-decisoes.md`) e `00-entrada`. As demais etapas
  nascem por `criar_etapa` quando a ordem de serviço as aciona, já com o
  conteúdo mínimo esperado (um `LEIA-ME.md` dizendo o que a etapa recebe e
  entrega). `_modelo/` guarda o conjunto completo como referência.
- R-E2. Nos itens 2026-001 a 2026-012, as etapas que só tinham `.gitkeep`
  são removidas e `projeto.md` registra "etapas não aplicáveis".
  `validar_estrutura.py` deixa de exigir as oito etapas; exige os três
  arquivos de controle e aceita só etapas do conjunto conhecido.

### Pergunta 14 — modo SRAES e modo UFG

**Resposta.** Dois blocos: o bloco SRAES, que é o padrão, e o bloco UFG
(projeto final do curso de Agentes Inteligentes). O engenheiro citou uma
ferramenta para "a estrutura da apresentação desse projeto"; a transcrição
registrou "Fest P / Fast P" e não deu para identificar com segurança.

**Regras derivadas.**

- R-E3. `OrcaAI/ufg/` reúne o que é acadêmico (`ml/`, `spec/ml_ufg/`,
  entregas). O catálogo declara dois modos: `sraes` (padrão; agentes A1 a
  A11) e `ufg` (A12 e os subagentes de ML; só leitura nas bases e no
  acervo). Ferramenta confirmada em 30/10/2026: **FastAPI ou Django**, a
  definir com o desenvolvimento do modo UFG, para expor o ORCA-AI à
  apresentação e à avaliação do curso; ponto de partida é a API Knowledge de
  `OrcaAI/ufg/spec/api_knowledge.md`.
- R-E4. O modo é escolhido pela ordem de serviço ou pelo comando
  (`/experimento-ml` entra no modo UFG). Nada do modo UFG altera itens,
  catálogo ou padrões do modo SRAES.

### Pergunta 15 — quem mais toca no repositório

**Resposta.** Ninguém mais. Poderia ser privado.

**Regras derivadas.**

- R-E5. Visibilidade: o repositório **permanece público** (decisão do
  engenheiro em 30/10/2026). Motivo: ele continuará atualizando o projeto e
  enviando links aos professores da pós-graduação em Agentes Inteligentes,
  como já fez com o professor Ronaldo. Consequência: nenhuma senha, dado
  pessoal de terceiros ou documento sigiloso pode ser versionado; o hook e a
  CI varrem segredos a cada commit, e a decisão D3 (reescrever o histórico
  por causa da senha antiga do Orçafascio) ganha peso.

Pendentes. As perguntas estão na nota "5 · Entrevista de maturidade" do
fichário "ORCA-AI · Layout" no Maestri e na seção 5 deste layout.
