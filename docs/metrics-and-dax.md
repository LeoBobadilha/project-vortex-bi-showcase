# Public benchmark metrics and DAX

Public measures are stored in the VortexMetrics table. Their formulas use portfolio-level aggregates and do not expose trade-level calculations.

## Source tables

- FactMonthlyResults: monthly portfolio totals for gross P&L, net C30 P&L, operation counts, winning-operation counts and contract units.
- Benchmark: reconciled portfolio-level metrics, including Profit Factor and separately defined drawdown statistics.
- DimDate and DimPortfolio: report dimensions used by the aggregate model.
- FactAnnualResults: approved annual aggregates.
- FactMonthlyRiskProxy: month-end cumulative P&L and drawdown proxy; it is not an intrabar equity curve.
- FactForwardValidation: qualitative validation-stage status only.
- FactCaseGallery: anonymized case-study labels, not an operation ledger.

## Portfolio separation

P6 and PSC are separate research portfolios and must never be added together. Every portfolio-scoped measure returns BLANK unless exactly one portfolio is in context, so an unfiltered visual cannot show a blended figure. The test is on DimPortfolio rather than a fact table: October 2024 has PSC data only, and a fact-table test would let that month through in an unfiltered view.

The PSC measures set DimPortfolio themselves, so they ignore any portfolio selection. A measure that needs a portfolio must get it from a chart series, a slicer or a page filter.

## Measures in the model

These examples match the expressions in VortexMetrics.tmdl. The same guard wraps Profit Factor, Max Realized DD (Full History), Longest Losing Streak, Max M5 Close DD, Max M5 OHLC Envelope DD, Monthly Drawdown Proxy, Cumulative Monthly Net C30 and Portfolio Records.

    Gross P&L =
        IF ( HASONEVALUE ( DimPortfolio[Portfolio] ), SUM ( FactMonthlyResults[GrossPnL_BRL] ) )

    Net C30 =
        IF ( HASONEVALUE ( DimPortfolio[Portfolio] ), SUM ( FactMonthlyResults[NetPnL_BRL_C30] ) )

    Operations =
        IF ( HASONEVALUE ( DimPortfolio[Portfolio] ), SUM ( FactMonthlyResults[TradeCount] ) )

    Contract Units =
        IF ( HASONEVALUE ( DimPortfolio[Portfolio] ), SUM ( FactMonthlyResults[ContractUnits] ) )

    Winning Operations =
        IF ( HASONEVALUE ( DimPortfolio[Portfolio] ), SUM ( FactMonthlyResults[WinningTrades] ) )

    Losing Operations = [Operations] - [Winning Operations]

    Win Rate = DIVIDE ( [Winning Operations], [Operations] )

    Profit Factor =
        IF (
            HASONEVALUE ( DimPortfolio[Portfolio] ),
            CALCULATE (
                MAX ( Benchmark[ProfitFactor] ),
                REMOVEFILTERS ( DimDate )
            )
        )

    PSC Net C30 =
        CALCULATE (
            [Net C30],
            REMOVEFILTERS ( DimPortfolio ),
            DimPortfolio[Portfolio] = "P6+SIZE+CE"
        )

    PSC Win Rate =
        CALCULATE (
            MAX ( Benchmark[WinRate] ),
            REMOVEFILTERS ( DimPortfolio ),
            Benchmark[Portfolio] = "P6+SIZE+CE"
        )

    PSC Profit Factor =
        CALCULATE (
            MAX ( Benchmark[ProfitFactor] ),
            REMOVEFILTERS ( DimPortfolio ),
            Benchmark[Portfolio] = "P6+SIZE+CE"
        )

    PSC Max Realized DD (Full History) =
        CALCULATE (
            MAX ( Benchmark[RealizedCloseOrderMaxDD_BRL] ),
            REMOVEFILTERS ( DimDate ),
            REMOVEFILTERS ( DimPortfolio ),
            Benchmark[Portfolio] = "P6+SIZE+CE"
        )

A DAX query using existing measure names:

    EVALUATE
    ROW (
        "Gross P&L", [PSC Gross P&L],
        "Net C30", [PSC Net C30],
        "Operations", [PSC Operations],
        "Win Rate", [PSC Win Rate],
        "Profit Factor", [PSC Profit Factor],
        "Realized close-order DD", [PSC Max Realized DD (Full History)]
    )

## Interpretation limits

- P6+SIZE+CE is the selected historical backtest benchmark. The P6 baseline remains separately selectable, is never added to it, and has a different recorded end date (16 Oct 2026 against 20 Oct 2026), so full-period totals are not directly comparable returns.
- C30 costs are already included in NetPnL_BRL_C30 and applied once upstream.
- PSC Operations counts portfolio records represented by monthly aggregates. Contract Units is distinct and must not be conflated with operation count.
- Profit Factor and the full-history drawdown measure intentionally ignore date slicing. Cumulative monthly P&L is not account equity.
- The three benchmark drawdowns are separate: realized close-order, M5 close and adverse M5 OHLC-envelope. Monthly Drawdown Proxy is only a month-end proxy.
- No percentage return is calculated because starting capital is unspecified. These are historical backtest results, not Paper Live or live-account performance.