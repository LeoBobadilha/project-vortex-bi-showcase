<#
.SYNOPSIS
  Captures all 14 report pages from an already-open Power BI Desktop window.

.DESCRIPTION
  Drives Power BI Desktop through Windows UI Automation in the normal interactive
  user session. Pages are selected by their real tab titles. Pixels are read with
  PrintWindow, so only the Power BI window is captured: other windows, meeting
  overlays and notifications cannot appear in the image.

  A page is rejected unless its tab is selected, the status bar reads
  "Page N of 14", the benchmark cards match, no error text is present, no tooltip
  overlaps the frame, and consecutive frames are pixel-identical. Slicers are left
  in the freshly opened state, so the images show what a new reader sees.

  Pane and ribbon changes are session state and are never saved by this script. Do
  not save the report afterwards. Inspect every image; automation does not replace
  human pixel review.

.PARAMETER OutputDir
  Staging folder. Defaults to %LOCALAPPDATA%\ProjectVortex\PowerBI_Capture\<timestamp>.

.PARAMETER Publish
  After all 14 pages pass, copy the images to images/powerbi and to the sibling
  website repository's public/images/powerbi.
#>
param(
  [string]$OutputDir = '',
  [switch]$Publish
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
if (-not ('VortexCapture.Native' -as [type])) { Add-Type -ReferencedAssemblies System.Drawing @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
namespace VortexCapture {
  public static class Native {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
    [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr value);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hWnd, IntPtr hdc, uint flags);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int command);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT point);
    public static void Capture(IntPtr hWnd, string path) {
      RECT r; GetWindowRect(hWnd, out r);
      using (var bitmap = new Bitmap(r.Right - r.Left, r.Bottom - r.Top, PixelFormat.Format32bppArgb))
      using (var graphics = Graphics.FromImage(bitmap)) {
        IntPtr dc = graphics.GetHdc();
        PrintWindow(hWnd, dc, 2); // PW_RENDERFULLCONTENT includes the GPU-composited report canvas
        graphics.ReleaseHdc(dc);
        bitmap.Save(path, ImageFormat.Png);
      }
    }
  }
}
'@ }
[void][VortexCapture.Native]::SetProcessDpiAwarenessContext([IntPtr](-4)) # per-monitor v2: native pixels

$Element = [System.Windows.Automation.AutomationElement]
$TreeScope = [System.Windows.Automation.TreeScope]
$Type = [System.Windows.Automation.ControlType]
$dot = [string][char]0xB7
$pages = @(
  @{ File='01-Knowledge.png';      Title='Knowledge & Intelligence' },
  @{ File='02-Research.png';       Title='Autonomous Research Pipeline' },
  @{ File='03-Executive.png';      Title='Executive Overview'; Expect=@('R$ 20,395.00','R$ 23,551.00','324','57.7%','1.951','R$ 1,932.00') },
  @{ File='04-Performance.png';    Title='Portfolio Performance'; Expect=@('P6 + SIZE + CE','P6 Baseline') },
  @{ File='05-Risk.png';           Title='Risk & Drawdown'; Expect=@('R$ 1,932.00','R$ 2,077.00','R$ 2,113.00') },
  @{ File='06-Trade-Explorer.png'; Title='Trade Explorer' },
  @{ File='07-Validation.png';     Title='Forward Validation & Governance' },
  @{ File='08-W02-Win.png';        Title="W02 $dot Winning Case Study" },
  @{ File='09-W03-Win.png';        Title="W03 $dot Winning Case Study" },
  @{ File='10-W04-Win.png';        Title="W04 $dot Winning Case Study" },
  @{ File='11-W05-Win.png';        Title="W05 $dot Winning Case Study" },
  @{ File='12-W06-Win.png';        Title="W06 $dot Winning Case Study" },
  @{ File='13-L01-Loss.png';       Title="L01 $dot Losing Case Study" },
  @{ File='14-L02-Loss.png';       Title="L02 $dot Losing Case Study" }
)

function New-Condition($property, $value) { New-Object System.Windows.Automation.PropertyCondition($property, $value) }
function Find-Control($scope, [string]$name, $controlType) {
  $condition = New-Object System.Windows.Automation.AndCondition((New-Condition $Element::NameProperty $name), (New-Condition $Element::ControlTypeProperty $controlType))
  $scope.FindFirst($TreeScope::Descendants, $condition)
}
function Find-All($scope, $controlType) { $scope.FindAll($TreeScope::Descendants, (New-Condition $Element::ControlTypeProperty $controlType)) }
function Get-Pattern($target, $pattern) {
  $value = $null
  if (-not $target.TryGetCurrentPattern($pattern, [ref]$value)) { throw "Control '$($target.Current.Name)' does not support $($pattern.ProgrammaticName)" }
  $value
}
function Assert-Foreground($hWnd) {
  if ([VortexCapture.Native]::GetForegroundWindow() -ne $hWnd) {
    [void][VortexCapture.Native]::SetForegroundWindow($hWnd)
    Start-Sleep -Milliseconds 600
  }
  if ([VortexCapture.Native]::GetForegroundWindow() -ne $hWnd) { throw 'Power BI Desktop is not the foreground window.' }
}

