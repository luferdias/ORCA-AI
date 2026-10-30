---
name: pesquisa-mercado-vitoria
description: Estratégia de automação de pesquisa de preços no comércio local de Vitória, Serra e Vila Velha (ES) para complementar insumos e serviços não catalogados nas tabelas oficiais.
---
# Pesquisa Dinâmica de Preços — Mercado Grande Vitória/ES

## 1. Contexto Estratégico
Muitas vezes, insumos muito específicos e esquadrias de vidros temperados, elevadores ou acabamentos de luxo não constam perfeitamente nos cadernos técnicos do **IOPES**, **SINAPI** ou **SICRO**. Para compor orçamentos exatos sem sobressaltos e mitigar denúncia no controle de contas para a **Região Metropolitana de Vitória (ES)**, precisamos recorrer à pesquisa de mercado focada.

## 2. Protocolo de Pesquisa Local
Ao detectar falta nas bases oficiais ou por solicitação do usuário, não estime nem invente preços. Adote a matriz abaixo:

1. **Especificação Restrita:** Refine o insumo antes da busca. Exemplo: De "Porcelanato" refine para "Porcelanato Esmaltado 60x60 tipo A para tráfego intenso" ou equivalente em lojas da região.
2. **Ferramenta de Ação:** Use a tool `search_web` com os argumentos contendo "Vitória ES", "Serra ES" ou "Vila Velha ES" combinado com as grandes distribuidoras/prestadoras civis do mercado capixaba.
   - Pinceis comerciais locais possíveis: *C&C, Balaroti, Sipolatti, Viminas (Vidros), entre os atacadões de materiais que atuam em Viana, CIVIT e Grande Vitória*.
3. **A Regra Inviolável de 3 Cotações:** Base das regras licitatórias (TCU/TCE). Forneça uma tabela listando as fontes originais e defina o preço de acordo com a **média aritmética ou menor preço referenciado**.
4. **Fallback Interestadual (RJ, SP, MG):** Caso a pesquisa focada exclusivamente na região de Vitória/ES não retorne 3 cotações online válidas, **amplie imediatamente a pesquisa para estados limítrofes ou de forte influência comercial como Rio de Janeiro (RJ), São Paulo (SP) e Minas Gerais (MG)**. É muito provável que você encontre referências de preços robustas nestas praças que balizarão o nosso custo, bastando apenas prever depois um acréscimo logístico/frete se for envio de material.

## 3. Formato de Extração e Anexo de Pesquisa
Insira no orçamento final este bloco demonstrando idoneidade de onde saiu o valor base da Composição Própria (CP):

> ⚠️ **PARADA OBRIGATÓRIA:** Assim que este relatório for produzido virtualmente (antes mesmo de transcrever para o software definitivo), você deverá usar a ferramenta `notify_user` e requerer aprovação do Eng. do MGI de forma ativa informando que um insumo/serviço teve Fallback ou Pesquisa Externa.

```text
### RELATÓRIO PÚBLICO DE COTAÇÃO EXTERNA DE INSUMO
**Preço Adotado na CP/Data-base atual (Cuidado com Códigos: Sempre Padrão SRAES)**

| CÓD EXCLUSIVO         | DESCRIÇÃO INSUMO      | FONTE ONLINE 1         | FONTE ONLINE 2         | FONTE ONLINE 3         | PREÇO BASE UTILIZADO|
|-----------------------|-----------------------|------------------------|------------------------|------------------------|---------------------|
| SRAES-CP-001 ou INS-1 | [Insumo pesquisado]   | www.loja-1-vitoria.com | www.loja-2-vitoria.com | www.loja-3-serr-es.com | R$ XX,XX (Média)    |

*Observação Técnica*: Fretes e taxas locais para locomoção da Grande Vitória (ex: descarregar no centro de Vitória ou Guarapari) devem estar alertados como custo à parte se a Cotação tratar de preço "retira balcão".
```
