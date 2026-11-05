# Power BI Screenshot QA - 2026-11-05

I inspected the pixels in all 14 page captures and the 14-panel contact sheet. The PBIP still contains 14 report pages; this audit concerns only screenshot assets. All page captures are 3240 x 1824 pixels. The contact sheet was 3200 x 1920 pixels and used the same image as the website's `report-gallery.png`.

| File | Dimensions | PBIP page | Zoom / other overlay visible | Report content obstructed | Sensitive or unrelated information exposed | Replacement status |
|---|---|---|---|---|---|---|
| `01-Knowledge.png` | 3240 x 1824 | 01 - Knowledge & Intelligence | No | No | No | Retained; no replacement needed |
| `02-Research.png` | 3240 x 1824 | 02 - Autonomous Research Pipeline | No | No | No | Retained; no replacement needed |
| `03-Executive.png` | 3240 x 1824 | 03 - Executive Overview | No | No | No | Retained; no replacement needed |
| `04-Performance.png` | 3240 x 1824 | 04 - Portfolio Performance | Yes - Zoom meeting window and controls | Yes - right-side visuals and content | Yes - participant name and meeting UI | Withheld; clean replacement unavailable |
| `05-Risk.png` | 3240 x 1824 | 05 - Risk & Drawdown | Yes - Zoom controls/window | Yes - right-side metrics and chart | Yes - screen-shared browser/market window | Withheld; clean replacement unavailable |
| `06-Trade-Explorer.png` | 3240 x 1824 | 06 - Trade Explorer | Yes - Zoom controls/window | Yes - case exhibit and chart | Yes - screen-shared browser/market window | Withheld; clean replacement unavailable |
| `07-Validation.png` | 3240 x 1824 | 07 - Forward Validation & Governance | Yes - Zoom window and controls | Yes - status text and right-side cards | Yes - participant name, reactions and market window | Withheld; clean replacement unavailable |
| `08-W02-Win.png` | 3240 x 1824 | 08 - Winning case study W02 | Yes - Zoom meeting window | Yes - execution chart and annotations | Yes - meeting controls and shared market window | Withheld; clean replacement unavailable |
| `09-W03-Win.png` | 3240 x 1824 | 09 - Winning case study W03 | Yes - Zoom window and reactions | Yes - most of the report chart | Yes - shared trading terminal, market values and meeting UI | Withheld; clean replacement unavailable |
| `10-W04-Win.png` | 3240 x 1824 | 10 - Winning case study W04 | Yes - Zoom window and controls | Yes - a large portion of the case chart | Yes - participant name and multi-market screen share | Withheld; clean replacement unavailable |
| `11-W05-Win.png` | 3240 x 1824 | 11 - Winning case study W05 | Yes - Zoom Workplace / Webinar preview | No clear chart obstruction | Yes - Zoom preview and unrelated desktop UI | Withheld; clean replacement unavailable |
| `12-W06-Win.png` | 3240 x 1824 | 12 - Winning case study W06 | No | No | No | Retained; no replacement needed |
| `13-L01-Loss.png` | 3240 x 1824 | 13 - Losing case study L01 | No | No | No | Retained; no replacement needed |
| `14-L02-Loss.png` | 3240 x 1824 | 14 - Losing case study L02 | No | No | No | Retained; no replacement needed |
Pages 04-10 expose meeting UI and unrelated shared-screen market information; pages 04, 07 and 10 visibly include a participant name. Page 11 includes Zoom window previews. These are presentation/privacy defects even where no personal trading account data is visible. The existing captures are not suitable for public presentation.

## Actions and limits

- Withheld pages 04-11 and `contact-sheet.png` from this local hotfix tree. The website's matching `report-gallery.png` was also removed from its source tree. Original files were copied to the workspace's local `out/qa-evidence/zoom-gallery-2026-11-05/` folder and SHA-256 checked before removal.
- Kept the six pixel-inspected, unobstructed screenshots. No chart pixels were altered and no replacement art was generated.
- Power BI Desktop was not available as a command or running process in this session. Eight genuine replacements and a regenerated 14-page contact sheet therefore remain outstanding.
- The already published v1.0.0 Git history was not rewritten. Until a future authenticated update removes the affected files from the current remote branch, the original public commits still contain them.

The full SHA-256 inventory for the original files is retained in the local QA evidence folder. The public PBIP and all 14 page definitions remain unchanged.
