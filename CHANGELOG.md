# Changelog

## Published screenshot-remediation update (main commit 401a28a)

- Withdrew contaminated screenshots for report pages 04-11 and the derived contact sheet from current `main`.
- Retained six inspected clean screenshots and the complete 14-page PBIP.
- Updated publication and security documentation. Existing `v1.0.0` remains the only tagged release; historical image blobs remain in its history.


## Unreleased

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
