$docxPath = "c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca\OrcaAI\Entregavel_3_TRL_e_PI_OrcaAI.docx"
$pdfPath = "c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra\Orca\OrcaAI\Entregavel_3_TRL_e_PI_OrcaAI.pdf"

Write-Host "Iniciando conversao Word -> PDF..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    $doc = $word.Documents.Open($docxPath)
    $doc.SaveAs([ref] $pdfPath, [ref] 17) # 17 = wdFormatPDF
    $doc.Close()
    Write-Host "PDF gerado com sucesso em: $pdfPath"
} catch {
    Write-Error "Erro ao converter para PDF: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
