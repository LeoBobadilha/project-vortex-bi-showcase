# Power BI Desktop screenshot capture

This procedure captures the actual public-safe PBIP from an authorized interactive Windows desktop. It does not recreate report visuals or alter the model.

## Prepare the report

1. Open this repository in the normal Windows user session and run `scripts/configure-data-root.ps1` from the repository root.
2. Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop and refresh the model. Confirm the 14 page tabs render and there are no source errors. Keep the clone-specific `DataRoot` configuration local; do not commit it.
3. For portfolio performance pages, select PSC with C30 and the complete supported period (2022-01-04 through 2026-10-20); do not combine P6 and PSC. Wait for each page to finish rendering, maximize the report, hide editing panes and use full-screen report view. Do not capture dialogs, taskbars, notifications or other application windows.

## Capture

Record the version under **Help > About**, then run `scripts/capture-powerbi-pages.ps1 -PowerBIDesktopVersion '<version>'` from the BI repository. By default it requests the eight missing pages, in order. Use `-AllPages` to recapture all 14 if the approved captures do not match the display resolution or framing. The helper waits for **F9** while Power BI is the foreground application; press it once per page when the prompt names the page. **Escape** stops without deleting earlier captures.

Raw captures are written to `%LOCALAPPDATA%\ProjectVortex\PowerBI_Capture\<timestamp>`. The helper captures the monitor containing the Power BI window and writes a private manifest with the Desktop version, filenames, dimensions and SHA-256 hashes. It does not determine whether a visual is complete or whether an overlay is present.

## Review and synchronize

Inspect every PNG at full size. Confirm the correct page, all visuals loaded, approved benchmark/slicer state, consistent dimensions, readable labels and no unrelated desktop content. Do not use image edits to conceal report defects. Keep unapproved captures in the local staging folder.

After visual review, copy only approved captures under their specified names to `images/powerbi/` and the matching website `public/images/powerbi/`. Then run:

```powershell
python scripts/audit_screenshot_set.py
python scripts/audit_screenshot_parity.py --website-root ..\project-vortex-portfolio
python scripts/audit_public_release.py
```

The first command requires all 14 images and writes `docs/screenshot-manifest.json`. The parity check confirms matching page sets, dimensions and SHA-256 hashes across both repositories. The final audit checks the PBIP and public release rules. Human pixel inspection remains required even when every script passes.
