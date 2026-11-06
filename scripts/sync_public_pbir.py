# The public report now carries corrections that are not in the private report. Rerunning this
# overwrites them; scripts/audit_report_semantics.py fails if that happens.
import argparse,hashlib,json,shutil,uuid
from pathlib import Path
CASES={"W01":"Case_01_Win.png","W02":"Case_02_Win.png","W03":"Case_03_Win.png","W04":"Case_04_Win.png","W05":"Case_05_Win.png","W06":"Case_06_Win.png","L01":"Case_07_Loss.png","L02":"Case_08_Loss.png"}
REPORT="ProjectVortex.Public.Report";MODEL="ProjectVortex.SemanticModel"
MN={"Gross P&L","Net C30","Operations","Contract Units","Winning Operations","Losing Operations","Win Rate","Profit Factor","Cumulative Net C30","Max Realized DD (Full History)","PSC Gross P&L","PSC Net C30","PSC Operations","PSC Win Rate","PSC Profit Factor","PSC Cumulative Net C30","PSC Max Realized DD (Full History)","Longest Losing Streak","Max M5 Close DD","Max M5 OHLC Envelope DD","Monthly Drawdown Proxy","Cumulative Monthly Net C30","Public Case Count","Portfolio Records"}
MM={f"FactTrades.{x}":f"VortexMetrics.{x}" for x in MN};MM.update({"FactTrades.Realized Underwater":"VortexMetrics.Monthly Drawdown Proxy","FactTrades.M5 Close Underwater":"VortexMetrics.Monthly Drawdown Proxy","FactCaseGallery.Case Set Net C30":"VortexMetrics.Public Case Count","FactCaseGallery.Case Set Gross P&L":"VortexMetrics.Public Case Count"})
CM={"FactTrades.CaseID":("FactCaseGallery","CaseID"),"FactTrades.Portfolio":("FactMonthlyResults","Portfolio"),"FactTrades.TradeDate":("FactMonthlyResults","YearMonth"),"FactTrades.Contracts":("FactMonthlyResults","ContractUnits"),"FactTrades.GrossPnL_BRL":("FactMonthlyResults","GrossPnL_BRL"),"FactTrades.NetPnL_BRL_C30":("FactMonthlyResults","NetPnL_BRL_C30"),"FactRealizedEquity.TradeDate":("DimDate","MonthStart"),"FactEquity.TimestampB3":("DimDate","MonthStart"),"FactCaseGallery.CaseID":("FactCaseGallery","CaseID"),"FactCaseGallery.TradeDate":("FactCaseGallery","ResultType"),"FactCaseGallery.Direction":("FactCaseGallery","PublicContext"),"FactCaseGallery.GrossPnL_BRL":("FactCaseGallery","PublicDisclosure"),"FactCaseGallery.NetPnL_BRL_C30":("FactCaseGallery","PublicDisclosure")}
def rd(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def texts(x):return[o["value"] for o in walk(x) if isinstance(o.get("value"),str)]
def tb(v,s,color="#DCE6F0",size="14pt"):
 v.clear();v.update({"visualType":"textbox","objects":{"general":[{"properties":{"paragraphs":[{"textRuns":[{"value":s,"textStyle":{"fontFamily":"Aptos","fontSize":size,"color":color}}],"horizontalTextAlignment":"left"}]}]},"visualContainerObjects":{"background":[{"properties":{"show":{"expr":{"Literal":{"Value":"'true'"}}},"color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#102236'"}}}}},"transparency":{"expr":{"Literal":{"Value":"'0'"}}}}}]},"drillFilterOtherVisuals":True})
def title(c,s):
 try:c["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"]="'"+s.replace("'","''")+"'"
 except (KeyError,IndexError,TypeError):pass
