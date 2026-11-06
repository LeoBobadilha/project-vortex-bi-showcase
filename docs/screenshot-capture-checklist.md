# Power BI screenshot capture checklist

The published PBIP is complete at 14 pages, and all 14 have current captures. Use this checklist for any future recapture, in an interactive Windows desktop session with Power BI Desktop available. `screenshot-capture-runbook.md` automates steps 3 to 5.

## Capture procedure

1. In the normal Windows desktop session, launch Power BI Desktop from Start and open `PowerBI/ProjectVortex-Public.pbip` from this repository.
2. Use only the public-safe PBIP and its public aggregate `data/` folder. Set the local `DataRoot` parameter to this clone if needed, refresh, and leave every slicer at All. Do not save report/model changes.
3. Use Report view, maximize the application, close unrelated windows, hide editing panes that reduce the canvas, and wait until every visual has rendered. Do not capture a shared meeting or screen-share session.
4. Capture every report page in page order at one consistent display resolution. The current set is 3208 x 1804 from a 3840 x 2160 display; the size follows the actual display, so use a single high-resolution 16:9 size for all pages. Do not stretch or reconstruct the images afterward.
5. Save the 14 PNGs in `images/powerbi/` using the filenames below. Replace all 14 together so the set comes from one session.
6. Inspect each image at full size for overlays, clipping, missing visuals, legibility, slicer state and sensitive content. Pixel inspection is required; the hash/dimension script only checks file identity and geometry.
7. Run `python scripts/audit_screenshot_set.py` after all 14 captures are present. Review its manifest, then update the website gallery from this one checked set.

## Page-to-file mapping

| Page | Report page | Filename | Current status |
|---:|---|---|---|
| 01 | Knowledge & Intelligence | `01-Knowledge.png` | Captured 2026-11-06 |
| 02 | Autonomous Research Pipeline | `02-Research.png` | Captured 2026-11-06 |
| 03 | Executive Overview | `03-Executive.png` | Captured 2026-11-06 |
| 04 | Portfolio Performance | `04-Performance.png` | Captured 2026-11-06 |
| 05 | Risk & Drawdown | `05-Risk.png` | Captured 2026-11-06 |
| 06 | Trade Explorer | `06-Trade-Explorer.png` | Captured 2026-11-06 |
| 07 | Forward Validation & Governance | `07-Validation.png` | Captured 2026-11-06 |
| 08 | Winning Case W02 | `08-W02-Win.png` | Captured 2026-11-06 |
| 09 | Winning Case W03 | `09-W03-Win.png` | Captured 2026-11-06 |
| 10 | Winning Case W04 | `10-W04-Win.png` | Captured 2026-11-06 |
| 11 | Winning Case W05 | `11-W05-Win.png` | Captured 2026-11-06 |
| 12 | Winning Case W06 | `12-W06-Win.png` | Captured 2026-11-06 |
| 13 | Losing Case L01 | `13-L01-Loss.png` | Captured 2026-11-06 |
| 14 | Losing Case L02 | `14-L02-Loss.png` | Captured 2026-11-06 |

The additional winning exhibit within Trade Explorer is not a separate PBIP page. Historical case-study winners are examples, not a representative performance sample.
