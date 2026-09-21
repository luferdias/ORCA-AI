---
name: orcafascio-mgi-automation
description: Procedimentos de navegação autônoma na plataforma Web do Orçafascio usando o browser_subagent e as credenciais oficias MGI-ES.
---
# Automação Orçafascio - MGI-ES

## 1. Diretriz de Operação
Você tem autonomia para interagir via interface web diretamente na plataforma **Orçafascio** ativando a ferramenta de `browser_subagent`, reproduzindo os cliques de um usuário real.

## 2. Credenciais de Acesso SRA-ES
- **URL Alvo:** `https://app.orcafascio.com/`
- **Login:** `mgi.sra-es.serl@gestao.gov.br`
- **Senha:** `SRAES@2025`

## 3. Regras de Preenchimento Web
1. **Autenticação:** Abra a URL, direcione o foco aos campos de E-mail e Senha e efetue o Login.
2. **Setup do Projeto/Busca:** No seletor de tabelas ou buscas de novos insumos/serviços, selecione impreterivelmente o **mês/ano mais recente** disponível para garantir a atualização monetária exigida pelo TCU e configure a localidade para a Base do Espírito Santo.
3. **BDI:** O BDI embutido na aplicação de relatórios deve ser travado em exatos **25%**.
4. **Acionamento de Gatilhos:** Caso não encontre de forma alguma o item desejado dentro da base local Vitória, recrute a skill correlata para formação e **obrigatóriamente notifique o usuário para validação antes de inserir qualquer preço próprio manual na tela**.

## 4. Inserção de CPs via Interface
Ao receber do usuário a aprovação para inserir uma nova composição ou insumo customizado via web, preste absoluta atenção ao campo de "Código" na interface HTML. Digite o identificador iniciado por `SRAES-...`.
