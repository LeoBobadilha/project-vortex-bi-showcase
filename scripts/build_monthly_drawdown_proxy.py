#!/usr/bin/env python3
"""Derive a public month-end drawdown proxy from approved monthly aggregates.
This is not trade-level realized DD or M5 mark-to-market DD.
"""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "Data" / "monthly_portfolio_results.csv"
target = root / "Data" / "monthly_drawdown_proxy.csv"
groups = defaultdict(list)
with source.open(newline="", encoding="utf-8-sig") as stream:
    for row in csv.DictReader(stream):
        groups[row["Portfolio"]].append(row)
rows = []
for portfolio, items in sorted(groups.items()):
    cumulative = Decimal("0")
    high_water = Decimal("0")
    for item in sorted(items, key=lambda x: x["YearMonth"]):
        cumulative += Decimal(item["NetPnL_BRL_C30"])
        high_water = max(high_water, cumulative)
        rows.append({
            "Portfolio": portfolio,
            "YearMonth": item["YearMonth"],
            "CumulativeMonthlyNetC30_BRL": f"{cumulative:.2f}",
            "MonthEndDrawdownProxy_BRL": f"{cumulative - high_water:.2f}",
        })
with target.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} monthly aggregate observations to {target.name}.")
