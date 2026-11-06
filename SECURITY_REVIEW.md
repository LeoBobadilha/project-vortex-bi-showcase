# Public Release Security Review

Review date: 2026-11-06. This review covers the public PBIP/PBIR/TMDL, aggregate data, registered chart resources, screenshot files, website references and repository documentation. It is a local source-and-tree review, not a claim of an external secret-scanner result.

## Report and data scope

The report retains 14 pages, 83 visual definitions, nine authored semantic-model tables, ten relationships and 24 measures. Its DataRoot remains a clone-safe placeholder. Public model inputs are approved portfolio aggregates; there is no broker, account or live-market connection. Individual trade ledgers, raw market archives, private strategy source, credentials and operational account details are excluded.

The 14 report-page screenshots are genuine Desktop captures from one refreshed session on 2026-11-06, each pixel-reviewed. They use a window-only capture, so other windows and notifications cannot appear in them. Known contaminated screenshot content is checked by Git blob identity rather than rejecting a filename that could later hold a newly generated safe contact sheet.

## Companion website

The [portfolio site](https://leobobadilha.github.io/project-vortex-portfolio/) is static and has no trading backend or broker connection. Its replay is a separate WIN research-model example, not a PSC, Paper Live or live-account result. The source market session date, 30 September 2022, is represented by source epoch timestamps; the source timezone is unauthenticated and the date is not a certified B3 local timestamp. Exact timestamps, internal event IDs and unshifted prices remain private. Publishing that date with recognizable candle geometry increases external market-correlation risk. The Entry 2 and modeled exit are off the five-point WIN tick grid; R$750.20 gross and R$738.20 after the distinct R$12 S2 assumption are adjusted-price model arithmetic, not executable performance. S2 is not C30.

The website shows the same 14 report screenshots, with matching SHA-256 hashes. Earlier public Git objects and v1.0.0 refs still hold the contaminated screenshots, which show meeting UI, including participant names, and unrelated shared-screen market windows. Anyone with the repository can still retrieve them, and current-tree withdrawal did not erase them. Removing them would need a history rewrite, which requires separate approval. No tag or public history was rewritten.

## Financial controls

The selected PSC benchmark remains separate from P6: R$23,551 gross less R$3,156 C30 costs applied once equals R$20,395 net across 324 portfolio records and 526 contract units. Win rate is 57.716%; profit factor is 1.950816. Realized close-order, M5-close and adverse OHLC-envelope drawdowns remain separately defined at R$1,932, R$2,077 and R$2,113. No percentage return is published without initial capital. Portfolio-scoped measures return BLANK unless one portfolio is in context, so P6 and PSC cannot be added together.

## Validation and links

`python scripts/audit_public_release.py` checks the PBIP structure, public aggregates, clone-safe DataRoot and the complete 14-image screenshot set. `python scripts/audit_screenshot_set.py` requires all 14 images, verifies names, dimensions and hashes, and writes the manifest. `python scripts/audit_screenshot_parity.py` compares BI and website copies. `python scripts/audit_report_semantics.py` checks portfolio separation and the report layout rules. `security-review-manifest.json` records canonical LF hashes for text and exact-byte hashes for images. Pixel inspection remains a human review requirement. See the [PBIP parity report](docs/pbip-parity-report.md), [capture runbook](docs/screenshot-capture-runbook.md), [BI repository](https://github.com/LeoBobadilha/project-vortex-bi-showcase) and [Pages workflow history](https://github.com/LeoBobadilha/project-vortex-portfolio/actions/workflows/deploy-pages.yml).