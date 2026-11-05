# Power BI screenshot capture checklist

The published PBIP is complete at 14 pages. Six clean captures are retained; pages 04-11 require recapture. This checklist is for an authorized interactive Windows desktop session with Power BI Desktop available.

## Capture procedure

1. In the normal Windows desktop session, launch Power BI Desktop from Start and open `PowerBI/ProjectVortex-Public.pbip` from this repository.
2. Use only the public-safe PBIP and its public aggregate `data/` folder. Set the local `DataRoot` parameter to this clone if needed, refresh, and confirm the selected portfolio is P6+SIZE+CE (PSC). Do not save report/model changes.
3. Use Report view, maximize the application, close unrelated windows, hide editing panes that reduce the canvas, and wait until every visual has rendered. Do not capture a shared meeting or screen-share session.
4. Capture every report page in page order at one consistent display resolution. Use 3240 x 1824 only if the actual display supports it; otherwise use a single high-resolution 16:9 size for all pages. Do not stretch or reconstruct the images afterward.
5. Save the 14 PNGs in `images/powerbi/` using the filenames below. Keep the six existing clean images unless the same capture session deliberately replaces and rechecks all 14.
6. Inspect each image at full size for overlays, clipping, missing visuals, legibility, slicer state and sensitive content. Pixel inspection is required; the hash/dimension script only checks file identity and geometry.
7. Run `python scripts/audit_screenshot_set.py` after all 14 captures are present. Review its manifest, then regenerate the contact sheet and website gallery from this one checked set.

## Page-to-file mapping

| Page | Report page | Filename | Current status |
|---:|---|---|---|
| 01 | Knowledge & Intelligence | `01-Knowledge.png` | Clean capture retained |
| 02 | Autonomous Research Pipeline | `02-Research.png` | Clean capture retained |
| 03 | Executive Overview | `03-Executive.png` | Clean capture retained |
| 04 | Portfolio Performance | `04-Performance.png` | Recapture required |
| 05 | Risk & Drawdown | `05-Risk.png` | Recapture required |
| 06 | Trade Explorer | `06-Trade-Explorer.png` | Recapture required |
| 07 | Forward Validation & Governance | `07-Validation.png` | Recapture required |
| 08 | Winning Case W02 | `08-W02-Win.png` | Recapture required |
| 09 | Winning Case W03 | `09-W03-Win.png` | Recapture required |
| 10 | Winning Case W04 | `10-W04-Win.png` | Recapture required |
| 11 | Winning Case W05 | `11-W05-Win.png` | Recapture required |
| 12 | Winning Case W06 | `12-W06-Win.png` | Clean capture retained |
| 13 | Losing Case L01 | `13-L01-Loss.png` | Clean capture retained |
| 14 | Losing Case L02 | `14-L02-Loss.png` | Clean capture retained |

The additional winning exhibit within Trade Explorer is not a separate PBIP page. Historical case-study winners are examples, not a representative performance sample.
