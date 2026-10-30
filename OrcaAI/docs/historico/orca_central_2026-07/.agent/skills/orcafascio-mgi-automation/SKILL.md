---
name: orcafascio-mgi-automation
description: Procedimentos seguros de navegacao e automacao no Orcafascio para criar, consultar, exportar e revisar orcamentos publicos, sem armazenar credenciais em texto claro.
allowed-tools: browser_subagent, read_file, run_command
---

# Automacao Orcafascio

Use esta skill quando a tarefa envolver acesso ao Orcafascio, consulta de bases, criacao de projeto, busca de composicoes, exportacao de planilhas ou revisao de relatorios do sistema.

## Seguranca de Credenciais

Nunca grave login ou senha em arquivos do projeto.

Use variaveis de ambiente:

- `ORCAFASCIO_URL`
- `ORCAFASCIO_LOGIN`
- `ORCAFASCIO_PASSWORD`

Se elas nao estiverem configuradas, solicite autenticacao manual ao usuario antes de continuar.

## Fluxo de Automacao

1. Abrir o Orcafascio pelo `browser_subagent`.
2. Autenticar com variaveis de ambiente ou sessao manual.
3. Criar ou selecionar o projeto de orcamento.
4. Configurar localidade, data-base e regime aplicavel.
5. Pesquisar composicoes e insumos em bases oficiais.
6. Exportar relatorios ou planilhas para `bases/orcafascio-export/` ou para a pasta do projeto.
7. Registrar toda fonte usada em `log-decisoes.md`.

## Ordem de Busca

1. SINAPI-ES.
2. IOPES/DER-ES.
3. SICRO, quando aplicavel.
4. Outras bases disponiveis no Orcafascio.
5. Bases regionais de fallback, quando justificadas.
6. Pesquisa de mercado com aprovacao humana.

## Regras de Pausa

Pausar e pedir validacao humana antes de:

- criar composicao propria;
- inserir preco manual;
- usar base de outro estado;
- usar cotacao externa;
- alterar BDI padrao;
- concluir pacote para assinatura.

## Saida Esperada

Ao finalizar, gerar um resumo com:

- projeto consultado;
- bases e datas usadas;
- itens encontrados;
- itens nao encontrados;
- exportacoes realizadas;
- pendencias de validacao.

