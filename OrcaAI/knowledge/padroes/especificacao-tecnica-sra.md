# Padrão: especificação técnica da SRAES

Derivado em 30/10/2026 das doze especificações técnicas do acervo
(`OrcaAI/projetos/2026-001` a `2026-012`, pasta `06-documentos`), em
cumprimento à regra R-C1 da entrevista de maturidade: "vale o modelo que já
foi usado nos itens 01 a 12". O A6 DescritorEspecificador escreve nesta
estrutura; o modelo genérico `OrcaAI/templates/modelo_especificacao_tecnica.md`
fica subordinado a este padrão.

## Duas famílias no acervo

| Família | Itens | Traço | Quando usar |
| --- | --- | --- | --- |
| **SRAES padrão** | 01 a 09 (maio de 2026) | Onze a quinze seções fixas; escopo por sequência técnica; tabelas de dados, materiais e normas; 580 a 1.900 palavras | Serviço ou manutenção com uma disciplina dominante |
| **Memorial por EAP** | 10, 11 e 12 | Especificação item a item seguindo os grupos da planilha; critérios de medição, inspeção e aceitação; entregáveis | Intervenção com várias disciplinas ou muitos grupos na EAP |

As duas famílias compartilham cabeçalho, objeto, normas e fecho. A estrutura
canônica abaixo é a da família SRAES padrão, com as seções da família por EAP
marcadas como condicionais.

## Cabeçalho institucional (todas)

```
MINISTÉRIO DA GESTÃO E DA INOVAÇÃO EM SERVIÇOS PÚBLICOS
SUPERINTENDÊNCIA DE ADMINISTRAÇÃO NO ESPÍRITO SANTO — SRAES
ESPECIFICAÇÃO TÉCNICA
<Título do serviço, em duas linhas: o que e onde>
Vitória/ES
<Mês de AAAA>
Setor de Engenharia — SRAES/MGI
```

O mês do cabeçalho é a data-base do orçamento (regra R-B8).

## Estrutura canônica

| Nº | Seção | Conteúdo observado no acervo | Obrigatória |
| --- | --- | --- | --- |
| 1 | **OBJETO** | Dois parágrafos. O primeiro começa com "Contratação de empresa especializada para execução dos serviços de …", nomeia o edifício e a cidade. O segundo resume o método e as normas de segurança que governam a execução. | Sim |
| 2 | **DADOS DA EDIFICAÇÃO** (ou DO RESERVATÓRIO, DOS ELEVADORES, DAS USINAS) | Tabela Parâmetro × Descrição: edificação, endereço, áreas ou quantidades principais, sistema de acesso, sistema construtivo em questão. | Sim |
| 3…n | **ESCOPO TÉCNICO** | "A execução obedecerá à seguinte sequência técnica e metodológica". Uma subseção numerada por etapa (3.1, 3.2 …), em lista com ponto e vírgula. Quando há mais de uma frente, um capítulo de escopo por frente ("ESCOPO TÉCNICO — PINTURA DAS FACHADAS", "— TELHADO"). O código da planilha aparece no título da subseção quando a etapa corresponde a um item orçado, como em "3.1. Mobilização, Montagem e Testes (SRAES-LIMP-001)". | Sim |
| n+1 | **ESPECIFICAÇÃO DOS MATERIAIS E EQUIPAMENTOS** | Tabela Material × Especificação mínima obrigatória; subseções por material quando há muitos. Desempenho e norma, nunca marca sem "ou similar". | Sim, exceto serviço sem material (item 09) |
| n+2 | **NORMAS TÉCNICAS E LEGISLAÇÃO APLICÁVEL** | Tabela Norma × Descrição. Sempre: Lei 14.133/2021 e NR-18; NR-35 em altura; NR-10 em elétrica; NR-33 em espaço confinado; NBR do sistema (9575 impermeabilização, 13245 pintura, 16401 HVAC …). | Sim |
| n+3 | **SEGURANÇA DO TRABALHO** | Qualificador entre parênteses quando o risco é específico: (TRABALHO EM ALTURA), (ESPAÇO CONFINADO), (NR-10 E NR-35). Lista: certificação e ASO, EPIs, ancoragem, clima. | Sim |
| n+4 | **CONDIÇÕES DE EXECUÇÃO E LOGÍSTICA** ou **CONDIÇÕES AMBIENTAIS PARA APLICAÇÃO** | Horários, isolamento, acessos, intempéries, condições de aplicação de tintas e selantes. | Quando aplicável |
| n+5 | **QUALIFICAÇÃO TÉCNICA EXIGIDA** | Registro no CREA, atestado de capacidade técnica compatível, treinamentos. | Sim |
| n+6 | **OBRIGAÇÕES DA CONTRATADA** | ART de execução (e de montagem quando há balancim ou andaime), fornecimento de materiais e EPIs, descarte legal, laudo final, garantia mínima em anos. | Sim |
| n+7 | **OBRIGAÇÕES DA CONTRATANTE** | Acessos, isolamentos, fiscalização designada. | Sim |
| n+8 | **DISPOSIÇÕES GERAIS** | Ajustes com a fiscalização, intempéries, omissões. | Sim |
| — | **CRITÉRIOS DE MEDIÇÃO E PAGAMENTO** | Unidade e forma de aferição por item da EAP. | Família por EAP; recomendada sempre que houver medição por etapas |
| — | **CRITÉRIOS DE INSPEÇÃO, TESTES E ACEITAÇÃO** | Ensaios, verificações e condição de aceite por grupo. | Família por EAP |
| — | **DOCUMENTAÇÃO TÉCNICA E ENTREGÁVEIS** / **SUSTENTABILIDADE E DESCARTE** | Laudos, as built, MTR de resíduos. | Família por EAP |

## Fecho (todas)

```
Vitória/ES, <mês> de <AAAA>.
__________________________________________________
Luis Fernando
Setor de Engenharia — SRAES/MGI
```

## Regras de redação observadas

- Títulos de seção numerados e em caixa alta; subseções "3.1." com inicial
  maiúscula; nenhuma seção sem número, exceto o cabeçalho.
- Itens de lista terminam em ponto e vírgula; o último, em ponto.
- Tabelas sempre de duas colunas (parâmetro × descrição, material ×
  especificação, norma × descrição).
- Verbos no futuro impessoal ("obedecerá", "será realizada") no escopo;
  infinitivo nas obrigações ("Providenciar", "Fornecer", "Emitir").
- Normas citadas com ano (NBR 13755:2017); leis com número e ano.
- O escopo nunca cita preço; cita código da planilha quando a etapa é um
  item orçado, o que amarra especificação e orçamento (regra R-C2).
- Revisões recebem sufixo "— Revisão 01" no nome do arquivo e, quando há
  inclusão de serviço, um capítulo final "(Inclusão Revisão 01)" (item 07).

## Como o A6 usa este padrão

1. Recebe de `01-escopo` o escopo aprovado e as premissas, e de
   `03-orcamento` a EAP com os códigos.
2. Escolhe a família: uma disciplina dominante → SRAES padrão; muitos grupos
   ou várias disciplinas → memorial por EAP.
3. Preenche cada seção obrigatória; seção condicional entra só com conteúdo
   real, nunca vazia.
4. Grava `06-documentos/especificacao-tecnica.md` e pede ao
   renderizador-documentos o DOCX e o PDF (`orca_tools.renderizar`).
5. O A4 confere a cobertura: todo item da EAP aparece no escopo, e toda norma
   citada existe (regra R-C5).
