# Padrão: exportação e enquadramento no Orçafascio (derivado do acervo)

Status: **validado por evidência do acervo** (29/10/2026). Fonte: as doze planilhas sintéticas normalizadas em `projetos/*/03-orcamento/planilha-normalizada.csv`, mais os treze memoriais de BDI. Este padrão não substitui trilhas de sessão ao vivo; é o ponto de partida do A3 até que as primeiras trilhas sejam gravadas.

## O que o engenheiro faz, de forma consistente

- Exporta do Orçafascio a planilha **Orçamento Sintético** com cabeçalho Obra | Bancos | B.D.I. | Encargos Sociais e colunas Item | Código | Banco | Descrição | Und | Quant. | Valor Unit | Valor Unit com BDI | Total | Peso (%). Itens analisados: 144.
- Aplica **BDI de 25%** em todos os itens de serviço (contagem por BDI arredondado: {25: 144}); regime **desonerado** nos memoriais.
- Data-base por item: 2026-001 2026-04, 2026-002 2026-02, 2026-003 2026-02, 2026-004 2026-04, 2026-005 2026-02, 2026-006 2026-04, 2026-007 2026-04, 2026-008 2026-02, 2026-009 2026-04, 2026-010 2026-04, 2026-011 2026-02, 2026-012 2026-06.
- Distribuição dos bancos usados: {'PROPRIA': 100, 'SINAPI': 17, 'IOPES': 9, 'ORSE': 6, 'EMOP': 4, 'SBC': 3, 'SCO': 2, 'SEDOP': 1, 'SIURB': 1, 'SICRO': 1}. Ordem de preferência observada: composição própria quando o serviço é atípico; SINAPI-ES e IOPES para serviços padronizados; ORSE, SBC, EMOP, SICRO, SIURB, SEDOP, SCO e SETOP como complementos pontuais.
- Séries de códigos próprios usadas: {'SRAES-CP': 33, 'COMP-CAG': 15, 'SRAES-JUNTAS': 13, 'SRAES-ELEV': 10, 'SRA-ES': 8, 'SRAES-SUB': 6, 'SRAES-FILM': 5, 'SRAES-GER': 4, 'SRAES-FV': 3, 'SRAES-LIMP': 2, 'COMP-HVAC': 1}. Todas têm a chancela do órgão, mas estão fora do padrão `SRAES-CP-NNN` / `SRAES-INS-NNN`: mapear na próxima revisão de cada item (ressalva G-01).
- Descrições de itens SINAPI são frequentemente reescritas para o contexto da obra (Item 07: 5 de 12); o código permanece o oficial. O A4 confere a compatibilidade técnica da reescrita.
- Unidades vêm com símbolo (`m²`, `m³`); as bases usam `m2`, `m3`. Normalizar antes de comparar.

## Como o A10 deve usar

- Ao observar uma sessão nova, comparar com este padrão e registrar divergências como eventos com `justificativa`.
- Em modo autônomo: buscar primeiro SINAPI-ES e IOPES na data-base do item; propor composição própria só com o De acordo; travar BDI em 25%; nunca inserir código sem validação do A4.
