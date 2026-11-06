# Power BI Report Scope

The published public report is an independent 14-page PBIP. It contains a nine-table semantic model, 24 DAX measures, Power Query transformations, approved portfolio-level aggregate data and anonymized embedded case-study images.

Power BI Desktop 2.159.1231.0 opened the named `ProjectVortex-Public` PBIP. After configuring the local `data/` root and refreshing, all 14 pages rendered and all 14 were recaptured in one session. See `screenshot-qa-2026-11-06.md`. The screenshots do not define page count or alter PBIP contents.

The report presents P6+SIZE+CE (PSC) and the P6 baseline separately and never adds them together: page 03 is PSC only, page 04 compares them as separate series, and page 05 is PSC only. The declared Vortex_Navy custom theme is embedded in the public PBIR resources. It does not include private trade-level facts, raw M5 bars, exact case dates or prices, individual case outcomes, strategy rules, brokerage data or Paper Live P&L. The monthly drawdown visualization is an explicitly labeled aggregate proxy.

See docs/pbip-parity-report.md for the reproducible comparison against the active local private report and the separately reported but unverified 88-visual count, not reproduced from the available 83-definition snapshot.
