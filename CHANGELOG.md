# Changelog

## Published screenshot-remediation update (main commit 401a28a)

- Withdrew contaminated screenshots for report pages 04-11 and the derived contact sheet from current `main`.
- Retained six inspected clean screenshots and the complete 14-page PBIP.
- Updated publication and security documentation. Existing `v1.0.0` remains the only tagged release; historical image blobs remain in its history.


## Unreleased

- Corrected cross-portfolio aggregation. Portfolio-scoped measures now return BLANK unless one portfolio is in context, so an unfiltered visual can no longer add P6 and PSC. The unfiltered Net C30 of R$34,036 was such a blend. Every single-portfolio value is unchanged.
- Page 04 is a genuine P6 and PSC comparison with labelled recorded periods and no combined total row. Page 05 is PSC only through a locked page filter, and its duplicate chart is replaced with cumulative net C30 P&L.
- Page 06 cards now show six winning and two losing examples, its table wraps, and its text correctly says W01 is on that page and seven cases have their own pages.
- Slicers are dropdowns that show their selection. Pages 08-14 are now 1280 x 720 and the footer no longer hides the exhibit's final caveat.
- Corrected the cumulative chart label on page 03 and the page 02 title, which named a selector that does not exist.
- Manifest hashes are now canonical across operating systems, and `scripts/audit_report_semantics.py` guards these corrections.
- Recaptured all 14 report pages from Power BI Desktop 2.159.1231.0 in one refreshed session, with pages 04 and 05 showing the PSC portfolio. The set replaces the six retained images and restores pages 04-11 with genuine new captures. The contact sheet was not regenerated.
- Replaced the F9 capture helper with `scripts/capture-powerbi-pages.ps1`, which drives Power BI through Windows UI Automation and captures only the Power BI window.
- Screenshot audits now require the complete 14-image set. Corrected the known-contaminated-blob check in `audit_public_release.py`, whose Git blob header was malformed and could not match.
- Reconciled public PBIP parity and documented the available private snapshot limitation.
- Corrected public DAX documentation and updated release, security and repository provenance notes.
- Refined README authorship and the page-count description.
- Withdrew eight Zoom-contaminated Desktop page captures and the derived contact sheet from the published main tree; no substitute captures were generated.

## v1.0.0 (published)

- Published the public-safe 14-page PBIP, aggregate-only semantic model, documentation and approved portfolio evidence.
- The initial release included all 14 Desktop page captures. A later visual inspection found meeting overlays in pages 04–11; their historical Git blobs are unchanged and the affected images are withheld from the current public tree.
