---
name: curva-abc-sobrepreco
description: Gera curva ABC e revisa risco de sobrepreco, priorizando itens materialmente relevantes do orcamento publico.
allowed-tools: read_file, run_command
---

# Curva ABC e Sobrepreco

Use esta skill depois que a planilha orcamentaria estiver normalizada.

## Procedimento

1. Calcular total por item.
2. Ordenar do maior para o menor valor.
3. Calcular percentual individual e acumulado.
4. Classificar A, B e C.
5. Priorizar revisao dos itens A.
6. Conferir fonte, data-base, BDI, unidade e descricao.

## Regras

- Item A sem fonte robusta e pendencia critica.
- Item com preco proprio deve ter memoria de calculo e aprovacao.
- Item com unidade divergente deve ser destacado antes da emissao final.

## Saida Padrao

```markdown
| Classe | Item | Descricao | Total | Percentual | Acumulado | Risco | Acao |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
```

