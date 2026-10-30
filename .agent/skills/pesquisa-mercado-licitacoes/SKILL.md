---
name: pesquisa-mercado-licitacoes
description: >
  Skill para condução metodológica de pesquisa de preços conforme
  IN SEGES/ME nº 65/2021, aplicável à aquisição de bens e contratação de
  serviços comuns sem caracterização de engenharia. Aciona quando o
  usuário mencionar pesquisa de preço, cotação, IN 65/2021, painel de
  preços, sistema BPS, contratações similares, aquisição de equipamento,
  ou fornecimento de bem para licitação. Padroniza solicitação de
  cotação, agrega resultados e calcula preço de referência.
allowed-tools: search_web, run_command, read_file
---

# Pesquisa de Mercado (IN SEGES/ME nº 65/2021)

Esta skill define a conduta para compor preços de itens de aquisição de bens ou serviços sem caracterização de engenharia. Exemplo: Aquisição de Módulos Fotovoltaicos e Inversores.

## Regras de Composição de Preço (Cotação)

Sempre que a base oficial (SINAPI, IOPES, etc) não possuir o insumo procurado:

1.  **Exigência Mínima:** Deverão ser encontradas no mínimo três (3) cotações válidas para o mesmo material com especificação técnica equivalente.
2.  **Fontes Prioritárias:** Painel de Preços, contratações similares de órgãos públicos (últimos 180 dias), lojas de e-commerce e fornecedores diretos do mercado de Vitória-ES ou sites nacionais de venda de equipamentos fotovoltaicos.
3.  **Filtro de Discrepância:** Valores inexequíveis ou excessivos (excedendo 30% acima ou abaixo da média) deverão ser descartados com justificativa, a não ser que os três valores sejam próximos.
4.  **Cálculo da Referência:** Aplique a **média aritmética**, a **mediana** ou o **menor preço**. Para aquisições no Orçamento MGI, recomendamos a Média Aritmética.
5.  **Registro Fotográfico/Link:** Ao documentar a cotação, inclua o nome do fornecedor/site e a URL para rastreabilidade, bem como a data do acesso.
