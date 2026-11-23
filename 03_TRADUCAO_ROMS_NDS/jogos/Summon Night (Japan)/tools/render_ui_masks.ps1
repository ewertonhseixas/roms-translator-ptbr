Add-Type -AssemblyName System.Drawing
$requests = [Console]::In.ReadToEnd() | ConvertFrom-Json
$results = foreach ($request in $requests) {
    $bitmap = [Drawing.Bitmap]::new(280, 36)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([Drawing.Color]::Black)
    $graphics.TextRenderingHint = [Drawing.Text.TextRenderingHint]::SingleBitPerPixelGridFit
    $style = if ($request.bold) { [Drawing.FontStyle]::Bold } else { [Drawing.FontStyle]::Regular }
    $font = [Drawing.Font]::new($request.family, $request.size, $style, [Drawing.GraphicsUnit]::Pixel)
    $graphics.DrawString($request.text, $font, [Drawing.Brushes]::White, 2, 2)
    $pixels = [System.Collections.Generic.List[int]]::new()
    for ($y = 0; $y -lt $bitmap.Height; $y++) {
        for ($x = 0; $x -lt $bitmap.Width; $x++) {
            if ($bitmap.GetPixel($x, $y).R -gt 127) { $pixels.Add($y * 280 + $x) }
        }
    }
    [pscustomobject]@{ pixels = $pixels }
    $font.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()
}
ConvertTo-Json -InputObject @($results) -Depth 4 -Compress
