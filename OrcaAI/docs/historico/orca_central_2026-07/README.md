# Orca

Central de Orcamento Publico Assistida por Agentes para uso no Antigravity.

Este projeto foi estruturado a partir da experiencia acumulada no workspace `Orcamento_de_Obra`, onde foram produzidos orcamentos, especificacoes tecnicas, planilhas, PDFs e documentos para 11 itens de servicos de engenharia.

## Objetivo

Automatizar a producao de novos orcamentos publicos com:

- triagem tecnica;
- consulta a bases oficiais;
- apoio ao Orcafascio;
- composicao de custos;
- calculo e justificativa de BDI;
- pesquisa de mercado controlada;
- validacao SINAPI/IOPES;
- documentos tecnicos;
- dossie final.

## Como Comecar

1. Abra esta pasta no Antigravity.
2. Configure as variaveis do `.env.example`, se for usar Orcafascio.
3. Crie um projeto:

```powershell
python scripts/criar_projeto_orca.py "2026-001-limpeza-hvac"
```

4. Coloque documentos de entrada em:

```text
projetos/2026-001-limpeza-hvac/00-entrada/
```

5. Use os workflows:

```text
/novo-orcamento
/orcafascio
/pesquisar-precos
/validar-orcamento
/gerar-documentos
/gerar-dossie
/status-orca
/revisar-final
```

## Estrutura

```text
Orca/
  .agent/
    agents/
    subagents/
    skills/
    workflows/
    rules/
    scripts/
  bases/
  templates/
  projetos/
  scripts/
  output/
```

## Regra de Ouro

Nenhum agente deve inventar codigo, preco, coeficiente ou fonte. Se a base oficial nao resolver, a central deve registrar pendencia, pesquisar mercado e pedir aprovacao humana.

