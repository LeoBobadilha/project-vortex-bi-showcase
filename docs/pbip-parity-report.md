# PBIP parity report

## Scope and reproducibility

This comparison uses the active local private PBIP report definitions and the separate public report definitions. It compares ordered page names, per-page visual types and counts, and required public resources. The private model was read locally; no private data, formulas, page IDs or filesystem path is included here.

The active private PBIP available for review contains 14 ordered pages and 83 visual.json definitions. The public PBIP contains 14 ordered pages and 83 visual.json definitions. The instruction-supplied private count of 88 could not be reproduced from the available active PBIR snapshot, leaving five reported visuals unaccounted for. This report does not invent or assign those five visuals. If a different private export is the intended reference, rerun the validator against that exact local export.

Reproduce the comparison from the BI repository root with local-only reference paths:

    python scripts/validate_pbip_parity.py ^
      --private-report-root "<local-private-report-root>" ^
      --private-model-root "<local-private-semantic-model-root>"

The command prints the comparison and refreshes docs/pbip-parity-report.json. It omits private paths, visual identifiers, data and formulas from that output. The private model remains local.

## Page and visual differences found

All 14 page names and their order match in the active local private PBIR and the public PBIR. Per-page visual totals also match. Three pages replace restricted or unsupported visuals with explanatory text while preserving their visual count:

| Page | Active private PBIR | Public PBIR | Difference |
|---|---|---|---|
| Autonomous Research Pipeline | 1 bar chart, 1 clustered column chart, 7 textboxes | 1 clustered column chart, 8 textboxes | The bar chart is replaced by an explanatory textbox because a reliable, publishable experiment-count series is not available. |
| Executive Overview | 6 cards, 1 line chart, 3 slicers, 4 textboxes, 1 clustered column chart | 6 cards, 1 line chart, 1 slicer, 6 textboxes, 1 clustered column chart | Two slicers are replaced by disclosure text because unsupported detail filters are not exposed by the aggregate-only model. |
| Portfolio Performance | 2 clustered column charts, 1 bar chart, 2 slicers, 1 table, 3 textboxes | 2 clustered column charts, 2 slicers, 1 table, 4 textboxes | The bar chart is replaced by an explanation because the public aggregate model does not support that detailed breakdown. |

The remaining pages preserve their visual counts and types. The report retains the same approved 14-page architecture and the same navy custom theme. The public PBIR includes the Vortex_Navy theme resource declared by report.json.

## Semantic-model differences

The private and public models are intentionally not equivalent at the data grain. The public model contains nine authored aggregate tables, ten declared relationships and 24 public measures. The locally checked private model contains more detailed semantics (14 relationships and 29 measures in the inspected TMDL snapshot). The five fewer public measures and four fewer relationships reflect the exclusion of trade-level and execution-detail facts; private definitions are not copied into this report.

The public model retains DAX for gross and net C30 P&L, aggregate operations and contract units, win rate, Profit Factor, selected PSC metrics, distinct drawdown definitions, and case counts. The monthly drawdown series remains explicitly identified as a proxy.

## Automated drift checks

Run the public validation baseline check after PBIR, theme, relationship or DAX edits:

    python scripts/validate_pbip_parity.py

The validator compares ordered page structure, all public visual-definition hashes, the custom-theme hash, TMDL relationship declarations, authored table and measure counts, and DAX declaration hashes with docs/pbip-structure-baseline.json. Unexpected drift fails the command. Refreshing the baseline requires the explicit --write-baseline option and should only follow review.