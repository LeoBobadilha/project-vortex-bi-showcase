# Getting Started

Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop. On Windows, configure the local aggregate folder from the repository root:

```powershell
.\scripts\configure-data-root.ps1
```

Refresh the model in Desktop. The script writes a machine-specific `DataRoot` value into the local semantic model; the committed PBIP retains a clone-safe placeholder. Never commit a configured local path.

Six unobstructed Desktop screenshots (pages 01–03 and 12–14) are retained in `images/powerbi/`. Screenshots 04–11 and the contact sheet are withheld pending genuine Power BI Desktop recaptures; the public PBIP itself still contains all 14 pages. A compatible Power BI Desktop installation is required to explore the interactive report. See `PowerBI/README.md`, `docs/data-model.md`, `docs/screenshot-qa-2026-11-05.md` and `SECURITY_REVIEW.md` for scope, metrics and exclusions.

Run python scripts/validate_pbip_parity.py after changing the PBIR, theme, relationships or measures. See docs/pbip-parity-report.md for the active local parity findings.
