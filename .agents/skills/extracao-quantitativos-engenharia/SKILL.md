---
name: extracao-quantitativos-engenharia
description: Extrai e organiza quantitativos de obras e servicos de engenharia a partir de memoriais, planilhas, PDFs, DWGs convertidos, fotos e especificacoes tecnicas.
allowed-tools: read_file, run_command
---

# Extracao de Quantitativos de Engenharia

Use esta skill para transformar arquivos de entrada em uma lista verificavel de servicos, unidades e quantidades.

## Entradas

- PDF, DOCX, XLSX, CSV, TXT ou imagens transcritas.
- Plantas DWG convertidas para PDF ou tabela.
- Propostas comerciais.
- Memoriais e especificacoes tecnicas.

## Procedimento

1. Identificar o objeto do contrato.
2. Listar servicos executaveis.
3. Extrair ou propor unidades de medicao.
4. Separar quantitativos medidos de quantitativos estimados.
5. Vincular cada quantidade a uma evidencia documental.
6. Marcar lacunas como `[PENDENTE DE MEDICAO]`.

## Saida Padrao

```markdown
| Item | Servico | Unidade | Quantidade | Fonte | Confianca | Observacao |
| --- | --- | --- | ---: | --- | --- | --- |
```

## Regras

- Nao inferir quantidade sem declarar premissa.
- Nao misturar unidade de execucao com unidade de pagamento.
- Quando houver divergencia entre planta, memoria e planilha, registrar conflito.

