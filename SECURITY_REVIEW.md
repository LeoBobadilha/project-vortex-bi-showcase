# Public Release Security Review

Review date: 2026-11-06. This review covers the public PBIP/PBIR/TMDL, aggregate data, registered chart resources, screenshot files, website references and repository documentation. It is a local source-and-tree review, not a claim of an external secret-scanner result.

## Report and data scope

The report retains 14 pages, 83 visual definitions, nine authored semantic-model tables, ten relationships and 24 measures. Its DataRoot remains a clone-safe placeholder. Public model inputs are approved portfolio aggregates; there is no broker, account or live-market connection. Individual trade ledgers, raw market archives, private strategy source, credentials and operational account details are excluded.

The six current report-page screenshots are genuine inspected Desktop captures for pages 01–03 and 12–14. Pages 04–11 remain unavailable pending genuine Power BI Desktop captures. The current `main` must not be described as a complete screenshot gallery. The PBIP itself contains all 14 report pages. Known contaminated screenshot content is checked by Git blob identity rather than rejecting a filename that could later hold a newly generated safe contact sheet.

## Companion website

The [portfolio site](https://leobobadilha.github.io/project-vortex-portfolio/) is static and has no trading backend or broker connection. Its replay is a separate WIN research-model example, not a PSC, Paper Live or live-account result. The source market session date, 30 September 2022, is represented by source epoch timestamps; the source timezone is unauthenticated and the date is not a certified B3 local timestamp. Exact timestamps, internal event IDs and unshifted prices remain private. Publishing that date with recognizable candle geometry increases external market-correlation risk. The Entry 2 and modeled exit are off the five-point WIN tick grid; R$750.20 gross and R$738.20 after the distinct R$12 S2 assumption are adjusted-price model arithmetic, not executable performance. S2 is not C30.

The website's six approved report screenshots are incomplete coverage, not a 14-image gallery. Historical screenshot blobs remain in earlier public Git objects and v1.0.0 refs; current-tree withdrawal did not erase history. No tag or public history was rewritten.

## Financial controls

The selected PSC benchmark remains separate from P6: R$23,551 gross less R$3,156 C30 costs applied once equals R$20,395 net across 324 portfolio records and 526 contract units. Win rate is 57.716%; profit factor is 1.950816. Realized close-order, M5-close and adverse OHLC-envelope drawdowns remain separately defined at R$1,932, R$2,077 and R$2,113. No percentage return is published without initial capital.

## Validation and links

`python scripts/audit_public_release.py` checks the PBIP structure, public aggregates, clone-safe DataRoot and the exact six-image or complete 14-image screenshot set. `python scripts/audit_screenshot_set.py` requires all 14 images, verifies names, dimensions and hashes, and writes the manifest. `python scripts/audit_screenshot_parity.py` compares BI and website copies. Pixel inspection remains a human review requirement. See the [PBIP parity report](docs/pbip-parity-report.md), [capture runbook](docs/screenshot-capture-runbook.md), [BI repository](https://github.com/LeoBobadilha/project-vortex-bi-showcase) and [Pages workflow history](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/workflows/deploy-pages.yml).