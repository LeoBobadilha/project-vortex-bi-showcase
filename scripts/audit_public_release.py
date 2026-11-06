from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
BINARY={'.png','.jpg','.jpeg','.gif','.webp','.ico','.pdf','.woff','.woff2','.ttf'}
def canonical(p):
 # Hash what Git stores: LF for text, exact bytes for binaries, on every operating system.
 raw=p.read_bytes()
 return raw if p.suffix.lower() in BINARY or b'\0' in raw else raw.replace(b'\r\n',b'\n')
files=sorted((p for p in ROOT.rglob('*') if p.is_file() and not {'.git','.pbi','__pycache__'}&set(p.parts) and p.name != 'security-review-manifest.json'),key=lambda p:p.relative_to(ROOT).as_posix())
rel=lambda p:p.relative_to(ROOT).as_posix()
forbidden_names={'HIST_LEGS.pkl','P6_BASELINE_LEDGER.csv','PSC_BASELINE_LEDGER.csv','FactTrades.csv','FactEquityDrawdown.csv','*.pbix','*.abf','*.parquet','*.sqlite','*.db'}
for p in files:
 if p.name in forbidden_names or p.suffix.lower() in {'.pkl','.pbix','.abf','.parquet','.sqlite','.db'}: errors.append(f'Forbidden file: {rel(p)}')
 text=None
 if p.suffix.lower() in {'.md','.txt','.json','.csv','.tmdl','.pbip','.pbir','.ps1','.py','.svg','.gitignore'}:
  try:text=p.read_text(encoding='utf-8-sig')
  except Exception as e:errors.append(f'Unreadable text {rel(p)}: {e}');continue
  for pattern in [r'(?i)C:\\Projects\\Project-robot-trader',r'(?i)D:\\Robot',r'(?i)file:///',r'(?i)ZZP_TRIANGLE',r'(?i)CATCH-LONG',r'(?i)H36AAH_RECT',r'(?i)AAF_DESC',r'(?i)account.?number',r'(?i)broker.?login',r'(?i)password\s*[:=]',r'(?i)api[_ -]?key\s*[:=]',r'(?i)secret\s*[:=]']:
   if p.name != 'audit_public_release.py' and re.search(pattern,text):errors.append(f'Sensitive or machine-specific text in {rel(p)}')
 if p.suffix.lower()=='.csv':
  with p.open(encoding='utf-8-sig',newline='') as f: headers=next(csv.reader(f),[])
  if {'TradeID','OpportunityID','EntryPrice','StopPrice','TargetPrice','ExitPrice','SignalTimeUTC','EntryTimeUTC','ExitTimeUTC'} & set(headers):errors.append(f'Trade-level field in public CSV: {rel(p)}')
