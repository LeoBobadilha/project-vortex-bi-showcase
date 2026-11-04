# Benchmark and metric methodology

## P6+SIZE+CE (PSC)

324 is the portfolio-record count; 526 is the number of final contract units. These counts are different measures. The source-defined gross formula is `gross points × final units × R$0.20`. C30 net is `(gross points − 30) × final units × R$0.20`. C30 is charged once per final unit at R$6.00. No second deduction is applied.

Win rate is the positive C30 portfolio records divided by all records. Profit factor is aggregate positive C30 P&L divided by the absolute value of aggregate negative C30 P&L. Payoff is average positive record divided by the absolute average negative record. No return percentage is calculated without a capital premise.

## Drawdown paths

- Realized close-order drawdown is calculated from completed C30 trade results in recorded exit-bar order.
- M5 close mark-to-market uses verified M5 close prices and recorded fill/exit indices for open positions.
- The adverse OHLC measure marks open net exposure to the adverse low/high of each M5 bar. It is a conservative bar-level envelope, not a reconstruction of tick path or within-bar execution order.

The three paths must not be presented as interchangeable values. Year and month aggregates contain periods with recorded portfolio activity only; empty periods are not filled with invented observations.

## Independent portfolio comparison

P6 and PSC are separate frozen ledgers. The aggregate comparison does not add extension totals to P6. Their data end dates differ, so total-period figures are not same-window performance.

Past performance, including historical backtests and simulated trading results, does not guarantee future results. Actual trading involves risk, and execution conditions may differ materially from simulations.
