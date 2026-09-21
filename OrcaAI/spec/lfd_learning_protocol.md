# Protocolo de Aprendizado por Demonstração (LfD)
## Interação Híbrida OrcaAI - Orçafascio Web

---

## 1. Visão Geral do Protocolo

O protocolo de **Aprendizado por Demonstração (*Learning from Demonstration - LfD*)** permite que o OrcaAI absorva o raciocínio prático e as escolhas do engenheiro no software Orçafascio antes de operar de modo autônomo. Isso elimina alucinações de dados e garante total alinhamento às preferências do órgão.

```mermaid
sequenceDiagram
    autonumber
    actor Eng as Engenheiro (MGI-ES)
    participant OF as Orçafascio Web
    participant Orca as OrcaAI (Agente 3 - Pilot)
    participant Mem as Memória de Padrões do Projeto
    participant Guard as Agente 9 (Auditor)

    Note over Eng,OF: FASE 1: Operação Guiada (Aprendizado)
    Eng->>OF: Faz login (mgi.sra-es.serl@gestao.gov.br)
    Eng->>OF: Digita termo de busca / Seleciona SINAPI-ES
    Eng->>OF: Escolhe CPU analítica e ajusta quantidade
    Orca->>OF: Observa cliques, seleções e filtros aplicados
    Orca->>Mem: Registra padrão: termo_busca -> codigo_selecionado -> ratio_coeficiente
    
    Note over Eng,Orca: FASE 2: Transição de Autonomia
    Orca->>Eng: "Padrão de 5 itens assimilado. Posso assumir os próximos 15 itens?"
    Eng-->>Orca: Autorização concedida

    Note over Orca,OF: FASE 3: Navegação Autônoma Supervisionada
    Orca->>OF: Executa navegação direta, busca termos e insere composições
    Orca->>Guard: Submete código para validação contra banco local
    alt Código Oficial Válido
        Guard-->>Orca: Aprovado
        Orca->>OF: Grava item na planilha
    else Insumo Não Encontrado
        Orca->>Eng: PAUSA OBRIGATÓRIA: Dispara Agente 4 (Pesquisa de Mercado)
    end
```

---

## 2. As Três Fases da Operação

### Fase 1: Co-Pilot & Gravação de Demonstração
1. O engenheiro abre o navegador e acessa o [Orçafascio](https://app.orcafascio.com/).
2. O OrcaAI ativa o `OrcafascioPilot` em modo observador passivo.
3. Para cada ação do engenheiro, o sistema registra:
   - Base de dados utilizada (`SINAPI`, `IOPES`, `ORSE`, etc.).
   - Estado/Praça selecionada (`Espírito Santo`, `Vitória`).
   - Termo de consulta digitado no campo de busca.
   - Código selecionado e tipo da composição (sintética ou analítica).
   - Quantitativo e eventual ajuste de produtividade ou perdas.
   - Percentual de BDI aplicado na tela.

### Fase 2: Assimilação e Síntese de Padrão
1. O OrcaAI constrói uma matriz de correspondência entre o escopo descrito no memorial e as composições escolhidas.
2. O sistema gera um resumo de calibração:
   - Taxa de desoneração detectada (Não Desonerado por padrão).
   - Famílias de composições prioritárias (ex: 88xxx para alvenaria/pintura, 98xxx para instalações).
   - Validação de que não houve desvios de BDI (travado em 25%).

### Fase 3: Operação Autônoma com Trava de Segurança
1. O OrcaAI assume a inserção dos itens subsequentes da EAP no Orçafascio Web via automação de browser.
2. **Garantia Anti-Alucinação**:
   - Cada código selecionado na automação é validado em microssegundos contra as tabelas oficiais locais (`bases/`).
   - Se o Orçafascio retornar resultado duvidoso ou se a base oficial não tiver o serviço exato, a automação **interrompe a digitação** e emite alerta com solicitação de validação humana.
