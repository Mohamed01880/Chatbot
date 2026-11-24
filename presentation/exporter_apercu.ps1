# Génère les aperçus PNG et le PDF depuis le fichier PowerPoint déjà préparé.
$ErrorActionPreference = 'Stop'
$deckFolder = $PSScriptRoot
$deckPath = Join-Path $deckFolder 'Presentation_Chatbot_RAG_Visuelle.pptx'
$pdfPath = Join-Path $deckFolder 'Presentation_Chatbot_RAG_Visuelle.pdf'
$previewPath = Join-Path $deckFolder 'apercu'
New-Item -ItemType Directory -Path $previewPath -Force | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $ppt.Presentations.Open($deckPath, -1, 0, 0)
    $overflow = @()
    foreach ($slide in $deck.Slides) {
        foreach ($item in $slide.Shapes) {
            if ($item.HasTextFrame -and $item.TextFrame.HasText) {
                $actual = $item.TextFrame2.TextRange.BoundHeight
                if ($actual -gt ($item.Height + 3)) {
                    $overflow += [PSCustomObject]@{ Slide=$slide.SlideIndex; Text=$item.TextFrame.TextRange.Text; Height=$item.Height; TextHeight=$actual }
                }
            }
        }
    }
    $deck.Export($previewPath, 'PNG', 1600, 900)
    $deck.SaveAs($pdfPath, 32)
    $overflow | ConvertTo-Json -Depth 3
    Write-Output ('Export terminé : ' + $deck.Slides.Count + ' diapositives et PDF.')
} finally {
    if ($null -ne $deck) { $deck.Close() }
    # Ne pas quitter PowerPoint : l’utilisateur y a déjà une présentation ouverte.
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt)
}
