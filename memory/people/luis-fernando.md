# Luis Fernando

Preferência registrada a pedido do usuário em 27/09/2026.

- **Nome:** Luis Fernando Dias.
- **Tratamento:** engenheiro Luis Fernando.
- **Comunicação:** português claro e direto e técnico.
- **Contexto fornecido:** atua com orçamentação de obras na SRA Espírito Santo,
em Vitória, usando Orçafascio.
- **Objetivo acadêmico:** aplicar ML no ORCA-AI para a disciplina da UFG e 
aproveitar os resultados no Projeto Aplicado do curso de Agentes Inteligentes, o
projeto ORCA-AI será usado também como projeto final do curso de Agentes 
Inteligentes da UFG.


## Forma de trabalho observada em 29/10/2026

- **Ambiente:** macOS, repositório dentro do OneDrive, Python 3.12 no 
`.venv (raiz)`, `uv`/`uvx` disponíveis no Homebrew. Ver efeitos do OneDrive 
sobre o git no `CLAUDE.md`, seção "Qualidade de código".
- **Fluxo com git:** prefere avançar em passos pequenos, cada um commitado e 
enviado para `origin/main` logo em seguida. Mensagens de commit em português, no
padrão `tipo(escopo): descrição`.
- **Decisões:** quer ver o diff ou a evidência antes de aprovar mudanças que não
pediu diretamente, como a correção do número de processo SEI e a remoção dos 
links simbólicos. Depois de ver, decide rápido e com instruções curtas.
- **Qualidade de código:** aprovou o ruff como padrão do projeto, a formatação 
de todo o repositório e o hook de pre-commit, e pediu que isso fosse documentado
no README, no README do ml, no `CLAUDE.md` e na memória.

## Forma de trabalho observada na sessão ORCA-AI 2.0 (29 e 30/10/2026)

- **Pedidos por voz:** envia solicitações longas transcritas por voz, com 
repetições e erros de transcrição. O conteúdo técnico é consistente; 
interpretar pela intenção e confirmar nomes próprios pelo contexto (Orçafascio, 
Antigravity, Codex, Claude Code).
- **Especificação antes da execução:** quer uma spec escrita, revisada por ele e
em PDF, antes de tocar na estrutura. Regra fixada: **não cortar nada do que já 
existe; melhorar**. Aprovou a spec e só depois autorizou a execução.
- **Autonomia depois da aprovação:** uma vez aprovada a spec, pediu execução 
contínua até o fim ("não pare até terminar"), sem pausar para confirmar cada 
comando. A aprovação vale para o escopo aprovado; decisões fora dele continuam 
pausando.
- **Segurança:** a senha do Orçafascio não pode existir no sistema em forma 
alguma. Login é manual, por ele, no início de cada sessão; os agentes só abrem o
site e esperam. Pediu a remoção da senha de todos os arquivos.
- **Plataformas:** usa as três em paralelo, Claude Code para orquestração e 
engenharia, Codex para composições, descrições e planilhas, Antigravity para 
operar o navegador e observar o trabalho dele no Orçafascio 
(aprendizado por demonstração).
- **Conferência:** pede `git log` ao fim de cada bloco de trabalho para conferir
os commits, e pede que memória e perfil sejam atualizados com os resultados, 
incluindo o da CI (run 40987495070, verde na primeira execução).
- **Pendências que reservou para si:** trocar a senha do Orçafascio, decidir D2 
e D3 da spec, e gravar as primeiras sessões reais no Antigravity.

## Entrevista de maturidade e reestruturação (30/10/2026)

- **Como responde a entrevistas:** por voz, bloco a bloco, em mensagens curtas e com transcrição imperfeita. Quando uma pergunta volta repetida na transcrição sem resposta, é sinal de que ele não a respondeu, não de que concordou. Pedir confirmação em uma linha funciona bem: responde "sim" ou corrige.
- **Pede clareza quando a pergunta é vaga:** "você poderia ser mais explícito quanto a essas duas pendências". Prefere que cada pendência venha com o que precisa saber, as opções possíveis e o que muda com a resposta.
- **Decisões de domínio que fixou** (registro completo em `OrcaAI/knowledge/padroes/entrevista-maturidade-2026-10.md`): regime desonerado por padrão; cascata SINAPI-ES → DER-ES → SICRO → SP → RJ → MG → demais estados; composições novas sempre em SRAES-CP, séries antigas congeladas; data-base do mês da elaboração, revisão rebaseia; "orçamento enxuto" significa precisão de códigos e descrições; os agentes fazem planilha, composições e BDI antes do Orçafascio, que vira o lugar de montar e formalizar; conclusão do orçamento e envio ao processo só com o De acordo dele.
- **Qualidade que mais valoriza:** códigos e descrições 100% alinhados às tabelas de referência. Chamou isso de "ponto crítico do projeto de orçamento".
- **Organização:** quer etapas criadas sob demanda, sem pastas vazias; dois blocos claros, SRAES (trabalho profissional, padrão) e UFG (projeto final da pós em Agentes Inteligentes); repositório público porque envia links aos professores do curso.
- **Ferramentas:** usa o Maestri para ver as três plataformas lado a lado (terminais Batuta, Prumo e Sextante) e quer os documentos de referência também em PDF.
- **Ambiente local:** o venv passou a ser `.venv` na raiz do repositório; RStudio aberto sobre o perfil gerou um `.html` e um `.Rhistory` ao lado deste arquivo, que ficam fora do Git.

