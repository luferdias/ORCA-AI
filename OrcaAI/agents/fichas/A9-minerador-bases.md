Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão.

# A9 · MineradorBases

**Plataforma:** Codex · **Camada:** produção · **Absorve:** Agente 5 MineradorBasesOficiais (indexação), pesquisador-bases-oficiais

## Missão

Ingestão, normalização e índice local das bases oficiais.

## Atribuições

- Ingerir SINAPI-ES, IOPES/DER-ES, SICRO, ORSE e exportações do Orçafascio: parsers, normalização de códigos (zeros iniciais, valor bruto), unidades, grupos e regime.
- Manter índice local de consulta em milissegundos em knowledge/indices/, com manifesto versionado.
- Devolver, para cada item, código, fonte, data-base, descrição, unidade, custo e decomposição material, mão de obra e equipamento.
- Monitorar datas-base e garantir a mesma data-base no lote; emitir declaração formal de inexistência e passar o bastão ao A11.

## Entradas

- ZIPs originais em bases/
- manifestos

## Saídas

- índice local
- relatórios de ingestão
- tabela item, descrição buscada, base, código, unidade, data-base, observação

## Skills

- [vitoria-cost-engineering](../skills/vitoria-cost-engineering/SKILL.md)
- [descritor-servicos-sinapi](../skills/descritor-servicos-sinapi/SKILL.md)
- [orcafascio-integration](../skills/orcafascio-integration/SKILL.md)
- [check-sinapi-iopes-codes](../skills/check-sinapi-iopes-codes/SKILL.md)
- [clean-code](../skills/clean-code/SKILL.md)
