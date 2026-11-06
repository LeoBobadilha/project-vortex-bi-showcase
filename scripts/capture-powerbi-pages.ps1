param([string]$PowerBIDesktopVersion = '')

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
if (-not ('VortexCapture.Native' -as [type])) { Add-Type @'
using System;
using System.Runtime.InteropServices;
namespace VortexCapture {
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X; public int Y; }
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct MSG { public IntPtr hwnd; public uint message; public UIntPtr wParam; public IntPtr lParam; public uint time; public POINT pt; }
  public static class Native {
    [DllImport("user32.dll", SetLastError=true)] public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint modifiers, uint key);
    [DllImport("user32.dll", SetLastError=true)] public static extern bool UnregisterHotKey(IntPtr hWnd, int id);
    [DllImport("user32.dll", SetLastError=true)] public static extern int GetMessage(out MSG msg, IntPtr hWnd, uint min, uint max);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", SetLastError=true)] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
  }
}
'@ }

$pages = @(
  [pscustomobject]@{ File='04-Performance.png'; Page='04 - Portfolio Performance' },
  [pscustomobject]@{ File='05-Risk.png'; Page='05 - Risk & Drawdown' },
  [pscustomobject]@{ File='06-Trade-Explorer.png'; Page='06 - Trade Explorer' },
  [pscustomobject]@{ File='07-Validation.png'; Page='07 - Forward Validation & Governance' },
  [pscustomobject]@{ File='08-W02-Win.png'; Page='08 - Winning Case W02' },
  [pscustomobject]@{ File='09-W03-Win.png'; Page='09 - Winning Case W03' },
  [pscustomobject]@{ File='10-W04-Win.png'; Page='10 - Winning Case W04' },
  [pscustomobject]@{ File='11-W05-Win.png'; Page='11 - Winning Case W05' }
)

$biRepo = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $biRepo
$websiteRepo = Join-Path $workspaceRoot 'project-vortex-portfolio'
$biImageDir = Join-Path $biRepo 'images\powerbi'
$websiteImageDir = Join-Path $websiteRepo 'public\images\powerbi'
$approvedReference = Join-Path $biImageDir '01-Knowledge.png'
foreach ($requiredPath in @($approvedReference, $websiteImageDir, (Join-Path $biRepo 'PowerBI\ProjectVortex-Public.pbip'))) {
  if (-not (Test-Path -LiteralPath $requiredPath)) { throw "Required release asset is missing: $requiredPath" }
}

$referenceImage = [System.Drawing.Image]::FromFile($approvedReference)
try { $expectedWidth = $referenceImage.Width; $expectedHeight = $referenceImage.Height }
finally { $referenceImage.Dispose() }

# Resume safely: skip a page only if both repositories already contain identical bytes.
$pending = [System.Collections.Generic.List[object]]::new()
foreach ($item in $pages) {
  $biPath = Join-Path $biImageDir $item.File
  $sitePath = Join-Path $websiteImageDir $item.File
  $biExists = Test-Path -LiteralPath $biPath
  $siteExists = Test-Path -LiteralPath $sitePath
  if ($biExists -and $siteExists) {
    $biHash = (Get-FileHash -LiteralPath $biPath -Algorithm SHA256).Hash
    $siteHash = (Get-FileHash -LiteralPath $sitePath -Algorithm SHA256).Hash
    if ($biHash -ne $siteHash) { throw "Existing copies differ for $($item.File); reconcile them before recapturing." }
    Write-Host "Already present in both repositories; skipping $($item.File)."
    continue
  }
  if ($biExists -or $siteExists) { throw "Only one repository has $($item.File); reconcile before capture. No file overwritten." }
  $pending.Add($item)
}
if ($pending.Count -eq 0) { Write-Host 'All eight requested pages already exist identically in both repositories.'; exit 0 }

$captureRoot = Join-Path $env:LOCALAPPDATA 'ProjectVortex\PowerBI_Capture'
$runDir = Join-Path $captureRoot (Get-Date -Format 'yyyyMMdd-HHmmss')
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
if ([string]::IsNullOrWhiteSpace($PowerBIDesktopVersion)) { $PowerBIDesktopVersion = Read-Host 'Power BI Desktop version from Help > About' }
$records = [System.Collections.Generic.List[object]]::new()

if (-not [VortexCapture.Native]::RegisterHotKey([IntPtr]::Zero, 1, 0, 0x78)) { throw 'Could not register F9 capture hotkey.' }
if (-not [VortexCapture.Native]::RegisterHotKey([IntPtr]::Zero, 2, 0, 0x1B)) { [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 1) | Out-Null; throw 'Could not register Escape hotkey.' }

