# Project Vortex | BI and Research Showcase

A public-safe, editable Power BI portfolio about the engineering process behind Project Vortex: structured market knowledge, AI-assisted research workflows, quantitative validation, risk analysis and human governance. The PBIP contains 14 pages and a public-only semantic model. It is separate from the private research system.

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

The first seven pages use approved aggregate data and bounded qualitative process descriptions. Trade exhibits are redacted visual case studies; dates, exact prices, position sizes, individual P&L and operational identifiers are not included. They are illustrative and are not a statistical performance sample.

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
