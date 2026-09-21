---
name: vitoria-cost-engineering
description: Engenharia de Custos e Orçamentação na Construção Civil focada em Vitória, Espírito Santo (ES). Prioriza SINAPI e IOPES.
allowed-tools: search_web, run_command, read_file
---

# Engenharia de Custos: Vitória - Espírito Santo

> **MANDATORY:** Utilize esta skill sempre que o usuário pedir análises de custo de obra, composições unitárias de preços (CPU) ou orçamentos voltados para o Estado do Espírito Santo, com foco na Grande Vitória.

---

## 1. Bancos de Dados Oficiais (Orçafascio)

Você deve utilizar estritamente os bancos de dados disponíveis no Orçafascio, seguindo esta ordem de prioridade regional para compor e formatar os orçamentos:

1. **Prioridade 1 (Nacional e Espírito Santo):**
   - SINAPI (ES)
   - SICRO 2 e SICRO 3
   - SBC
   - IOPES (Espírito Santo)

2. **Prioridade 2 (Região Sudeste - Alternativas):**
   - SETOP (Minas Gerais)
   - CPOS e FDE (São Paulo)
   - EMOP e SCO (Rio de Janeiro)

3. **Prioridade 3 (Região Norte - Alternativas):**
   - SEDOP (Pará)

**Regra de Uso:** Sempre que um insumo ou composição exata não for encontrado nas bases do Espírito Santo/Nacionais (Prioridade 1), você está autorizado a pesquisar nas tabelas do Sudeste (Prioridade 2) ou Norte (Prioridade 3), garantindo que a descrição técnica corresponda exatamente ao serviço exigido no projeto.

---

## 2. Regra de Fallback Dinâmico (Cotação de Mercado)

Caso o insumo ou a composição de serviço requerida NÃO seja encontrada no SINAPI-ES ou no IOPES, siga EXATAMENTE este procedimento:

1. **Pesquisa Externa Obrigatória:** Você não deve inventar o preço. Utilize a ferramenta de pesquisa (`search_web`) para buscar fornecedores/lojas de construção que atuem no mercado da **Grande Vitória** (Serra, Vila Velha, Vitória, Cariacica, Viana).
2. **As 3 Cotações:** Obtenha ou estime os preços em **NO MÍNIMO TRÊS (3)** cotações distintas para o item no comércio local.
3. **Média Aritmética:** O preço final a ser utilizado no faturamento ou na composição unitária deve ser estritamente a **média aritmética simples** dessas três cotações.

### Exemplo de Aplicação Prática:
- Insumo não catalogado no IOPES: "Fechadura tipo XYZ Específica".
- Cotação 1 (Loja A - Vitória): R$ 100,00
- Cotação 2 (Loja B - Vila Velha): R$ 110,00
- Cotação 3 (Loja C - Serra): R$ 105,00
- Preço Adotado na Composição: `(100+110+105)/3 = R$ 105,00`

---

## 3. Metodologia de Resposta

Sempre que concluir um orçamento ou gerar uma Composição Unitária:
- Formate a saída como uma Tabela Limpa e Profissional.
- Preços finais devem conter duas casas decimais no padrão PT-BR (R$ 0,00).
- Descreva sempre a fonte de cada insumo (Ex: *SINAPI*, *IOPES*, ou *Média de Mercado Vitória - 3 Cotações*).
