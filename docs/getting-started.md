# Getting Started

Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop. On Windows, configure the local aggregate folder from the repository root:

```powershell
.\scripts\configure-data-root.ps1
```

Refresh the model in Desktop. The script writes a machine-specific `DataRoot` value into the local semantic model; the committed PBIP retains a clone-safe placeholder. Never commit a configured local path.

Genuine Desktop screenshots of all 14 pages are in `images/powerbi/`. A compatible Power BI Desktop installation is required to explore the interactive report. See `PowerBI/README.md`, `docs/data-model.md`, `docs/screenshot-qa-2026-11-06.md` and `SECURITY_REVIEW.md` for scope, metrics and exclusions.

Run python scripts/validate_pbip_parity.py after changing the PBIR, theme, relationships or measures. See docs/pbip-parity-report.md for the active local parity findings.
