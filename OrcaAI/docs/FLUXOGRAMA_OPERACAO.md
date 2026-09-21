# Fluxograma de Operacao da Central Orca

Use este arquivo como roteiro pratico para operar os agentes no Antigravity.

## Fluxo Geral

```mermaid
flowchart TD
    A["1. Criar projeto"] --> B["2. Colocar arquivos em 00-entrada"]
    B --> C["3. Rodar /novo-orcamento"]
    C --> D["4. Triagem e plano de execucao"]
    D --> E["5. Extrair escopo e quantitativos"]
    E --> F["6. Consultar bases oficiais"]
    F --> G{"Item encontrado?"}
    G -- "Sim" --> H["7. Compor custo"]
    G -- "Nao" --> I["8. Pesquisar mercado"]
    I --> J["9. Aprovacao humana"]
    J --> H
    H --> K["10. Calcular BDI e memoria"]
    K --> L["11. Validar SINAPI/IOPES"]
    L --> M["12. Guardrails e curva ABC"]
    M --> N{"Bloqueios criticos?"}
    N -- "Sim" --> O["Corrigir pendencias"]
    O --> L
    N -- "Nao" --> P["13. Gerar documentos"]
    P --> Q["14. Gerar dossie"]
    Q --> R["15. Revisao final"]
    R --> S["Pacote pronto para assinatura"]
```

## Roteiro de Uso

### 1. Criar projeto

```powershell
python scripts/criar_projeto_orca.py "2026-001-nome-do-servico"
```

### 2. Inserir arquivos

Coloque PDFs, DOCX, XLSX, imagens, plantas e propostas em:

```text
projetos/2026-001-nome-do-servico/00-entrada/
```

### 3. Iniciar agentes

No Antigravity, use:

```text
/novo-orcamento 2026-001-nome-do-servico
```

### 4. Consultar Orcafascio

Quando precisar consultar composicoes, use:

```text
/orcafascio consultar composicoes do projeto 2026-001-nome-do-servico
```

### 5. Pesquisar mercado

Quando nao houver base oficial adequada:

```text
/pesquisar-precos item sem referencia oficial
```

O fluxo deve parar para aprovacao humana antes de usar o preco.

### 6. Validar

```text
/validar-orcamento 2026-001-nome-do-servico
```

### 7. Gerar documentos

```text
/gerar-documentos 2026-001-nome-do-servico
```

### 8. Gerar dossie

```text
/gerar-dossie 2026-001-nome-do-servico
```

### 9. Revisao final

```text
/revisar-final 2026-001-nome-do-servico
```

## Pontos de Pausa Obrigatoria

- composicao propria;
- pesquisa de mercado;
- uso de base de outro estado;
- BDI excepcional;
- divergencia de unidade;
- pacote final para assinatura.

