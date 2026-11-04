# Public Release Security Review

Review date: 2026-11-04. Scope: current public BI working tree, PBIP/PBIR/TMDL content, aggregate CSVs, scripts, images, screenshots, documentation and all Git refs considered for release.

## Approved content

- A separately generated 14-page public PBIP and its public-only semantic model.
- Aggregate portfolio/month/year datasets and a clearly labeled month-end drawdown proxy.
- Eight anonymized illustrative case charts embedded as resources and in Desktop screenshots. Dates, exact price levels, sizes, individual P&L and operational identifiers are redacted.
- English documentation and source-parity metadata.

## Explicit exclusions

No private trade ledger, full portfolio dataset, raw M5 data, account identifiers, credentials, broker links, proprietary strategy code or exact signal rules are approved for publication. The configured machine-specific DataRoot has been reset to the public placeholder. No Paper Live or live-account P&L is claimed. No local file URL is used to render case charts; public visuals use embedded, redacted resources.

## Metric controls

The PSC/P6+SIZE+CE benchmark remains separate from P6. Its gross R$23,551 less C30 costs R$3,156 once equals net R$20,395 over 324 portfolio records and 526 contract units. The published drawdown figures retain separate labels for realized close-order (R$1,932), M5 close (R$2,077) and adverse M5 OHLC-envelope (R$2,113). Starting capital is undefined, so no percentage return is published. Individual trade outcomes are omitted from the public model.

## History and publication controls

This directory previously held a one-page demo with stale content. Release must use a clean-root public commit containing only the reviewed current tree, with only the approved `main` branch and a fresh release tag pushed. Do not push legacy branches, old tags, or the existing local Git history. Local review does not itself publish content.

## Limitations

The final GitHub remote has not been configured in this environment, so online content and repository permissions cannot be verified here. This review is a local content and Git-tree review, not an external GitHub secret-scanner result. Public GitHub release remains blocked until an authenticated GitHub connection is available and the clean-root tree is re-audited immediately before push. Website deployment is separate and is not performed.
