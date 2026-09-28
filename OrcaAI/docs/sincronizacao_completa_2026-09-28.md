# Consolidação do projeto e sincronização — 28/09/2026

Solicitação do engenheiro Luis Fernando: publicar o projeto completo no GitHub e manter os mesmos arquivos de conteúdo na pasta do OneDrive.

## Conteúdo incluído

- Códigos, agentes, especificações, documentos, bases oficiais, datasets, modelos e relatórios.
- Planilhas e documentos pendentes dos 12 projetos de orçamento e da governança SEI/AGU/CGU.
- Todas as execuções de Machine Learning existentes nas duas pastas, inclusive históricos, prévias e diagnósticos, com seus manifestos e status originais.
- `Orca.zip`, arquivo histórico de materiais do projeto. Não substitui a árvore atual.

Os arquivos foram comparados por conteúdo, considerando as duas formas de representar acentos nos nomes de arquivos do macOS. As três versões de documentos mais recentes na pasta principal foram preservadas. Arquivos exclusivos de uma das pastas foram acrescentados à outra, sem apagar o acervo.

A entrega acadêmica atual continua em [entrega ao professor Ronaldo](../ml/ENTREGA_UFG.md). A inclusão de históricos não transforma prévias ou execuções com erro em resultados finais. Em particular, `estudo_acabamentos_2026-09-27` conserva o status de erro registrado durante o desenvolvimento.

## Arquivos locais de funcionamento

Ambientes `.venv`, caches `__pycache__` e `.pytest_cache`, arquivos `.pyc`, `.DS_Store` e diretórios locais de ferramentas `.temp_ag_kit` e `.sixth` permanecem excluídos do Git. Os metadados internos `.git` são próprios de cada checkout. A igualdade verificada entre os destinos se refere ao conteúdo versionado do projeto.

## Verificações realizadas

- Comparação de hashes dos arquivos entre o worktree e a pasta principal do OneDrive; os conteúdos originais do acervo foram preservados.
- Conferência de integridade dos arquivos pendentes: 16 XLSX, cinco DOCX, dois PDFs, dois PNG, três Markdown e sintaxe de dois scripts Python.
- Os 21 arquivos XLSX/DOCX passaram pela leitura do contêiner ZIP e dos componentes XML. Os PDFs permitiram leitura de todas as páginas; o leitor corrigiu um índice XRef no PDF SEI 64558648, sem impedir sua leitura. Esse arquivo foi preservado.
- Suíte de Machine Learning executada na pasta `OrcaAI/ml`: 223 testes e nove subtestes aprovados.
- Nenhum arquivo do conteúdo a publicar ultrapassou 100 MB.

## Ponto de conteúdo que requer revisão

O despacho de engenharia e sua cópia apresentam uma divergência editorial na classificação ABC da mesma memória de 11 itens:

- O texto das linhas 47 e 86 informa Classe A com quatro itens e 74,46%.
- A tabela inclui o item 05 na Classe A e apresenta cinco itens, totalizando 79,57%. A diferença de 5,11 pontos percentuais corresponde ao item 05.

Documentos afetados:

- [Despacho de engenharia em Markdown](../projetos/_governanca_sei_agu_cgu/pareceres_agu/DESPACHO_ENGENHARIA_SRA_RESPOSTA_PARECER_AGU.md).
- [Cópia SEI 64490579 em Markdown](../projetos/_governanca_sei_agu_cgu/despachos_sei/SEI_64490579_Despacho_Engenharia_Resposta_AGU.md).
- Respectivos DOCX `DESPACHO_ENGENHARIA_SRA_RESPOSTA_PARECER_AGU_v2.docx` e `SEI_64490579_Despacho_Engenharia_Resposta_AGU.docx`.

As somas monetárias da tabela conferem. A divergência não foi identificada nos documentos SEI 64558648 revisados. Todos foram sincronizados como recebidos; a decisão editorial sobre o texto desses despachos fica registrada para revisão própria.
