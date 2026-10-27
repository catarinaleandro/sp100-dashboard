import concurrent.futures, urllib.request, json, pathlib, datetime, time, subprocess
from zoneinfo import ZoneInfo
root=pathlib.Path(__file__).resolve().parents[1]
companies=json.loads((root/'public/companies.json').read_text())['companies']
def fetch(symbol):
 for attempt in range(3):
  try:
   req=urllib.request.Request(f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range=2y&interval=1d',headers={'User-Agent':'Mozilla/5.0'})
   raw=json.loads(subprocess.check_output(['curl','-sS','--fail','--max-time','20','-A','Mozilla/5.0',req.full_url]))['chart']['result'][0]
   quotes=raw['indicators']['quote'][0]['close']
   points=[{'date':datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m-%d'),'close':round(v,4)} for t,v in zip(raw['timestamp'],quotes) if v is not None]
   today=datetime.datetime.now(ZoneInfo('America/New_York')).strftime('%Y-%m-%d')
   points=[p for p in points if p['date']<today]
   return symbol,{'points':points,'currency':raw['meta'].get('currency','USD'),'source':'Yahoo Finance','asOf':points[-1]['date']}
  except Exception as e:
   time.sleep(attempt+1)
 return symbol,{'error':'Price history unavailable'}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=dict(pool.map(fetch,[c['symbol'] for c in companies]+['OEF']))
(root/'public/snapshot.json').write_text(json.dumps({'fetchedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'series':results}))
print('Downloaded',sum('points' in v for v in results.values()),'of',len(results))
