---
name: documentos-tecnicos-fv
description: >
  Skill geradora de documentos técnicos formais para sistemas fotovoltaicos
  na Administração Pública Federal: parecer técnico de unidade geradora,
  laudo com registro fotográfico, especificação técnica de módulo FV para
  licitação, memorial descritivo de O&M, e minutas de ART/RRT. Aciona
  quando o usuário pedir parecer, laudo, ART, RRT, especificação técnica
  de módulo FV, memorial de manutenção FV, ou documento de inspeção
  fotovoltaica. Fundamenta-se em ABNT NBR 16690, NBR 16274, NBR 5410,
  NR-10, NR-35, Resolução ANEEL 1.059/2023 e diretrizes do CREA.
allowed-tools: search_web, run_command, read_file
---

# Documentos Técnicos para Sistemas Fotovoltaicos

Esta skill é responsável por gerar os documentos de engenharia e memoriais necessários para o processo de manutenção (O&M) ou especificação de usinas fotovoltaicas.

## Entregáveis Suportados

Você deve gerar os seguintes documentos quando requisitados, adotando uma linguagem técnica, formal e objetiva:

1. **Parecer Técnico de Unidade Geradora**
   *   Deve conter conclusões e recomendações rastreáveis e numeradas.
   *   Deve referenciar a identificação da UG (nº de registro na concessionária e nº ANEEL).
2. **Laudo Técnico com Registro Fotográfico**
   *   Deve indicar a necessidade de no mínimo 1 foto por string, contendo data, horário e geolocalização.
3. **Especificação Técnica de Módulo FV (Para Licitação)**
   *   Deve garantir a padronização e requisitos técnicos compatíveis com a usina existente para fins de aquisição/substituição.
4. **Memorial Descritivo de O&M**
   *   Descreve as rotinas de manutenção preventiva e limpeza, métodos permitidos (ex: água desmineralizada, panos técnicos) e vedações (ex: sem produtos químicos abrasivos ou jatos de alta pressão).
5. **Checklist e Minuta de ART (CREA)**
   *   Orientações para o preenchimento da Anotação de Responsabilidade Técnica.

## Regras de Conteúdo

*   **Identificação:** Todo documento gerado deve conter espaço para cabeçalho com identificação do órgão (MGI/ES), local da usina, data, e identificação do engenheiro responsável.
*   **Fundamentação Legal:** Basear as orientações técnicas nas normativas: ABNT NBR 16690, NBR 16274, NBR 5410, NR-10, NR-35, Resolução ANEEL 1.059/2023.
*   **Clareza e Precisão:** Não deixar margem para interpretações dúbias que possam prejudicar a fiscalização do serviço de manutenção.
