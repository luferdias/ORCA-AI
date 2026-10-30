---
name: orcamento-gerador-es
description: >
  Skill de parametrização orçamentária e composições de custo unitário para 
  serviços de manutenção de grupo gerador de energia elétrica na Administração 
  Pública Federal (Espírito Santo). Define a precedência de bancos oficiais 
  (SINAPI/SICRO) frente às pesquisas de mercado (IN 65/2021).
allowed-tools: search_web, run_command, read_file
---

# Orçamento Manutenção Gerador (MNT_gerador)

> **MANDATORY:** Utilize estas regras para balizar qualquer orçamento ou justificativa de preço de grupos geradores.

## 1. Diretrizes de Composição e Base de Preços
O orçamento de manutenção de geradores deve mesclar fontes oficiais e cotações da seguinte forma:
1. **Precedência do Banco Oficial (SINAPI/SICRO):** Serviços genéricos (Ex: mão de obra de eletromecânico, engenheiro eletricista) e insumos padronizados (Ex: Óleo Lubrificante 15W40) DEVEM adotar os preços da base referencial SINAPI-ES e SICRO3-ES, rejeitando sobrepreços de mercado local.
2. **Deslocamento:** É proibido acatar custos de "Diárias, Passagens, Hospedagem" de fornecedores sediados em outros estados (ou quilometragem abusiva) em licitações comuns em capitais. Utilize o custo por quilômetro rodado (Veículo Leve) do SICRO3.
3. **Cotações (IN 65/2021):** Para peças especializadas do motor (Filtros Scania, retentores, produtos químicos TUNAP), deve-se adotar o método estatístico da IN 65/2021.
   - **Regra de Cálculo:** Utilizar preferencialmente a **Mediana** de 3 orçamentos (fornecedores) para evitar distorções de preços extremos (outliers).

## 2. Estrutura de BDI
- **Regime:** Desonerado.
- **Taxa de BDI:** O BDI adotado para manutenção eletromecânica no Espírito Santo (Praça de Vitória) é fixado em **25,00%**, incidindo uniformemente sobre materiais e serviços.