# PBIP structure and parity
pbip=ROOT/'PowerBI/ProjectVortex-Public.pbip'
if not pbip.exists():errors.append('Missing ProjectVortex-Public.pbip')
else:
 b=pbip.read_bytes()
 if b.startswith(b'\xef\xbb\xbf'):errors.append('PBIP has UTF-8 BOM')
 manifest=json.loads((ROOT/'PowerBI/ProjectVortex.Public.Report/definition/pages/pages.json').read_text(encoding='utf-8-sig'))
 if len(manifest.get('pageOrder',[]))!=14:errors.append('Public PBIR does not contain 14 ordered pages')
 pages=list((ROOT/'PowerBI/ProjectVortex.Public.Report/definition/pages').glob('*/page.json'))
 if len(pages)!=14:errors.append(f'Expected 14 page definitions, found {len(pages)}')
 model_files=[p for p in (ROOT/'PowerBI/ProjectVortex.SemanticModel/definition/tables').glob('*.tmdl') if not p.name.startswith(('LocalDateTable_','DateTableTemplate_'))]
 if len(model_files)!=9:errors.append(f'Expected 9 model tables, found {len(model_files)}')
 if '__CONFIGURE_DATA_ROOT__/' not in (ROOT/'PowerBI/ProjectVortex.SemanticModel/definition/expressions.tmdl').read_text(encoding='utf-8-sig'):errors.append('DataRoot is not the clone-safe placeholder')
 case_images=list((ROOT/'PowerBI/ProjectVortex.Public.Report/StaticResources/RegisteredResources').glob('*_Embedded.png'))
 if len(case_images)!=8:errors.append(f'Expected eight embedded redacted case resources, found {len(case_images)}')
 report=json.loads((ROOT/'PowerBI/ProjectVortex.Public.Report/definition/report.json').read_text(encoding='utf-8-sig'))
 theme_name=report.get('themeCollection',{}).get('customTheme',{}).get('name')
 if not theme_name or not (ROOT/f'PowerBI/ProjectVortex.Public.Report/StaticResources/RegisteredResources/{theme_name}.json').exists():errors.append('Declared public PBIR custom theme resource is missing')
 public_screens=list((ROOT/'images/powerbi').glob('[0-9][0-9]-*.png'))
 complete_screens={'01-Knowledge.png','02-Research.png','03-Executive.png','04-Performance.png','05-Risk.png','06-Trade-Explorer.png','07-Validation.png','08-W02-Win.png','09-W03-Win.png','10-W04-Win.png','11-W05-Win.png','12-W06-Win.png','13-L01-Loss.png','14-L02-Loss.png'}
 actual_screens={p.name for p in public_screens}
 if actual_screens!=complete_screens:errors.append(f'Expected the complete 14-page screenshot set; found {sorted(actual_screens)}')
 forbidden_blob='a8eca13931878c6b686c30f3b4890e0398d977ce'
 for image in [p for p in (ROOT/'images/powerbi').glob('*.png')]:
  raw=image.read_bytes(); oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  if oid==forbidden_blob:errors.append(f'Known contaminated screenshot blob is present: {image.name}')
 visual_files=list((ROOT/'PowerBI/ProjectVortex.Public.Report/definition/pages').glob('*/visuals/*/visual.json'))
 if len(visual_files)!=83:errors.append(f'Expected 83 PBIR visual definitions, found {len(visual_files)}')
for required in ['README.md','SECURITY_REVIEW.md','PowerBI/README.md','docs/pbip-parity-report.md','docs/pbip-parity-report.json','docs/pbip-structure-baseline.json','data/benchmark_summary.csv','data/annual_portfolio_results.csv','data/monthly_portfolio_results.csv','data/monthly_drawdown_proxy.csv']:
 if not (ROOT/required).exists():errors.append('Missing '+required)
# Verify headline arithmetic from the approved benchmark row.
with (ROOT/'data/benchmark_summary.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
psc=next((r for r in rows if 'P6+SIZE+CE' in str(r)),None)
if psc is None:errors.append('PSC benchmark row not found')
else:
 values=' '.join(str(v) for v in psc.values())
 if '20395' not in values and '20,395' not in values:errors.append('PSC net C30 20,395 not found in benchmark aggregate')
 if '23551' not in values and '23,551' not in values:errors.append('PSC gross 23,551 not found in benchmark aggregate')
 if '3156' not in values and '3,156' not in values:errors.append('PSC C30 cost 3,156 not found in benchmark aggregate')
# manifest hashes every public file except its own self-referential manifest
payload={'reviewDate':'2026-11-06','scope':'local public BI working tree; PBIP/PBIR/TMDL; public aggregates; images; scripts; documentation','fileCount':len(files),'pageCount':14,'publicScreenshotCount':len(public_screens),'withheldScreenshotCount':14-len(public_screens),'galleryComplete':len(public_screens)==14,'errors':errors,'files':[{'path':rel(p),'size':len(canonical(p)),'sha256':hashlib.sha256(canonical(p)).hexdigest()} for p in sorted(files)]}
(ROOT/'security-review-manifest.json').write_bytes((json.dumps(payload,indent=2)+'\n').encode('utf-8'))
print(json.dumps({k:v for k,v in payload.items() if k!='files'},indent=2))
if errors:raise SystemExit(1)
