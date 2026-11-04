# Public BI Architecture

The public analytics flow is:

**Approved portfolio aggregates → Power Query transformations → dimensional semantic model and DAX → interactive 14-page Power BI report.**

The Power BI project is independent of the trading executor and contains no broker connection. The case gallery uses embedded, redacted chart resources. The public dataset contains no individual trade ledger or raw market bars.
