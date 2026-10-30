# Trilhas de aprendizado por demonstração

Uma pasta por item (`<AAAA-NNN-slug>/`) e um arquivo JSONL por sessão observada, com o nome `AAAA-MM-DD-<atividade>.jsonl` (atividades: `orcafascio`, `excel`, `word`, `pdf`, `cad`). O formato de cada evento está em `OrcaAI/tools/orca_tools/trilhas_lfd.py`.

Quem grava: o A10 PilotoOrcafascio (Antigravity, comando `/observar-orcafascio`) durante a sessão do engenheiro no navegador, depois do login manual; o A2 para arquivos de Excel e Word, por diferença entre versões salvas na pasta do item.

Quem lê: o A3 EngenheiroCivilSenior, que escreve os padrões em `../padroes/`; o A4 valida cada padrão contra os parâmetros fixos antes de ele entrar nas instruções dos agentes de produção.

Regras: nunca registrar senha ou dado pessoal; cada evento guarda a tela ou aba e, no navegador, a versão da tela; uma trilha não é apagada, é substituída por outra mais recente.
