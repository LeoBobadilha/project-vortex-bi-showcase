# Project Vortex | BI and Research Showcase

**Live portfolio:** [leobobadilha.github.io/project-vortex-portfolio](https://leobobadilha.github.io/project-vortex-portfolio/)
**Website source:** [project-vortex-portfolio](https://github.com/LeoBobadilha/project-vortex-portfolio)

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

## Public PBIP structure

The report has 14 pages and 83 visual definitions. Its semantic model contains nine authored tables, ten relationships and 24 measures. The separately reported 88-visual count is not reproduced by the inspected snapshot and is not used as the current count.

## Screenshots and documentation

`images/powerbi/` contains one genuine Power BI Desktop capture of each of the 14 report pages, taken in one refreshed session and pixel-reviewed. Page 04 compares P6 and PSC as separate series, and page 05 is PSC only; the report never combines them. See `docs/screenshot-qa-2026-11-06.md` for the page-by-page review and `docs/screenshot-capture-runbook.md` for the automated capture procedure. An earlier capture set was withdrawn because it contained desktop or meeting overlays; `docs/screenshot-qa-2026-11-05.md` records that audit.

## Repository relationship

The companion [Project Vortex portfolio website](https://leobobadilha.github.io/project-vortex-portfolio/) and its [source repository](https://github.com/LeoBobadilha/project-vortex-portfolio) are maintained separately and link back to this BI showcase.

## About the author

My professional background is in Business Intelligence and Data Engineering, with experience using SQL Server, Python, SSIS and Power BI. Project Vortex applies those disciplines to financial research, historical testing and AI-assisted software development.

## Risk disclosure

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations.

## Release provenance and parity

The original [BI v1.0.0 release](https://github.com/LeoBobadilha/project-vortex-bi-showcase/releases/tag/v1.0.0) and [website v1.0.0 release](https://github.com/LeoBobadilha/project-vortex-portfolio/releases/tag/v1.0.0) remain intact. Later corrections are tracked on the repositories' `main` branches; see the [website Pages workflow history](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/workflows/deploy-pages.yml) for deployments.

The available active private PBIR snapshot and public PBIP each contain 14 pages and 83 visual definitions. The separately reported 88-visual count could not be reproduced from that snapshot. See `docs/pbip-parity-report.md` for the page-level differences and validation limits.

The current public `main` contains 14 clean page captures and the complete public-safe 14-page PBIP. The original v1.0.0 history still contains the earlier contaminated screenshots, including meeting UI with participant names. No history rewrite or tag deletion has been performed. See `SECURITY_REVIEW.md` for current-tree controls and historical limits.
