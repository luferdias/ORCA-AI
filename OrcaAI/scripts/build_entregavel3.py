import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color_hex="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{color_hex}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color_hex}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color_hex}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def make_callout(doc, text_p_list, title=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Set left border thick navy, others none
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(4)
    p0.paragraph_format.line_spacing = 1.15
    if title:
        run_t = p0.add_run(title + "\n")
        run_t.bold = True
        run_t.font.name = 'Calibri'
        run_t.font.size = Pt(11)
        run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    for idx, item in enumerate(text_p_list):
        if idx == 0 and not title:
            p = p0
        else:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
        
        run = p.add_run(item)
        run.font.name = 'Calibri'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # spacing after callout
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def build_docx():
    target_dir = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca\OrcaAI"
    docx_filename = os.path.join(target_dir, "Entregavel_3_TRL_e_PI_OrcaAI.docx")
    
    doc = Document()
    
    # Page Margins 2.5 cm
    for section in doc.sections:
        section.top_margin = Inches(0.98)
        section.bottom_margin = Inches(0.98)
        section.left_margin = Inches(0.98)
        section.right_margin = Inches(0.98)
        
        # Header / Footer setup
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Orca-AI | Projeto Integrador — Entregável 3 (TRL e Propriedade Intelectual)")
        f_run.font.name = 'Calibri'
        f_run.font.size = Pt(9)
        f_run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Document Header Box / Title Area
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_after = Pt(2)
    run_hdr0 = p_hdr.add_run("UNIVERSIDADE FEDERAL DE GOIÁS — INF/UFG\n")
    run_hdr0.font.size = Pt(9.5)
    run_hdr0.font.bold = True
    run_hdr0.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)
    
    run_hdr1 = p_hdr.add_run("PÓS-GRADUAÇÃO EM SISTEMAS E AGENTES INTELIGENTES\n")
    run_hdr1.font.size = Pt(9.5)
    run_hdr1.font.bold = True
    run_hdr1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    run_hdr2 = p_hdr.add_run("DISCIPLINA: EMPREENDEDORISMO E GESTÃO DA INOVAÇÃO")
    run_hdr2.font.size = Pt(9)
    run_hdr2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run("PROJETO INTEGRADOR — ENTREGÁVEL 3")
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(22)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Maturidade Tecnológica (TRL) e Estratégia de Propriedade Intelectual (PI) da Startup Orca-AI")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(14)
    run_sub.font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    
    # Metadata Block Table
    tbl_meta = doc.add_table(rows=2, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_meta, "E0E0E0")
    
    meta_data = [
        [("Startup:", " Orca-AI (Central de Engenharia de Custos Públicos)"), ("Equipe:", " Luis Fernando Dias")],
        [("Curso:", " Pós-Graduação em Sistemas e Agentes Inteligentes - UFG"), ("Data:", " 18/08/2026")]
    ]
    for r_idx, row in enumerate(meta_data):
        for c_idx, (label, val) in enumerate(row):
            cell = tbl_meta.cell(r_idx, c_idx)
            set_cell_background(cell, "F8F9FA")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r1 = p.add_run(label)
            r1.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            r2 = p.add_run(val)
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 1
    h1 = doc.add_heading("1. Visão Geral e Arquitetura Tecnológica da Orca-AI", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.runs[0].font.size = Pt(15)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("A elaboração e a auditoria de orçamentos de obras e serviços de engenharia no setor público enfrentam gargalos históricos: morosidade na fase interna da licitação (processos que costumam levar de 3 a 6 meses), alta complexidade regulatória (estrito cumprimento da Lei nº 14.133/2021, Instrução Normativa SEGES/ME nº 65/2021 e Acórdãos do TCU) e constante risco de paralisação ou apontamentos de sobrepreço por órgãos de controle.")
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("A ")
    r_bold = p.add_run("Orca-AI")
    r_bold.bold = True
    p.add_run(" foi concebida como uma plataforma GovTech de ")
    p.add_run("Engenharia de Custos Públicos Assistida por Agentes Inteligentes (Agentic AI)").bold = True
    p.add_run(". O sistema combina a capacidade semântica e de raciocínio de Grandes Modelos de Linguagem (LLMs) com um motor determinístico de cálculo matemático e uma camada contínua de guardrails regulatórios, visando reduzir em até 80% o tempo de instrução processual com 100% de conformidade técnica.")

    h2 = doc.add_heading("1.1 Arquitetura Multiagente Especializada em Operação", level=2)
    h2.runs[0].font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    h2.runs[0].font.size = Pt(12.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Com base nos testes rigorosos e na execução prática realizada no ambiente operacional do projeto (com validação em 11 escopos complexos de engenharia predial e infraestrutura — como limpeza robotizada de dutos HVAC, lavagem de fachadas pele de vidro, manutenção de grupos geradores, usinas fotovoltaicas solar, impermeabilização estrutural e trocas de cabos de elevadores), a Orca-AI organiza o trabalho por meio de papéis especializados:")

    agents = [
        ("intake-triage-agent (Agente de Triagem e Leitura):", " Recebe a demanda em múltiplos formatos (PDF, DWG, XLSX, DOCX), realiza a leitura técnica preliminar, extrai o escopo executivo, identifica quantitativos preliminares e aponta pendências de documentação."),
        ("project-planner (Agente Planejador):", " Mapeia o plano de trabalho do orçamento, define as etapas requeridas, identifica as bases referenciais obrigatorias e atribui tarefas aos agentes operacionais."),
        ("engenheiro-orcamentista-publico (Engenheiro Orçamentista Sênior):", " Analisa os critérios de medição, a codificação de serviços e o enquadramento metodológico conforme normas ABNT e diretrizes governamentais."),
        ("pesquisador-bases-oficiais (Pesquisador de Custos públicos):", " Consulta e conecta-se automaticamente aos bancos referenciais oficiais obrigatórios: SINAPI (CAIXA), SICRO (DNIT) e IOPES (DER-ES), além de realizar integração via raspagem estruturada na plataforma Orçafascio."),
        ("compositor-custos (Compositor de CPUs):", " Monta analiticamente as Composições de Preços Unitários (CPUs), detalhando insumos de mão de obra, materiais, equipamentos e coeficientes de produtividade."),
        ("pesquisador-mercado (Pesquisador de Preços - IN 65/2021):", " Para itens não catalogados em bases oficiais, coleta e organiza cotações de fornecedores locais, aplicando critérios de média, mediana ou menor preço com expurgo de valores inexequíveis e validação humana obrigatória (Human-in-the-Loop)."),
        ("calculador-bdi-encargos (Engine Determinística de BDI e Encargos):", " Executa o cálculo exato da taxa de Bonificação e Despesas Indiretas (BDI) segundo o Acórdão TCU nº 2.622/2013, aplicando alíquotas tributárias municipais (ISS local) e segregando BDI de serviços e BDI diferenciado de fornecimento de materiais/equipamentos."),
        ("guardrail-controladoria (Guardião de Compliance):", " Audita a planilha orçamentária em tempo real contra riscos de sobrepreço, estancamento de quartis do TCU, duplicidade de insumos, ausência de memória de cálculo e distorções na Curva ABC."),
        ("documentalista-tecnico (Gerador Autônomo de Dossiês):", " Converte a estrutura de dados validada em peças formais editáveis e padronizadas (DFD, ETP, Termo de Referência, Especificação Técnica, Memoriais Descritivos, Justificativas de BDI e Despachos padronizados para autuação no SEI / e-Docs).")
    ]

    for title, desc in agents:
        p_ag = doc.add_paragraph()
        p_ag.paragraph_format.left_indent = Inches(0.2)
        p_ag.paragraph_format.space_after = Pt(3)
        p_ag.paragraph_format.line_spacing = 1.15
        r_bullet = p_ag.add_run("▪ ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_t = p_ag.add_run(title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_d = p_ag.add_run(desc)
        r_d.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    h2 = doc.add_heading("1.2 Mecanismo Híbrido: Separação entre Raciocínio (LLM) e Cálculo Determinístico", level=2)
    h2.runs[0].font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    h2.runs[0].font.size = Pt(12.5)

    make_callout(doc, [
        "Para eliminar 100% o risco de alucinação financeira (um problema crítico das LLMs convencionais), a Orca-AI adota uma arquitetura estritamente desacoplada:",
        "• As LLMs e Agentes são utilizados exclusivamente para compreensão de linguagem natural, extração de requisitos, navegação semântica e redação de documentos técnicos.",
        "• Toda a matemática orçamentária (multiplicações de quantitativos, composição de custos unitários, aplicação de encargos sociais, fórmulas analíticas de BDI e montagem da Curva ABC) é executada por um Motor Determinístico em Python (OpenPyXL / Pandas). Nenhuma operação aritmética é realizada via geração de texto pela IA."
    ], title="DIFERENCIAL TECNOLÓGICO: ZERO ALUCINAÇÃO FINANCEIRA")

    # Section 2
    h1 = doc.add_heading("2. Autoavaliação do Technology Readiness Level (TRL)", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.runs[0].font.size = Pt(15)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("A avaliação do nível de maturidade tecnológica da Orca-AI foi realizada considerando o sistema completo: orquestrador multiagente, motor determinístico, base de conhecimento técnico, integração com tabelas oficiais de custos e módulo de guardrails regulatórios.")

    # TRL Table
    tbl_trl = doc.add_table(rows=10, cols=4)
    tbl_trl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_trl.autofit = False
    set_table_borders(tbl_trl, "D3D3D3")

    headers = ["TRL", "Critério Objetivo de Avaliação", "Status", "Evidências Práticas no Ecossistema Orca-AI"]
    hdr_cells = tbl_trl.rows[0].cells
    col_widths = [Inches(0.6), Inches(2.3), Inches(0.7), Inches(2.9)]

    for idx, title in enumerate(headers):
        hdr_cells[idx].width = col_widths[idx]
        set_cell_background(hdr_cells[idx], "1B365D")
        set_cell_margins(hdr_cells[idx], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    trl_rows = [
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

    for r_idx, (trl_num, crit, stat, evid) in enumerate(trl_rows, start=1):
        row_cells = tbl_trl.rows[r_idx].cells
        bg_color = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        if trl_num == "6":
            bg_color = "E6F0FA" # highlight current TRL 6

        for c_idx, text in enumerate([trl_num, crit, stat, evid]):
            cell = row_cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            if c_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            run = p.add_run(text)
            run.font.size = Pt(9)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            elif c_idx == 2:
                run.bold = True
                run.font.color.rgb = RGBColor(0x27, 0xAE, 0x60) if text == "Sim" else RGBColor(0xC0, 0x39, 0x2B)

    p_res = doc.add_paragraph()
    p_res.paragraph_format.space_before = Pt(10)
    p_res.paragraph_format.space_after = Pt(12)
    r_r1 = p_res.add_run("Resultado da Autoavaliação: ")
    r_r1.bold = True
    r_r1.font.size = Pt(12)
    r_r2 = p_res.add_run("TRL 6 — Protótipo Funcional Demonstrado em Ambiente Operacional Relevante.")
    r_r2.bold = True
    r_r2.font.size = Pt(12)
    r_r2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    # Section 3
    h1 = doc.add_heading("3. Avaliação do TRL e Roadmap Técnico-Operacional", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.runs[0].font.size = Pt(15)

    h2 = doc.add_heading("3.1 Justificativa Consolidada do TRL 6", level=2)
    h2.runs[0].font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    h2.runs[0].font.size = Pt(12.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("A Orca-AI encontra-se em ")
    p.add_run("TRL 6").bold = True
    p.add_run(" porque possui uma arquitetura completamente integrada e testada com dados representativos de demandas reais de engenharia pública. A solução foi validada no processamento de 11 contratações complexas da Administração Pública Federal (SRA/MGI-ES), demonstrando capacidade de:")
    
    items_trl6 = [
        "Processar descrições e extrair quantitativos de serviços complexos;",
        "Consultar e associar códigos oficiais SINAPI, SICRO e IOPES com exatidão;",
        "Calcular analiticamente o BDI e os encargos sociais sem erros de arredondamento ou alucinação;",
        "Executar varredura de compliance através de guardrails de sobrepreço;",
        "Gerar automaticamente a documentação instrutória editável (.xlsx, .docx, .pdf) pronta para autuação."
    ]
    for item in items_trl6:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.left_indent = Inches(0.2)
        p_it.paragraph_format.space_after = Pt(3)
        p_it.paragraph_format.line_spacing = 1.15
        p_it.add_run("• ").bold = True
        p_it.add_run(item)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Contudo, o avanço para ")
    p.add_run("TRL 7").bold = True
    p.add_run(" exige formalmente que a tecnologia seja incorporada de maneira contínua ao fluxo real de trabalho de engenheiros e servidores públicos no exercício regular de suas funções, em um projeto-piloto em ambiente operacional efetivo.")

    h2 = doc.add_heading("3.2 Plano de Ação e Roadmap para Alcançar o TRL 7 (Projeto-Piloto)", level=2)
    h2.runs[0].font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    h2.runs[0].font.size = Pt(12.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("O próximo objetivo estratégico da Orca-AI é a execução de um ")
    p.add_run("Projeto-Piloto Controlado em Ambiente Real (TRL 7)").bold = True
    p.add_run(" nos próximos 6 meses. O piloto será realizado em parceria com órgãos públicos demandantes (como a Secretaria Regional de Administração do MGI no Espírito Santo - SRA/MGI-ES ou Prefeituras municipais).")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Diretrizes e Indicadores de Desempenho (KPIs) para a Declaração do TRL 7:").bold = True

    kpis = [
        ("Precisão e Rastreabilidade Financeira:", " Mapear divergências entre os valores gerados pela Orca-AI e a auditoria humana final (Meta: 0% de erro de cálculo e 100% de rastreabilidade de insumos)."),
        ("Redução do Tempo de Instrução Processual:", " Mensurar o tempo economizado na montagem do dossiê de licitação (Meta: redução do tempo médio de elaboração de 30 dias para menos de 4 horas por processo)."),
        ("Taxa de Intervenção Humana (HITL):", " Registrar a frequência e o tipo de ajustes manuais necessários durante a atuação dos agentes orçamentistas."),
        ("Desempenho dos Guardrails:", " Quantificar a taxa de detecção prévia de sobrepreço, alíquotas incorretas de ISS e inconsistências de BDI antes da submissão do processo aos órgãos de controle (TCU/CGU)."),
        ("Integração com Sistemas de Governo:", " Validar o funcionamento dos conectores automáticos para exportação de despachos e peças formais diretamente para o SEI e e-Docs.")
    ]
    for k_title, k_desc in kpis:
        p_k = doc.add_paragraph()
        p_k.paragraph_format.left_indent = Inches(0.2)
        p_k.paragraph_format.space_after = Pt(3)
        p_k.paragraph_format.line_spacing = 1.15
        r_k1 = p_k.add_run("✔ " + k_title)
        r_k1.bold = True
        r_k1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_k2 = p_k.add_run(k_desc)

    p_warn = doc.add_paragraph()
    p_warn.paragraph_format.space_before = Pt(6)
    p_warn.paragraph_format.space_after = Pt(10)
    p_warn.paragraph_format.line_spacing = 1.15
    r_w = p_warn.add_run("Nota Metodológica: ")
    r_w.bold = True
    r_w.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
    p_warn.add_run("O avanço para o TRL 7 somente será declarado após a existência de um relatório formal com evidências documentadas de operação real, continuada e repetível por usuários finais do setor público.")

    # Section 4
    h1 = doc.add_heading("4. Estratégia de Proteção da Propriedade Intelectual (PI)", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.runs[0].font.size = Pt(15)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Para assegurar o domínio tecnológico, proteger o valuation da startup e criar barreiras de entrada efetivas em um mercado de alta complexidade regulatória, a Orca-AI adota uma ")
    p.add_run("Estratégia Híbrida e Multicamadas de Proteção da Propriedade Intelectual").bold = True
    p.add_run(":")

    # IP Table
    tbl_ip = doc.add_table(rows=7, cols=3)
    tbl_ip.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ip.autofit = False
    set_table_borders(tbl_ip, "D3D3D3")

    ip_headers = ["Ativo Estratégico", "Proteção Proposta", "Justificativa Técnica e Estratégica"]
    ip_widths = [Inches(1.8), Inches(1.7), Inches(3.0)]

    for idx, title in enumerate(ip_headers):
        tbl_ip.rows[0].cells[idx].width = ip_widths[idx]
        set_cell_background(tbl_ip.rows[0].cells[idx], "1B365D")
        set_cell_margins(tbl_ip.rows[0].cells[idx], top=100, bottom=100, left=100, right=100)
        p = tbl_ip.rows[0].cells[idx].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ip_rows = [
        ("Código-Fonte da Engine Agentic AI Orca-AI", "Registro de Software no INPI (Lei 9.609/98)", "Constitui o núcleo computacional da plataforma (scripts Python, orquestradores de agentes, conectores de bases de dados e compiladores). O registro no INPI assegura comprovação formal de autoria, titularidade e segurança jurídica para investimentos e licitações."),
        ("Módulos de Dossiês, Guardrails e BDI", "Registro de Programa de Computador no INPI", "Protege as rotinas específicas de verificação de regras (G-01 a G-10), o motor de cálculo analítico de BDI e os geradores de documentos em DOCX/PDF."),
        ("Método Híbrido de Validação Multiagente", "Avaliação de Patente de Invenção (Lei 9.279/96)", "Caso demonstrada novidade, atividade inventiva e aplicação industrial no método de coordenação entre IA semântica e motor determinístico com guardrails, será realizado o depósito de patente antes de qualquer publicação acadêmica detalhada."),
        ("Prompts de Sistema, Grafo de Agentes e Heurísticas", "Segredo de Negócio / Trade Secret (Lei 9.279/96)", "A sintaxe refinada dos prompts de controle de alucinação, as regras de ponderação de cotações e a lógica de exceções dos agentes serão mantidas em estrito segredo comercial protegidas por NDAs rígidos."),
        ("Normalização e Associação das Bases Oficiais", "Segredo de Negócio sobre a Implementação", "As tabelas SINAPI, SICRO e IOPES são públicas; o diferencial protegível reside na arquitetura proprietária de ETL, higienização, mapeamento semântico e histórico temporal de insumos desenvolvido pela Orca-AI."),
        ("Marca Comercial 'Orca-AI' e 'Orca Intelligence'", "Registro de Marca no INPI (Lei 9.279/96)", "Depósito de marca nominativa e mista na classe NCL(12) 42 (Serviços de Tecnologia e Software SaaS GovTech), assegurando a exclusividade de uso comercial e identidade da marca.")
    ]

    for r_idx, (ativo, prot, just) in enumerate(ip_rows, start=1):
        row_cells = tbl_ip.rows[r_idx].cells
        bg_color = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"

        for c_idx, text in enumerate([ativo, prot, just]):
            cell = row_cells[c_idx]
            cell.width = ip_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(text)
            run.font.size = Pt(9)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            elif c_idx == 1:
                run.bold = True
                run.font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)

    h2 = doc.add_heading("4.1 Governança da PI e Mitigação de Riscos Legal-Tecnológicos", level=2)
    h2.runs[0].font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)
    h2.runs[0].font.size = Pt(12.5)

    gov_points = [
        ("Acordos de Confidencialidade (NDA) e Cessão de Direitos:", " Todos os desenvolvedores, pesquisadores da UFG e prestadores de serviço assinam termos formais de cessão total dos direitos patrimoniais de PI para a empresa Orca-AI, acompanhados de cláusulas de não competição."),
        ("Conformidade com Licenças Open-Source:", " A infraestrutura utiliza apenas componentes de código aberto com licenças permissivas (MIT, Apache 2.0, BSD), garantindo a ausência de licenças copyleft virais (como GPL v3) que pudessem forçar a abertura do código proprietário."),
        ("Rastreabilidade das Fontes Públicas:", " A solução não se apropria de bases públicas de terceiros (SINAPI/SICRO/IOPES), mas sim protege a camada computacional de inteligência, organização e integração agregada.")
    ]
    for g_title, g_desc in gov_points:
        p_g = doc.add_paragraph()
        p_g.paragraph_format.left_indent = Inches(0.2)
        p_g.paragraph_format.space_after = Pt(3)
        p_g.paragraph_format.line_spacing = 1.15
        p_g.add_run("▪ ").bold = True
        p_g.add_run(g_title).bold = True
        p_g.add_run(g_desc)

    # Section 5
    h1 = doc.add_heading("5. Síntese Executiva", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    h1.runs[0].font.size = Pt(15)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("A ")
    p.add_run("Orca-AI").bold = True
    p.add_run(" consolida sua maturidade no nível ")
    p.add_run("TRL 6").bold = True
    p.add_run(", apresentando um protótipo perfeitamente integrado e exaustivamente testado com dados reais e complexos de engenharia de custos públicos. A plataforma soluciona gargalos críticos do setor ao unir a inteligência semântica de sistemas multiagentes à precisão inegociável de motores determinísticos e à rigorosa governança de guardrails de compliance.")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("O roadmap estratégico direciona os esforços imediatos para a realização de um ")
    p.add_run("projeto-piloto em ambiente operacional real junto a órgãos públicos (TRL 7)").bold = True
    p.add_run(", validando a tecnologia na rotina diária de servidores e medindo conclusivamente os ganhos de produtividade e a redução do tempo de instrução licitatória.")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    p.add_run("Acompanhando a maturidade tecnológica, a ")
    p.add_run("Estratégia de Propriedade Intelectual da Orca-AI").bold = True
    p.add_run(" combina o registro formal do software e da marca no INPI com a preservação de inteligência estratégica sob a forma de segredos de negócio e a avaliação criteriosa de patentes. Essa abordagem holística assegura a blindagem jurídica, atrai investidores e estabelece uma base sólida para a escala comercial da GovTech no mercado brasileiro.")

    # Save DOCX
    doc.save(docx_filename)
    print(f"DOCX gerado com sucesso em: {docx_filename}")

def build_md():
    target_dir = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca\OrcaAI"
    md_filename = os.path.join(target_dir, "Entregavel_3_TRL_e_PI_OrcaAI.md")
    
    md_content = """# PROJETO INTEGRADOR — ENTREGÁVEL 3
## Avaliação de Maturidade Tecnológica (TRL) e Estratégia de Propriedade Intelectual (PI) da Startup Orca-AI

**Startup:** Orca-AI (Central de Engenharia de Custos e Orçamentos Públicos Assistida por Agentes Inteligentes)  
**Equipe:** Luis Fernando Dias  
**Curso:** Pós-Graduação em Sistemas e Agentes Inteligentes — INF/UFG  
**Disciplina:** Empreendedorismo e Gestão da Inovação  
**Data de Entrega:** 18/08/2026  

---

### 1. Visão Geral e Arquitetura Tecnológica da Orca-AI

#### 1.1 Contexto e Problema de Mercado
A elaboração e a auditoria de orçamentos de obras e serviços de engenharia no setor público enfrentam gargalos históricos: morosidade na fase interna da licitação (processos que costumam levar de 3 a 6 meses), alta complexidade regulatória (estrito cumprimento da Lei nº 14.133/2021, Instrução Normativa SEGES/ME nº 65/2021 e Acórdãos do TCU) e constante risco de paralisação ou apontamentos de sobrepreço por órgãos de controle.

A **Orca-AI** foi concebida como uma plataforma GovTech de **Engenharia de Custos Públicos Assistida por Agentes Inteligentes (Agentic AI)**. O sistema combina a capacidade semântica e de raciocínio de Grandes Modelos de Linguagem (LLMs) com um motor determinístico de cálculo matemático e uma camada contínua de guardrails regulatórios, visando reduzir em até 80% o tempo de instrução processual com 100% de conformidade técnica.

#### 1.2 Arquitetura Multiagente Especializada em Operação
Com base nos testes rigorosos e na execução prática realizada no ambiente operacional do projeto (com validação em 11 escopos complexos de engenharia predial e infraestrutura — como limpeza robotizada de dutos HVAC, lavagem de fachadas pele de vidro, manutenção de grupos geradores, usinas fotovoltaicas solar, impermeabilização estrutural e trocas de cabos de elevadores), a Orca-AI organiza o trabalho por meio de papéis especializados:

- **`intake-triage-agent` (Agente de Triagem e Leitura):** Recebe a demanda em múltiplos formatos (PDF, DWG, XLSX, DOCX), realiza a leitura técnica preliminar, extrai o escopo executivo, identifica quantitativos preliminares e aponta pendências de documentação.
- **`project-planner` (Agente Planejador):** Mapeia o plano de trabalho do orçamento, define as etapas requeridas, identifica as bases referenciais obrigatorias e atribui tarefas aos agentes operacionais.
- **`engenheiro-orcamentista-publico` (Engenheiro Orçamentista Sênior):** Analisa os critérios de medição, a codificação de serviços e o enquadramento metodológico conforme normas ABNT e diretrizes governamentais.
- **`pesquisador-bases-oficiais` (Pesquisador de Custos públicos):** Consulta e conecta-se automaticamente aos bancos referenciais oficiais obrigatórios: SINAPI (CAIXA), SICRO (DNIT) e IOPES (DER-ES), além de realizar integração via raspagem estruturada na plataforma Orçafascio.
- **`compositor-custos` (Compositor de CPUs):** Monta analiticamente as Composições de Preços Unitários (CPUs), detalhando insumos de mão de obra, materiais, equipamentos e coeficientes de produtividade.
- **`pesquisador-mercado` (Pesquisador de Preços - IN 65/2021):** Para itens não catalogados em bases oficiais, coleta e organiza cotações de fornecedores locais, aplicando critérios de média, mediana ou menor preço com expurgo de valores inexequíveis e validação humana obrigatória (Human-in-the-Loop).
- **`calculador-bdi-encargos` (Engine Determinística de BDI e Encargos):** Executa o cálculo exato da taxa de Bonificação e Despesas Indiretas (BDI) segundo o Acórdão TCU nº 2.622/2013, aplicando alíquotas tributárias municipais (ISS local) e segregando BDI de serviços e BDI diferenciado de fornecimento de materiais/equipamentos.
- **`guardrail-controladoria` (Guardião de Compliance):** Audita a planilha orçamentária em tempo real contra riscos de sobrepreço, estancamento de quartis do TCU, duplicidade de insumos, ausência de memória de cálculo e distorções na Curva ABC.
- **`documentalista-tecnico` (Gerador Autônomo de Dossiês):** Converte a estrutura de dados validada em peças formais editáveis e padronizadas (DFD, ETP, Termo de Referência, Especificação Técnica, Memoriais Descritivos, Justificativas de BDI e Despachos padronizados para autuação no SEI / e-Docs).

#### 1.3 Mecanismo Híbrido: Separação entre Raciocínio (LLM) e Cálculo Determinístico
> **DIFERENCIAL TECNOLÓGICO: ZERO ALUCINAÇÃO FINANCEIRA**  
> Para eliminar 100% o risco de alucinação financeira (um problema crítico das LLMs convencionais), a Orca-AI adota uma arquitetura estritamente desacoplada:  
> • As LLMs e Agentes são utilizados exclusivamente para compreensão de linguagem natural, extração de requisitos, navegação semântica e redação de documentos técnicos.  
> • Toda a matemática orçamentária (multiplicações de quantitativos, composição de custos unitários, aplicação de encargos sociais, fórmulas analíticas de BDI e montagem da Curva ABC) é executada por um Motor Determinístico em Python (OpenPyXL / Pandas). Nenhuma operação aritmética é realizada via geração de texto pela IA.

---

### 2. Autoavaliação do Technology Readiness Level (TRL)

A avaliação do nível de maturidade tecnológica da Orca-AI foi realizada considerando o sistema completo: orquestrador multiagente, motor determinístico, base de conhecimento técnico, integração com tabelas oficiais de custos e módulo de guardrails regulatórios.

| TRL | Critério Objetivo de Avaliação | Status | Evidências Práticas no Ecossistema Orca-AI |
| :---: | :--- | :---: | :--- |
| **1** | Os princípios tecnológicos necessários à solução foram identificados e estudados? | **Sim** | Estudo dos fundamentos de Agentic AI, LLMs, engenharia de custos públicos (Lei 14.133/2021, Acórdão TCU 2.622/2013) e validações determinísticas. |
| **2** | A aplicação da IA e dos agentes inteligentes à engenharia de custos públicos foi formulada de maneira estruturada? | **Sim** | Formulation da arquitetura multiagente com divisão de papéis (Triagem, Planejador, Orçamentista, Pesquisador, Auditor, Documentalista). |
| **3** | As funções críticas da solução foram demonstradas por provas de conceito? | **Sim** | PoCs isoladas demonstrando leitura de especificações, busca de códigos SINAPI/IOPES, cálculo de BDI e geração automática de trechos de Termos de Referência. |
| **4** | Os principais componentes foram integrados e testados em ambiente controlado? | **Sim** | Integração do motor determinístico em Python com a camada de agentes e scripts de geração de planilhas e minutas textuais. |
| **5** | O protótipo integrado foi testado com dados representativos do contexto real de engenharia de custos? | **Sim** | Validação completa com dados orçamentários reais de manutenção predial e infraestrutura (HVAC, Geradores, Lavagem Envidraçada, Impermeabilização, Fotovoltaica). |
| **6** | Existe protótipo funcional com os principais componentes integrados e testados em condições próximas ao ambiente operacional pretendido? | **Sim** | Protótipo completo operando com 11 escopos reais do MGI/SRA-ES, gerando planilhas .xlsx validadas, memórias de cálculo auditáveis e dossiês em .docx/.pdf. |
| **7** | O sistema completo já opera como piloto incorporado ao fluxo real de trabalho de usuários finais? | **Não** | O sistema opera em ambiente computacional simulado e representativo; necessita de implantação piloto integrada à rotina diária de engenheiros de órgãos públicos. |
| **8** | O sistema foi qualificado e está pronto para implantação regular junto aos clientes? | **Não** | Requer homologação final de interoperabilidade (conectores com SEI/e-Docs) e testes de estabilidade sob carga de múltiplos órgãos simultâneos. |
| **9** | A tecnologia possui operação comercial consolidada e repetível em condições reais? | **Não** | Necessita de histórico comercial contínuo, contratos recorrentes SaaS GovTech e operação em escala nacional. |

**Resultado da Autoavaliação: TRL 6 — Protótipo Funcional Demonstrado em Ambiente Operacional Relevante.**

---

### 3. Avaliação do TRL e Roadmap Técnico-Operacional

#### 3.1 Justificativa Consolidada do TRL 6
A Orca-AI encontra-se em **TRL 6** porque possui uma arquitetura completamente integrada e testada com dados representativos de demandas reais de engenharia pública. A solução foi validada no processamento de 11 contratações complexas da Administração Pública Federal (SRA/MGI-ES), demonstrando capacidade de:
- Processar descrições e extrair quantitativos de serviços complexos;
- Consultar e associar códigos oficiais SINAPI, SICRO e IOPES com exatidão;
- Calcular analiticamente o BDI e os encargos sociais sem erros de arredondamento ou alucinação;
- Executar varredura de compliance através de guardrails de sobrepreço;
- Gerar automaticamente a documentação instrutória editável (.xlsx, .docx, .pdf) pronta para autuação.

Contudo, o avanço para **TRL 7** exige formalmente que a tecnologia seja incorporada de maneira contínua ao fluxo real de trabalho de engenheiros e servidores públicos no exercício regular de suas funções, em um projeto-piloto em ambiente operacional efetivo.

#### 3.2 Plano de Ação e Roadmap para Alcançar o TRL 7 (Projeto-Piloto)
O próximo objetivo estratégico da Orca-AI é a execução de um **Projeto-Piloto Controlado em Ambiente Real (TRL 7)** nos próximos 6 meses. O piloto será realizado em parceria com órgãos públicos demandantes (como a Secretaria Regional de Administração do MGI no Espírito Santo - SRA/MGI-ES ou Prefeituras municipais).

**Diretrizes e Indicadores de Desempenho (KPIs) para a Declaração do TRL 7:**
- ✔ **Precisão e Rastreabilidade Financeira:** Mapear divergências entre os valores gerados pela Orca-AI e a auditoria humana final (Meta: 0% de erro de cálculo e 100% de rastreabilidade de insumos).
- ✔ **Redução do Tempo de Instrução Processual:** Mensurar o tempo economizado na montagem do dossiê de licitação (Meta: redução do tempo médio de elaboração de 30 dias para menos de 4 horas por processo).
- ✔ **Taxa de Intervenção Humana (HITL):** Registrar a frequência e o tipo de ajustes manuais necessários durante a atuação dos agentes orçamentistas.
- ✔ **Desempenho dos Guardrails:** Quantificar a taxa de detecção prévia de sobrepreço, alíquotas incorretas de ISS e inconsistências de BDI antes da submissão do processo aos órgãos de controle (TCU/CGU).
- ✔ **Integração com Sistemas de Governo:** Validar o funcionamento dos conectores automáticos para exportação de despachos e peças formais diretamente para o SEI e e-Docs.

> **Nota Metodológica:** O avanço para o TRL 7 somente será declarado após a existência de um relatório formal com evidências documentadas de operação real, continuada e repetível por usuários finais do setor público.

---

### 4. Estratégia de Proteção da Propriedade Intelectual (PI)

Para assegurar o domínio tecnológico, proteger o valuation da startup e criar barreiras de entrada efetivas em um mercado de alta complexidade regulatória, a Orca-AI adota uma **Estratégia Híbrida e Multicamadas de Proteção da Propriedade Intelectual**:

| Ativo Estratégico | Proteção Proposta | Justificativa Técnica e Estratégica |
| :--- | :--- | :--- |
| **Código-Fonte da Engine Agentic AI Orca-AI** | **Registro de Software no INPI** *(Lei 9.609/98)* | Constitui o núcleo computacional da plataforma (scripts Python, orquestradores de agentes, conectores de bases de dados e compiladores). O registro no INPI assegura comprovação formal de autoria, titularidade e segurança jurídica para investimentos e licitações. |
| **Módulos de Dossiês, Guardrails e BDI** | **Registro de Programa de Computador no INPI** | Protege as rotinas específicas de verificação de regras (G-01 a G-10), o motor de cálculo analítico de BDI e os geradores de documentos em DOCX/PDF. |
| **Método Híbrido de Validação Multiagente** | **Avaliação de Patente de Invenção** *(Lei 9.279/96)* | Caso demonstrada novidade, atividade inventiva e aplicação industrial no método de coordenação entre IA semântica e motor determinístico com guardrails, será realizado o depósito de patente antes de qualquer publicação acadêmica detalhada. |
| **Prompts de Sistema, Grafo de Agentes e Heurísticas** | **Segredo de Negócio / Trade Secret** *(Lei 9.279/96)* | A sintaxe refinada dos prompts de controle de alucinação, as regras de ponderação de cotações e a lógica de exceções dos agentes serão mantidas em estrito segredo comercial protegidas por NDAs rígidos. |
| **Normalização e Associação das Bases Oficiais** | **Segredo de Negócio sobre a Implementação** | As tabelas SINAPI, SICRO e IOPES são públicas; o diferencial protegível reside na arquitetura proprietária de ETL, higienização, mapeamento semântico e histórico temporal de insumos desenvolvido pela Orca-AI. |
| **Marca Comercial 'Orca-AI' e 'Orca Intelligence'** | **Registro de Marca no INPI** *(Lei 9.279/96)* | Depósito de marca nominativa e mista na classe NCL(12) 42 (Serviços de Tecnologia e Software SaaS GovTech), assegurando a exclusividade de uso comercial e identidade da marca. |

#### 4.1 Governança da PI e Mitigação de Riscos Legal-Tecnológicos
- ▪ **Acordos de Confidencialidade (NDA) e Cessão de Direitos:** Todos os desenvolvedores, pesquisadores da UFG e prestadores de serviço assinam termos formais de cessão total dos direitos patrimoniais de PI para a empresa Orca-AI, acompanhados de cláusulas de não competição.
- ▪ **Conformidade com Licenças Open-Source:** A infraestrutura utiliza apenas componentes de código aberto com licenças permissivas (MIT, Apache 2.0, BSD), garantindo a ausência de licenças copyleft virais (como GPL v3) que pudessem forçar a abertura do código proprietário.
- ▪ **Rastreabilidade das Fontes Públicas:** A solução não se apropria de bases públicas de terceiros (SINAPI/SICRO/IOPES), mas sim protege a camada computacional de inteligência, organização e integração agregada.

---

### 5. Síntese Executiva

A **Orca-AI** consolida sua maturidade no nível **TRL 6**, apresentando um protótipo perfeitamente integrado e exaustivamente testado com dados reais e complexos de engenharia de custos públicos. A plataforma soluciona gargalos críticos do setor ao unir a inteligência semântica de sistemas multiagentes à precisão inegociável de motores determinísticos e à rigorosa governança de guardrails de compliance.

O roadmap estratégico direciona os esforços imediatos para a realização de um **projeto-piloto em ambiente operacional real junto a órgãos públicos (TRL 7)**, validando a tecnologia na rotina diária de servidores e medindo conclusivamente os ganhos de produtividade e a redução do tempo de instrução licitatória.

Acompanhando a maturidade tecnológica, a **Estratégia de Propriedade Intelectual da Orca-AI** combina o registro formal do software e da marca no INPI com a preservação de inteligência estratégica sob a forma de segredos de negócio e a avaliação criteriosa de patentes. Essa abordagem holística assegura a blindagem jurídica, atrai investidores e estabelece uma base sólida para a escala comercial da GovTech no mercado brasileiro.
"""
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown gerado com sucesso em: {md_filename}")

if __name__ == "__main__":
    build_docx()
    build_md()
