# Estrutura Minima dos Arquivos

Use este guia quando a skill precisar entender ou normalizar arquivos de referencia `SINAPI` e `IOPES`.

## Colunas detectadas automaticamente

O script `scripts/validate_codes.py` tenta localizar colunas equivalentes a:

- `codigo`: `codigo`, `cod`, `item`, `codigo composicao`, `codigo insumo`
- `descricao`: `descricao`, `descrição`, `especificacao`, `servico`, `insumo`
- `sistema`: `sistema`, `origem`, `fonte`, `base`, `tabela`, `referencia`
- `unidade`: `unidade`, `un`, `und`
- `preco`: `preco`, `valor`, `custo`, `preco unitario`

## Formatos aceitos

- `.csv`
- `.tsv`
- `.json` com lista de objetos
- `.xlsx` e `.xlsm`

Para planilhas do Excel, use `arquivo.xlsx#NomeDaAba` quando a aba correta nao for a primeira.

## Boas praticas

- Padronize a coluna de codigo com o mesmo tipo de item dentro de cada arquivo.
- Mantenha uma coluna `sistema` no orcamento quando houver mistura de `SINAPI` e `IOPES`.
- Exporte as bases oficiais para um formato tabular antes de validar.
- Revise manualmente casos com divergencia de descricao, porque pequenas adaptacoes locais podem ser aceitaveis.
