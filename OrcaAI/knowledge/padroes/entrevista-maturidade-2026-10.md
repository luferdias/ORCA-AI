# Entrevista de maturidade — outubro de 2026

Registro das respostas do engenheiro Luis Fernando às quinze perguntas do A3
(engenheiro civil sênior), feitas em 30/10/2026 no canvas do Maestri. As
respostas chegaram por voz; o texto abaixo é a interpretação, e cada regra
derivada aponta a resposta que a sustenta. Regras marcadas **a confirmar**
dependem de um ponto ambíguo na transcrição.

Estado: bloco A respondido; blocos B a E pendentes.

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

## Blocos B a E

Pendentes. As perguntas estão na nota "5 · Entrevista de maturidade" do
fichário "ORCA-AI · Layout" no Maestri e na seção 5 deste layout.
