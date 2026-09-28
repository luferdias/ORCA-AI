import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

def build_despacho_engenharia_agu():
    doc = docx.Document()

    # Margens padrão ABNT / SEI
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)

    # Cores institucionais
    NAVY = RGBColor(0, 51, 102)      # #003366
    SLATE = RGBColor(45, 55, 72)     # #2D3748
    TEXT_DARK = RGBColor(30, 41, 59) # #1E293B

    def set_cell_shading(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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

    def set_table_borders(table, color="CBD5E0"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    # Estilo Normal
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = TEXT_DARK

    # Cabeçalho Oficial
    headers_info = [
        ("MINISTÉRIO DA GESTÃO E DA INOVAÇÃO EM SERVIÇOS PÚBLICOS", True, Pt(11), NAVY),
        ("Secretaria de Serviços Compartilhados", False, Pt(10), SLATE),
        ("Diretoria de Contratações e Unidades Descentralizadas", False, Pt(9.5), SLATE),
        ("Superintendência Regional de Administração no Estado do Espírito Santo – SRA/MGI-ES", True, Pt(9.5), SLATE),
        ("Setor de Engenharia e Infraestrutura Predial – Projeto Orca AI", False, Pt(9), SLATE)
    ]

    for t, b, sz, col in headers_info:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        r = p.add_run(t)
        r.bold = b
        r.font.size = sz
        r.font.color.rgb = col

    # Título do Despacho
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(10)
    r_t = p_title.add_run("DESPACHO DE ENGENHARIA Nº 01/2026/ENG-SRA-ES\n")
    r_t.bold = True
    r_t.font.size = Pt(13)
    r_t.font.color.rgb = NAVY
    r_sub = p_title.add_run("(Atendimento Integral às Recomendações Técnicas do Parecer AGU – Doc. SEI nº 64490579)")
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = SLATE
    r_sub.italic = True

    # Bloco de Metadados
    def add_meta(label, val, bold_val=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        r0 = p.add_run(label + " ")
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        r1 = p.add_run(val)
        r1.bold = bold_val
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = TEXT_DARK
        return p

    add_meta("Processo NUP:", "10783.000206/2026-71", bold_val=True)
    add_meta("Referência:", "Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820)")
    add_meta("Assunto:", "Atendimento Integral e Saneamento das Recomendações Técnicas de Engenharia, Arquitetura e Orçamentação da AGU.")
    add_meta("Objeto:", "Contratação de serviços comuns de engenharia e conservação predial dividida em 11 Itens para o Edifício Sede do MGI-ES e Edifício Anexo em Vitória/ES (Valor Global Estimado: R$ 1.005.726,92).")
    add_meta("Para:", "Superintendência Regional de Administração no Espírito Santo (SRA/MGI-ES)")
    add_meta("De:", "Engenheiro Civil Responsável Técnico / Fiscal de Obras")

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

    # Saudação
    p_greet = doc.add_paragraph()
    p_greet.paragraph_format.space_after = Pt(6)
    r_g = p_greet.add_run("Senhora Superintendente Regional de Administração,")
    r_g.bold = True
    r_g.font.size = Pt(10.5)

    def add_p(text, space_after=5, bold=False, italic=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(10)
        return p

    def add_section_header(num_title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(num_title)
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = NAVY
        return p

    add_p("1. Submeto a Vossa Senhoria o presente DESPACHO TÉCNICO DE ENGENHARIA, elaborado no âmbito do Projeto Orca AI, com a finalidade de consolidar todas as respostas técnicas, justificativas normativas e comprovações documentais necessárias ao integral saneamento das recomendações constantes do Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820).")

    add_p("2. Registra-se que a douta Consultoria Jurídica da União concluiu pela viabilidade jurídica do prosseguimento do certame, condicionando-o ao acolhimento das recomendações afetas ao planejamento da contratação e à orçamentação das obras e serviços de engenharia.")

    add_p("3. O presente expediente consolida, atualiza e substitui o Despacho de Engenharia preliminar acostado sob o Doc. SEI nº 64490579, fornecendo o mapeamento exato de todos os documentos já encartados nas Pastas I a VII da árvore do processo SEI nº 10783.000206/2026-71.")

    # SEÇÃO I: QUADRO SINÓTICO
    add_section_header("I. QUADRO SINÓTICO DE ATENDIMENTO ÀS RECOMENDAÇÕES DA AGU")

    # Tabela Sinóptica Geral
    table_sinop = doc.add_table(rows=18, cols=4)
    table_sinop.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_sinop, "CBD5E0")
    s_widths = [Inches(0.8), Inches(2.0), Inches(0.9), Inches(3.0)]

    s_headers = ["Item AGU", "Assunto / Recomendação", "Situação", "Providência Técnica Adotada e Localização no SEI"]
    for c_i, h_t in enumerate(s_headers):
        cell = table_sinop.rows[0].cells[c_i]
        cell.width = s_widths[c_i]
        set_cell_margins(cell, 50, 50, 60, 60)
        set_cell_shading(cell, "003366")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_t)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    sinop_data = [
        ("§ 24", "Adoção do IPPC Engenharia", "ATENDIDO", "Atestada a observância ao IPPC Engenharia (Guia CGU/AGU), formalizada no Despacho SEI nº 64558648, TJTR SEI nº 64474274 e Listas de Verificação AGU SEI nº 61487393 e 63811592."),
        ("§ 34", "Assinatura nos Documentos de Planejamento", "ATENDIDO", "Peças técnicas assinadas digitalmente via SEI pela Equipe de Planejamento: ETP (SEI nº 63787321), TR (SEI nº 63787318), Mapa de Riscos (SEI nº 63787257) e Projetos Básicos (SEI nº 64530669)."),
        ("§ 39", "Projeto Básico vs. TR e Acervo de Projetos", "ATENDIDO", "Demonstrado o acervo arquitetônico completo existente (Sede, Anexos, Marquise, Elevadores, Vila Rubim, Calçada Cidadã) e aplicação do art. 46, § 3º da Lei 14.133/21 no TR (SEI nº 63787318) e Projetos (SEI nº 64530669)."),
        ("§ 44-45", "Obrigações e Custos de Projeto Executivo", "ATENDIDO", "Custos declarados e absorvidos na Adm. Local/BDI e minuta de cláusula repassada à Licitação no Despacho SEI nº 62223146, TR (SEI nº 63787318) e Projetos Básicos (SEI nº 64530669)."),
        ("§ 48", "Declaração de Atividades Acessórias (Dec. 9.507/18)", "ATENDIDO", "Declarações formais anexadas aos autos confirmando a natureza acessória predial sob o Doc. SEI nº 64532939 e Doc. SEI nº 62229498."),
        ("§ 57", "Planilhas Orçamentárias Analíticas", "ATENDIDO", "Relatórios analíticos de composições de custos unitários dos 11 itens emitidos via Orçafascio e juntados ao processo sob o Doc. SEI nº 64507136 (sem uso de verbas)."),
        ("§ 58", "Hierarquia de Preços (SINAPI / Cotações)", "ATENDIDO", "Justificada a ordem hierárquica do art. 23 da Lei 14.133/21 (>76% em bases oficiais SINAPI/IOPES e IN 65/21 para itens atípicos) no Despacho SEI nº 64558648 e Mapa Orçafascio SEI nº 62792889."),
        ("§ 63", "Critérios de Aceitabilidade de Preços", "ATENDIDO", "Ratificados os limites máximos unitários e globais (Súmulas TCU nº 258 e 259) no Item 9.4 do Termo de Referência (SEI nº 63787318) e Despacho SEI nº 64474566."),
        ("§ 67", "Justificativa de BDI Pleno (Súmula 253 TCU)", "ATENDIDO", "Justificada a indivisibilidade de fornecimento e instalação (Acórdão TCU nº 2.622/13), atestando que materiais são insumos intrínsecos, no documento de BDI (SEI nº 63355968) e TJTR (SEI nº 64474274)."),
        ("§ 72", "Vantajosidade da Desoneração (CPRB)", "ATENDIDO", "Demonstrada a vantajosidade em serviços com mão de obra intensiva (Lei 14.973/24) no documento de BDI (SEI nº 63355968) e no Despacho SEI nº 64558648."),
        ("§ 73", "Curva ABC de Serviços e Insumos", "ATENDIDO", "Curva ABC expressa na coluna 'Peso %' do Orçafascio (SEI nº 64507136), com concentração de 74,46% na Classe A (Itens 07, 06, 11 e 03), consolidada no presente despacho."),
        ("§ 74-76", "Cronograma Físico-Financeiro por Demanda", "ATENDIDO", "Cronogramas físicos e financeiros estruturados com prazos estimados individualizados por Ordem de Serviço (OS) no documento de BDI (SEI nº 63355968) e no TR (SEI nº 63787318)."),
        ("§ 79", "Regularização das ARTs / RRTs", "ATENDIDO", "ART definitiva registrada e quitada perante o CREA-ES acostada aos autos sob o Doc. SEI nº 64468889, cobrindo todos os 11 projetos e orçamentos do certame."),
        ("§ 92", "Justificativa da Empreitada por Preço Global", "ATENDIDO", "Justificada a escolha do regime global (art. 46 da Lei 14.133/21 e Acórdão TCU nº 1.977/13) pela precisão métrica do acervo arquitetônico no TJTR (SEI nº 64474274) e TR (SEI nº 63787318)."),
        ("§ 97-98", "Matriz de Riscos (Acórdão 1.977/13 TCU)", "ATENDIDO", "Matriz de riscos com limites de tolerância de 10% (Dec. 7.983/13 e Acórdão TCU 1.977/13) formalizada sob o Doc. SEI nº 63787257 e recepcionada no TJTR (SEI nº 64474274)."),
        ("§ 103", "Sistema de Registro de Preços (SRP)", "ATENDIDO", "Justificada a conveniência do SRP para atendimento sob demanda no documento de justificativa SRP (SEI nº 63786173), Minuta Ata SRP (SEI nº 63802412) e TJTR (SEI nº 64474274)."),
        ("§ 110", "Harmonização da Vistoria Técnica", "ATENDIDO", "Vistoria facultativa com exigência alternativa de Declaração de Pleno Conhecimento harmonizada no Edital (SEI nº 63787481) e Termo de Referência (SEI nº 63787318)."),
    ]

    for r_i, r_data in enumerate(sinop_data, start=1):
        row = table_sinop.rows[r_i]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.width = s_widths[c_i]
            set_cell_margins(cell, 35, 35, 45, 45)
            set_cell_shading(cell, "FFFFFF" if r_i % 2 != 0 else "F8FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if c_i == 0:
                r.bold = True
            elif c_i == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)

    add_p("4. Quanto ao parágrafo 120 (Previsão Orçamentária e LRF), informa-se que o atesto de dotação orçamentária e conformidade fiscal (arts. 16 e 17 da LRF) está a cargo do Setor Administrativo/Financeiro (SEAL / Paulinho), encontrando-se em fase de certificação para oportuna juntada aos autos.", space_after=8)

    # SEÇÃO II: MANIFESTAÇÃO DETALHADA
    add_section_header("II. MANIFESTAÇÃO E SANEAMENTO PORMENORIZADO DAS RECOMENDAÇÕES")

    add_p("1. Quanto ao Instrumento de Padronização - IPPC Engenharia (§ 24): Atesta-se que a presente instrução processual observou integralmente as diretrizes do IPPC Engenharia da CGU/AGU, formalizado no Despacho de Justificativa Itens § 24 e § 58 (Doc. SEI nº 64558648), no Termo de Justificativas Técnicas Relevantes - TJTR saneado (Doc. SEI nº 64474274) e nas Listas de Verificação AGU (Docs. SEI nº 61487393 e 63811592).")

    add_p("2. Quanto ao Projeto Básico, Acervo Técnico e Suficiência do Termo de Referência (§ 39): Este responsável técnico atesta formalmente que a Administração possui acervo arquitetônico completo e consolidado, o qual serviu de base absoluta para o levantamento métrico rigoroso dos 11 itens licitados, devidamente reunido no Caderno de Projetos Básicos dos Itens 01 a 11 (Doc. SEI nº 64530669), compreendendo: (a) Projeto Arquitetônico Sede e Anexo; (b) Projeto Calçada Cidadã; (c) Projeto Estacionamento Princesa Isabel; (d) Projeto Anexo Vila Rubim; (e) Projeto Marquise em CAD DWG; e (f) Projeto Básico Elevadores. Com base no art. 46, § 3º da Lei nº 14.133/2021, as especificações foram consolidadas no Termo de Referência (Doc. SEI nº 63787318).")

    add_p("3. Quanto à Elaboração de Detalhamentos Executivos pela Contratada (§ 44 e § 45): Com amparo no art. 46, § 1º, e art. 6º, inciso XXVI da Lei nº 14.133/2021, caberá à Contratada elaborar peças executivas de canteiro, ancoragens NR-35 e balancins. DECLARA-SE FORMALMENTE que tais custos encontram-se incluídos no BDI (Administração Central) e Administração Local, sem custos extras, conforme Despacho à Equipe de Licitações (Doc. SEI nº 62223146) e TR (Doc. SEI nº 63787318).")

    add_p("4. Quanto às Planilhas Orçamentárias Analíticas (§ 57): Em cumprimento à Súmula TCU nº 258/2010, emitiu-se da plataforma Orçafascio o Caderno Geral de Orçamentos Analíticos dos Itens 01 a 11 (Doc. SEI nº 64507136), discriminando todos os custos unitários, insumos, mão de obra e encargos, sem o uso de verbas genéricas.")

    add_p("5. Quanto à Hierarquia de Preços e Suficiência do SINAPI (§ 58): A orçamentação seguiu estritamente o art. 23, § 2º da Lei nº 14.133/2021: 76,34% do valor provém de tabelas públicas oficiais (SINAPI Vitória R$ 652.502,74 e IOPES/ES R$ 115.228,84). Apenas 23,66% (R$ 237.995,34) decorrem de cotações mercadológicas sob a IN SEGES/ME nº 65/2021, restritas a tecnologias atípicas não catalogadas pela CEF (Item 02 - Robótica HVAC, Item 06 - Películas Térmicas Nanocerâmicas e Item 10 - Gerador e Subestação), tudo devidamente comprovado no Despacho de Justificativa Técnica (Doc. SEI nº 64558648) e Mapas de Preços Orçafascio (Docs. SEI nº 62078605 e 62792889).")

    add_p("6. Quanto aos Critérios de Aceitabilidade de Preços Unitários e Globais (§ 63): Ratifica-se que os preços referenciais representam os limites máximos aceitáveis para julgamento das propostas (Súmulas TCU nº 258 e 259), conforme estabelecido no item 9.4 do Termo de Referência (Doc. SEI nº 63787318).")

    add_p("7. Quanto à Inaplicabilidade de BDI Diferenciado para Fornecimento (§ 65 a § 67 / Súmula TCU 253): Não há aquisição autônoma de bens de capital. Todos os materiais (tintas, mastiques, argamassas poliméricas, películas e peças sobressalentes) constituem insumos intrínsecos e indivisíveis dos serviços de conservação predial. O BDI pleno de 25,00% (Acórdão TCU nº 2.622/2013-Plenário) incide legitimamente sobre o valor global, conforme justificado no Documento de BDI (Doc. SEI nº 63355968) e TJTR (Doc. SEI nº 64474274).")

    add_p("8. Quanto à Vantajosidade do Regime Desonerado (§ 68 a § 72): Por se tratar de serviços com mão de obra intensiva, a redução dos encargos no SINAPI Desonerado supera amplamente a alíquota compensatória de 4,5% da CPRB no BDI, garantindo um preço global mais econômico para o erário (Leis nº 12.546/2011 e 14.973/2024), conforme memória anexada sob o Doc. SEI nº 63355968.")

    add_p("9. Quanto à Apresentação da Curva ABC (§ 73): A representatividade percentual e as classes da Curva ABC encontram-se discriminadas na planilha analítica do Orçafascio (Doc. SEI nº 64507136), destacando a concentração de 74,46% nos itens de Classe A, detalhados pormenorizadamente na Seção III deste expediente.")

    add_p("10. Quanto à Regularização da ART Definitiva (§ 79): A Anotação de Responsabilidade Técnica definitiva foi registrada e quitada junto ao CREA-ES sob o Doc. SEI nº 64468889, contemplando a responsabilidade técnica integral por projetos, especificações e orçamentos dos 11 itens.")

    add_p("11. Quanto à Empreitada por Preço Global e Matriz de Riscos (§ 92, § 97 e § 98): A escolha pelo regime global fundamenta-se na precisão métrica do acervo arquitetônico (art. 46 da Lei 14.133/21). Formalizou-se nos autos a Matriz de Riscos do Contrato (Doc. SEI nº 63787257 e TJTR Doc. SEI nº 64474274), disciplinando variações ordinárias e o teto regulamentar de tolerância de erros de 10% (art. 13 do Dec. 7.983/13).")

    add_p("12. Quanto à Harmonização da Vistoria Técnica (§ 110): Fica harmonizado no Edital (Doc. SEI nº 63787481) e TR (Doc. SEI nº 63787318) que a vistoria prévia é facultativa (art. 63, § 2º da Lei 14.133/21), devendo a licitante apresentar Declaração de Pleno Conhecimento.")

    # SEÇÃO III: MATRIZ PADRONIZADA DOS 11 ITENS E CURVA ABC
    add_section_header("III. MATRIZ PADRONIZADA DOS 11 ITENS LICITADOS E ANÁLISE DA CURVA ABC")

    add_p("13. Em atendimento expresso às diretrizes do IPPC Engenharia e ao parágrafo 73 do Parecer AGU, apresenta-se a matriz completa dos 11 itens da contratação, detalhando a base referencial adotada, o valor estimado com BDI de 25,00%, a participação percentual individual no orçamento global (R$ 1.005.726,92), o percentual acumulado, a respectiva Classe na Curva ABC e a precisa localização de cada Especificação Técnica e Orçamento Sintético no SEI:")

    # TABELA DOS 11 ITENS COM CURVA ABC E SEI
    table_abc = doc.add_table(rows=13, cols=8)
    table_abc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_abc, "CBD5E0")
    abc_widths = [Inches(0.4), Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.6), Inches(0.6), Inches(0.6), Inches(1.5)]

    abc_headers = ["Item", "Objeto Especializado", "Base Legal", "Valor (R$)", "% Part.", "% Acum.", "Classe", "Documentos no SEI (ET / Orçamento)"]
    for c_i, h_t in enumerate(abc_headers):
        cell = table_abc.rows[0].cells[c_i]
        cell.width = abc_widths[c_i]
        set_cell_margins(cell, 40, 40, 50, 50)
        set_cell_shading(cell, "003366")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_t)
        r.bold = True
        r.font.size = Pt(7.0)
        r.font.color.rgb = RGBColor(255, 255, 255)

    abc_data = [
        ("01", "Substituição Teto Elevadores", "SINAPI/Própria", "R$ 32.194,17", "3,20%", "91,87%", "Classe B", "ET: 61826193 | Orç: 61826267"),
        ("02", "Limpeza Robotizada Dutos AC", "IN SEGES 65/21", "R$ 44.011,83", "4,38%", "88,67%", "Classe B", "ET: 61826396 | Orç: 61826477"),
        ("03", "Lavagem Fachada Envidraçada", "IOPES / SINAPI", "R$ 94.172,48", "9,36%", "74,46%", "Classe A", "ET: 61826554 | Orç: 61826643"),
        ("04", "Tratamento Juntas Dilatação", "SINAPI Vitória", "R$ 31.794,07", "3,16%", "95,03%", "Classe C", "ET: 61826777 | Orç: 61826863"),
        ("05", "Pintura Anticorrosiva Grades", "SINAPI Vitória", "R$ 51.398,76", "5,11%", "79,57%", "Classe A", "ET: 61831609 | Orç: 61831673"),
        ("06", "Películas de Controle Solar", "IN SEGES 65/21", "R$ 171.299,50", "17,03%", "52,66%", "Classe A", "ET: 61832077 | Orç: 61832194"),
        ("07", "Pintura Geral Sede e Garagem", "SINAPI Vitória", "R$ 358.338,32", "35,63%", "35,63%", "Classe A", "ET: 62216617 | Orç: 62216913"),
        ("08", "Impermeabilização Cisterna", "SINAPI Vitória", "R$ 47.508,76", "4,72%", "84,29%", "Classe B", "ET: 61833595 | Orç: 61833731"),
        ("09", "Limpeza Painéis Fotovoltaicos", "IOPES / SINAPI", "R$ 27.153,65", "2,70%", "97,73%", "Classe C", "ET: 61834144 | Orç: 61834527"),
        ("10", "Manutenção Gerador/Subestação", "IN SEGES 65/21", "R$ 22.829,87", "2,27%", "100,00%", "Classe C", "ET: 61834884 | Orç: 61835041"),
        ("11", "Impermeabilização Marquise", "SINAPI Vitória", "R$ 125.025,51", "12,43%", "65,09%", "Classe A", "ET: 61835197 | Orç: 61835298"),
        ("TOT", "VALOR GLOBAL CONSOLIDADO", "CONSOLIDADO", "R$ 1.005.726,92", "100,00%", "100,00%", "100%", "Caderno Geral: SEI 64507136 | Projetos: SEI 64530669")
    ]

    for r_i, r_data in enumerate(abc_data, start=1):
        row = table_abc.rows[r_i]
        is_tot = (r_i == 12)
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.width = abc_widths[c_i]
            set_cell_margins(cell, 30, 30, 40, 40)
            if is_tot:
                set_cell_shading(cell, "EDF2F7")
            else:
                set_cell_shading(cell, "FFFFFF" if r_i % 2 != 0 else "F8FAFC")
            p = cell.paragraphs[0]
            if c_i in [0, 4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_i == 3:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            r = p.add_run(val)
            r.font.size = Pt(7.0)
            if is_tot:
                r.bold = True
                if c_i == 3:
                    r.font.color.rgb = NAVY
            elif c_i == 6:
                r.bold = True
                if "Classe A" in val:
                    r.font.color.rgb = RGBColor(185, 28, 28) # Vermelho escuro
                elif "Classe B" in val:
                    r.font.color.rgb = RGBColor(194, 65, 12) # Laranja
                else:
                    r.font.color.rgb = RGBColor(71, 85, 105) # Slate

    add_p("14. Análise Estratégica da Curva ABC:")
    add_p("• Classe A (Alta Materialidade): Os itens 07 (Pintura Sede), 06 (Insulfilm), 11 (Marquise), 03 (Lavagem Fachada) e 05 (Pintura Grades) concentram 79,57% do orçamento global (R$ 800.234,57), constituindo o foco prioritário de fiscalização e controle de medição.")
    add_p("• Classe B (Média Materialidade): Os itens 08 (Cisterna), 02 (Dutos AC) e 01 (Elevadores) perfazem 12,30% do orçamento (R$ 123.714,76).")
    add_p("• Classe C (Baixa Materialidade): Os itens 04 (Juntas Dilatação), 09 (Módulos Solares) e 10 (Gerador/Subestação) somam 8,13% do certame (R$ 81.777,59).")

    # SEÇÃO IV: GUIA DE MAPEAMENTO DOS LINKS NO SEI
    add_section_header("IV. GUIA DE INDEXAÇÃO E MAPEAMENTO DOS LINKS NO SEI")

    add_p("15. Para fins de auditoria e conferência imediata pelos órgãos de controle e pela Consultoria Jurídica da União, relacionam-se os números oficiais dos documentos SEI que instruem cada exigência técnica:")
    add_p("1. Parecer Jurídico da AGU: Parecer nº 01199/2026 (Doc. SEI nº 64468820);")
    add_p("2. ART Definitiva Quitada perante o CREA-ES: Doc. SEI nº 64468889;")
    add_p("3. Despacho Justificativa Itens § 24 e § 58: Doc. SEI nº 64558648;")
    add_p("4. Caderno Geral de Orçamentos Analíticos (11 Itens - Orçafascio): Doc. SEI nº 64507136;")
    add_p("5. Acervo de Projetos Básicos Consolidados (Itens 01 a 11): Doc. SEI nº 64530669;")
    add_p("6. Termo de Justificativas Técnicas Relevantes (TJTR Saneado): Doc. SEI nº 64474274;")
    add_p("7. Termo de Referência Consolidado: Doc. SEI nº 63787318;")
    add_p("8. Estudo Técnico Preliminar (ETP): Doc. SEI nº 63787321;")
    add_p("9. Matriz de Alocação de Riscos pós-TR: Doc. SEI nº 63787257;")
    add_p("10. Memória de BDI e Justificativa de Cronograma: Doc. SEI nº 63355968;")
    add_p("11. Declaração de Atendimento ao Parecer Jurídico: Doc. SEI nº 64532939;")
    add_p("12. Declaração de Utilização de Modelos AGU/MGI: Doc. SEI nº 63476776;")
    add_p("13. Listas de Verificação AGU: Docs. SEI nº 61487393 e 63811592;")
    add_p("14. Justificativa de Utilização do SRP e Minuta de Ata: Docs. SEI nº 63786173 e 63802412;")
    add_p("15. Minuta de Edital de Pregão e Contrato: Docs. SEI nº 63787481 e 63807532.")

    # SEÇÃO V: CONCLUSÃO
    add_section_header("V. CONCLUSÃO E ENCAMINHAMENTO")

    add_p("16. Diante do exposto, resta demonstrado o pleno atendimento e saneamento de todas as recomendações de Engenharia, Arquitetura e Orçamentação insertas no Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820).")

    add_p("17. O processo encontra-se técnica e juridicamente apto para deliberação superior e regular prosseguimento das etapas do certame licitatório.")

    add_p("18. Encaminhe-se o presente despacho à Superintendência Regional de Administração no Estado do Espírito Santo (SRA/MGI-ES) para conhecimento, aprovação e posterior remessa à Equipe de Licitações e Contratos para os atos de publicação do Edital, substituindo-se em definitivo a minuta anterior acostada sob o Doc. SEI nº 64490579.", space_after=14)

    # Bloco de Assinatura
    p_dt = doc.add_paragraph()
    p_dt.paragraph_format.space_after = Pt(14)
    p_dt.add_run("Vitória, 22 de setembro de 2026.").font.size = Pt(10)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.line_spacing = 1.15
    p_sig.paragraph_format.space_after = Pt(2)
    r_s0 = p_sig.add_run("Documento assinado eletronicamente\n")
    r_s0.italic = True
    r_s0.font.size = Pt(9.5)
    r_s0.font.color.rgb = SLATE

    r_s1 = p_sig.add_run("LUIS FERNANDO DIAS\n")
    r_s1.bold = True
    r_s1.font.size = Pt(10.5)
    r_s1.font.color.rgb = NAVY

    r_s2 = p_sig.add_run("Engenheiro Civil, MSc. – Fiscal Técnico\n")
    r_s2.font.size = Pt(9.5)

    r_s3 = p_sig.add_run("CREARJ: 1985100024\n")
    r_s3.font.size = Pt(9.5)

    r_s4 = p_sig.add_run("Setor de Engenharia e Infraestrutura Predial – SRA/MGI-ES\n\n")
    r_s4.font.size = Pt(9.5)

    r_s5 = p_sig.add_run("Referência: Processo nº 10783.000206/2026-71. SEI nº 64490579")
    r_s5.bold = True
    r_s5.font.size = Pt(9)
    r_s5.font.color.rgb = SLATE

    # Salvar nos diretórios adequados
    out_dir_despachos = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\ORCA-AI\OrcaAI\projetos\_governanca_sei_agu_cgu\despachos_sei"
    out_dir_pareceres = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\ORCA-AI\OrcaAI\projetos\_governanca_sei_agu_cgu\pareceres_agu"

    # Salva com nome oficial SEI 64490579
    docx_sei = os.path.join(out_dir_despachos, "SEI_64490579_Despacho_Engenharia_Resposta_AGU.docx")
    doc.save(docx_sei)
    print(f"Salvo: {docx_sei}")

    # Salva cópia na pasta pareceres_agu como versão 2
    docx_v2 = os.path.join(out_dir_pareceres, "DESPACHO_ENGENHARIA_SRA_RESPOSTA_PARECER_AGU_v2.docx")
    try:
        doc.save(docx_v2)
        print(f"Salvo: {docx_v2}")
    except PermissionError:
        print(f"Aviso: {docx_v2} em uso por outro processo.")

if __name__ == "__main__":
    build_despacho_engenharia_agu()
