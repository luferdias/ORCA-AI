---
trigger: always_on
---

# Regras Globais da Central Orca

Este workspace opera como uma Central de Orcamento Publico Assistida por Agentes.

## Classificacao de Pedido

| Tipo | Acao |
| --- | --- |
| Pergunta simples | Responder direto, sem criar arquivos. |
| Nova demanda de orcamento | Usar `/novo-orcamento` e `central-orchestrator`. |
| Consulta Orcafascio | Usar `/orcafascio` e credenciais seguras. |
| Pesquisa de mercado | Usar `/pesquisar-precos` e pedir aprovacao antes de aplicar preco. |
| Validacao | Usar `/validar-orcamento`. |
| Documentos finais | Usar `/gerar-documentos`. |
| Dossie | Usar `/gerar-dossie`. |

## Regras Tecnicas

1. Nunca inventar codigo, preco, coeficiente ou fonte.
2. Todo item deve ter fonte, data-base e unidade.
3. Usar SINAPI-ES e IOPES como primeiras referencias quando o servico for no Espirito Santo.
4. Usar Orcafascio como ferramenta de estruturacao e conferencia quando disponivel.
5. Pesquisa de mercado exige no minimo 3 cotacoes comparaveis ou justificativa formal.
6. Composicao propria exige codigo controlado e aprovacao humana.
7. BDI deve ser declarado e justificado.
8. Documentos tecnicos devem ser coerentes com a planilha.
9. Validacao final deve ocorrer antes de qualquer dossie final.

## Credenciais

Nenhuma credencial fica no sistema. Para o Orcafascio, o agente abre `https://app.orcafascio.com/` e aguarda o engenheiro Luis Fernando fazer o login manualmente. Nunca preencher, solicitar ou armazenar a senha.

## Pastas Padrao

- Entrada: `00-entrada`
- Escopo: `01-escopo`
- Quantitativos: `02-quantitativos`
- Orcamento: `03-orcamento`
- Cotacoes: `04-cotacoes`
- Validacoes: `05-validacoes`
- Documentos: `06-documentos`
- Assinados: `07-assinados`

## Ponto de Parada Obrigatorio

Pausar e solicitar aprovacao quando:

- nao houver base oficial;
- houver cotacao externa;
- houver composicao propria;
- houver divergencia de unidade;
- houver BDI excepcional;
- o pacote estiver pronto para assinatura.

