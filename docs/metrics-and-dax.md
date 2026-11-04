# Benchmark metrics and DAX

- Gross P&L: sum of recorded gross monthly portfolio aggregates.
- Net C30 P&L: sum after the recorded C30 methodology; costs are applied once upstream.
- Portfolio records: sum of aggregate monthly record counts; records are not contract units.
- Win rate: sum of winning records divided by portfolio records.
- PF: approved full-history net-C30 summary value.
- Realized close-order DD: approved full-history portfolio metric. It is not intrabar DD.

Representative model formulas:

```DAX
PSC Gross P&L = SUM(FactTrades[GrossPnL_BRL])
PSC Net C30 = SUM(FactTrades[NetPnL_BRL_C30])
PSC Portfolio Records = SUM(FactTrades[TradeCount])
PSC Win Rate = DIVIDE(SUM(FactTrades[WinningTrades]), [PSC Portfolio Records])
PSC Profit Factor = MAX(Benchmark[ProfitFactor])
PSC Max Realized DD (Full History) = MAX(Benchmark[RealizedCloseOrderMaxDD_BRL])
```

The year dimension filters monthly P&L; PF and DD are sourced from the portfolio summary and remain full-history measures. Cumulative monthly P&L is not account equity. Return percentage is omitted because no starting capital is specified.