def refs(v):
 z=set()
 for x in walk(v.get("query",{})):
  f=x.get("field")
  if isinstance(f,dict):
   for k in ("Column","Measure","Aggregation"):
    a=f.get(k)
    if isinstance(a,dict):
     e=a.get("Expression",{}).get("SourceRef",{}).get("Entity");p=a.get("Property")
     if e and p:z.add(f"{e}.{p}")
 return z
def mp(obj):
 for x in walk(obj):
  f=x.get("field")
  if isinstance(f,dict):
   for k in ("Column","Measure","Aggregation"):
    a=f.get(k)
    if not isinstance(a,dict):continue
    e=a.get("Expression",{}).get("SourceRef",{}).get("Entity");p=a.get("Property");key=f"{e}.{p}"
    if k=="Measure" and key in MM:e,p=MM[key].split(".",1)
    elif k=="Column" and key in CM:e,p=CM[key]
    elif k=="Column" and e=="DimDate" and p=="Date":e,p="DimDate","MonthStart"
    else:continue
    a["Expression"]["SourceRef"]["Entity"]=e;a["Property"]=p
  if isinstance(x.get("SourceRef"),dict):
   e=x["SourceRef"].get("Entity");p=x.get("Property");key=f"{e}.{p}"
   if key in MM:e,p=MM[key].split(".",1)
   elif key in CM:e,p=CM[key]
   elif e=="DimDate" and p=="Date":e,p="DimDate","MonthStart"
   else:continue
   x["SourceRef"]["Entity"]=e;x["Property"]=p
  for k in ("queryRef","nativeQueryRef"):
   val=x.get(k)
   if isinstance(val,str):
    if val in MM:x[k]=MM[val]
    elif val in CM:x[k]=".".join(CM[val])
    elif val=="DimDate.Date":x[k]="DimDate.MonthStart"
def cols(c,fields):
 q=c["visual"]["query"]["queryState"];r="Columns" if "Columns" in q else next(iter(q));old=q[r]["projections"];t=old[0];a=[]
 for e,p in fields:
  z=json.loads(json.dumps(t));z["field"]={"Column":{"Expression":{"SourceRef":{"Entity":e}},"Property":p}};z["queryRef"]=f"{e}.{p}";z["nativeQueryRef"]=p;z.pop("active",None);a.append(z)
 q.clear();q[r]={"projections":a}
