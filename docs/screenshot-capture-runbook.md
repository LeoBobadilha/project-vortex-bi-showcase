# Power BI Desktop screenshot capture

This procedure captures the actual public-safe PBIP from an authorized interactive Windows desktop. It does not recreate report visuals or alter the model.

## Prepare the report

1. Open this repository in the normal Windows user session and run `scripts/configure-data-root.ps1` from the repository root.
2. Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop and refresh the model. Confirm the 14 page tabs render and there are no source errors. Keep the clone-specific `DataRoot` configuration local; do not commit it.
3. For portfolio performance pages, select PSC with C30 and the complete supported period (2022-01-04 through 2026-10-20); do not combine P6 and PSC. Wait for each page to finish rendering, maximize the report, hide editing panes and use full-screen report view. Do not capture dialogs, taskbars, notifications or other application windows.

## Capture

Record the version under **Help > About**, then run this helper in that same interactive Windows session:

```powershell
& 'C:\Projects\Vortex-Edge02-Implementador\release-staging\project-vortex-bi-showcase\scripts\capture-powerbi-pages.ps1'
```

The helper prompts for the Desktop version and captures the eight missing pages in order. Select the named tab and wait for it to render, then press **F9** once. It captures only when the foreground window is Power BI. **Escape** stops safely; rerunning resumes, skipping identical files already present in both repositories. The approved images are 3240 x 1824, and the helper enforces the same dimensions.

Each PNG is saved automatically under its final filename to both `images/powerbi/` in this BI repository and `public/images/powerbi/` in the sibling website repository. It also keeps the original capture and a private manifest in `%LOCALAPPDATA%\ProjectVortex\PowerBI_Capture\<timestamp>`. It does not determine whether the report page is correct, fully rendered, or free of overlays; visually inspect each capture before release.

## Review and synchronize

Inspect every PNG at full size. Confirm the correct page, all visuals loaded, approved benchmark/slicer state, consistent dimensions, readable labels and no unrelated desktop content. Do not use image edits to conceal report defects. Keep unapproved captures in the local staging folder.

After visual review, run these checks from the BI repository root:

```powershell
python scripts/audit_screenshot_set.py
python scripts/audit_screenshot_parity.py --website-root ..\project-vortex-portfolio
python scripts/audit_public_release.py
```

The first command requires all 14 images and writes `docs/screenshot-manifest.json`. The parity check confirms matching page sets, dimensions and SHA-256 hashes across both repositories. The final audit checks the PBIP and public release rules. Human pixel inspection remains required even when every script passes.
