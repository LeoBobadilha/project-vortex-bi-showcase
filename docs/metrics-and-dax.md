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

## Measures in the model

These examples match the expressions in VortexMetrics.tmdl:

    Gross P&L = SUM ( FactMonthlyResults[GrossPnL_BRL] )

    Net C30 = SUM ( FactMonthlyResults[NetPnL_BRL_C30] )

    Operations = SUM ( FactMonthlyResults[TradeCount] )

    Contract Units = SUM ( FactMonthlyResults[ContractUnits] )

    Winning Operations = SUM ( FactMonthlyResults[WinningTrades] )

    Losing Operations = [Operations] - [Winning Operations]

    Win Rate = DIVIDE ( [Winning Operations], [Operations] )

    Profit Factor =
        CALCULATE (
            MAX ( Benchmark[ProfitFactor] ),
            REMOVEFILTERS ( DimDate )
        )

    PSC Net C30 =
        CALCULATE (
            [Net C30],
            REMOVEFILTERS ( DimPortfolio ),
            FactMonthlyResults[Portfolio] = "P6+SIZE+CE"
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

- P6+SIZE+CE is the selected historical backtest benchmark; the P6 baseline remains separately selectable and is not added to it.
- C30 costs are already included in NetPnL_BRL_C30 and applied once upstream.
- PSC Operations counts portfolio records represented by monthly aggregates. Contract Units is distinct and must not be conflated with operation count.
- Profit Factor and the full-history drawdown measure intentionally ignore date slicing. Cumulative monthly P&L is not account equity.
- The three benchmark drawdowns are separate: realized close-order, M5 close and adverse M5 OHLC-envelope. Monthly Drawdown Proxy is only a month-end proxy.
- No percentage return is calculated because starting capital is unspecified. These are historical backtest results, not Paper Live or live-account performance.