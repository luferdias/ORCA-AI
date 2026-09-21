# Comandos de Terminal para Operar a Central Orca

Este roteiro considera Windows PowerShell e a pasta `Orca` criada dentro do projeto `Orcamento_de_Obra`.

> Ajuste o nome do projeto conforme o servico real.

## 0. Entrar na pasta Orca

```powershell
cd "C:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca"
```

## 1. Validar se a estrutura da Central Orca esta correta

```powershell
python scripts\validar_estrutura_orca.py
```

Resultado esperado:

```text
Estrutura Orca OK.
```

## 2. Configurar variaveis do Orcafascio

```powershell
Copy-Item .env.example .env
notepad .env
```

Preencha no arquivo `.env`:

```text
ORCAFASCIO_URL=https://app.orcafascio.com/
ORCAFASCIO_LOGIN=seu_login
ORCAFASCIO_PASSWORD=sua_senha
ORCA_DEFAULT_UF=ES
ORCA_DEFAULT_MUNICIPIO=Vitoria
ORCA_DEFAULT_BDI_SERVICO=25.00
```

## 3. Criar um novo projeto de orcamento

Exemplo para limpeza robotizada de ar condicionado:

```powershell
python scripts\criar_projeto_orca.py "2026-001-limpeza-hvac"
```

Exemplo para pintura externa:

```powershell
python scripts\criar_projeto_orca.py "2026-002-pintura-externa"
```

Exemplo para impermeabilizacao:

```powershell
python scripts\criar_projeto_orca.py "2026-003-impermeabilizacao"
```

## 4. Definir uma variavel com o nome do projeto

Use o mesmo slug criado no passo anterior:

```powershell
$PROJETO = "2026-001-limpeza-hvac"
```

## 5. Abrir a pasta de entrada para colocar documentos

```powershell
explorer ".\projetos\$PROJETO\00-entrada"
```

Coloque nessa pasta:

- PDF;
- DOCX;
- XLSX;
- plantas;
- fotos;
- propostas;
- memorias;
- exportacoes antigas do Orcafascio.

## 6. Conferir os arquivos de entrada

```powershell
Get-ChildItem ".\projetos\$PROJETO\00-entrada"
```

## 7. Abrir os arquivos de controle do projeto

```powershell
notepad ".\projetos\$PROJETO\projeto.md"
notepad ".\projetos\$PROJETO\plano-execucao.md"
notepad ".\projetos\$PROJETO\log-decisoes.md"
```

## 8. Operar os agentes no Antigravity

Os comandos abaixo nao sao do terminal PowerShell. Eles devem ser digitados no chat/comando do Antigravity com a pasta `Orca` aberta.

### 8.1 Abrir a demanda

```text
/novo-orcamento 2026-001-limpeza-hvac
```

### 8.2 Consultar Orcafascio

```text
/orcafascio consultar composicoes para o projeto 2026-001-limpeza-hvac
```

### 8.3 Pesquisar precos, se faltar base oficial

```text
/pesquisar-precos item sem base oficial no projeto 2026-001-limpeza-hvac
```

### 8.4 Validar orcamento

```text
/validar-orcamento 2026-001-limpeza-hvac
```

### 8.5 Gerar especificacao tecnica e documentos

```text
/gerar-documentos 2026-001-limpeza-hvac
```

### 8.6 Gerar dossie final

```text
/gerar-dossie 2026-001-limpeza-hvac
```

### 8.7 Revisar antes da assinatura

```text
/revisar-final 2026-001-limpeza-hvac
```

## 9. Verificar pastas produzidas depois dos agentes

Volte ao terminal e rode:

```powershell
Get-ChildItem ".\projetos\$PROJETO" -Recurse
```

## 10. Gerar indice do dossie pelo terminal

```powershell
python scripts\gerar_indice_dossie.py $PROJETO
```

Arquivo gerado:

```text
projetos/2026-001-limpeza-hvac/indice-dossie.md
```

## 11. Abrir documentos finais

```powershell
explorer ".\projetos\$PROJETO\06-documentos"
explorer ".\projetos\$PROJETO\07-assinados"
notepad ".\projetos\$PROJETO\indice-dossie.md"
```

## 12. Rodar validacao final da estrutura

```powershell
python scripts\validar_estrutura_orca.py
```

## 13. Compactar o projeto final

```powershell
Compress-Archive -Path ".\projetos\$PROJETO" -DestinationPath ".\output\$PROJETO.zip" -Force
```

## 14. Abrir o pacote final

```powershell
explorer ".\output"
```

## Sequencia Resumida

```powershell
cd "C:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca"
python scripts\validar_estrutura_orca.py
Copy-Item .env.example .env
notepad .env
python scripts\criar_projeto_orca.py "2026-001-limpeza-hvac"
$PROJETO = "2026-001-limpeza-hvac"
explorer ".\projetos\$PROJETO\00-entrada"
Get-ChildItem ".\projetos\$PROJETO\00-entrada"
```

Depois, no Antigravity:

```text
/novo-orcamento 2026-001-limpeza-hvac
/orcafascio consultar composicoes para o projeto 2026-001-limpeza-hvac
/pesquisar-precos item sem base oficial no projeto 2026-001-limpeza-hvac
/validar-orcamento 2026-001-limpeza-hvac
/gerar-documentos 2026-001-limpeza-hvac
/gerar-dossie 2026-001-limpeza-hvac
/revisar-final 2026-001-limpeza-hvac
```

E finalize no terminal:

```powershell
python scripts\gerar_indice_dossie.py $PROJETO
Compress-Archive -Path ".\projetos\$PROJETO" -DestinationPath ".\output\$PROJETO.zip" -Force
explorer ".\output"
```

