# Power BI Desktop screenshot capture

This procedure captures the actual public-safe PBIP from an authorized interactive Windows desktop. It does not recreate report visuals or alter the model.

## Prepare the report

1. Open this repository in the normal Windows user session and run `scripts/configure-data-root.ps1` from the repository root.
2. Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop and refresh the model. Confirm the 14 page tabs render and there are no source errors. Keep the clone-specific `DataRoot` configuration local; do not commit it.
3. Leave the report open. Close any meeting or screen-share session first if you are also reviewing the report by eye.

Do not save the report during or after capture. Pane, ribbon and slicer changes are session state only, and saving would write them into the PBIP.

## Capture

From the repository root, in the same interactive Windows session:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\capture-powerbi-pages.ps1 -Publish
```

The helper needs no keyboard input. It maximizes Power BI, opens Report view, collapses the side panes, switches to the simplified ribbon, and then visits all 14 pages by their tab titles. Keep the mouse and keyboard free during the run, which takes about three minutes.

It reads pixels with `PrintWindow`, so only the Power BI window is captured. Other windows, meeting overlays and notifications cannot appear in the images. Each image is a native-pixel 16:9 crop of the report canvas with no resampling, and its size follows the display.

A page is rejected, and the run stops, unless:

- its tab is selected and the status bar reads `Page N of 14`
- two consecutive frames are pixel-identical
- no visual reports an error, and no tooltip overlaps the frame
- the benchmark cards on pages 03 and 05 show the frozen values, and page 04 shows both portfolios

Slicers stay in their freshly opened state, so the images show what a new reader sees. The pointer is parked on blank workspace during the run and returned afterwards.

Images go to a staging folder under `%LOCALAPPDATA%\ProjectVortex\PowerBI_Capture\<timestamp>`, or to `-OutputDir` if given. With `-Publish`, they are copied to `images/powerbi/` here and `public/images/powerbi/` in the sibling website repository, but only after all 14 pass. Omit `-Publish` to review them first.

## Review and synchronize

Inspect every PNG at full size. Confirm the correct page, all visuals loaded, approved benchmark/slicer state, consistent dimensions, readable labels and no unrelated desktop content. Do not use image edits to conceal report defects.

After visual review, run these checks from the BI repository root:

```powershell
python scripts/audit_screenshot_set.py
python scripts/audit_screenshot_parity.py --website-root ..\project-vortex-portfolio
python scripts/audit_report_semantics.py
python scripts/audit_public_release.py
```

If you configured `DataRoot` in this repository, run `scripts/configure-data-root.ps1 -Reset` before committing. Capturing from a separate clone avoids that step. The first command requires all 14 images and writes `docs/screenshot-manifest.json`. The parity check confirms matching page sets, dimensions and SHA-256 hashes across both repositories. The final audit checks the PBIP and public release rules. Human pixel inspection remains required even when every script passes.
