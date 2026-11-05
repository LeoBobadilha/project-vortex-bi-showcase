# Project Vortex | BI and Research Showcase

I established the research direction for Project Vortex, drawing on prior Price Action study and a Business Intelligence and Data Engineering background. AI agents supported research, implementation, backtesting, analysis and documentation; strategic decisions and validation remained subject to human review. This public-safe PBIP presents aggregate performance and research evidence in an editable 14-page report, separate from the private research system.

## Verified historical benchmark

The selected benchmark is **P6+SIZE+CE (PSC)** from 2022-01-04 through 2026-10-20: 324 portfolio records, 526 contract units, R$23,551 gross P&L, R$3,156 C30 costs applied once, and R$20,395 net C30 P&L. Historical win rate is 57.716%; PF is 1.950816. Maximum drawdown figures are R$1,932 realized close-order, R$2,077 M5 close, and R$2,113 adverse M5 OHLC-envelope. These are backtest results, not Paper Live or live-account performance. The P6 baseline is presented separately. No percentage return is calculated because initial capital is not specified.

## Report pages

1. Knowledge & Intelligence
2. Autonomous Research Pipeline
3. Executive Overview
4. Portfolio Performance
5. Risk & Drawdown
6. Trade Explorer
7. Forward Validation & Governance
8-12. Five anonymized winning case studies
13-14. Two anonymized losing case studies

One additional winning example appears in Trade Explorer.

The first seven pages combine approved aggregate data with a concise account of the knowledge and validation workflow. Trade exhibits are redacted visual case studies; dates, exact prices, position sizes, individual P&L and operational identifiers are not included. They are illustrative and are not a statistical performance sample.

## Open the PBIP

Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop. From a fresh clone on Windows, run:

```powershell
.\scripts\configure-data-root.ps1
```

Then open the PBIP and refresh the model. It reads only the CSV aggregates under `data/`. No broker, account or live-market connection is configured. If moving the folder, rerun the setup script. Do not commit the locally configured `DataRoot` value.

## Data and metric definitions

- `data/benchmark_summary.csv`: reconciled portfolio-level benchmark metrics.
- `data/monthly_portfolio_results.csv`: approved monthly aggregates.
- `data/annual_portfolio_results.csv`: approved annual aggregates.
- `data/monthly_drawdown_proxy.csv`: month-end aggregate drawdown proxy only.
- Close-order, M5-close and adverse OHLC-envelope drawdowns are separate definitions. The monthly line does not reconstruct trade-order or intrabar equity paths.
- Portfolio comparisons do not add P6 and PSC together. Cost scenario C30 is applied once in the benchmark net result.
- No trade-level ledger or private market archive is included.

## Screenshots and documentation

`images/powerbi/` currently retains six visually checked, unobstructed page captures (01–03 and 12–14). Eight captures (04–11) and the contact sheet have been withdrawn from this local hotfix because they show Zoom windows or meeting controls. No clean replacements are available until Power BI Desktop can be used to recapture the public PBIP. The report still has 14 pages; this image limitation does not change the PBIP. See `docs/screenshot-qa-2026-11-05.md` for the inspection record.

## Repository relationship

The companion [Project Vortex portfolio source](https://github.com/LeoBobadilha/project-vortex-portfolio) is maintained separately and links to this BI showcase.

## About the author

My professional background is in Business Intelligence and Data Engineering, with experience using SQL Server, Python, SSIS and Power BI. Project Vortex applies those disciplines to financial research, historical testing and AI-assisted software development.

## Risk disclosure

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations.

## Release provenance and parity

Public BI release: https://github.com/LeoBobadilha/project-vortex-bi-showcase/releases/tag/v1.0.0
Base commit: a1593c1e6f0fb86ec8c5cc18bc08f50b92cdf38d.
Companion website release: https://github.com/LeoBobadilha/project-vortex-portfolio/releases/tag/v1.0.0
Base commit: 0fc9239bfd860c63cb60fa0d2186f09492c48545.

The available active private PBIR snapshot and public PBIP each contain 14 pages and 83 visual definitions. The separately reported 88-visual count could not be reproduced from that snapshot. See `docs/pbip-parity-report.md` for the page-level differences and validation limits.

The public remote remains at v1.0.0. This local hotfix branch includes the reviewed documentation follow-up and the screenshot withdrawal; it has not been pushed or released. The original `feature/personal-author-voice` branch is preserved.
