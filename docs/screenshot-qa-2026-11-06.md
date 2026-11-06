# Power BI Screenshot QA - 2026-11-06

All 14 report pages were recaptured in one session from Power BI Desktop 2.159.1231.0, using `scripts/capture-powerbi-pages.ps1`. Every image is 3208 x 1804 and is a native-pixel crop with no resampling. Two consecutive runs produced byte-identical files for all 14 pages. The set replaces the six images retained on 2026-11-05 and the eight pages withheld that day.

## Model state

The model was refreshed before capture. All partitions reported Ready with no error, and the local engine returned the frozen PSC benchmark: R$23,551 gross, R$20,395 net C30, 324 records, 57.716% win rate, profit factor 1.950816, and R$1,932, R$2,077 and R$2,113 drawdowns.

## Page review

Each image was inspected for the correct page, complete content, refresh errors, overlays and unrelated content. None was found on any page.

| Page | Report page | File | Notes |
|---:|---|---|---|
| 01 | Knowledge & Intelligence | `01-Knowledge.png` |  |
| 02 | Autonomous Research Pipeline | `02-Research.png` | Series split by portfolio |
| 03 | Executive Overview | `03-Executive.png` | Cards match the benchmark |
| 04 | Portfolio Performance | `04-Performance.png` | PSC selected; annual bars match the PSC rows |
| 05 | Risk & Drawdown | `05-Risk.png` | PSC selected; proxy trough is -R$1,648 |
| 06 | Trade Explorer | `06-Trade-Explorer.png` | W01 exhibit |
| 07 | Forward Validation & Governance | `07-Validation.png` |  |
| 08 | W02 Winning Case Study | `08-W02-Win.png` | Matches `W02_Embedded.png` |
| 09 | W03 Winning Case Study | `09-W03-Win.png` | Matches `W03_Embedded.png` |
| 10 | W04 Winning Case Study | `10-W04-Win.png` | Matches `W04_Embedded.png` |
| 11 | W05 Winning Case Study | `11-W05-Win.png` | Matches `W05_Embedded.png` |
| 12 | W06 Winning Case Study | `12-W06-Win.png` | Matches `W06_Embedded.png` |
| 13 | L01 Losing Case Study | `13-L01-Loss.png` | Matches `L01_Embedded.png` |
| 14 | L02 Losing Case Study | `14-L02-Loss.png` | Matches `L02_Embedded.png` |

Each case page was also compared with the embedded image its `visual.json` references. All seven scored at least 0.990 against their own image and no more than 0.163 against any other.

## Slicer state

`Net C30` sums both portfolios when the portfolio slicer is unset, so pages 04 and 05 were captured with `P6 + SIZE + CE` selected. As a result, the "portfolio comparison" chart on page 04 shows PSC only. The Year slicers are unset, which shows the full period. Page 02 splits by portfolio and page 03 uses PSC-specific measures, so neither needed a selection.

## Report characteristics left unchanged

These appear in the captures because they are part of the report. The report was not modified.

- Slicer items on pages 03, 04 and 05 are clipped by their visuals, so the slicers show only their field name and the selection is not visible.
- On the case pages, the disclaimer overlaps the bottom of the exhibit and hides its last line, "Selected historical case; not representative of the complete trade distribution." The line is visible on page 06.
- The two charts in the upper half of page 05 use the same measure and look identical, as do the two cards on page 06.
- The pale panels inside the exhibits are part of the embedded images, where they mask the price axes.
- The 1280 x 780 case pages are narrower than the 16:9 frame, so the white Desktop canvas margin shows at each side.
- The `contact-sheet.png` withdrawn on 2026-11-05 was not regenerated.
