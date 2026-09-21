$directories = Get-ChildItem -Path "c:\Users\luis.fernando\OneDrive\04 - Meus Documentos\GitHub\Orcamento_de_Obra" -Filter "Item*" -Directory
foreach ($dir in $directories) {
    Write-Host "Running for $($dir.FullName)"
    powershell.exe -ExecutionPolicy Bypass -File .\convert_to_pdf.ps1 -Directory $dir.FullName
}
