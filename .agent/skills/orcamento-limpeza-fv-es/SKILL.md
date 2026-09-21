---
name: orcamento-limpeza-fv-es
description: >
  Skill especializada em composição analítica de custos para serviços de
  operação e manutenção (O&M) de usinas fotovoltaicas em órgãos públicos
  federais sediados no Espírito Santo. Aciona quando o usuário mencionar:
  limpeza de módulos fotovoltaicos, manutenção de usina solar, orçamento
  de O&M fotovoltaico, composição de custo para limpeza de placas solares,
  serviço continuado de manutenção FV, parecer técnico fotovoltaico, ou
  laudo de unidade geradora. Opera com bases referenciais SINAPI, SICRO,
  IOPES/DER-ES e composições próprias, priorizando insumos do ES e consulta ao Orçafascio.
allowed-tools: search_web, run_command, read_file
---

# Orçamento Limpeza FV - Espírito Santo

> **MANDATORY:** Utilize esta skill sempre que elaborar composições analíticas e orçamentos de O&M para usinas fotovoltaicas, especialmente a Usina MGI/ES.

## 1. Priorização de Bases Referenciais

Para buscar preços e montar composições analíticas, você deve seguir a seguinte ordem de prioridade estrita:

1. **Prioridade 1 (Local):** Vitória e Espírito Santo (SINAPI-ES, IOPES/DER-ES).
2. **Prioridade 2 (Nacional via Orçafascio):** Utilize os bancos de dados disponíveis no Orçafascio (SBC, SICRO, etc.). Você pode e deve pesquisar no sistema Orçafascio para conferir códigos e composições. Se necessário, utilize as skills `orcafascio-integration` e `orcafascio-mgi-automation`.
3. **Prioridade 3 (Regiões alternativas):** Caso não encontre nas bases locais ou nacionais primárias, pode utilizar tabelas de outras regiões (Sudeste: SETOP, CPOS, EMOP; Norte/Nordeste/Centro-Oeste/Sul) como referência.
4. **Prioridade 4 (Cotação de Mercado):** Insumos específicos de FV (como fornecimento de módulos, inversores) que não existirem nas bases oficiais deverão ser cotados no mercado (mínimo de 3 cotações).

**IMPORTANTE:** Conferir o código exato da composição/insumo na base correspondente é fundamental. Não invente códigos. Utilize o prefixo `SRAES-FV-` apenas para composições próprias.

## 2. Composição de Preço Unitário SRAES-FV-001 — Limpeza de Módulo

Para orçar a limpeza das placas solares, utilize esta base analítica própria:

**Código interno:** SRAES-FV-001
**Descrição:** Limpeza técnica de módulo fotovoltaico instalado em cobertura/estrutura existente, incluindo mão de obra, ferramentas manuais, materiais compatíveis, pequenos equipamentos, registro fotográfico e limpeza final da área.
**Unidade:** un (módulo limpo)

**Componentes Mínimos Sugeridos:**
*   **Eletricista / oficial técnico** (Hora produtiva) -> Fonte: SINAPI-ES ou DER-ES.
*   **Ajudante / servente** (Hora produtiva) -> Fonte: SINAPI-ES ou DER-ES.
*   **Supervisão técnica** (Rateio por visita/lote) -> Fonte: SINAPI-ES, DER-ES ou própria.
*   **Consumíveis** (Água, panos técnicos, escova macia, rodo, pulverizador) -> Fonte: SINAPI-ES, DER-ES ou Cotação.
*   **Equipamentos de acesso** (Andaime, plataforma, linha de vida, escada) -> Fonte: DER-ES, SINAPI-ES ou Cotação.
*   **Mobilização** -> Fonte: SICRO, SINAPI-ES ou DER-ES.
*   **Registro Fotográfico/Relatório** -> Composição própria (homem-hora engenheiro/técnico).
*   **EPIs** (Cinto, talabarte, capacete) -> Rateio (SINAPI-ES).

**Fórmula-base de Cálculo:**
`PU_módulo = Σ(coef_insumo × custo_unitário_oficial) + Σ(rateios) × (1 + BDI_serviço)`

## 3. Regras e Restrições
*   Sinalizar `[VALIDAR COEFICIENTE]` para toda produtividade adotada que não esteja amparada em norma técnica, ensaio ou histórico comprovado.
*   A memória de cálculo deve declarar explicitamente: data-base, UF, regime tributário, encargos sociais aplicados, quantidade total de módulos (ex: 561 un), tipo de acesso, e produtividade (ex: módulos/hora/equipe).
