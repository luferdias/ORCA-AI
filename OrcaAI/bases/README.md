# Bases de Referencia

## Fontes verificadas e atualização

- [Catálogo de fontes oficiais e condições de acesso](catalogo_fontes_referenciais.json).
- [Auditoria dos portais e amostras em 27/09/2026](../docs/auditoria_bases_referenciais_2026-09-27.md).
- [Especificação de dados, ML e atualização por projeto](../spec/ml_ufg/bases_servicos_e_atualizacao.md).

Ao iniciar um orçamento, consultar a última edição publicada para a fonte e a UF aplicáveis, conferir o arquivo e registrar a versão usada. Competência, publicação e captura são datas distintas. Retificações geram nova revisão; arquivos anteriores permanecem disponíveis.

O catálogo registra uma checagem pontual e amostral. Ele não executa downloads nem comprova a integridade de todas as linhas das bases. As pastas existentes e os 12 projetos foram preservados.

### SINAPI obtido em 27/09/2026

O [ZIP Excel de agosto/2026](sinapi/2026-08/originais/SINAPI-2026-08-formato-xlsx.zip) foi baixado pelo navegador no site da CAIXA e permanece compactado. O [manifesto](sinapi/2026-08/originais/manifesto_download.json) registra URL, publicação, tamanho, SHA-256 e nomes das quatro planilhas. O pacote contém todas as UFs, conforme o publicador; a seleção dos dados do ES será feita na próxima etapa.

## Arquivos locais

Coloque aqui as bases locais usadas para validacao e composicao:

- `sinapi/`
- `iopes/`
- `sicro/`
- `orcafascio-export/`
- `outras-bases/`

## Boas Praticas

- Nomeie arquivos com UF e data-base.
- Preserve exportacoes originais.
- Nao sobrescreva bases antigas.
- Use formatos tabulares quando possivel: `.xlsx`, `.csv`, `.tsv` ou `.json`.

Exemplo:

```text
bases/sinapi/SINAPI_ES_2026-05_composicoes.xlsx
bases/iopes/IOPES_ES_2026-05_servicos.xlsx
```
