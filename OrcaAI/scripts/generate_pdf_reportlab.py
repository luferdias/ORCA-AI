import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "INF/UFG — Pós-Graduação em Sistemas e Agentes Inteligentes | Empreendedorismo e Inovação")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(54, 793, 541, 793)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        
        self.drawString(54, 32, "Orca-AI — Entregável 3: TRL e Propriedade Intelectual (Luis Fernando Dias)")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 32, page_text)
        self.restoreState()

def build_pdf():
    target_dir = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca\OrcaAI"
    pdf_filename = os.path.join(target_dir, "Entregavel_3_TRL_e_PI_OrcaAI.pdf")
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    c_navy = colors.HexColor("#1B365D")
    c_slate = colors.HexColor("#2B547E")
    c_dark = colors.HexColor("#222222")
    
    style_subhdr = ParagraphStyle(
        'SubHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#7F8C8D"),
        spaceAfter=4
    )
    
    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_navy,
        spaceAfter=4
    )
    
    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_slate,
        spaceAfter=12
    )
    
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_slate,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    style_tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )

    style_tbl_hdr = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # Header block
    story.append(Paragraph("UNIVERSIDADE FEDERAL DE GOIÁS — INF/UFG | PÓS-GRADUAÇÃO EM SISTEMAS E AGENTES INTELIGENTES", style_subhdr))
    story.append(Paragraph("PROJETO INTEGRADOR — ENTREGÁVEL 3", style_title))
    story.append(Paragraph("Maturidade Tecnológica (TRL) e Estratégia de Propriedade Intelectual (PI) da Startup Orca-AI", style_subtitle))
    
    # Metadata Table
    meta_table_data = [
        [
            Paragraph("<b>Startup:</b> Orca-AI (Central de Engenharia de Custos Públicos)", style_body),
            Paragraph("<b>Equipe:</b> Luis Fernando Dias", style_body)
        ],
        [
            Paragraph("<b>Curso:</b> Pós-Graduação em Sistemas e Agentes Inteligentes (UFG)", style_body),
            Paragraph("<b>Data de Entrega:</b> 18/08/2026", style_body)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[270, 217])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8F9FA")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=c_navy, spaceBefore=4, spaceAfter=10))

    # Section 1
    story.append(Paragraph("1. Visão Geral e Arquitetura Tecnológica da Orca-AI", style_h1))
    story.append(Paragraph("A elaboração e a auditoria de orçamentos de obras e serviços de engenharia no setor público enfrentam gargalos históricos: morosidade na fase interna da licitação (processos que costumam levar de 3 a 6 meses), alta complexidade regulatória (estrito cumprimento da Lei nº 14.133/2021, Instrução Normativa SEGES/ME nº 65/2021 e Acórdãos do TCU) e constante risco de paralisação ou apontamentos de sobrepreço por órgãos de controle.", style_body))
    story.append(Paragraph("A <b>Orca-AI</b> foi concebida como uma plataforma GovTech de <b>Engenharia de Custos Públicos Assistida por Agentes Inteligentes (Agentic AI)</b>. O sistema combina a capacidade semântica e de raciocínio de Grandes Modelos de Linguagem (LLMs) com um motor determinístico de cálculo matemático e uma camada contínua de guardrails regulatórios, visando reduzir em até 80% o tempo de instrução processual com 100% de conformidade técnica.", style_body))

    story.append(Paragraph("1.1 Arquitetura Multiagente Especializada em Operação", style_h2))
    story.append(Paragraph("Com base nos testes rigorosos e na execução prática realizada no ambiente operacional do projeto (com validação em 11 escopos complexos de engenharia predial e infraestrutura — como limpeza robotizada de dutos HVAC, lavagem de fachadas pele de vidro, manutenção de grupos geradores, usinas fotovoltaicas solar, impermeabilização estrutural e trocas de cabos de elevadores), a Orca-AI organiza o trabalho por meio de papéis especializados:", style_body))

    agents_pdf = [
        ("intake-triage-agent (Agente de Triagem e Leitura):", " Recebe a demanda em múltiplos formatos (PDF, DWG, XLSX, DOCX), realiza a leitura técnica preliminar, extrai o escopo executivo, identifica quantitativos preliminares e aponta pendências de documentação."),
        ("project-planner (Agente Planejador):", " Mapeia o plano de trabalho do orçamento, define as etapas requeridas, identifica as bases referenciais obrigatórias e atribui tarefas aos agentes operacionais."),
        ("engenheiro-orcamentista-publico (Engenheiro Orçamentista Sênior):", " Analisa os critérios de medição, a codificação de serviços e o enquadramento metodológico conforme normas ABNT e diretrizes governamentais."),
        ("pesquisador-bases-oficiais (Pesquisador de Custos Públicos):", " Consulta e conecta-se automaticamente aos bancos referenciais oficiais obrigatórios: SINAPI (CAIXA), SICRO (DNIT) e IOPES (DER-ES), além de realizar integração via raspagem estruturada na plataforma Orçafascio."),
        ("compositor-custos (Compositor de CPUs):", " Monta analiticamente as Composições de Preços Unitários (CPUs), detalhando insumos de mão de obra, materiais, equipamentos e coeficientes de produtividade."),
        ("pesquisador-mercado (Pesquisador de Preços - IN 65/2021):", " Para itens não catalogados em bases oficiais, coleta e organiza cotações de fornecedores locais, aplicando critérios de média, mediana ou menor preço com expurgo de valores inexequíveis e validação humana obrigatória (Human-in-the-Loop)."),
        ("calculador-bdi-encargos (Engine Determinística de BDI e Encargos):", " Executa o cálculo exato da taxa de Bonificação e Despesas Indiretas (BDI) segundo o Acórdão TCU nº 2.622/2013, aplicando alíquotas tributárias municipais (ISS local) e segregando BDI de serviços e BDI diferenciado de fornecimento de materiais/equipamentos."),
        ("guardrail-controladoria (Guardião de Compliance):", " Audita a planilha orçamentária em tempo real contra riscos de sobrepreço, estancamento de quartis do TCU, duplicidade de insumos, ausência de memória de cálculo e distorções na Curva ABC."),
        ("documentalista-tecnico (Gerador Autônomo de Dossiês):", " Converte a estrutura de dados validada em peças formais editáveis e padronizadas (DFD, ETP, Termo de Referência, Especificação Técnica, Memoriais Descritivos, Justificativas de BDI e Despachos padronizados para autuação no SEI / e-Docs).")
    ]

    for title, desc in agents_pdf:
        story.append(Paragraph(f"• <b>{title}</b>{desc}", style_bullet))

    story.append(Spacer(1, 4))
    story.append(Paragraph("1.2 Mecanismo Híbrido: Separação entre Raciocínio (LLM) e Cálculo Determinístico", style_h2))

    callout_data = [[
        Paragraph(
            "<b>DIFERENCIAL TECNOLÓGICO: ZERO ALUCINAÇÃO FINANCEIRA</b><br/>"
            "Para eliminar 100% o risco de alucinação financeira (um problema crítico das LLMs convencionais), a Orca-AI adota uma arquitetura estritamente desacoplada:<br/>"
            "• As LLMs e Agentes são utilizados exclusivamente para compreensão de linguagem natural, extração de requisitos, navegação semântica e redação de documentos técnicos.<br/>"
            "• Toda a matemática orçamentária (multiplicações de quantitativos, composição de custos unitários, aplicação de encargos sociais, fórmulas analíticas de BDI e montagem da Curva ABC) é executada por um Motor Determinístico em Python (OpenPyXL / Pandas). Nenhuma operação aritmética é realizada via geração de texto pela IA.",
            style_body
        )
    ]]
    t_callout = Table(callout_data, colWidths=[487])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINELEFT', (0, 0), (0, 0), 4, c_navy),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 8))

    # Section 2
    story.append(Paragraph("2. Autoavaliação do Technology Readiness Level (TRL)", style_h1))
    story.append(Paragraph("A avaliação do nível de maturidade tecnológica da Orca-AI foi realizada considerando o sistema completo: orquestrador multiagente, motor determinístico, base de conhecimento técnico, integração com tabelas oficiais de custos e módulo de guardrails regulatórios.", style_body))

    trl_headers = [Paragraph("TRL", style_tbl_hdr), Paragraph("Critério Objetivo de Avaliação", style_tbl_hdr), Paragraph("Status", style_tbl_hdr), Paragraph("Evidências Práticas no Ecossistema Orca-AI", style_tbl_hdr)]
    trl_data = [trl_headers]

    trl_rows_pdf = [
        ("1", "Os princípios tecnológicos necessários à solução foram identificados e estudados?", "Sim", "Estudo dos fundamentos de Agentic AI, LLMs, engenharia de custos públicos (Lei 14.133/2021, Acórdão TCU 2.622/2013) e validações determinísticas."),
        ("2", "A aplicação da IA e dos agentes inteligentes à engenharia de custos públicos foi formulada de maneira estruturada?", "Sim", "Formulação da arquitetura multiagente com divisão de papéis (Triagem, Planejador, Orçamentista, Pesquisador, Auditor, Documentalista)."),
        ("3", "As funções críticas da solução foram demonstradas por provas de conceito?", "Sim", "PoCs isoladas demonstrando leitura de especificações, busca de códigos SINAPI/IOPES, cálculo de BDI e geração automática de trechos de Termos de Referência."),
        ("4", "Os principais componentes foram integrados e testados em ambiente controlado?", "Sim", "Integração do motor determinístico em Python com a camada de agentes e scripts de geração de planilhas e minutas textuais."),
        ("5", "O protótipo integrado foi testado com dados representativos do contexto real de engenharia de custos?", "Sim", "Validação completa com dados orçamentários reais de manutenção predial e infraestrutura (HVAC, Geradores, Lavagem Envidraçada, Impermeabilização, Fotovoltaica)."),
        ("6", "Existe protótipo funcional com os principais componentes integrados e testados em condições próximas ao ambiente operacional pretendido?", "Sim", "Protótipo completo operando com 11 escopos reais do MGI/SRA-ES, gerando planilhas .xlsx validadas, memórias de cálculo auditáveis e dossiês em .docx/.pdf."),
        ("7", "O sistema completo já opera como piloto incorporado ao fluxo real de trabalho de usuários finais?", "Não", "O sistema opera em ambiente computacional simulado e representativo; necessita de implantação piloto integrada à rotina diária de engenheiros de órgãos públicos."),
        ("8", "O sistema foi qualificado e está pronto para implantação regular junto aos clientes?", "Não", "Requer homologação final de interoperabilidade (conectores com SEI/e-Docs) e testes de estabilidade sob carga de múltiplos órgãos simultâneos."),
        ("9", "A tecnologia possui operação comercial consolidada e repetível em condições reais?", "Não", "Necessita de histórico comercial contínuo, contratos recorrentes SaaS GovTech e operação em escala nacional.")
    ]

    for num, crit, stat, evid in trl_rows_pdf:
        st_color = "#27AE60" if stat == "Sim" else "#C0392B"
        trl_data.append([
            Paragraph(f"<b>{num}</b>", style_tbl_cell),
            Paragraph(crit, style_tbl_cell),
            Paragraph(f"<font color='{st_color}'><b>{stat}</b></font>", style_tbl_cell),
            Paragraph(evid, style_tbl_cell)
        ])

    t_trl = Table(trl_data, colWidths=[30, 160, 45, 252])
    t_trl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor("#E6F0FA")), # Highlight TRL 6 row
    ]))
    story.append(t_trl)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Resultado da Autoavaliação: TRL 6 — Protótipo Funcional Demonstrado em Ambiente Operacional Relevante.</b>", ParagraphStyle('ResTRL', parent=style_body, fontName='Helvetica-Bold', fontSize=10, textColor=c_navy)))

    story.append(Spacer(1, 8))

    # Section 3
    story.append(Paragraph("3. Avaliação do TRL e Roadmap Técnico-Operacional", style_h1))
    story.append(Paragraph("3.1 Justificativa Consolidada do TRL 6", style_h2))
    story.append(Paragraph("A Orca-AI encontra-se em <b>TRL 6</b> porque possui uma arquitetura completamente integrada e testada com dados representativos de demandas reais de engenharia pública. A solução foi validada no processamento de 11 contratações complexas da Administração Pública Federal (SRA/MGI-ES), demonstrando capacidade de:", style_body))

    story.append(Paragraph("• Processar descrições e extrair quantitativos de serviços complexos;", style_bullet))
    story.append(Paragraph("• Consultar e associar códigos oficiais SINAPI, SICRO e IOPES com exatidão;", style_bullet))
    story.append(Paragraph("• Calcular analiticamente o BDI e os encargos sociais sem erros de arredondamento ou alucinação;", style_bullet))
    story.append(Paragraph("• Executar varredura de compliance através de guardrails de sobrepreço;", style_bullet))
    story.append(Paragraph("• Gerar automaticamente a documentação instrutória editável (.xlsx, .docx, .pdf) pronta para autuação.", style_bullet))

    story.append(Paragraph("Contudo, o avanço para <b>TRL 7</b> exige formalmente que a tecnologia seja incorporada de maneira contínua ao fluxo real de trabalho de engenheiros e servidores públicos no exercício regular de suas funções, em um projeto-piloto em ambiente operacional efetivo.", style_body))

    story.append(Paragraph("3.2 Plano de Ação e Roadmap para Alcançar o TRL 7 (Projeto-Piloto)", style_h2))
    story.append(Paragraph("O próximo objetivo estratégico da Orca-AI é a execução de um <b>Projeto-Piloto Controlado em Ambiente Real (TRL 7)</b> nos próximos 6 meses. O piloto será realizado em parceria com órgãos públicos demandantes (como a Secretaria Regional de Administração do MGI no Espírito Santo - SRA/MGI-ES ou Prefeituras municipais).", style_body))

    story.append(Paragraph("<b>Diretrizes e Indicadores de Desempenho (KPIs) para a Declaração do TRL 7:</b>", style_body))

    kpis_pdf = [
        ("Precisão e Rastreabilidade Financeira:", " Mapear divergências entre os valores gerados pela Orca-AI e a auditoria humana final (Meta: 0% de erro de cálculo e 100% de rastreabilidade de insumos)."),
        ("Redução do Tempo de Instrução Processual:", " Mensurar o tempo economizado na montagem do dossiê de licitação (Meta: redução do tempo médio de elaboração de 30 dias para menos de 4 horas por processo)."),
        ("Taxa de Intervenção Humana (HITL):", " Registrar a frequência e o tipo de ajustes manuais necessários durante a atuação dos agentes orçamentistas."),
        ("Desempenho dos Guardrails:", " Quantificar a taxa de detecção prévia de sobrepreço, alíquotas incorretas de ISS e inconsistências de BDI antes da submissão do processo aos órgãos de controle (TCU/CGU)."),
        ("Integração com Sistemas de Governo:", " Validar o funcionamento dos conectores automáticos para exportação de despachos e peças formais diretamente para o SEI e e-Docs.")
    ]

    for title, desc in kpis_pdf:
        story.append(Paragraph(f"✔ <b>{title}</b>{desc}", style_bullet))

    story.append(Paragraph("<i>Nota Metodológica: O avanço para o TRL 7 somente será declarado após a existência de um relatório formal com evidências documentadas de operação real, continuada e repetível por usuários finais do setor público.</i>", ParagraphStyle('NoteM', parent=style_body, fontSize=8.5, textColor=colors.HexColor("#C0392B"))))

    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. Estratégia de Proteção da Propriedade Intelectual (PI)", style_h1))
    story.append(Paragraph("Para assegurar o domínio tecnológico, proteger o valuation da startup e criar barreiras de entrada efetivas em um mercado de alta complexidade regulatória, a Orca-AI adota uma <b>Estratégia Híbrida e Multicamadas de Proteção da Propriedade Intelectual</b>:", style_body))

    ip_hdr_pdf = [Paragraph("Ativo Estratégico", style_tbl_hdr), Paragraph("Proteção Proposta", style_tbl_hdr), Paragraph("Justificativa Técnica e Estratégica", style_tbl_hdr)]
    ip_data = [ip_hdr_pdf]

    ip_rows_pdf = [
        ("Código-Fonte da Engine Agentic AI Orca-AI", "Registro de Software no INPI (Lei 9.609/98)", "Constitui o núcleo computacional da plataforma (scripts Python, orquestradores de agentes, conectores de bases de dados e compiladores). O registro no INPI assegura comprovação formal de autoria, titularidade e segurança jurídica para investimentos e licitações."),
        ("Módulos de Dossiês, Guardrails e BDI", "Registro de Programa de Computador no INPI", "Protege as rotinas específicas de verificação de regras (G-01 a G-10), o motor de cálculo analítico de BDI e os geradores de documentos em DOCX/PDF."),
        ("Método Híbrido de Validação Multiagente", "Avaliação de Patente de Invenção (Lei 9.279/96)", "Caso demonstrada novidade, atividade inventiva e aplicação industrial no método de coordenação entre IA semântica e motor determinístico com guardrails, será realizado o depósito de patente antes de qualquer publicação acadêmica detalhada."),
        ("Prompts de Sistema, Grafo de Agentes e Heurísticas", "Segredo de Negócio / Trade Secret (Lei 9.279/96)", "A sintaxe refinada dos prompts de controle de alucinação, as regras de ponderação de cotações e a lógica de exceções dos agentes serão mantidas em estrito segredo comercial protegidas por NDAs rígidos."),
        ("Normalização e Associação das Bases Oficiais", "Segredo de Negócio sobre a Implementação", "As tabelas SINAPI, SICRO e IOPES são públicas; o diferencial protegível reside na arquitetura proprietária de ETL, higienização, mapeamento semântico e histórico temporal de insumos desenvolvido pela Orca-AI."),
        ("Marca Comercial 'Orca-AI' e 'Orca Intelligence'", "Registro de Marca no INPI (Lei 9.279/96)", "Depósito de marca nominativa e mista na classe NCL(12) 42 (Serviços de Tecnologia e Software SaaS GovTech), assegurando a exclusividade de uso comercial e identidade da marca.")
    ]

    for ativo, prot, just in ip_rows_pdf:
        ip_data.append([
            Paragraph(f"<b>{ativo}</b>", style_tbl_cell),
            Paragraph(f"<b>{prot}</b>", style_tbl_cell),
            Paragraph(just, style_tbl_cell)
        ])

    t_ip = Table(ip_data, colWidths=[120, 120, 247])
    t_ip.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ip)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.1 Governança da PI e Mitigação de Riscos Legal-Tecnológicos", style_h2))

    gov_pdf = [
        ("Acordos de Confidencialidade (NDA) e Cessão de Direitos:", " Todos os desenvolvedores, pesquisadores da UFG e prestadores de serviço assinam termos formais de cessão total dos direitos patrimoniais de PI para a empresa Orca-AI, acompanhados de cláusulas de não competição."),
        ("Conformidade com Licenças Open-Source:", " A infraestrutura utiliza apenas componentes de código aberto com licenças permissivas (MIT, Apache 2.0, BSD), garantindo a ausência de licenças copyleft virais (como GPL v3) que pudessem forçar a abertura do código proprietário."),
        ("Rastreabilidade das Fontes Públicas:", " A solução não se apropria de bases públicas de terceiros (SINAPI/SICRO/IOPES), mas sim protege a camada computacional de inteligência, organização e integração agregada.")
    ]
    for title, desc in gov_pdf:
        story.append(Paragraph(f"▪ <b>{title}</b>{desc}", style_bullet))

    story.append(Spacer(1, 8))

    # Section 5
    story.append(Paragraph("5. Síntese Executiva", style_h1))
    story.append(Paragraph("A <b>Orca-AI</b> consolida sua maturidade no nível <b>TRL 6</b>, apresentando um protótipo perfeitamente integrado e exaustivamente testado com dados reais e complexos de engenharia de custos públicos. A plataforma soluciona gargalos críticos do setor ao unir a inteligência semântica de sistemas multiagentes à precisão inegociável de motores determinísticos e à rigorosa governança de guardrails de compliance.", style_body))
    story.append(Paragraph("O roadmap estratégico direciona os esforços imediatos para a realização de um <b>projeto-piloto em ambiente operacional real junto a órgãos públicos (TRL 7)</b>, validando a tecnologia na rotina diária de servidores e medindo conclusivamente os ganhos de produtividade e a redução do tempo de instrução licitatória.", style_body))
    story.append(Paragraph("Acompanhando a maturidade tecnológica, a <b>Estratégia de Propriedade Intelectual da Orca-AI</b> combina o registro formal do software e da marca no INPI com a preservação de inteligência estratégica sob a forma de segredos de negócio e a avaliação criteriosa de patentes. Essa abordagem holística assegura a blindagem jurídica, atrai investidores e estabelece uma base sólida para a escala comercial da GovTech no mercado brasileiro.", style_body))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF gerado com sucesso em: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
