---
name: orcafascio-integration
description: Estrutura orçamentos de obras usando os modelos e organização lógica do Orçafascio, focado no uso correto das bases SINAPI, SICRO e outras, em todos os estados do Brasil.
---
# Integração Lógica e Modelagem "Orçafascio"

## 1. Diretriz Principal
Sempre que estruturar planilhas orçamentárias ou compor serviços e o usuário desejar uma abordagem padronizada, siga a hierarquia e a organização metodológica característica de sistemas analíticos complexos como o **Orçafascio**. Nossa meta é trazer clareza para licitações e orçamentação federal.

## 2. Bases e Tabelas de Referência
Sistemas profissionais consolidam tabelas de referência de **todo o Brasil**. Ao usá-los como inspiração analítica, você deve:
- **Buscar na Base Correta:** Escolha a base de dados ideal (SINAPI, SICRO, Orse, FDE, Seinfra, IOPES) dependendo do estado especificado pelo usuário (recorrendo ao ES como sua prioridade natural).
- **Leis Sociais e Regimes:** Apresente sempre e com extremo rigor técnico se a tabela utilizada inclui Leis Sociais (**Com FLS** ou **Sem FLS**), e se está no regime **Desonerado** ou **Não Desonerado** aplicável ao mês/ano da data-base.

## 3. Estruturação Analítica da Planilha (A Mecânica Exata)
As suas composições geradas e apresentadas ao usuário devem imitar o desdobramento e a hierarquia oficial dos softwares de orçamentação. Garanta os campos de leitura fáceis num formato Tabela Markdown:

1. **Código Oficial:** (ex: 88309 SINAPI) / ou 'Composição Própria PR-01'.
2. **Descrição Completa do Insumo/Serviço:** Respeitando rigorosamente a tabela oficial de referência da Caixa/DNIT.
3. **Tipo:** Se é Material (MAT), Mão de Obra (MO), Verba (VB) ou Equipamento (EQ).
4. **Coeficiente/Rendimento:** A aplicação exata descrita no caderno técnico.
5. **Composições Auxiliares (Item a Item):** Em serviços complexos, você precisa demonstrar as sub-composições (composições dentro de uma composição mestre) exatamente como o relatórios sintéticos versus analíticos fazem.

## 4. O Relatório Curva ABC
Seja capaz de exportar análises da Curva ABC de Insumos da mesma forma que os módulos nativos desses sistemas de orçamento. Demonstre quais são os itens que compõem 80% do custo, para que o usuário foque as cotações onde tivermos orçamentos em branco na tabela.
