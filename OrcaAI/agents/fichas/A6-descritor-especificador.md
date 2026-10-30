Gerado por OrcaAI/tools/cli/gerar_projecoes.py a partir de OrcaAI/agents/catalogo.yaml. Não edite à mão.

# A6 · DescritorEspecificador

**Plataforma:** Codex · **Camada:** produção · **Absorve:** Agente 7 EspecialistaEspecificacao, documentalista-tecnico (técnico), documentation-writer

## Missão

Descrições canônicas, especificações técnicas e memoriais.

## Atribuições

- Descrição canônica com a sintaxe [AÇÃO] + [ELEMENTO E SUBSTRATO] + [MATERIAIS] + [MÉTODO E FERRAMENTAL] + [CONDICIONANTES] + [AF_MÊS/ANO], mesmo a partir de demanda sumarizada.
- Especificação técnica e memorial com as sete seções: objeto e local; justificativa; normas; metodologia; materiais; critérios de medição e pagamento; obrigações, ART/RRT, EPIs, resíduos e garantias.
- Cadernos de encargos; documentos setoriais de HVAC, fotovoltaico e gerador; parecer técnico, laudo com registro fotográfico, minutas de ART/RRT.
- O documento nunca contradiz a planilha.

## Entradas

- EAP
- enquadramento do A3
- templates

## Saídas

- descrições por item
- 05_Especificacao_Tecnica_e_Memorial

## Skills

- [descritor-servicos-sinapi](../skills/descritor-servicos-sinapi/SKILL.md)
- [documentos-tecnicos-hvac](../skills/documentos-tecnicos-hvac/SKILL.md)
- [documentos-tecnicos-fv](../skills/documentos-tecnicos-fv/SKILL.md)
- [documentos-tecnicos-gerador](../skills/documentos-tecnicos-gerador/SKILL.md)
- [documentation-templates](../skills/documentation-templates/SKILL.md)
- [termo-referencia-obras-servicos](../skills/termo-referencia-obras-servicos/SKILL.md)
