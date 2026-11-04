import json,uuid
from pathlib import Path
def gid():return str(uuid.uuid4())
def col(n,t,fmt=None,s="none"):
 q="'"+n.replace("'","''")+"'" if any(c in n for c in " ()-") else n
 r=[f"\tcolumn {q}",f"\t\tdataType: {t}",f"\t\tlineageTag: {gid()}",f"\t\tsummarizeBy: {s}",f"\t\tsourceColumn: {n}"]
 if fmt:r.append(f"\t\tformatString: {fmt}")
 return "\n".join(r)
def build_table(n,columns,m):
 a=[f"table {n}",f"\tlineageTag: {gid()}",""]
 for c in columns:a += [col(*c),""]
 a += [f"\tpartition {n} = m","\t\tmode: import","\t\tsource ="]
 a += ["\t\t\t"+z for z in m.strip().splitlines()]
 return "\n".join(a)+"\n"
def main():
 repo=Path(__file__).resolve().parents[1];root=repo/"PowerBI";model=root/"ProjectVortex.SemanticModel";d=model/"definition";td=d/"tables";td.mkdir(parents=True,exist_ok=True)
 (model/".platform").write_text(json.dumps({"$schema":"https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json","metadata":{"type":"SemanticModel","displayName":"Project Vortex Public Semantic Model"},"config":{"version":"2.0","logicalId":gid()}},indent=2)+"\n",encoding="utf-8")
 (model/"definition.pbism").write_text('{\n  "version": "4.2",\n  "settings": {}\n}\n',encoding="utf-8")
 (d/"database.tmdl").write_text("database\n\tcompatibilityLevel: 1700\n",encoding="utf-8")
 (d/"expressions.tmdl").write_text('expression DataRoot = "__CONFIGURE_DATA_ROOT__/" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n\tlineageTag: '+gid()+'\n\n\tannotation PBI_ResultType = Text\n',encoding="utf-8")
 monthly='''let
    Source = Csv.Document(File.Contents(DataRoot & "monthly_portfolio_results.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Portfolio", type text}, {"YearMonth", type text}, {"NetPnL_BRL_C30", type number}, {"GrossPnL_BRL", type number}, {"TradeCount", Int64.Type}, {"WinningTrades", Int64.Type}, {"ContractUnits", Int64.Type}}, "en-US"),
    Month = Table.AddColumn(Types, "MonthStart", each Date.FromText([YearMonth] & "-01", [Culture="en-US"]), type date)
in
    Month'''
 annual='''let
    Source = Csv.Document(File.Contents(DataRoot & "annual_portfolio_results.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Portfolio", type text}, {"Year", Int64.Type}, {"NetPnL_BRL_C30", type number}, {"GrossPnL_BRL", type number}, {"TradeCount", Int64.Type}, {"WinningTrades", Int64.Type}, {"ContractUnits", Int64.Type}}, "en-US")
in
    Types'''
 bench='''let
    Source = Csv.Document(File.Contents(DataRoot & "benchmark_summary.csv"), [Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Portfolio", type text}, {"DataOrigin", type text}, {"PeriodStart", type date}, {"PeriodEnd", type date}, {"PortfolioRecords", Int64.Type}, {"FinalContractUnits", Int64.Type}, {"GrossPnL_BRL", type number}, {"C30NetPnL_BRL", type number}, {"RecordedCosts_BRL", type number}, {"WinRate", type number}, {"ProfitFactor", type number}, {"RealizedCloseOrderMaxDD_BRL", type number}, {"M5CloseMaxDD_BRL", type number}, {"M5AdverseOHLCEnvelopeDD_BRL", type number}, {"LongestLosingStreak", Int64.Type}}, "en-US")
in
    Types'''
 risk='''let
    Source = Csv.Document(File.Contents(DataRoot & "monthly_drawdown_proxy.csv"), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Portfolio", type text}, {"YearMonth", type text}, {"CumulativeMonthlyNetC30_BRL", type number}, {"MonthEndDrawdownProxy_BRL", type number}}, "en-US"),
    Month = Table.AddColumn(Types, "MonthStart", each Date.FromText([YearMonth] & "-01", [Culture="en-US"]), type date)
in
    Month'''
 dimdate='''let
    Source = FactMonthlyResults,
    DistinctMonths = Table.Distinct(Table.SelectColumns(Source, {"MonthStart", "YearMonth"})),
    AddDate = Table.AddColumn(DistinctMonths, "Date", each [MonthStart], type date),
    AddYear = Table.AddColumn(AddDate, "Year", each Date.Year([MonthStart]), Int64.Type),
    AddMonthNumber = Table.AddColumn(AddYear, "MonthNumber", each Date.Month([MonthStart]), Int64.Type),
    AddMonth = Table.AddColumn(AddMonthNumber, "Month", each Date.ToText([MonthStart], "MMM", "en-US"), type text),
    Sort = Table.Sort(AddMonth, {{"MonthStart", Order.Ascending}})
in
    Sort'''
 portfolio='''let
    Source = Benchmark,
    Distinct = Table.Distinct(Table.SelectColumns(Source, {"Portfolio"})),
    AddLabel = Table.AddColumn(Distinct, "PortfolioLabel", each if [Portfolio] = "P6+SIZE+CE" then "P6 + SIZE + CE" else "P6 Baseline", type text)
in
    AddLabel'''
 cases=[]
 for i in range(1,7):
  k=f"W{i:02}";cases.append("{"+",".join(json.dumps(x) for x in (k,"Win","Selected historical case; exact dates, price levels, and individual P&L redacted.","Illustrative only; not representative of portfolio distribution.","Embedded anonymized image"))+"}")
 for i in range(1,3):
  k=f"L{i:02}";cases.append("{"+",".join(json.dumps(x) for x in (k,"Loss","Selected historical loss case; exact dates, price levels, and individual P&L redacted.","Illustrative only; not representative of portfolio distribution.","Embedded anonymized image"))+"}")
 case_query="#table(type table [CaseID=text, ResultType=text, PublicContext=text, PublicDisclosure=text, ImageUrl=text], {"+",".join(cases)+"})"
 validation='#table(type table [Stage=text, Status=text, PublicNote=text], {{"Paper Live","No prospective metrics included","Simulated trading is not real-money performance; no live-account results are presented."}})'
 templates={
 "FactMonthlyResults":([("Portfolio","string"),("YearMonth","string"),("NetPnL_BRL_C30","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00","sum"),("GrossPnL_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00","sum"),("TradeCount","int64","#,0","sum"),("WinningTrades","int64","#,0","sum"),("ContractUnits","int64","#,0","sum"),("MonthStart","dateTime","MMM yyyy")],monthly),
 "FactAnnualResults":([("Portfolio","string"),("Year","int64","0"),("NetPnL_BRL_C30","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00","sum"),("GrossPnL_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00","sum"),("TradeCount","int64","#,0","sum"),("WinningTrades","int64","#,0","sum"),("ContractUnits","int64","#,0","sum")],annual),
 "Benchmark":([("Portfolio","string"),("DataOrigin","string"),("PeriodStart","dateTime","Short Date"),("PeriodEnd","dateTime","Short Date"),("PortfolioRecords","int64","#,0"),("FinalContractUnits","int64","#,0"),("GrossPnL_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("C30NetPnL_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("RecordedCosts_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("WinRate","double","0.00%"),("ProfitFactor","double","0.000"),("RealizedCloseOrderMaxDD_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("M5CloseMaxDD_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("M5AdverseOHLCEnvelopeDD_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("LongestLosingStreak","int64","#,0")],bench),
 "DimDate":([("Date","dateTime","Short Date"),("MonthStart","dateTime","MMM yyyy"),("YearMonth","string"),("Year","int64","0"),("MonthNumber","int64","0"),("Month","string")],dimdate),
 "DimPortfolio":([("Portfolio","string"),("PortfolioLabel","string")],portfolio),
 "FactMonthlyRiskProxy":([("Portfolio","string"),("YearMonth","string"),("CumulativeMonthlyNetC30_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("MonthEndDrawdownProxy_BRL","double","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("MonthStart","dateTime","MMM yyyy")],risk),
 "FactCaseGallery":([("CaseID","string"),("ResultType","string"),("PublicContext","string"),("PublicDisclosure","string"),("ImageUrl","string")],case_query),
 "FactForwardValidation":([("Stage","string"),("Status","string"),("PublicNote","string")],validation),
 }
 for n,(cs,m) in templates.items():(td/f"{n}.tmdl").write_text(build_table(n,cs,m),encoding="utf-8")
 measures=[
 ("Gross P&L","SUM(FactMonthlyResults[GrossPnL_BRL])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Net C30","SUM(FactMonthlyResults[NetPnL_BRL_C30])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Operations","SUM(FactMonthlyResults[TradeCount])","#,0"),("Contract Units","SUM(FactMonthlyResults[ContractUnits])","#,0"),("Winning Operations","SUM(FactMonthlyResults[WinningTrades])","#,0"),("Losing Operations","[Operations] - [Winning Operations]","#,0"),("Win Rate","DIVIDE([Winning Operations],[Operations])","0.0%"),
 ("Profit Factor","CALCULATE(MAX(Benchmark[ProfitFactor]),REMOVEFILTERS(DimDate))","0.000"),("Cumulative Net C30","VAR Cutoff=MAX(DimDate[Date]) RETURN CALCULATE([Net C30],FILTER(ALLSELECTED(DimDate[Date]),DimDate[Date]<=Cutoff))","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Max Realized DD (Full History)","CALCULATE(MAX(Benchmark[RealizedCloseOrderMaxDD_BRL]),REMOVEFILTERS(DimDate))","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),
 ("PSC Gross P&L",'CALCULATE([Gross P&L],REMOVEFILTERS(DimPortfolio),FactMonthlyResults[Portfolio]="P6+SIZE+CE")',"R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("PSC Net C30",'CALCULATE([Net C30],REMOVEFILTERS(DimPortfolio),FactMonthlyResults[Portfolio]="P6+SIZE+CE")',"R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("PSC Operations",'CALCULATE([Operations],REMOVEFILTERS(DimPortfolio),FactMonthlyResults[Portfolio]="P6+SIZE+CE")',"#,0"),("PSC Win Rate",'CALCULATE(MAX(Benchmark[WinRate]),REMOVEFILTERS(DimPortfolio),Benchmark[Portfolio]="P6+SIZE+CE")',"0.0%"),("PSC Profit Factor",'CALCULATE(MAX(Benchmark[ProfitFactor]),REMOVEFILTERS(DimPortfolio),Benchmark[Portfolio]="P6+SIZE+CE")',"0.000"),("PSC Cumulative Net C30",'VAR Cutoff=MAX(DimDate[Date]) RETURN CALCULATE([PSC Net C30],FILTER(ALLSELECTED(DimDate[Date]),DimDate[Date]<=Cutoff))',"R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("PSC Max Realized DD (Full History)",'CALCULATE(MAX(Benchmark[RealizedCloseOrderMaxDD_BRL]),REMOVEFILTERS(DimDate),REMOVEFILTERS(DimPortfolio),Benchmark[Portfolio]="P6+SIZE+CE")',"R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),
 ("Longest Losing Streak","MAX(Benchmark[LongestLosingStreak])","#,0"),("Max M5 Close DD","MAX(Benchmark[M5CloseMaxDD_BRL])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Max M5 OHLC Envelope DD","MAX(Benchmark[M5AdverseOHLCEnvelopeDD_BRL])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Monthly Drawdown Proxy","MIN(FactMonthlyRiskProxy[MonthEndDrawdownProxy_BRL])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Cumulative Monthly Net C30","MAX(FactMonthlyRiskProxy[CumulativeMonthlyNetC30_BRL])","R$ #,##0.00;(R$ #,##0.00);R$ 0.00"),("Public Case Count","DISTINCTCOUNT(FactCaseGallery[CaseID])","#,0"),("Portfolio Records","MAX(Benchmark[PortfolioRecords])","#,0")]
 mc=[f"\tmeasure '{n}' = {d}\n\t\tformatString: {fmt}\n\t\tlineageTag: {gid()}" for n,d,fmt in measures]
 v=build_table("VortexMetrics",[("MetricSource","string")],'#table(type table [MetricSource=text], {{"Approved public aggregates"}})')
 # Measures are kept with a harmless one-row table partition.
 v=v.replace("\tpartition VortexMetrics = m", "\n".join(mc)+"\n\n\tpartition VortexMetrics = m")
 (td/"VortexMetrics.tmdl").write_text(v,encoding="utf-8")
 rel=[("Monthly_Date","FactMonthlyResults.MonthStart","DimDate.Date"),("Monthly_Portfolio","FactMonthlyResults.Portfolio","DimPortfolio.Portfolio"),("Annual_Portfolio","FactAnnualResults.Portfolio","DimPortfolio.Portfolio"),("Benchmark_Portfolio","Benchmark.Portfolio","DimPortfolio.Portfolio"),("RiskProxy_Date","FactMonthlyRiskProxy.MonthStart","DimDate.Date"),("RiskProxy_Portfolio","FactMonthlyRiskProxy.Portfolio","DimPortfolio.Portfolio")]
 (d/"relationships.tmdl").write_text("\n\n".join(f"relationship {n}\n\tfromColumn: {a}\n\ttoColumn: {b}" for n,a,b in rel)+"\n",encoding="utf-8")
 order=list(templates)+["VortexMetrics"]
 lines=["model Model","\tculture: en-US","\tdefaultPowerBIDataSourceVersion: powerBI_V3","\tsourceQueryCulture: en-US","\tdataAccessOptions","\t\tlegacyRedirects","\t\treturnErrorValuesAsNull","","annotation PBI_QueryOrder = "+json.dumps(order,separators=(",",":")),""]+[f"ref table {x}" for x in order]
 (d/"model.tmdl").write_text("\n".join(lines)+"\n",encoding="utf-8")
 (model/"diagramLayout.json").unlink(missing_ok=True)
 for name in ["FactTrades.tmdl","DimStrategy.tmdl","FactEquity.tmdl","FactRealizedEquity.tmdl","FactPaperLive.tmdl","FactForwardValidation_old.tmdl","DimCase.tmdl"]:
  (td/name).unlink(missing_ok=True)
 print(f"Generated public semantic model with {len(order)} tables and {len(measures)} measures.")
if __name__=="__main__":main()
