param (
    [string]$Directory
)

$word = New-Object -ComObject Word.Application
$excel = New-Object -ComObject Excel.Application

$word.Visible = $false
$excel.Visible = $false
$excel.DisplayAlerts = $false

$docxFiles = Get-ChildItem -Path $Directory -Filter "*.docx" -Recurse
foreach ($file in $docxFiles) {
    if ($file.Name -notmatch "~\$") {
        Write-Host "Converting $($file.FullName)"
        $doc = $word.Documents.Open($file.FullName)
        $pdfPath = $file.FullName -replace '\.docx$', '.pdf'
        $doc.SaveAs([ref] $pdfPath, [ref] 17) # 17 is wdFormatPDF
        $doc.Close()
    }
}

$xlsxFiles = Get-ChildItem -Path $Directory -Filter "*.xlsx" -Recurse
foreach ($file in $xlsxFiles) {
    if ($file.Name -notmatch "~\$") {
        Write-Host "Converting $($file.FullName)"
        $wb = $excel.Workbooks.Open($file.FullName)
        $pdfPath = $file.FullName -replace '\.xlsx$', '.pdf'
        # xlTypePDF = 0
        $wb.ExportAsFixedFormat(0, $pdfPath)
        $wb.Close($false)
    }
}

$word.Quit()
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