$biRepo = Split-Path -Parent $PSScriptRoot
$websiteRepo = Join-Path (Split-Path -Parent $biRepo) 'project-vortex-portfolio'
if ([string]::IsNullOrWhiteSpace($OutputDir)) { $OutputDir = Join-Path $env:LOCALAPPDATA ('ProjectVortex\PowerBI_Capture\' + (Get-Date -Format 'yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$process = Get-Process PBIDesktop -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -match 'ProjectVortex-Public' } | Select-Object -First 1
if (-not $process) { throw 'Open PowerBI/ProjectVortex-Public.pbip in Power BI Desktop, refresh it, then rerun.' }
$current = [System.Diagnostics.Process]::GetCurrentProcess()
if ($process.SessionId -ne $current.SessionId) { throw "Power BI runs in session $($process.SessionId); this script runs in session $($current.SessionId). Run it from the interactive desktop session." }
$desktopVersion = (Get-Item $process.Path).VersionInfo.FileVersion
$hWnd = $process.MainWindowHandle

[void][VortexCapture.Native]::ShowWindow($hWnd, 9)
Start-Sleep -Milliseconds 800
[void][VortexCapture.Native]::ShowWindow($hWnd, 3)
Start-Sleep -Seconds 2
Assert-Foreground $hWnd

$root = $Element::FromHandle($hWnd)
$reportTab = Find-Control $root 'Report view' $Type::TabItem
if (-not $reportTab) { throw 'Report view tab not found.' }
(Get-Pattern $reportTab ([System.Windows.Automation.SelectionItemPattern]::Pattern)).Select()
Start-Sleep -Seconds 5
$report = $root.FindFirst($TreeScope::Descendants, (New-Condition $Element::NameProperty 'ms-pbi.pbi.microsoft.com/minerva/reportView.html'))
if (-not $report) { throw 'Report view surface not found.' }

$parking = $null
foreach ($button in (Find-All $report $Type::Button)) {
  $control = $button.Current
  if ($control.IsOffscreen -or $control.BoundingRectangle.IsEmpty) { continue }
  $isPaneToggle = $control.Name -like 'Collapse or expand the filter pane*' -or ($control.ClassName -like 'toggle-button*' -and $control.Name -in @('Visualizations','Data'))
  if (-not $isPaneToggle) { continue }
  $toggle = Get-Pattern $button ([System.Windows.Automation.ExpandCollapsePattern]::Pattern)
  if ($toggle.Current.ExpandCollapseState -ne 'Collapsed') { $toggle.Collapse(); Start-Sleep -Milliseconds 1200 }
  if ($control.Name -eq 'Data') { $parking = $button }
}
if (-not $parking) { throw 'Could not find the Data pane toggle used to hold keyboard focus outside the canvas.' }

$canvas = Find-Control $report 'Power BI Report' $Type::Group
if (-not $canvas) { throw 'Report canvas not found.' }
if ($canvas.Current.BoundingRectangle.Y -gt 200) {
  $switch = Find-Control $report 'Switch ribbons' $Type::Button
  if ($switch) { (Get-Pattern $switch ([System.Windows.Automation.InvokePattern]::Pattern)).Invoke(); Start-Sleep -Seconds 3 }
}

# A pointer resting on the ribbon or a visual would raise a tooltip over the canvas, so
# park it on blank workspace beside the page for the run.
$canvas = Find-Control $report 'Power BI Report' $Type::Group
$bounds = $canvas.Current.BoundingRectangle
$pointer = New-Object VortexCapture.Native+POINT
[void][VortexCapture.Native]::GetCursorPos([ref]$pointer)
[void][VortexCapture.Native]::SetCursorPos([int]($bounds.X - 90), [int]($bounds.Y + $bounds.Height / 2))
Start-Sleep -Seconds 2

$sha = [System.Security.Cryptography.SHA256]::Create()
$records = [System.Collections.Generic.List[object]]::new()
$frameWidth = 0; $frameHeight = 0; $frameTop = 0

for ($index = 0; $index -lt $pages.Count; $index++) {
  $page = $pages[$index]
  $number = $index + 1
  $tab = Find-Control $report $page.Title $Type::TabItem
  if (-not $tab) { throw "Page tab not found: $($page.Title)" }
  $selection = Get-Pattern $tab ([System.Windows.Automation.SelectionItemPattern]::Pattern)
  $selection.Select()
  Start-Sleep -Seconds 4

  # UI Automation selection leaves focus on the tab, whose tooltip would cover the canvas.
  $parking.SetFocus()
  Start-Sleep -Seconds 3

  $raw = Join-Path $OutputDir ('raw-' + $page.File)
  $previous = ''; $stable = 0; $timer = [Diagnostics.Stopwatch]::StartNew()
  while ($stable -lt 2 -and $timer.Elapsed.TotalSeconds -lt 45) {
    [VortexCapture.Native]::Capture($hWnd, $raw)
    $hash = [BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($raw)))
    if ($hash -eq $previous) { $stable++ } else { $stable = 0 }
    $previous = $hash
    if ($stable -lt 2) { Start-Sleep -Milliseconds 1500 }
  }
  if ($stable -lt 2) { throw "Page $number did not finish rendering." }
  if (-not $selection.Current.IsSelected) { throw "Page $number tab is not selected." }
  if (-not (Find-Control $report "Page $number of 14" $Type::Text)) { throw "Status bar does not read 'Page $number of 14'." }

  $canvas = Find-Control $report 'Power BI Report' $Type::Group
  $bounds = $canvas.Current.BoundingRectangle
  $texts = @(Find-All $canvas $Type::Text | ForEach-Object { $_.Current.Name })
  $names = @($canvas.FindAll($TreeScope::Descendants, [System.Windows.Automation.Condition]::TrueCondition) | ForEach-Object { $_.Current.Name })
  $errors = @($texts | Where-Object { $_ -match "(?i)can.t display|couldn.t|see details|something went wrong|fix this|query error|failed|absolute path" })
  if ($errors.Count) { throw "Page $number reports an error: $($errors -join ' | ')" }
  foreach ($value in @($page.Expect | Where-Object { $_ })) {
    if (-not ($names | Where-Object { $_ -like "*$value*" })) { throw "Page $number is missing expected value '$value'. Refresh the model and rerun." }
  }

  # All 14 pages are 1280x720. Each sits at the bottom of the canvas host.
  if ($frameWidth -eq 0) {
    $frameWidth = [int]$bounds.Width
    $frameHeight = [int][math]::Round($frameWidth * 9 / 16)
    $frameTop = [int]($bounds.Y + $bounds.Height) - $frameHeight
  }
  $frameLeft = [int]($bounds.X + $bounds.Width / 2) - [int]($frameWidth / 2)
  foreach ($tip in (Find-All $report $Type::ToolTip)) {
    $t = $tip.Current.BoundingRectangle
    if (-not $t.IsEmpty -and $t.X -lt ($frameLeft + $frameWidth) -and ($t.X + $t.Width) -gt $frameLeft -and $t.Y -lt ($frameTop + $frameHeight) -and ($t.Y + $t.Height) -gt $frameTop) {
      throw "Tooltip overlaps the frame on page ${number}: $($tip.Current.Name)"
    }
  }

  $window = New-Object VortexCapture.Native+RECT
  [void][VortexCapture.Native]::GetWindowRect($hWnd, [ref]$window)
  $source = [System.Drawing.Bitmap]::FromFile($raw)
  $crop = New-Object System.Drawing.Bitmap($frameWidth, $frameHeight, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $graphics = [System.Drawing.Graphics]::FromImage($crop)
  $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor # 1:1 copy, no resampling
  $graphics.DrawImage($source, (New-Object System.Drawing.Rectangle(0, 0, $frameWidth, $frameHeight)), (New-Object System.Drawing.Rectangle(($frameLeft - $window.Left), ($frameTop - $window.Top), $frameWidth, $frameHeight)), [System.Drawing.GraphicsUnit]::Pixel)
  $graphics.Dispose(); $source.Dispose()
  $target = Join-Path $OutputDir $page.File
  $crop.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
  $crop.Dispose()
  Remove-Item -LiteralPath $raw

  $digest = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
  $records.Add([pscustomobject]@{ page=$number; title=$page.Title; file=$page.File; width=$frameWidth; height=$frameHeight; sha256=$digest })
  Write-Host ('{0:00} {1} -> {2} ({3}x{4})' -f $number, $page.Title, $page.File, $frameWidth, $frameHeight)
}

[void][VortexCapture.Native]::SetCursorPos($pointer.X, $pointer.Y)

$manifest = [pscustomobject]@{ source='Power BI Desktop window capture (PrintWindow) driven by Windows UI Automation'; desktopVersion=$desktopVersion; capturedAt=(Get-Date).ToString('o'); pages=$records }
[IO.File]::WriteAllText((Join-Path $OutputDir 'capture-manifest.json'), ($manifest | ConvertTo-Json -Depth 5), [System.Text.UTF8Encoding]::new($false))
Write-Host "Captured 14 pages to $OutputDir"

if ($Publish) {
  $biImages = Join-Path $biRepo 'images\powerbi'
  $siteImages = Join-Path $websiteRepo 'public\images\powerbi'
  foreach ($folder in @($biImages, $siteImages)) { if (-not (Test-Path -LiteralPath $folder)) { throw "Image folder is missing: $folder" } }
  foreach ($page in $pages) {
    Copy-Item -LiteralPath (Join-Path $OutputDir $page.File) -Destination $biImages -Force
    Copy-Item -LiteralPath (Join-Path $OutputDir $page.File) -Destination $siteImages -Force
  }
  Write-Host 'Copied all 14 images to both repositories. Inspect each one before committing.'
}
