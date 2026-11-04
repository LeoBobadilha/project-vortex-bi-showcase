# Public Release Security Review

Review date: 2026-11-04. The BI repository is https://github.com/LeoBobadilha/project-vortex-bi-showcase; the companion website source is https://github.com/LeoBobadilha/project-vortex-portfolio.

## Published release

- BI v1.0.0: clean-root commit a1593c1e6f0fb86ec8c5cc18bc08f50b92cdf38d.
- Website v1.0.0: clean-root commit 0fc9239bfd860c63cb60fa0d2186f09492c48545.
- Each public repository was created with a single root commit. Only main and the new v1.0.0 tag were pushed; legacy local refs were excluded.
- The BI tree was verified online with the 14-page PBIP, 83 visuals, public aggregate model and 14 Desktop captures.

## Approved content and exclusions

The BI release contains approved portfolio/month/year aggregates, a month-end drawdown proxy, eight anonymized embedded chart exhibits, report screenshots and public documentation. It excludes private trade ledgers, complete portfolio files, raw M5 data, account identifiers, credentials, broker connections, proprietary strategy code and exact signal rules. The committed DataRoot is the clone-safe placeholder. Paper Live and live-account P&L are not claimed.

## Metric controls

The selected P6+SIZE+CE benchmark is separate from P6: R$23,551 gross less R$3,156 C30 costs applied once equals R$20,395 net across 324 portfolio records and 526 contract units. Realized close-order DD (R$1,932), M5 close DD (R$2,077) and adverse M5 OHLC-envelope DD (R$2,113) remain distinct. Starting capital is undefined, so no percentage return is published.

## Local verification

scripts/audit_public_release.py checks the public file tree, prohibited material, clone-safe configuration, key benchmark arithmetic, 14 page definitions, nine authored model tables, eight embedded cases, 14 Desktop captures and 83 visual definitions. scripts/validate_pbip_parity.py verifies page, visual, theme, relationship and DAX structure against a reviewed public baseline. It can optionally compare a locally supplied private PBIR/model without writing private paths, identifiers, formulas or data to its output.

The website has a separate static-content audit and reproducible build. No unrestricted Power BI sharing, broker connection or trading endpoint is configured.

## Scope and limitations

These are local source and public Git-tree checks, not a claim that GitHub secret scanning issued a clean scan. Public files and commit ancestry were verified through GitHub's API. The website source repository is published separately from its hosting deployment.