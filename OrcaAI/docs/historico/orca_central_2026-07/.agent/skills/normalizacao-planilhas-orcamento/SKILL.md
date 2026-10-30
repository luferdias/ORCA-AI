---
name: normalizacao-planilhas-orcamento
description: Normaliza planilhas de orcamento para o modelo unico da Central Orca, preservando fontes, codigos, unidades, BDI, quantitativos e observacoes.
allowed-tools: read_file, run_command
---

# Normalizacao de Planilhas de Orcamento

Use esta skill para converter planilhas recebidas, exportadas do Orcafascio ou criadas manualmente para o padrao da Central Orca.

## Colunas Minimas

- `item`
- `codigo`
- `sistema`
- `descricao`
- `unidade`
- `quantidade`
- `custo_unitario_sem_bdi`
- `bdi_percentual`
- `preco_unitario_com_bdi`
- `preco_total_com_bdi`
- `fonte`
- `data_base`
- `observacoes`

## Procedimento

1. Identificar abas relevantes.
2. Detectar linha de cabecalho.
3. Mapear colunas antigas para o modelo padrao.
4. Separar itens de servico, insumo, composicao propria e fornecimento.
5. Padronizar decimal e moeda.
6. Gerar arquivo normalizado na pasta `03-orcamento`.

## Regras

- Preservar o codigo original.
- Nunca substituir fonte sem evidencias.
- Itens sem fonte devem ser marcados como `[SEM FONTE]`.