def main():
 a=argparse.ArgumentParser();a.add_argument("--private-report",type=Path,required=True);a.add_argument("--public-assets",type=Path,required=True);a.add_argument("--repo-root",type=Path,required=True);x=a.parse_args()
 s=x.private_report.resolve();assets=x.public_assets.resolve();repo=x.repo_root.resolve();root=repo/"PowerBI";out=root/REPORT
 if not (s/"definition/pages/pages.json").is_file() or not assets.is_dir():raise SystemExit("PBIR source or public images missing")
 if out.exists():shutil.rmtree(out)
 shutil.copytree(s/"definition",out/"definition")
 shutil.copy2(s/"definition.pbir",out/"definition.pbir")
 reg=out/"StaticResources/RegisteredResources";reg.mkdir(parents=True,exist_ok=True)
 theme=s/"StaticResources/RegisteredResources/Vortex_Navy.json"
 if not theme.exists():raise SystemExit("Theme source missing")
 shutil.copy2(theme,reg/theme.name);im={k:k+"_Embedded.png" for k in CASES}
 for k,f in CASES.items():shutil.copy2(assets/f,reg/im[k])
 rj=rd(out/"definition/report.json")
 for pkg in rj.get("resourcePackages",[]):
  if pkg.get("name")=="RegisteredResources":
   th=next((z for z in pkg.get("items",[]) if z.get("name")=="Vortex_Navy.json"),{"name":"Vortex_Navy.json","path":"Vortex_Navy.json","type":"CustomTheme"})
   pkg["items"]=[{"name":v,"path":v,"type":"Image"} for v in im.values()]+[th]
 for an in rj.get("annotations",[]):
  if an.get("name")=="evidence":an["value"]="Approved portfolio aggregates and anonymized embedded case exhibits only; no trade ledger or raw market data."
 wr(out/"definition/report.json",rj)
 pbir=rd(out/"definition.pbir");pbir["datasetReference"]["byPath"]["path"]="../"+MODEL;wr(out/"definition.pbir",pbir)
 (out/".platform").write_text(json.dumps({"$schema":"https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json","metadata":{"type":"Report","displayName":"Project Vortex Public Portfolio"},"config":{"version":"2.0","logicalId":str(uuid.uuid4())}},indent=2)+"\n",encoding="utf-8")
 manifest=rd(out/"definition/pages/pages.json")
 for pid in manifest["pageOrder"]:
  pd=out/"definition/pages"/pid;pn=rd(pd/"page.json").get("displayName","");case=next((k for k in CASES if k in pn),None)
  for vf in (pd/"visuals").glob("*/visual.json"):
   c=rd(vf);v=c.get("visual",{});vt=v.get("visualType","");rr=refs(v)
   if vt=="image" and (case or "FactCaseGallery.ImageUrl" in rr):
    k=case or "W01";resource=im[k]
    try:
     ii=v["objects"]["image"][0]["properties"]["sourceFile"]["image"];ii["name"]["expr"]["Literal"]["Value"]="'"+resource+"'";ii["url"]["expr"]["ResourcePackageItem"]["ItemName"]=resource
    except (KeyError,IndexError,TypeError):pass
    v.pop("query",None);title(c,"Anonymized historical case exhibit")
   if pn=="Autonomous Research Pipeline" and "DimStrategy.PublicLabel" in rr:tb(v,"Strategy-family attribution is not in the public aggregates.",color="#DCE6F0",size="12pt");title(c,"Public data boundary")
   if pn=="Executive Overview" and vt=="slicer" and ("FactTrades.Direction" in rr or "DimStrategy.PublicLabel" in rr):
    tb(v,"No public strategy-family split" if "DimStrategy.PublicLabel" in rr else "No public direction split",color="#DCE6F0",size="12pt");title(c,"Public data boundary")
   if pn=="Portfolio Performance" and "DimStrategy.PublicLabel" in rr:tb(v,"Strategy-family attribution is omitted; public results are by portfolio and period.",color="#DCE6F0",size="12pt");title(c,"Public data boundary")
   if pn=="Portfolio Performance" and vt=="tableEx" and "FactTrades.TradeDate" in rr:
    cols(c,[("DimPortfolio","PortfolioLabel"),("FactMonthlyResults","YearMonth"),("FactMonthlyResults","TradeCount"),("FactMonthlyResults","ContractUnits"),("FactMonthlyResults","GrossPnL_BRL"),("FactMonthlyResults","NetPnL_BRL_C30")]);title(c,"Verified monthly portfolio aggregates — not individual trades")
   if pn=="Risk & Drawdown":
    if "FactRealizedEquity.TradeDate" in rr:mp(c);title(c,"Month-end drawdown proxy from aggregate monthly C30 P&L")
    elif "FactEquity.TimestampB3" in rr:mp(c);title(c,"Monthly aggregate series — not an M5 mark-to-market path")
   if pn=="Trade Explorer":
    if vt=="tableEx" and "FactCaseGallery.CaseID" in rr:cols(c,[("FactCaseGallery","CaseID"),("FactCaseGallery","ResultType"),("FactCaseGallery","PublicContext")]);title(c,"Anonymized case index — no trade dates or individual results")
    elif vt=="card":mp(c);title(c,"Selected visual examples — not a performance sample")
   if pn=="Forward Validation & Governance" and vt=="tableEx":cols(c,[("FactForwardValidation","Stage"),("FactForwardValidation","Status"),("FactForwardValidation","PublicNote")]);title(c,"Public validation scope")
   tx=texts(v)
   if pn=="Forward Validation & Governance" and any("PROSPECTIVE SIMULATION" in t or "session registry" in t.lower() or "session folder" in t.lower() for t in tx):tb(v,"No session-level prospective metrics are included. Paper Live is simulated and separate from historical backtests and real-money trading. Any move toward live capital requires human approval.",color="#DCE6F0",size="12pt");title(c,"Validation status and governance")
   if pn=="Portfolio Performance" and any("family and period contributions" in t.lower() for t in tx):tb(v,"Compare the separate PSC and P6 baseline portfolios. Monthly and annual views use approved aggregates; strategy-family and trade-level attribution are not included.",color="#DCE6F0",size="12pt")
   if pn=="Risk & Drawdown" and any("REALIZED DD" in t for t in tx):tb(v,"Drawdown is the peak-to-trough decline. Cards show verified close-order, M5-close and adverse OHLC-envelope maximums. The line is a month-end aggregate proxy; it does not reconstruct trade-order or intrabar paths.",color="#DCE6F0",size="12pt")
   if pn=="Trade Explorer" and any("Featured image:" in t or "table lists eight" in t for t in tx):tb(v,"Eight anonymized cases appear on the case pages. Dates, exact prices and individual P&L are redacted; examples are illustrative, not a performance sample.",color="#DCE6F0",size="12pt")
   if case and vt=="textbox" and not any("Past performance" in t for t in tx):tb(v,f"{case} is a selected historical case. The embedded chart preserves anonymized candle structure; dates, price levels, and individual financial results are redacted. Selected examples are not representative of the full trade distribution.")
   if v.get("visualType")!="textbox":mp(c)
   else:
    _txt=" ".join(texts(v))
    if "Drawdown is the peak-to-trough decline" in _txt:c["position"]["height"]=120
    elif "No session-level prospective metrics" in _txt:c["position"]["height"]=140
    elif "Eight anonymized cases appear" in _txt:c["position"]["height"]=70
    elif "Strategy-family attribution" in _txt:c["position"]["height"]=80
   fc=c.get("filterConfig",{}).get("filters",[])
   if "filterConfig" in c:c["filterConfig"]["filters"]=[f for f in fc if not (f.get("field",{}).get("Column",{}).get("Expression",{}).get("SourceRef",{}).get("Entity")=="FactTrades" and f.get("field",{}).get("Column",{}).get("Property") in {"Direction","StrategyFamily","MFE_Points","MAE_Points"})]
   wr(vf,c)
 for f in reg.glob("*.png"):
  if f.name not in im.values():f.unlink()
 wr(root/"ProjectVortex-Public.pbip",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/pbip/1.0.0/schema.json","version":"1.0","artifacts":[{"report":{"path":REPORT}}],"settings":{"enableAutoRecovery":True}})
 files=sorted(p for p in s.rglob("*") if p.is_file() and "StaticResources" not in p.parts and ".pbi" not in p.parts)
 material="\n".join(f"{p.relative_to(s).as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}" for p in files).encode()
 h=hashlib.sha256(material).hexdigest()
 (repo/"docs").mkdir(exist_ok=True)
 (repo/"docs/source-parity.json").write_text(json.dumps({"sourceManifestSha256":h,"pageCount":len(manifest["pageOrder"]),"pageOrderAndIdsCopied":True,"publicDataScope":"approved aggregates plus anonymized chart exhibits","intentionalSubstitutions":["trade-level facts to monthly/annual/benchmark aggregates","M5 and trade-order paths to explicitly labeled month-end proxy","unsupported direction/strategy filters to disclosure text","case metadata to redacted labels and images","forward session details to qualitative scope"],"websiteRepository":"project-vortex-portfolio; public URL unavailable until repository publication"},indent=2)+"\n",encoding="utf-8")
 print(f"Copied PBIR structure: {len(manifest['pageOrder'])} pages; source manifest SHA256 {h}")
if __name__=="__main__":main()
