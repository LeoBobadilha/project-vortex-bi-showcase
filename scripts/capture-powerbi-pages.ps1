param([switch]$AllPages, [string]$PowerBIDesktopVersion = '')
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @'
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
'@

$all = @(
  [pscustomobject]@{ File='01-Knowledge.png'; Page='01 — Knowledge & Intelligence' },
  [pscustomobject]@{ File='02-Research.png'; Page='02 — Autonomous Research Pipeline' },
  [pscustomobject]@{ File='03-Executive.png'; Page='03 — Executive Overview' },
  [pscustomobject]@{ File='04-Performance.png'; Page='04 — Portfolio Performance' },
  [pscustomobject]@{ File='05-Risk.png'; Page='05 — Risk & Drawdown' },
  [pscustomobject]@{ File='06-Trade-Explorer.png'; Page='06 — Trade Explorer' },
  [pscustomobject]@{ File='07-Validation.png'; Page='07 — Forward Validation & Governance' },
  [pscustomobject]@{ File='08-W02-Win.png'; Page='08 — Winning Case W02' },
  [pscustomobject]@{ File='09-W03-Win.png'; Page='09 — Winning Case W03' },
  [pscustomobject]@{ File='10-W04-Win.png'; Page='10 — Winning Case W04' },
  [pscustomobject]@{ File='11-W05-Win.png'; Page='11 — Winning Case W05' },
  [pscustomobject]@{ File='12-W06-Win.png'; Page='12 — Winning Case W06' },
  [pscustomobject]@{ File='13-L01-Loss.png'; Page='13 — Losing Case L01' },
  [pscustomobject]@{ File='14-L02-Loss.png'; Page='14 — Losing Case L02' }
)
$pages = if ($AllPages) { $all } else { $all | Where-Object { $_.File -in @('04-Performance.png','05-Risk.png','06-Trade-Explorer.png','07-Validation.png','08-W02-Win.png','09-W03-Win.png','10-W04-Win.png','11-W05-Win.png') } }
$captureRoot = Join-Path $env:LOCALAPPDATA 'ProjectVortex\PowerBI_Capture'
$runDir = Join-Path $captureRoot (Get-Date -Format 'yyyyMMdd-HHmmss')
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
if ([string]::IsNullOrWhiteSpace($PowerBIDesktopVersion)) { $PowerBIDesktopVersion = Read-Host 'Power BI Desktop version from Help > About' }
$records = [System.Collections.Generic.List[object]]::new()

if (-not [VortexCapture.Native]::RegisterHotKey([IntPtr]::Zero, 1, 0, 0x78)) { throw 'Could not register F9 capture hotkey.' }
if (-not [VortexCapture.Native]::RegisterHotKey([IntPtr]::Zero, 2, 0, 0x1B)) { [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 1) | Out-Null; throw 'Could not register Escape hotkey.' }

try {
  Write-Host "Capture folder: $runDir"
  Write-Host 'Open the public PBIP in Power BI Desktop, refresh it, maximize the report and use full-screen report view.'
  Write-Host 'Navigate to each requested page in the listed order. Press F9 while Power BI is foreground to capture; press Escape to stop.'
  Write-Host "Next page: $($pages[0].Page)"
  $index = 0
  while ($index -lt $pages.Count) {
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
    if ($bounds.Width -lt 1920 -or $bounds.Height -lt 1080) { throw "Capture display is too small ($($bounds.Width)x$($bounds.Height)); use at least 1920x1080." }
    if ([Math]::Abs(($bounds.Width / $bounds.Height) - (16.0 / 9.0)) -gt 0.01) { throw "Capture display must be close to 16:9; found $($bounds.Width)x$($bounds.Height)." }

    $item = $pages[$index]
    $path = Join-Path $runDir $item.File
    $bitmap = [System.Drawing.Bitmap]::new($bounds.Width,$bounds.Height)
    try {
      $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
      try { $graphics.CopyFromScreen($bounds.Location,[System.Drawing.Point]::Empty,$bounds.Size); $bitmap.Save($path,[System.Drawing.Imaging.ImageFormat]::Png) }
      finally { $graphics.Dispose() }
    } finally { $bitmap.Dispose() }
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    $records.Add([pscustomobject]@{ file=$item.File; page=$item.Page; width=$bounds.Width; height=$bounds.Height; sha256=$hash })
    Write-Host ("Captured {0}: {1} ({2}x{3}, SHA256 {4})" -f $item.File,$item.Page,$bounds.Width,$bounds.Height,$hash)
    $index++
    if ($index -lt $pages.Count) { Write-Host "Next page: $($pages[$index].Page)" }
  }
  $manifest = [pscustomobject]@{ source='Actual Power BI Desktop screen capture'; desktopVersion=$PowerBIDesktopVersion; capturedAt=(Get-Date).ToString('o'); requestedPages=$pages.Count; capturedPages=$records }
  [IO.File]::WriteAllText((Join-Path $runDir 'capture-manifest.json'),($manifest | ConvertTo-Json -Depth 5),[System.Text.UTF8Encoding]::new($false))
  if ($index -eq $pages.Count) { Write-Host "Captured all $($pages.Count) requested pages. Inspect every PNG before copying it into either repository." }
  else { Write-Warning "Captured $index of $($pages.Count) requested pages. Partial images remain in the timestamped private folder." }
} finally {
  [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 1) | Out-Null
  [VortexCapture.Native]::UnregisterHotKey([IntPtr]::Zero, 2) | Out-Null
}
