# Project Vortex Public Power BI Project

I built this report to examine historical performance, risk and the research process in a format that is easier to compare and audit. The [Project Vortex portfolio website](https://github.com/LeoBobadilha/project-vortex-portfolio) explains the broader engineering story.

Open `ProjectVortex-Public.pbip` in Power BI Desktop. This independent 14-page project uses an aggregate-only semantic model and anonymized embedded case images.

## Clone setup

On Windows, run from this repository root:

```powershell
.\scripts\configure-data-root.ps1
```

The script points the semantic model's `DataRoot` parameter to this clone's `data/` folder. Refresh the model in Power BI Desktop. The value is machine-specific and must not be committed. The checked-in PBIP should retain the `__CONFIGURE_DATA_ROOT__/` placeholder.

## Model scope

The public model contains portfolio/period aggregate facts, benchmark summaries, public case metadata and qualitative validation status. It excludes individual trade records, precise case timestamps/prices/results, raw M5 data, strategy rules and account data. Its monthly drawdown line is explicitly a month-end proxy. It is not intrabar mark-to-market equity.

The 14 pages cover seven core analytics and governance views, five winning case-study pages, and two losing case studies. Trade Explorer includes one additional winning example.

## Rebuild and validation

The model tables and DAX live in TMDL. Public data extracts live in `../data/`. `../scripts/` contains the public model and report utilities. Genuine Desktop screenshots for each page are in `../images/powerbi/`.

Validated in Power BI Desktop 2.159.883.0: the PBIP opens as a named report, refresh clears the initial model-load warning, all 14 page tabs render, and aggregate benchmark cards reconcile to R$20,395 net C30, R$23,551 gross, 324 records, 57.7% win rate, PF 1.951 and R$1,932 realized close-order maximum drawdown. Screenshots are from the native Desktop application. The private report and private dataset are not part of this repository.

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations.

## Published release provenance and parity

BI repository: https://github.com/LeoBobadilha/project-vortex-bi-showcase
Companion portfolio source: https://github.com/LeoBobadilha/project-vortex-portfolio
Base v1.0.0 commit SHAs: BI a1593c1e6f0fb86ec8c5cc18bc08f50b92cdf38d; website 0fc9239bfd860c63cb60fa0d2186f09492c48545.

See ../docs/pbip-parity-report.md for the page-by-page comparison, the difference between the operator-reported 88 visuals and the 83 definitions in the available active private PBIR snapshot, and the intentionally aggregate-only public model. Run python scripts/validate_pbip_parity.py to detect drift against the reviewed public structural baseline. The optional private comparison reads local private files only and writes sanitized counts.
