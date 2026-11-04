# Getting Started

Open `PowerBI/ProjectVortex-Public.pbip` in Power BI Desktop. On Windows, configure the local aggregate folder from the repository root:

```powershell
.\scripts\configure-data-root.ps1
```

Refresh the model in Desktop. The script writes a machine-specific `DataRoot` value into the local semantic model; the committed PBIP retains a clone-safe placeholder. Never commit a configured local path.

Use the 14 genuine Desktop screenshots in `images/powerbi/` for a quick visual tour. A compatible Power BI Desktop installation is required to explore the interactive report. See `PowerBI/README.md`, `docs/data-model.md` and `SECURITY_REVIEW.md` for scope, metrics and exclusions.

Run python scripts/validate_pbip_parity.py after changing the PBIR, theme, relationships or measures. See docs/pbip-parity-report.md for the active local parity findings.