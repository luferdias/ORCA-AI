# Entrevista de maturidade — outubro de 2026

Registro das respostas do engenheiro Luis Fernando às quinze perguntas do A3
(engenheiro civil sênior), feitas em 30/10/2026 no canvas do Maestri. As
respostas chegaram por voz; o texto abaixo é a interpretação, e cada regra
derivada aponta a resposta que a sustenta. Regras marcadas **a confirmar**
dependem de um ponto ambíguo na transcrição.

Estado: blocos A e B respondidos; blocos C a E pendentes.

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

- R-A6. Cascata de bases para o serviço: SINAPI-ES → SICRO-ES → composição
  própria SRAES-CP. **A confirmar:** a posição do DER-ES/IOPES nessa cascata;
  o catálogo atual o coloca entre o SINAPI-ES e o SICRO.
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

**Leitura adotada e ponto a confirmar.** A transcrição traz "padrão mesmo não
desonerado" e, logo em seguida, "encargos sociais do Espírito Santo
desonerado". Os treze memoriais fecham 25,00% só com a CPRB de 1,8%, o que é
regime desonerado, e encargos desonerados exigem a CPRB no BDI (Acórdão
2.622/2013-TCU-Plenário). A leitura coerente é **regime desonerado como
padrão**, corrigindo as fichas e a spec que dizem "não desonerado". **A
confirmar** com o engenheiro antes de alterar o catálogo. Também a confirmar o
que muda no "orçamento bem enxuto".

**Regras derivadas.**

- R-B1. BDI de serviço padrão: 25,00% pela decomposição dos memoriais
  (AC 3,38; R 0,85; S+G 0,48; DF 0,85; L 6,00; I 10,45 com CPRB 1,8), regime
  desonerado. BDI de fornecimento: 14,02%, taxa fixa.
- R-B2. Fichas, spec e `catalogo.yaml` passam a dizer "desonerado por padrão"
  assim que a leitura de R-B1 for confirmada; `bdi_calculator` já reproduz a
  decomposição.
- R-B3. Qualquer BDI fora do padrão exige memorial próprio em
  `06-documentos/` e registro em `log-decisoes.md`.

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

**Leitura adotada e ponto a confirmar.** Duas leituras possíveis: (a) as
séries antigas (`SRAES-ELEV-`, `COMP-CAG-`, `SRA-ES-`) continuam válidas e em
uso, sem migração; (b) elas passam a seguir o padrão `SRAES-CP-nnn` daqui em
diante, sem reescrever os itens aprovados. **A confirmar.**

**Regras derivadas.**

- R-B6. Nenhum item aprovado é reescrito por causa de código próprio. O
  guardrail G-01 deixa de emitir ressalva para as séries históricas nos
  itens de 2026-001 a 2026-012.
- R-B7. Para composições novas, o padrão é `SRAES-CP-nnn` (serviço) e
  `SRAES-INS-nnn` (insumo), salvo decisão contrária na confirmação de R-B6.

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

## Blocos C a E

Pendentes. As perguntas estão na nota "5 · Entrevista de maturidade" do
fichário "ORCA-AI · Layout" no Maestri e na seção 5 deste layout.
