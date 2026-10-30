# OS-NNN · <título curto da delegação>

Copie este arquivo para `05-validacoes/os-NNN.md` (NNN sequencial dentro do item,
começando em 001). A mensagem `maestri ask` leva só o caminho do arquivo e um resumo;
o contrato da delegação é este arquivo. Se `05-validacoes/` ainda não existir, crie
com `python OrcaAI/tools/cli/criar_projeto.py <item> --etapa 05-validacoes`.

## Pedido (preenche o solicitante)

| Campo | Valor |
| --- | --- |
| Item | `AAAA-NNN-slug` |
| Etapa | `0X-nome` |
| Solicitante | Batuta (A1 OrcaMaestro) ou outro agente |
| Destinatário | Prumo (A6/A7/A8/A9) ou Sextante (A10/A11) |
| Plataforma | Codex ou Antigravity |
| Data de abertura | AAAA-MM-DD |
| Prazo | AAAA-MM-DD ou "sem prazo" |

**Objetivo.** Uma frase: o que deve existir ao final.

**Entradas.** Caminhos dos arquivos de partida dentro do item, base e data-base a usar.

**Saídas esperadas.** Caminhos exatos dos artefatos a produzir, dentro do item.

**Critérios de aceite.** Lista verificável; sem critério, a OS não é emitida.

**Dependências.** Outras OS, aprovações pendentes ou gatilhos de aprovação humana.

## Resposta (preenche o destinatário, no mesmo arquivo)

| Campo | Valor |
| --- | --- |
| Estado | concluída · parcial · bloqueada |
| Data de resposta | AAAA-MM-DD |
| Próximo responsável | Batuta (A4) para fechar, ou quem a OS indicar |

**Artefatos.** Caminhos dos arquivos gravados.

**Evidências.** Fonte, URL, data da consulta, hash ou competência de cada dado usado.

**Decisões.** O que foi decidido e por quê; cada aprovação ou pendência também vai
para `log-decisoes.md`.

**Limitações.** O que não foi possível resolver com base oficial, com a pendência
registrada; nenhum código, preço, coeficiente ou fonte é inventado.

**Devolução.** `maestri ask "Batuta" "OS-NNN <item>: <estado> — ver 05-validacoes/os-NNN.md"`.
