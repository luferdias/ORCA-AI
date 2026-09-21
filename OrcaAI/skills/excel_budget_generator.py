"""
Compilador de Planilhas Orçamentárias em Excel (.xlsx) - OrcaAI
Gera arquivos Excel com abas coordenadas para Orçamento, CPUs Próprias, BDI e Cronograma.
"""

from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def criar_planilha_orcamentaria_excel(
    nome_obra: str,
    local: str,
    data_base: str,
    itens_orcamento: List[Dict[str, Any]],
    composicoes_proprias: List[Dict[str, Any]] = None,
    bdi_servico: float = 25.0,
    bdi_fornecimento: float = 14.02,
    caminho_saida: str = "Planilha_Orcamentaria_OrcaAI.xlsx"
) -> str:
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Estilos Padronizados MGI/SRA-ES
    # ----------------------------------------------------
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid") # Azul Petróleo Institucional
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=14, bold=True, color="1F4E79")
    subtitle_font = Font(name="Calibri", size=10, italic=True, color="595959")
    bold_font = Font(name="Calibri", size=11, bold=True)
    normal_font = Font(name="Calibri", size=10)
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # ====================================================
    # ABA 1: PLANILHA ORÇAMENTÁRIA
    # ====================================================
    ws1 = wb.active
    ws1.title = "01_Planilha_Orcamentaria"
    ws1.views.sheetView[0].showGridLines = True
    
    # Cabeçalho do Projeto
    ws1["A1"] = "MINISTÉRIO DA GESTÃO E DA INOVAÇÃO EM SERVIÇOS PÚBLICOS - MGI"
    ws1["A1"].font = title_font
    ws1["A2"] = f"SUPERINTENDÊNCIA REGIONAL DE ADMINISTRAÇÃO NO ESPÍRITO SANTO (SRA-ES)"
    ws1["A2"].font = bold_font
    ws1["A3"] = f"OBRA: {nome_obra} | LOCAL: {local} | DATA-BASE: {data_base}"
    ws1["A3"].font = subtitle_font
    
    colunas_orc = [
        "ITEM", "CÓDIGO", "FONTE", "DESCRIÇÃO DOS SERVIÇOS E MATERIAIS",
        "UNID.", "QUANT.", "CUSTO UNIT. (R$)", "BDI (%)", "PREÇO UNIT. (R$)", "TOTAL (R$)"
    ]
    
    row_idx = 5
    for col_idx, col_name in enumerate(colunas_orc, start=1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    row_idx = 6
    for it in itens_orcamento:
        ws1.cell(row=row_idx, column=1, value=it.get("item", "")).alignment = Alignment(horizontal="center")
        ws1.cell(row=row_idx, column=2, value=it.get("codigo", "")).alignment = Alignment(horizontal="center")
        ws1.cell(row=row_idx, column=3, value=it.get("fonte", "")).alignment = Alignment(horizontal="center")
        ws1.cell(row=row_idx, column=4, value=it.get("descricao", "")).alignment = Alignment(horizontal="left", wrap_text=True)
        ws1.cell(row=row_idx, column=5, value=it.get("unidade", "")).alignment = Alignment(horizontal="center")
        
        c_qtd = ws1.cell(row=row_idx, column=6, value=float(it.get("quantidade", 0.0)))
        c_qtd.number_format = "#,##0.00"
        
        c_custo = ws1.cell(row=row_idx, column=7, value=float(it.get("custo_unitario", 0.0)))
        c_custo.number_format = "R$ #,##0.00"
        
        bdi_val = float(it.get("bdi", bdi_servico))
        c_bdi = ws1.cell(row=row_idx, column=8, value=bdi_val / 100.0)
        c_bdi.number_format = "0.00%"
        
        # Fórmulas Excel Nativas
        c_preco = ws1.cell(row=row_idx, column=9, value=f"=G{row_idx}*(1+H{row_idx})")
        c_preco.number_format = "R$ #,##0.00"
        
        c_total = ws1.cell(row=row_idx, column=10, value=f"=F{row_idx}*I{row_idx}")
        c_total.number_format = "R$ #,##0.00"
        
        for c in range(1, 11):
            ws1.cell(row=row_idx, column=c).border = thin_border
            ws1.cell(row=row_idx, column=c).font = normal_font
            
        row_idx += 1
        
    # Linha de Total Geral
    ws1.cell(row=row_idx, column=4, value="TOTAL GERAL DO ORÇAMENTO (R$)").font = bold_font
    ws1.cell(row=row_idx, column=4).alignment = Alignment(horizontal="right")
    total_geral_cell = ws1.cell(row=row_idx, column=10, value=f"=SUM(J6:J{row_idx-1})")
    total_geral_cell.font = bold_font
    total_geral_cell.number_format = "R$ #,##0.00"
    total_geral_cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    
    # Auto-ajuste de colunas
    larguras = [8, 14, 12, 55, 10, 12, 16, 12, 16, 18]
    for i, w in enumerate(larguras, start=1):
        ws1.column_dimensions[get_column_letter(i)].width = w

    # ====================================================
    # ABA 2: COMPOSIÇÕES PRÓPRIAS (CPUs)
    # ====================================================
    if composicoes_proprias:
        ws2 = wb.create_sheet(title="02_Composicoes_Proprias")
        ws2.views.sheetView[0].showGridLines = True
        ws2["A1"] = "COMPOSIÇÕES DE CUSTOS UNITÁRIOS PRÓPRIAS (SRAES-CP)"
        ws2["A1"].font = title_font
        
        row_cpu = 3
        for cp in composicoes_proprias:
            ws2.cell(row=row_cpu, column=1, value=f"CÓDIGO: {cp.get('codigo')}").font = bold_font
            ws2.cell(row=row_cpu, column=2, value=f"DESCRIÇÃO: {cp.get('descricao')}").font = bold_font
            ws2.cell(row=row_cpu, column=4, value=f"UNIDADE: {cp.get('unidade')}").font = bold_font
            row_cpu += 1
            
            headers_cpu = ["TIPO", "CÓDIGO INSUMO", "DESCRIÇÃO DO INSUMO", "UNID.", "COEFICIENTE", "PREÇO UNIT. (R$)", "TOTAL (R$)"]
            for c_i, h_t in enumerate(headers_cpu, start=1):
                c = ws2.cell(row=row_cpu, column=c_i, value=h_t)
                c.fill = PatternFill(start_color="595959", end_color="595959", fill_type="solid")
                c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            row_cpu += 1
            
            insumos = cp.get("insumos", [])
            inicio_insumos = row_cpu
            for ins in insumos:
                ws2.cell(row=row_cpu, column=1, value=ins.get("tipo", "Material")).alignment = Alignment(horizontal="center")
                ws2.cell(row=row_cpu, column=2, value=ins.get("codigo", "")).alignment = Alignment(horizontal="center")
                ws2.cell(row=row_cpu, column=3, value=ins.get("descricao", "")).alignment = Alignment(horizontal="left")
                ws2.cell(row=row_cpu, column=4, value=ins.get("unidade", "")).alignment = Alignment(horizontal="center")
                
                c_coef = ws2.cell(row=row_cpu, column=5, value=float(ins.get("coeficiente", 1.0)))
                c_coef.number_format = "#,##0.0000"
                
                c_pr = ws2.cell(row=row_cpu, column=6, value=float(ins.get("preco_unitario", 0.0)))
                c_pr.number_format = "R$ #,##0.00"
                
                c_tot = ws2.cell(row=row_cpu, column=7, value=f"=E{row_cpu}*F{row_cpu}")
                c_tot.number_format = "R$ #,##0.00"
                
                for c in range(1, 8):
                    ws2.cell(row=row_cpu, column=c).border = thin_border
                    ws2.cell(row=row_cpu, column=c).font = normal_font
                row_cpu += 1
                
            fim_insumos = row_cpu - 1
            ws2.cell(row=row_cpu, column=6, value="CUSTO DIRETO TOTAL (R$):").font = bold_font
            ws2.cell(row=row_cpu, column=7, value=f"=SUM(G{inicio_insumos}:G{fim_insumos})").font = bold_font
            ws2.cell(row=row_cpu, column=7).number_format = "R$ #,##0.00"
            row_cpu += 3

        larguras_cpu = [12, 16, 45, 10, 14, 16, 18]
        for i, w in enumerate(larguras_cpu, start=1):
            ws2.column_dimensions[get_column_letter(i)].width = w

    wb.save(caminho_saida)
    return caminho_saida


if __name__ == "__main__":
    itens_teste = [
        {
            "item": "1.1", "codigo": "98458", "fonte": "SINAPI-ES",
            "descricao": "LIMPEZA DE SUPERFÍCIE COM HIDROJATEAMENTO DE ALTA PRESSÃO",
            "unidade": "M2", "quantidade": 500.0, "custo_unitario": 12.50, "bdi": 25.0
        },
        {
            "item": "1.2", "codigo": "SRAES-CP-001", "fonte": "PRÓPRIA",
            "descricao": "TRATAMENTO ESPECIALIZADO DE JUNTA DE DILATAÇÃO ESTRUTURAL",
            "unidade": "M", "quantidade": 120.0, "custo_unitario": 145.00, "bdi": 25.0
        }
    ]
    cp_teste = [
        {
            "codigo": "SRAES-CP-001",
            "descricao": "TRATAMENTO ESPECIALIZADO DE JUNTA DE DILATAÇÃO",
            "unidade": "M",
            "insumos": [
                {"tipo": "Material", "codigo": "SRAES-INS-001", "descricao": "Mastique Elastomérico de Poliuretano", "unidade": "UN", "coeficiente": 0.40, "preco_unitario": 65.00},
                {"tipo": "Mão de Obra", "codigo": "88316", "descricao": "Servente com Encargos Complementares", "unidade": "H", "coeficiente": 0.50, "preco_unitario": 22.50},
                {"tipo": "Mão de Obra", "codigo": "88309", "descricao": "Pedreiro com Encargos Complementares", "unidade": "H", "coeficiente": 0.50, "preco_unitario": 28.00}
            ]
        }
    ]
    arquivo = criar_planilha_orcamentaria_excel(
        "Edifício Sede MGI-ES", "Vitória/ES", "05/2026", itens_teste, cp_teste, caminho_saida="Orcamento_Teste_OrcaAI.xlsx"
    )
    print(f"Planilha Excel gerada com sucesso: {arquivo}")
