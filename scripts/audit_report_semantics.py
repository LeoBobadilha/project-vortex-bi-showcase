#!/usr/bin/env python3
"""Fail if the public report loses the portfolio-separation and layout corrections."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "PowerBI/ProjectVortex.Public.Report/definition/pages"
MODEL = ROOT / "PowerBI/ProjectVortex.SemanticModel/definition"
GUARDED = [
    "Gross P&L", "Net C30", "Operations", "Contract Units", "Winning Operations", "Profit Factor",
    "Max Realized DD (Full History)", "Longest Losing Streak", "Max M5 Close DD",
    "Max M5 OHLC Envelope DD", "Monthly Drawdown Proxy", "Cumulative Monthly Net C30", "Portfolio Records",
]
PSC_ON_DIMENSION = ["PSC Gross P&L", "PSC Net C30", "PSC Operations"]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def visuals(page: str) -> list[dict]:
    return [load(path) for path in sorted((PAGES / page / "visuals").glob("*/visual.json"))]


def page_id(order: list[str], name: str) -> str:
    return next(page for page in order if load(PAGES / page / "page.json")["displayName"] == name)


def fields(visual: dict, role: str) -> list[str]:
    state = visual["visual"].get("query", {}).get("queryState", {})
    return [row["queryRef"] for row in state.get(role, {}).get("projections", [])]


def literal(visual: dict, group: str, name: str):
    rows = visual["visual"].get("objects", {}).get(group, [{}])
    return rows[0].get("properties", {}).get(name, {}).get("expr", {}).get("Literal", {}).get("Value")


def main() -> int:
    errors: list[str] = []
    order = load(PAGES / "pages.json")["pageOrder"]
    measures = (MODEL / "tables/VortexMetrics.tmdl").read_text(encoding="utf-8-sig")

    for name in GUARDED:
        pattern = rf"measure ('{re.escape(name)}'|{re.escape(name)}) = IF\(HASONEVALUE\(DimPortfolio\[Portfolio\]\),"
        if not re.search(pattern, measures):
            errors.append(f"Measure can blend portfolios: {name}")
    for name in PSC_ON_DIMENSION:
        if not re.search(rf"measure '{re.escape(name)}' = .*DimPortfolio\[Portfolio\]=\"P6\+SIZE\+CE\"\)", measures):
            errors.append(f"PSC measure does not filter DimPortfolio: {name}")

    performance = visuals(page_id(order, "Portfolio Performance"))
    charts = [v for v in performance if v["visual"]["visualType"] == "clusteredColumnChart"]
    if len(charts) != 2 or any(fields(v, "Series") != ["DimPortfolio.PortfolioLabel"] for v in charts):
        errors.append("Page 04 charts must show portfolios as separate series")
    tables = [v for v in performance if v["visual"]["visualType"] == "tableEx"]
    if len(tables) != 1 or literal(tables[0], "total", "totals") != "false":
        errors.append("Page 04 table total row must stay off; it would add both portfolios")

    risk_page = page_id(order, "Risk & Drawdown")
    filters = load(PAGES / risk_page / "page.json").get("filterConfig", {}).get("filters", [])
    if "'P6+SIZE+CE'" not in json.dumps(filters):
        errors.append("Page 05 must keep its PSC page filter")
    risk = visuals(risk_page)
    lines = sorted(fields(v, "Y")[0] for v in risk if v["visual"]["visualType"] == "lineChart")
    if len(lines) != 2 or lines[0] == lines[1]:
        errors.append(f"Page 05 line charts must be distinct: {lines}")
    if any(v["visual"]["visualType"] == "slicer" for v in risk):
        errors.append("Page 05 is PSC-only and must not offer a portfolio slicer")

    trade_page = page_id(order, "Trade Explorer")
    cards = [v for v in visuals(trade_page) if v["visual"]["visualType"] == "card"]
    scopes = {json.dumps(v.get("filterConfig", {}).get("filters", [{}])[0].get("filter")) for v in cards}
    if len(cards) != 2 or len(scopes) != 2 or not all("Win" in s or "Loss" in s for s in scopes):
        errors.append("Page 06 cards must count winning and losing examples separately")
    tables = [v for v in visuals(trade_page) if v["visual"]["visualType"] == "tableEx"]
    if len(tables) != 1 or literal(tables[0], "values", "wordWrap") != "true":
        errors.append("Page 06 table must wrap PublicContext")

    for page in order:
        data = load(PAGES / page / "page.json")
        if (data["width"], data["height"]) != (1280, 720):
            errors.append(f"Page is not 1280x720: {data['displayName']}")
        rows = visuals(page)
        for visual in rows:
            kind = visual["visual"]["visualType"]
            if kind == "slicer" and literal(visual, "data", "mode") != "'Dropdown'":
                errors.append(f"Slicer hides its selection on {data['displayName']}")
        if "Case Study" in data["displayName"]:
            image = next(v for v in rows if v["visual"]["visualType"] == "image")
            footer = next(v for v in rows if v["visual"]["visualType"] == "textbox")
            if image["position"]["y"] + image["position"]["height"] > footer["position"]["y"]:
                errors.append(f"Footer overlaps the exhibit on {data['displayName']}")

    text = "\n".join(path.read_text(encoding="utf-8-sig") for path in PAGES.glob("*/visuals/*/visual.json"))
    for stale in ("Cumulative realized C30 equity", "portfolio selector applies", "Realized Underwater", "M5 Close Underwater"):
        if stale in text:
            errors.append(f"Misleading or leftover label remains: {stale}")
    if '"__CONFIGURE_DATA_ROOT__/"' not in (MODEL / "expressions.tmdl").read_text(encoding="utf-8-sig"):
        errors.append("DataRoot must keep its clone-safe placeholder")

    for error in errors:
        print(error)
    print(f"Report semantics audit: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
