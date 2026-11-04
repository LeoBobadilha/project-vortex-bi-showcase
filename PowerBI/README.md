# Project Vortex Public Power BI Project

Companion project: [Project Vortex portfolio website](https://github.com/LeoBobadilha/project-vortex-portfolio).

Open `ProjectVortex-Public.pbip` in Power BI Desktop. This is an independent, public-safe 14-page PBIP containing an aggregate-only semantic model and anonymized embedded case images.

## Clone setup

On Windows, run from this repository root:

```powershell
.\scripts\configure-data-root.ps1
```

The script points the semantic model's `DataRoot` parameter to this clone's `data/` folder. Refresh the model in Power BI Desktop. The value is machine-specific and must not be committed. The checked-in PBIP should retain the `__CONFIGURE_DATA_ROOT__/` placeholder.

## Model scope

The public model contains portfolio/period aggregate facts, benchmark summaries, public case metadata and qualitative validation status. It excludes individual trade records, precise case timestamps/prices/results, raw M5 data, strategy rules and account data. Its monthly drawdown line is explicitly a month-end proxy. It is not intrabar mark-to-market equity.

The 14 pages are: Knowledge & Intelligence; Autonomous Research Pipeline; Executive Overview; Portfolio Performance; Risk & Drawdown; Trade Explorer; Forward Validation & Governance; six selected winning case studies; and two selected losing case studies.

## Rebuild and validation

The model tables and DAX live in TMDL. Public data extracts live in `../data/`. `../scripts/` contains the public model and report utilities. Genuine Desktop screenshots for each page are in `../images/powerbi/`.

Validated in Power BI Desktop 2.159.883.0: the PBIP opens as a named report, refresh clears the initial model-load warning, all 14 page tabs render, and aggregate benchmark cards reconcile to R$20,395 net C30, R$23,551 gross, 324 records, 57.7% win rate, PF 1.951 and R$1,932 realized close-order maximum drawdown. Screenshots are from the native Desktop application. The private report and private dataset are not part of this repository.

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk and execution conditions may differ materially from simulations.