try {
  Write-Host "Private capture evidence: $runDir"
  Write-Host "Required capture dimensions: ${expectedWidth}x${expectedHeight} (match the six approved screenshots)."
  Write-Host 'Open and refresh the public PBIP, maximize Power BI Desktop, hide editing panes, and use report full-screen view.'
  Write-Host 'Select each named page in order. Wait for every visual to finish rendering, then press F9 once with Power BI foreground.'
  Write-Host 'Each accepted capture is saved immediately to both repositories using its required filename. Escape stops safely.'
  Write-Host "Next page: $($pending[0].Page)"
  $index = 0
  while ($index -lt $pending.Count) {
    $msg = [VortexCapture.MSG]::new()
    $result = [VortexCapture.Native]::GetMessage([ref]$msg, [IntPtr]::Zero, 0, 0)
    if ($result -le 0) { break }
    if ($msg.message -ne 0x0312) { continue }
    $hotkey = [int]$msg.wParam.ToUInt32()
    if ($hotkey -eq 2) { Write-Host 'Capture stopped by Escape.'; break }
    if ($hotkey -ne 1) { continue }

    $window = [VortexCapture.Native]::GetForegroundWindow()
    $title = [System.Text.StringBuilder]::new(512)
    [void][VortexCapture.Native]::GetWindowText($window, $title, $title.Capacity)
    if ($title.ToString() -notmatch '(?i)Power BI') { Write-Warning 'Power BI is not the foreground window; no image was captured.'; continue }

    $rect = [VortexCapture.RECT]::new()
    if (-not [VortexCapture.Native]::GetWindowRect($window, [ref]$rect)) { Write-Warning 'Could not read the Power BI window bounds.'; continue }
    $bounds = [System.Windows.Forms.Screen]::FromRectangle([System.Drawing.Rectangle]::FromLTRB($rect.Left,$rect.Top,$rect.Right,$rect.Bottom)).Bounds
    if ($bounds.Width -ne $expectedWidth -or $bounds.Height -ne $expectedHeight) {
      throw "Capture display is $($bounds.Width)x$($bounds.Height); approved screenshots require ${expectedWidth}x${expectedHeight}. Adjust display/report framing, then rerun."
    }

    $item = $pending[$index]
    $stagePath = Join-Path $runDir $item.File
    $bitmap = [System.Drawing.Bitmap]::new($bounds.Width,$bounds.Height)
    try {
      $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
      try { $graphics.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size); $bitmap.Save($stagePath,[System.Drawing.Imaging.ImageFormat]::Png) }
      finally { $graphics.Dispose() }
    } finally { $bitmap.Dispose() }

    $checkImage = [System.Drawing.Image]::FromFile($stagePath)
    try {
      if ($checkImage.Width -ne $expectedWidth -or $checkImage.Height -ne $expectedHeight) { throw "Image dimensions are wrong for $($item.File)." }
    } finally { $checkImage.Dispose() }
    $hash = (Get-FileHash -LiteralPath $stagePath -Algorithm SHA256).Hash.ToLowerInvariant()
    $biPath = Join-Path $biImageDir $item.File
    $sitePath = Join-Path $websiteImageDir $item.File
    Copy-Item -LiteralPath $stagePath -Destination $biPath
    try { Copy-Item -LiteralPath $stagePath -Destination $sitePath }
    catch { Remove-Item -LiteralPath $biPath -ErrorAction SilentlyContinue; throw }
    $records.Add([pscustomobject]@{ file=$item.File; page=$item.Page; width=$expectedWidth; height=$expectedHeight; sha256=$hash })
    Write-Host ("Saved {0} to both repositories ({1}x{2}, SHA256 {3})" -f $item.File,$expectedWidth,$expectedHeight,$hash)
    $index++
    if ($index -lt $pending.Count) { Write-Host "Next page: $($pending[$index].Page)" }
  }
  $manifest = [pscustomobject]@{ source='Actual Power BI Desktop screen capture'; desktopVersion=$PowerBIDesktopVersion; capturedAt=(Get-Date).ToString('o'); requestedPages=$pending.Count; capturedPages=$records }
  [IO.File]::WriteAllText((Join-Path $runDir 'capture-manifest.json'),($manifest | ConvertTo-Json -Depth 5),[System.Text.UTF8Encoding]::new($false))
  if ($index -eq $pending.Count) { Write-Host "Captured and copied all $($pending.Count) pending pages. Visually inspect each PNG before release; capture does not verify report content or overlays." }
  else { Write-Warning "Saved $index of $($pending.Count) pending pages. Rerun this helper to resume; identical copies are skipped." }
} finally {
  [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 1) | Out-Null
  [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 2) | Out-Null
}
