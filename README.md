# Project Vortex | BI and Research Showcase

I built this Power BI report to make the results of my quantitative research easier to compare, inspect and explain. I wanted one place to follow the path from organized market knowledge through AI-assisted experiments to historical portfolio and risk analysis. The public PBIP has 14 pages and an aggregate-only semantic model, separate from my private research system.

## Verified historical benchmark

The selected benchmark is **P6+SIZE+CE (PSC)** from 2022-01-04 through 2026-10-20: 324 portfolio records, 526 contract units, R$23,551 gross P&L, R$3,156 C30 costs applied once, and R$20,395 net C30 P&L. Historical win rate is 57.716%; PF is 1.950816. Maximum drawdown figures are R$1,932 realized close-order, R$2,077 M5 close, and R$2,113 adverse M5 OHLC-envelope. These are backtest results, not Paper Live or live-account performance. The P6 baseline is presented separately. No percentage return is calculated because initial capital is not specified.

## 14-page report

1. Knowledge & Intelligence
2. Autonomous Research Pipeline
3. Executive Overview
4. Portfolio Performance
5. Risk & Drawdown
6. Trade Explorer
7. Forward Validation & Governance
8–13. Six anonymized winning case studies
14. Two anonymized losing case studies

The first seven pages combine approved aggregate data with a concise account of how I organized knowledge, directed research and reviewed the evidence. Trade exhibits are redacted visual case studies; dates, exact prices, position sizes, individual P&L and operational identifiers are not included. They are illustrative and are not a statistical performance sample.

## Open the PBIP

Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop. From a fresh clone on Windows, run:

```powershell
.\scripts\configure-data-root.ps1
```

Then open the PBIP and refresh the model. It reads only the CSV aggregates under `data/`. No broker, account or live-market connection is configured. If moving the folder, rerun the setup script. Do not commit the locally configured `DataRoot` value.

## Data and metric limits

- `data/benchmark_summary.csv`: reconciled portfolio-level benchmark metrics.
- `data/monthly_portfolio_results.csv`: approved monthly aggregates.
- `data/annual_portfolio_results.csv`: approved annual aggregates.
- `data/monthly_drawdown_proxy.csv`: month-end aggregate drawdown proxy only.
- Close-order, M5-close and adverse OHLC-envelope drawdowns are separate definitions. The monthly line does not reconstruct trade-order or intrabar equity paths.
- Portfolio comparisons do not add P6 and PSC together. Cost scenario C30 is applied once in the benchmark net result.
- No trade-level ledger or private market archive is included.

## Screenshots and documentation

`images/powerbi/` contains genuine Power BI Desktop captures of all 14 pages, plus a contact sheet. `docs/` documents source parity, model boundaries, benchmark definitions, knowledge workflow and security review. `scripts/` contains reproducible public-model and PBIR utilities.

## Repository relationship

The companion [Project Vortex portfolio website source](https://github.com/LeoBobadilha/project-vortex-portfolio) is maintained separately. The website links back to this BI showcase repository.

## Risk disclosure

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations.

## Published releases and parity

Public BI release: https://github.com/LeoBobadilha/project-vortex-bi-showcase/releases/tag/v1.0.0
Base commit: a1593c1e6f0fb86ec8c5cc18bc08f50b92cdf38d.
Companion website release: https://github.com/LeoBobadilha/project-vortex-portfolio/releases/tag/v1.0.0
Base commit: 0fc9239bfd860c63cb60fa0d2186f09492c48545.

The active local private PBIR source and public PBIP both contain 14 pages and 83 visual definitions. The separately reported 88-visual count was not reproducible in the available active source; see docs/pbip-parity-report.md for the page-level substitutions and exact limitation.
