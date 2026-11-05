# Public Release Security Review

Review date: 2026-11-05. The BI repository is https://github.com/LeoBobadilha/project-vortex-bi-showcase; the companion website source is https://github.com/LeoBobadilha/project-vortex-portfolio.

## Published release and screenshot remediation

- BI public `main`: `401a28a95c7ae9dc82ab3634911e8429ce761185`.
- Website public `main`: `0b4b617d072d37e3ef8a668bca948b21bad4ce24`.
- BI `v1.0.0` points to `a1593c1e6f0fb86ec8c5cc18bc08f50b92cdf38d`; website `v1.0.0` points to `0fc9239bfd860c63cb60fa0d2186f09492c48545`. Both original refs contain earlier screenshot assets. BI commit `da3a78e` withdraws them from current main at `401a28a`; no history or tag was rewritten.
- The current BI tree retains six inspected clean captures (pages 01?03 and 12?14). Captures 04?11 and the derived contact sheet are withdrawn from current `main`.
- The website retains only the clean Executive Overview preview. Its screenshot gallery remains withheld pending genuine recaptures.
- The successful Pages deployment is workflow run 42029504199. Historical image blobs remain obtainable from earlier public commits/tags; this current-tree fix does not erase them.
- Eight genuine Power BI Desktop recaptures remain outstanding. The public PBIP retains all 14 pages and its semantic model.

## Approved content and exclusions

The report contains approved portfolio/month/year aggregates, a month-end drawdown proxy and eight anonymized embedded chart exhibits. The current public tree retains only six unobstructed report-page captures. It excludes private trade ledgers, complete portfolio files, raw M5 data, account identifiers, credentials, broker connections, proprietary strategy code and exact signal rules. The committed DataRoot is the clone-safe placeholder. Paper Live and live-account P&L are not claimed.

## Metric controls

The selected P6+SIZE+CE benchmark is separate from P6: R$23,551 gross less R$3,156 C30 costs applied once equals R$20,395 net across 324 portfolio records and 526 contract units. Realized close-order DD (R$1,932), M5 close DD (R$2,077) and adverse M5 OHLC-envelope DD (R$2,113) remain distinct. Starting capital is undefined, so no percentage return is published.

## Local verification

scripts/audit_public_release.py checks the public file tree, prohibited material, clone-safe configuration, key benchmark arithmetic, 14 page definitions, nine authored model tables, eight embedded cases, the six retained clean captures and 83 visual definitions. scripts/validate_pbip_parity.py verifies page, visual, theme, relationship and DAX structure against a reviewed public baseline. It can optionally compare a locally supplied private PBIR/model without writing private paths, identifiers, formulas or data to its output.

The website has a separate static-content audit and reproducible build. No unrestricted Power BI sharing, broker connection or trading endpoint is configured.

## Scope and limitations

These are local source and public Git-tree checks, not a claim that GitHub secret scanning issued a clean scan. The v1.0.0 public baseline and commit ancestry were previously verified online; the screenshot hotfix is published on current main. The companion portfolio is deployed at https://leobobadilha.github.io/project-vortex-portfolio/ (successful workflow run 42029504199).
