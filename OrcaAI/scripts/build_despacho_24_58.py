import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

def create_consolidated_despacho():
    doc = docx.Document()

    # Page setup - Margins (Standard SEI / A4)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.header_distance = Inches(0.4)
        section.footer_distance = Inches(0.4)

    # Styling colors
    NAVY = RGBColor(0, 51, 102)      # #003366
    SLATE = RGBColor(45, 55, 72)     # #2D3748
    TEXT_DARK = RGBColor(30, 41, 59) # #1E293B

    # Helper: Set Cell Shading
    def set_cell_shading(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # Helper: Set Cell Margins (Padding)
    def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
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

    # Helper: Set Table Borders
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

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = TEXT_DARK

    # Header - Órgão Completo (Conforme SEI)
    header_lines = [
        ("MINISTÉRIO DA GESTÃO E DA INOVAÇÃO EM SERVIÇOS PÚBLICOS", True, Pt(11), NAVY),
        ("Secretaria de Serviços Compartilhados", False, Pt(10), SLATE),
        ("Diretoria de Contratações e Unidades Descentralizadas", False, Pt(9.5), SLATE),
        ("Superintendência Regional de Administração no Estado do Espírito Santo", False, Pt(9.5), SLATE),
        ("Serviço de Administração e Logística", False, Pt(9.5), SLATE),
        ("Equipe de Planejamento de Contratação", True, Pt(9.5), SLATE),
    ]

    for text, is_bold, sz, col in header_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        run = p.add_run(text)
        run.bold = is_bold
        run.font.size = sz
        run.font.color.rgb = col

    # Document Banner / Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("DESPACHO")
    r_title.bold = True
    r_title.font.size = Pt(13)
    r_title.font.color.rgb = NAVY

    # Meta table / Information block
    def add_meta_field(label, val, bold_val=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        r_lbl = p.add_run(label + " ")
        r_lbl.bold = True
        r_lbl.font.size = Pt(10)
        r_lbl.font.color.rgb = NAVY
        r_val = p.add_run(val)
        r_val.bold = bold_val
        r_val.font.size = Pt(10)
        r_val.font.color.rgb = TEXT_DARK
        return p

    add_meta_field("Referência Processual:", "Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820) – Itens § 24 e § 58")
    add_meta_field("Assunto:", "Atendimento Integrado aos §§ 24 e 58 do Parecer AGU: Atesto de Adoção do IPPC Engenharia, Demonstração da Hierarquia do Art. 23 da Lei nº 14.133/21, Insuficiência do SINAPI e Adequação da Tabela IOPES ao Mercado Local de Vitória/ES.")
    add_meta_field("Objeto da Contratação:", "Serviços de engenharia e manutenção predial continuada dividida em 11 Itens para o Edifício Sede do MGI-ES e Edifício Anexo em Vitória/ES (Valor Global: R$ 1.005.726,92).")

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)

    # Greeting
    p_greet = doc.add_paragraph()
    p_greet.paragraph_format.space_after = Pt(6)
    r_greet = p_greet.add_run("Senhora Superintendente,")
    r_greet.bold = True
    r_greet.font.size = Pt(10.5)

    def add_p(text, space_after=6, bold=False, italic=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(10.5)
        return p

    def add_section_header(num_title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(num_title)
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = NAVY
        return p

    def add_callout(quote_text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.right_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(quote_text)
        run.italic = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = SLATE
        return p

    add_p("1. Na condição de Engenheiro Civil Responsável Técnico pela elaboração e consolidação dos projetos de engenharia e orçamentos referenciais da presente contratação, dirijo-me a Vossa Senhoria para formalizar a manifestação técnica e conclusiva do Setor de Engenharia em atendimento direto às recomendações formuladas no Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820), especificamente quanto aos seguintes tópicos:")

    add_callout('“24. Somado a isso, recomenda-se também a adoção do Instrumento de Padronização dos Procedimentos de Contratação de Obras e Serviços de Engenharia – IPPC Engenharia.”')
    add_callout('“58. Nesse contexto, recomendamos: seja juntada aos autos justificativa detalhada demonstrando que a Administração seguiu rigorosamente a sequência hierárquica prevista no art. 23, § 2º, da Lei nº 14.133/2021, explicitando as razões pelas quais o sistema SINAPI se mostrou insuficiente para determinados itens; em sendo o caso, recomenda-se que seja demonstrada a adequação das tabelas referenciais de outros entes federativos ao mercado local da obra.”')

    add_p("2. As explanações a seguir detalham as providências técnicas adotadas e indexam todas as peças comprobatórias já encartadas na árvore processual do SEI, conferindo cabal higidez formal, técnica e jurídica aos autos.")

    # 1 DA ADOÇÃO INTEGRAL DO IPPC ENGENHARIA (ATENDIMENTO AO § 24)
    add_section_header("1 DA ADOÇÃO INTEGRAL DO IPPC ENGENHARIA (ATENDIMENTO AO § 24)")

    add_p("3. O Instrumento de Padronização dos Procedimentos de Contratação de Obras e Serviços de Engenharia (IPPC Engenharia), formulado pela Consultoria-Geral da União (CGU/AGU) em conjunto com a e-CJU/Engenharia, estabelece as boas práticas de governança e os modelos obrigatórios para instrução de processos de engenharia pública.")

    add_p("4. A incorporação do IPPC Engenharia a este certame comprova-se documentalmente no processo pelos seguintes atos materiais indexados no SEI:")

    add_p("4.1. Termo de Justificativas Técnicas Relevantes (TJTR): Em atendimento aos §§ 21 a 23 do parecer, o modelo-padrão da AGU de Justificativas Técnicas Relevantes foi integralmente preenchido e motivado técnica e juridicamente sob o Doc. SEI nº 64474274 (sucedendo as versões preliminares 61728530 e 61790928). O documento fundamenta as opções de parcelamento, regime de execução (empreitada por preço global), prazos, critérios de qualificação e matriz de riscos, devidamente subscrito por engenheiro habilitado com Anotação de Responsabilidade Técnica registrada e quitada no CREA-ES (Doc. SEI nº 64468889).")

    add_p("4.2. Listas de Verificação e Declarações Padronizadas da AGU: Foram acostadas aos autos as Listas de Verificação oficiais da AGU/CGU para obras e serviços de engenharia devidamente preenchidas e checadas (Docs. SEI nº 61487393 e 63811592), além da Declaração Formal de Utilização de Modelos AGU/MGI (Doc. SEI nº 63476776) e da Declaração de Atendimento ao Parecer Jurídico (Doc. SEI nº 64532939).")

    add_p("4.3. Acervo de Projetos Básicos e Orçamentos Analíticos Consolidados: Em estrita sintonia com os fluxos do IPPC Engenharia, o processo foi enriquecido com a juntada dos Projetos Básicos Consolidados dos 11 Itens (Doc. SEI nº 64530669) e do Caderno Geral de Orçamentos Analíticos dos Itens 01 a 11 emitidos na plataforma Orçafascio (Doc. SEI nº 64507136), acompanhados do Despacho de Engenharia de Atendimento às Recomendações da AGU (Doc. SEI nº 64490579).")

    add_p("4.4. Matriz de Padronização Documental dos 11 Itens Licitados: Cada um dos 11 itens da contratação recebeu tratamento homogêneo composto por 6 entregáveis técnicos padronizados, com suas respectivas especificações técnicas e orçamentos sintéticos autônomos indexados nas Pastas IV e V do SEI, conforme tabela a seguir:")

    # Table: 11 Items with SEI links
    table_items = doc.add_table(rows=12, cols=6)
    table_items.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_items, "CBD5E0")
    t_widths = [Inches(0.5), Inches(1.9), Inches(1.0), Inches(1.0), Inches(1.4), Inches(0.7)]

    headers_t = ["ITEM", "OBJETO ESPECIALIZADO", "BASE PREÇO", "VALOR ESTIMADO", "DOCS. SEI (ESPEC / ORÇ)", "IPPC"]
    hdr_row = table_items.rows[0]
    for c_idx, head_text in enumerate(headers_t):
        cell = hdr_row.cells[c_idx]
        cell.width = t_widths[c_idx]
        set_cell_margins(cell, 50, 50, 60, 60)
        set_cell_shading(cell, "003366")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(head_text)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_11 = [
        ("01", "SUBSTITUIÇÃO TETO ELEVADORES", "SINAPI VITÓRIA", "R$ 32.194,17", "ET: 61826193 | ORÇ: 61826267", "CONFORME"),
        ("02", "LIMPEZA ROBOTIZADA DUTOS AC", "IN SEGES 65/21", "R$ 44.011,83", "ET: 61826396 | ORÇ: 61826477", "CONFORME"),
        ("03", "LAVAGEM FACHADA ENVIDRAÇADA", "IOPES / SINAPI", "R$ 94.172,48", "ET: 61826554 | ORÇ: 61826643", "CONFORME"),
        ("04", "TRATAMENTO JUNTAS DILATAÇÃO", "SINAPI VITÓRIA", "R$ 31.794,07", "ET: 61826777 | ORÇ: 61826863", "CONFORME"),
        ("05", "PINTURA ANTICORROSIVA GRADES", "SINAPI VITÓRIA", "R$ 51.398,76", "ET: 61831609 | ORÇ: 61831673", "CONFORME"),
        ("06", "PELÍCULA SOLAR TÉRMICA", "IN SEGES 65/21", "R$ 171.299,50", "ET: 61832077 | ORÇ: 61832194", "CONFORME"),
        ("07", "PINTURA GERAL SEDE E GARAGEM", "SINAPI VITÓRIA", "R$ 358.338,32", "ET: 62216617 | ORÇ: 62216913", "CONFORME"),
        ("08", "IMPERMEABILIZAÇÃO CISTERNA", "SINAPI VITÓRIA", "R$ 47.508,76", "ET: 61833595 | ORÇ: 61833731", "CONFORME"),
        ("09", "LIMPEZA PAINÉIS FOTOVOLTAICOS", "IOPES / SINAPI", "R$ 27.153,65", "ET: 61834144 | ORÇ: 61834527", "CONFORME"),
        ("10", "MANUTENÇÃO GERADOR/SUBESTAÇÃO", "IN SEGES 65/21", "R$ 22.829,87", "ET: 61834884 | ORÇ: 61835041", "CONFORME"),
        ("11", "IMPERMEABILIZAÇÃO MARQUISE", "SINAPI VITÓRIA", "R$ 125.025,51", "ET: 61835197 | ORÇ: 61835298", "CONFORME"),
    ]

    for row_idx, data_row in enumerate(data_11, start=1):
        row = table_items.rows[row_idx]
        for col_idx, val in enumerate(data_row):
            cell = row.cells[col_idx]
            cell.width = t_widths[col_idx]
            set_cell_margins(cell, 35, 35, 45, 45)
            set_cell_shading(cell, "FFFFFF" if row_idx % 2 != 0 else "F8FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 4, 5] else (WD_ALIGN_PARAGRAPH.RIGHT if col_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if col_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)

    add_p("5. Dessa forma, com a plena instrução das peças retromencionadas, resta cabalmente evidenciada e certificada a adoção integral das diretrizes do IPPC Engenharia, sanando em definitivo o parágrafo 24 do parecer jurídico.", space_after=8)

    # 2 DA ESTRITA OBSERVÂNCIA HIERÁRQUICA DO ART. 23, § 2º, DA LEI Nº 14.133/2021 (ATENDIMENTO AO § 58)
    add_section_header("2 DA ESTRITA OBSERVÂNCIA HIERÁRQUICA DO ART. 23, § 2º, DA LEI Nº 14.133/2021 (ATENDIMENTO AO § 58)")

    add_p("6. Em adstrição ao que determina o art. 23, § 2º, da Nova Lei de Licitações (Lei nº 14.133/2021), c/c o Decreto nº 7.983/2013, o Setor de Engenharia da SRA/MGI-ES empregou uma metodologia descendente rígida para a obtenção dos custos unitários referenciais:")

    # Table: Hierarchy Distribution
    table_hier = doc.add_table(rows=4, cols=4)
    table_hier.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_hier, "CBD5E0")
    h_widths = [Inches(1.8), Inches(2.2), Inches(1.3), Inches(1.2)]

    h_heads = ["Nível Hierárquico Legal", "Base de Dados Adotada", "Valor Estimado (R$)", "Participação %"]
    for c_i, head_t in enumerate(h_heads):
        cell = table_hier.rows[0].cells[c_i]
        cell.width = h_widths[c_i]
        set_cell_margins(cell, 50, 50, 60, 60)
        set_cell_shading(cell, "003366")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(head_t)
        r.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(255, 255, 255)

    hier_rows = [
        ("Inciso I (Prioridade Legal)", "SINAPI Desonerado (Vitória/ES)", "R$ 652.502,74", "64,88%"),
        ("Inciso III (Tabela Oficial Estadual)", "IOPES (Estado do Espírito Santo)", "R$ 115.228,84", "11,46%"),
        ("Inciso V (Pesquisa IN SEGES 65/21)", "Cotações de Mercado Especializado", "R$ 237.995,34", "23,66%"),
    ]

    for r_i, r_data in enumerate(hier_rows, start=1):
        row = table_hier.rows[r_i]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.width = h_widths[c_i]
            set_cell_margins(cell, 40, 40, 50, 50)
            set_cell_shading(cell, "FFFFFF" if r_i % 2 != 0 else "F8FAFC")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_i < 2 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(8.0)
            if c_i == 0:
                r.bold = True

    add_p("7. A constatação matemática acima é categórica: 76,34% de todo o orçamento de referência provém exclusivamente de tabelas oficiais públicas (SINAPI Vitória e IOPES). A pesquisa de mercado sob a égide da IN SEGES/ME nº 65/2021 atuou estritamente como fonte subsidiária extraordinária (23,66%), respeitando com máxima fidelidade o comando do art. 23, § 2º, da Lei nº 14.133/2021.", space_after=8)

    # 3 DAS RAZÕES TÉCNICAS DA INSUFICIÊNCIA DO SINAPI PARA ITENS ESPECÍFICOS
    add_section_header("3 DAS RAZÕES TÉCNICAS DA INSUFICIÊNCIA DO SINAPI PARA ITENS ESPECÍFICOS")

    add_p("8. O SINAPI (Caixa Econômica Federal / IBGE) é concebido para orçamentação de obras e serviços civis correntes (edificações residenciais e comerciais habituais). Não integra o escopo da CEF a catalogação de serviços que envolvem tecnologia proprietária, equipamentos robotizados ou intervenções eletromecânicas em maquinários de grande porte.")

    add_p("9. Caso a Engenharia tentasse adaptar composições ordinárias do SINAPI para tais serviços, geraria uma falsa estimativa orçamentária, com grave risco de licitação deserta ou contratações inexequíveis. A insuficiência do catálogo do SINAPI manifestou-se comprovadamente nos seguintes itens:")

    add_p("9.1. Item 02 – Limpeza Robotizada de Dutos de Climatização (HVAC): O SINAPI apenas precifica a montagem física de redes de dutos novos de chapa galvanizada. Não existe no catálogo federal custo para desinfecção interna mecanizada por escovação rotativa robótica guiada por microcâmeras e aplicação de biocida homologado, serviço expressamente obrigatório por força da Portaria MS nº 3.523/1998, da Resolução RE nº 09/2003 da ANVISA e da ABNT NBR 14679:2012.")

    add_p("9.2. Item 06 – Películas Solares de Alta Rejeição Térmica (Insulfilm de Engenharia): O SINAPI apresenta apenas filme plástico decorativo simples para privacidade visual. O projeto executivo da SRA/MGI-ES demanda película nanocerâmica de alto desempenho com laudo atestando bloqueio de raios infravermelhos (IV ≥ 85%) e ultravioleta (UV ≥ 99%), visando à eficiência energética predial e à redução de carga térmica dos chillers, em perfeita consonância com o Guia Nacional de Contratações Sustentáveis da AGU.")

    add_p("9.3. Item 10 – Manutenção Especializada de Grupo Gerador e Subestação de Média Tensão: O SINAPI contempla a instalação civil do grupo motor-gerador (assentamento). Não possui composições para manutenção preventiva e corretiva especializada com parametrização de quadro de transferência automática (QTA), testes dinâmicos de carga em banco resistivo de potência nem ensaios físico-químicos e cromatográficos de óleo isolante em transformadores de média tensão.")

    add_p("10. Para esses 3 itens atípicos, a estimativa foi realizada com esteio no art. 23, § 2º, inciso V c/c IN SEGES/ME nº 65/2021, apurando valores medianos e decompondo todos os custos em composições analíticas abertas de custos unitários na plataforma Orçafascio (Doc. SEI nº 64507136), em integral cumprimento à Súmula TCU nº 258/2010.", space_after=8)

    # 4 DA PERFEITA ADEQUAÇÃO DA BASE IOPES AO MERCADO LOCAL DE VITÓRIA/ES
    add_section_header("4 DA PERFEITA ADEQUAÇÃO DA BASE IOPES AO MERCADO LOCAL DE VITÓRIA/ES")

    add_p("11. Na ausência de composições no SINAPI para a lavagem técnica de fachada envidraçada em altura (Item 03) e para a limpeza técnica de painéis solares fotovoltaicos (Item 09), a Administração acionou de imediato o inciso III do art. 23, § 2º, adotando a tabela do IOPES (Instituto de Obras Públicas do Espírito Santo). A legitimidade dessa opção fundamenta-se nos seguintes aspectos técnicos:")

    add_p("11.1. Identidade Territorial Direta com o Local da Obra: O Edifício Sede da SRA/MGI-ES e seu Edifício Anexo situam-se na cidade de Vitória/ES. O IOPES é a autarquia técnica oficial do Governo do Estado do Espírito Santo que apura mensalmente os preços de insumos e mão de obra coletados diretamente no mercado da Grande Vitória (Vitória, Vila Velha, Serra e Cariacica). Não se trata de aplicar tabela de outro Estado (como CPOS/SP ou EMOP/RJ), mas sim o banco de dados oficial da própria praça onde os serviços serão executados.")

    add_p("11.2. Aderência às Convenções Coletivas e Normas de Segurança Locais: Os coeficientes de mão de obra do IOPES espelham os salários, encargos e benefícios homologados nas Convenções Coletivas celebradas entre SINDUSCON-ES e SINTRACONST-ES, bem como os adicionais de insalubridade, periculosidade e os equipamentos de segurança obrigatórios para trabalho em altura com alpinismo industrial sob a NR-35.")

    add_p("11.3. Jurisprudência Consolidada do Tribunal de Contas da União: O TCU ratifica que, na falta de itens no SINAPI/SICRO, a utilização de tabelas estaduais formalmente homologadas é o caminho legal e técnico mandatório para a orçamentação fidedigna (Acórdãos TCU nº 2.622/2013-Plenário e nº 1.446/2018-Plenário).")

    # 5 CONCLUSÃO E ENCAMINHAMENTO
    add_section_header("5 CONCLUSÃO E ENCAMINHAMENTO")

    add_p("12. Diante de todo o arcabouço fático e documental demonstrado, este Engenheiro Fiscal certifica e atesta que:")
    add_p("a) O Instrumento de Padronização – IPPC Engenharia da CGU/AGU encontra-se plenamente incorporado e comprovado nos autos mediante o TJTR saneado (Doc. 64474274), o checklist AGU (Doc. 63811592), a ART no CREA-ES (Doc. 64468889) e a matriz de 11 cadernos padronizados, saneando o § 24;")
    add_p("b) A ordem hierárquica do art. 23, § 2º, da Lei nº 14.133/2021 foi estritamente honrada, com mais de 76% da materialidade contratual balizada em tabelas públicas oficiais (SINAPI Vitória e IOPES);")
    add_p("c) A insuficiência do SINAPI para os itens 02, 06 e 10 é técnica e notória, tendo as composições sido detalhadas analiticamente na plataforma Orçafascio (Doc. 64507136) sem verbas genéricas (Súmula 258 TCU);")
    add_p("d) A base IOPES representa com exatidão cirúrgica o mercado da construção civil e manutenção predial da Grande Vitória/ES, conferindo higidez aos preços estimados.")

    add_p("13. Submeto o presente expediente à elevada apreciação de Vossa Senhoria, recomendando o acolhimento integral deste despacho, para oportuna remessa à Consultoria Jurídica da União, considerando-se plenamente atendidas e saneadas as recomendações exaradas nos §§ 24 e 58 do Parecer Jurídico nº 01199/2026/CJENG-EST-SUMÁRIO/SCGP/CGU/AGU (Doc. SEI nº 64468820).", space_after=14)

    # Date and Signature Block (Conforme PDF SEI assinado)
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_after = Pt(14)
    p_date.add_run("Vitória, 22 de setembro de 2026.").font.size = Pt(10)

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

    r_s2 = p_sig.add_run("Engenheiro Civil, MSc.\n")
    r_s2.font.size = Pt(9.5)
    r_s2.font.color.rgb = TEXT_DARK

    r_s3 = p_sig.add_run("CREARJ: 1985100024\n\n")
    r_s3.font.size = Pt(9.5)
    r_s3.font.color.rgb = TEXT_DARK

    r_s4 = p_sig.add_run("Referência: Processo nº 10783.000206/2026-71. SEI nº 64558648")
    r_s4.bold = True
    r_s4.font.size = Pt(9)
    r_s4.font.color.rgb = SLATE

    # Save to disk
    out_dir = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\ORCA-AI\OrcaAI\projetos\_governanca_sei_agu_cgu\despachos_sei"
    out_docx_sei = os.path.join(out_dir, "SEI_64558648_Despacho_Consolidado.docx")
    doc.save(out_docx_sei)
    print(f"Document saved successfully: {out_docx_sei}")

    out_docx_orig = os.path.join(out_dir, "Despacho_SRA_Atendimento_AGU_Paragrafos_24_e_58.docx")
    try:
        doc.save(out_docx_orig)
        print(f"Document updated successfully: {out_docx_orig}")
    except PermissionError:
        print(f"Notice: {out_docx_orig} is currently locked by Word. Saved to {out_docx_sei} instead.")

if __name__ == "__main__":
    create_consolidated_despacho()
