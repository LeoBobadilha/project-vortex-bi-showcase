param([switch]$Reset)
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$dataRoot = Join-Path $repoRoot 'data'
$expressionFile = Join-Path $repoRoot 'PowerBI\ProjectVortex.SemanticModel\definition\expressions.tmdl'
if (-not (Test-Path -LiteralPath $dataRoot)) { throw "Power BI Data directory not found: $dataRoot" }
$value = if ($Reset) { '__CONFIGURE_DATA_ROOT__/' } else { ((Resolve-Path -LiteralPath $dataRoot).Path -replace '\\','/') + '/' }
$content = Get-Content -LiteralPath $expressionFile -Raw -Encoding UTF8
$replacement = 'expression DataRoot = "' + $value + '" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
$updated = [regex]::Replace($content, '(?m)^expression DataRoot = .*$', [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $replacement })
if ($updated -eq $content -and -not $Reset -and $content -notmatch [regex]::Escape($value)) { throw 'Could not update DataRoot parameter.' }
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($expressionFile, $updated, $utf8)
if ($Reset) { Write-Output 'DataRoot reset to clone-safe placeholder.' } else { Write-Output 'DataRoot configured for this clone; do not commit this machine-specific value.' }

