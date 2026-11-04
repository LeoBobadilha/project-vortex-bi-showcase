# Public Data Model

The report model has nine tables and 24 measures. Its public facts are portfolio-level benchmark, annual, monthly and month-end risk aggregates, plus anonymized case labels and qualitative validation scope. No individual trade records or raw market bars are distributed.

`DataRoot` points Power Query to the `data/` folder after running the Windows clone-setup script. The committed value is a placeholder. Re-run the setup command after moving the clone; do not commit a machine-specific path.

The monthly drawdown line is a month-end aggregate proxy and does not reconstruct trade-order or intrabar equity. The full-history realized close-order, M5 close and adverse M5 OHLC-envelope drawdown measures are separate and retain their source definitions. No return percentage is shown because starting capital is undefined.
