# Power BI Screenshot QA - 2026-11-06

All 14 report pages were captured in one session from Power BI Desktop 2.159.1231.0, using `scripts/capture-powerbi-pages.ps1`. The report was opened from a fresh clone configured with `scripts/configure-data-root.ps1`. Every image is 3208 x 1804 and is a native-pixel crop with no resampling. This set replaces the set published earlier the same day, which predated the report corrections.

## Model state

After refresh, all partitions reported Ready with no error. The live model was then compared with the source CSVs: 877 checks across benchmark, annual and monthly values passed with no failures.

| Measure context | Result |
|---|---|
| PSC measures, unfiltered | R$23,551 gross, R$20,395 net C30, 324 records, 57.716% win rate, profit factor 1.950816, R$1,932 realized drawdown |
| PSC measures, with P6 selected | The same values |
| P6 Baseline selected | R$15,963 gross, R$13,641 net C30, 267 records |
| `Net C30` with no portfolio in context | BLANK, previously R$34,036 |
| `Operations` with no portfolio in context | BLANK, previously 591 |
| Any month or year with no portfolio in context | BLANK for all 58 months and 5 years |

## Slicer states on page 04

| State | Slicer shows | Charts | Table |
|---|---|---|---|
| Default | All | P6 and PSC as separate series | Both portfolios |
| PSC selected | P6 + SIZE + CE | PSC only | PSC only |
| P6 selected | P6 Baseline | P6 only | P6 only |
| Cleared | All | P6 and PSC as separate series | Both portfolios |

## Page review

Each image was inspected for the correct page, complete content, refresh errors, overlays and unrelated content. None was found on any page.

| Page | Report page | File | Notes |
|---:|---|---|---|
| 01 | Knowledge & Intelligence | `01-Knowledge.png` |  |
| 02 | Autonomous Research Pipeline | `02-Research.png` | P6 and PSC as separate series |
| 03 | Executive Overview | `03-Executive.png` | PSC only; cards match the benchmark |
| 04 | Portfolio Performance | `04-Performance.png` | Slicers at All; P6 and PSC as separate series |
| 05 | Risk & Drawdown | `05-Risk.png` | PSC only; proxy trough is -R$1,648 |
| 06 | Trade Explorer | `06-Trade-Explorer.png` | Six winning and two losing examples; W01 exhibit |
| 07 | Forward Validation & Governance | `07-Validation.png` |  |
| 08 | W02 Winning Case Study | `08-W02-Win.png` | Matches `W02_Embedded.png` |
| 09 | W03 Winning Case Study | `09-W03-Win.png` | Matches `W03_Embedded.png` |
| 10 | W04 Winning Case Study | `10-W04-Win.png` | Matches `W04_Embedded.png` |
| 11 | W05 Winning Case Study | `11-W05-Win.png` | Matches `W05_Embedded.png` |
| 12 | W06 Winning Case Study | `12-W06-Win.png` | Matches `W06_Embedded.png` |
| 13 | L01 Losing Case Study | `13-L01-Loss.png` | Matches `L01_Embedded.png` |
| 14 | L02 Losing Case Study | `14-L02-Loss.png` | Matches `L02_Embedded.png` |

Each case page was also compared with the embedded image its `visual.json` references. All seven scored at least 0.991 against their own image and no more than 0.163 against any other.

## Known limits

- The Year slicers show All in the images. Page 03 states which values follow the Year selector and which always show the full period.
- The monthly chart on page 04 is dense, because it shows 58 months for two portfolios.
- The pale panels inside the exhibits are part of the embedded images, where they mask the price axes.
- Power BI Desktop keeps a "Some of the tables have incomplete or no data" notice in its hidden background views after refresh. It is not shown in Report view, and all partitions report Ready.
- The `contact-sheet.png` withdrawn on 2026-11-05 was not regenerated.
