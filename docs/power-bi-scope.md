# Power BI Report Scope

The public release candidate is an independent 14-page PBIP. It contains a nine-table semantic model, 24 DAX measures, Power Query transformations, approved portfolio-level aggregate data and anonymized embedded case-study images.

Power BI Desktop 2.159.883.0 opened the named `ProjectVortex-Public` PBIP. After configuring the local `data/` root and refreshing, all 14 pages rendered. Native Desktop screenshots for every page are in `../images/powerbi/`. The refresh cleared the incomplete-table warning and displayed the reconciled PSC aggregate metrics.

The report presents P6+SIZE+CE (PSC) and the P6 baseline separately. It does not include private trade-level facts, raw M5 bars, exact case dates or prices, individual case outcomes, strategy rules, brokerage data or Paper Live P&L. The monthly drawdown visualization is an explicitly labeled aggregate proxy.
