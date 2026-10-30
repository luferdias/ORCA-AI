import os
import subprocess
import sys

# Garantir que openpyxl esteja instalado
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    print("openpyxl não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def criar_excel_bdi():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cálculo do BDI"
    
    # Ativar linhas de grade visualmente no Excel
    ws.views.sheetView[0].showGridLines = True
    
    # Paleta de Cores Premium (Azul Escuro e Tons de Cinza)
    cor_cabecalho_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    cor_cabecalho_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    
    cor_subsecao_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    cor_subsecao_font = Font(name="Segoe UI", size=11, bold=True, color="1F497D")
    
    cor_destaque_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
    
    font_padrao = Font(name="Segoe UI", size=10, bold=False, color="333333")
    font_bold = Font(name="Segoe UI", size=10, bold=True, color="333333")
    font_titulo = Font(name="Segoe UI", size=14, bold=True, color="1F497D")
    font_formula = Font(name="Consolas", size=9, italic=True, color="555555")
    
    # Bordas
    border_fina = Side(border_style="thin", color="C0C0C0")
    border_double = Side(border_style="double", color="1F497D")
    border_thick = Side(border_style="medium", color="1F497D")
    
    box_border = Border(left=border_fina, right=border_fina, top=border_fina, bottom=border_fina)
    total_border = Border(top=border_fina, bottom=border_double)
    
    # Título da Planilha
    ws["A1"] = "CÁLCULO E SIMULAÇÃO DETALHADA DO BDI"
    ws["A1"].font = font_titulo
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 30
    
    ws["A2"] = "Referência: Acórdão TCU nº 2.622/2013 - Plenário | Regime: COM DESONERAÇÃO"
    ws["A2"].font = Font(name="Segoe UI", size=10, italic=True, color="555555")
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 20
    
    # Cabeçalhos
    headers = ["Item", "Componente do BDI", "Sigla", "Taxa (%)", "Justificativa / Parâmetro de Referência"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.fill = cor_cabecalho_fill
        cell.font = cor_cabecalho_font
        cell.alignment = Alignment(horizontal="center" if col_idx <= 3 else "left", vertical="center")
    ws.row_dimensions[4].height = 26
    
    # Dados da tabela
    dados = [
        # Linha 5
        ["1.0", "Custos Indiretos e Margens", "", "", ""], 
        # Linhas 6 a 11
        ["1.1", "Administração Central", "AC", 0.0380, "Rateio dos custos administrativos de matriz compatível com complexidade do contrato."],
        ["1.2", "Seguros", "S", 0.0080, "Cobertura de seguros de riscos de engenharia e responsabilidade civil."],
        ["1.3", "Riscos", "R", 0.0100, "Provisão para imprevistos (trabalhos em altura, instalações elétricas e espaço confinado)."],
        ["1.4", "Garantias", "G", 0.0096, "Exigência contratual de garantia de execução financeira do objeto."],
        ["1.5", "Despesas Financeiras", "DF", 0.0100, "Custo de oportunidade decorrente do fluxo de caixa e intervalo de pagamento."],
        ["1.6", "Lucro (Remuneração)", "L", 0.0610, "Margem de remuneração bruta justa para execução do objeto."],
        
        # Linha 12
        ["2.0", "Tributos Incidentes sobre o Faturamento", "", "", ""],
        # Linhas 13 a 15
        ["2.1", "PIS", "PIS", 0.0065, "Alíquota sob regime de incidência cumulativa (Lei 9.718/98)."],
        ["2.2", "COFINS", "COFINS", 0.0300, "Alíquota sob regime de incidência cumulativa (Lei 9.718/98)."],
        ["2.3", "ISSQN", "ISS", 0.0500, "Imposto Sobre Serviços de Qualquer Natureza (alíquota local média)."],
        
        # Linha 16
        ["2.4", "Soma dos Tributos", "I", "=SUM(D13:D15)", "Total de impostos que incidem sobre o preço de venda."]
    ]
    
    current_row = 5
    for r in dados:
        is_subheading = (r[1] in ["Custos Indiretos e Margens", "Tributos Incidentes sobre o Faturamento"])
        is_sum_tributos = (r[1] == "Soma dos Tributos")
        
        # Escrever células
        for col_idx, val in enumerate(r, 1):
            if is_subheading and col_idx > 2:
                # Não gravar valor nas colunas mescladas secundárias
                cell = ws.cell(row=current_row, column=col_idx)
            else:
                cell = ws.cell(row=current_row, column=col_idx, value=val)
            
            # Estilos de Font, Fill e Borders
            if is_subheading:
                cell.font = cor_subsecao_font
                cell.fill = cor_subsecao_fill
            elif is_sum_tributos:
                cell.font = font_bold
                cell.fill = cor_destaque_fill
                cell.border = total_border
                if col_idx == 4:
                    cell.number_format = '0.00%'
            else:
                cell.font = font_padrao
                cell.border = box_border
                if col_idx == 4:
                    cell.number_format = '0.00%'
                    
            # Alinhamentos específicos
            if col_idx == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [2, 5]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif col_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 4 and not is_subheading:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                
        # Fazer mesclagem da subseção depois de tratar as células
        if is_subheading:
            ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=5)
            
        ws.row_dimensions[current_row].height = 20
        current_row += 1
        
    # Pular uma linha
    current_row += 1
    
    # Linha do BDI Calculado
    ws.cell(row=current_row, column=1, value="3.0").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=current_row, column=1).font = font_bold
    ws.cell(row=current_row, column=1).border = Border(top=border_thick, bottom=border_thick, left=border_fina, right=border_fina)
    
    lbl_bdi = ws.cell(row=current_row, column=2, value="TAXA DE BDI CALCULADA (RESULTANTE)")
    lbl_bdi.font = Font(name="Segoe UI", size=11, bold=True, color="1F497D")
    lbl_bdi.fill = cor_subsecao_fill
    lbl_bdi.alignment = Alignment(horizontal="left", vertical="center")
    lbl_bdi.border = Border(top=border_thick, bottom=border_thick, left=border_fina, right=border_fina)
    
    ws.cell(row=current_row, column=3, value="BDI").alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=current_row, column=3).font = font_bold
    ws.cell(row=current_row, column=3).fill = cor_subsecao_fill
    ws.cell(row=current_row, column=3).border = Border(top=border_thick, bottom=border_thick, left=border_fina, right=border_fina)
    
    # FÓRMULA DO BDI DO TCU
    # AC = D6, S = D7, R = D8, G = D9, DF = D10, L = D11, I = D16
    formula_bdi = "=ROUND((((1+(D6+D7+D8+D9))*(1+D10)*(1+D11))/(1-D16))-1, 4)"
    val_bdi = ws.cell(row=current_row, column=4, value=formula_bdi)
    val_bdi.font = Font(name="Segoe UI", size=11, bold=True, color="1F497D")
    val_bdi.fill = cor_subsecao_fill
    val_bdi.number_format = '0.00%'
    val_bdi.alignment = Alignment(horizontal="right", vertical="center")
    val_bdi.border = Border(top=border_thick, bottom=border_thick, left=border_fina, right=border_fina)
    
    ws.cell(row=current_row, column=5, value="Fórmula oficial do TCU aplicada sobre o custo direto.").font = font_bold
    ws.cell(row=current_row, column=5).fill = cor_subsecao_fill
    ws.cell(row=current_row, column=5).alignment = Alignment(horizontal="left", vertical="center")
    ws.cell(row=current_row, column=5).border = Border(top=border_thick, bottom=border_thick, left=border_fina, right=border_fina)
    
    ws.row_dimensions[current_row].height = 26
    
    # Mostrar a fórmula em formato de texto para clareza
    current_row += 2
    ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=5)
    formula_txt_cell = ws.cell(row=current_row, column=2, value="Fórmula de Referência TCU: BDI = [((1 + (AC + S + R + G)) * (1 + DF) * (1 + L)) / (1 - I)] - 1")
    formula_txt_cell.font = font_formula
    formula_txt_cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # Fazer merge do cabeçalho de título
    ws.merge_cells("A1:E1")
    ws.merge_cells("A2:E2")
    
    # Ajustar as larguras das colunas para visualização perfeita
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 38
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 14
    ws.column_dimensions['E'].width = 75
    
    # Garantir que a pasta destino exista
    os.makedirs(r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra", exist_ok=True)
    
    output_path = r"c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Calculo_BDI_TCU_25.xlsx"
    wb.save(output_path)
    print(f"Planilha Excel criada com sucesso em: {output_path}")

if __name__ == "__main__":
    criar_excel_bdi()
