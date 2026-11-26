# Exports slides/memory_for_llm_agents.pptx to PDF and to 1920x1080 PNGs (one per slide) with PowerPoint.
# Usage (from the repo root):  powershell -ExecutionPolicy Bypass -File src\export_slides.ps1 [-PngDir <folder>]
param([string]$PngDir = "build\slides_png")
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$pptx = Join-Path $root "slides\memory_for_llm_agents.pptx"
$pdf = Join-Path $root "slides\memory_for_llm_agents.pdf"
if (-not [System.IO.Path]::IsPathRooted($PngDir)) { $PngDir = Join-Path $root $PngDir }
New-Item -ItemType Directory -Force $PngDir | Out-Null
Get-ChildItem $PngDir -Filter "slide*.png" | Remove-Item -Force -Confirm:$false
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($pptx, $true, $false, $false)
    $pres.SaveAs($pdf, 32)   # 32 = ppSaveAsPDF
    $i = 1
    foreach ($slide in $pres.Slides) {
        $slide.Export((Join-Path $PngDir ("slide{0:D2}.png" -f $i)), "PNG", 1920, 1080)
        $i++
    }
    Write-Output ("exported {0} slides to {1}" -f $pres.Slides.Count, $PngDir)
    $pres.Close()
}
finally {
    $app.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($app) | Out-Null
}
