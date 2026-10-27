import {readFile} from 'node:fs/promises';
export default async function handler(req,res){
 const symbol=String(req.query?.symbol||'AAPL');
 const {companies}=JSON.parse(await readFile(new URL('../public/companies.json',import.meta.url)));
 if(![...companies.map(c=>c.symbol),'OEF'].includes(symbol))return res.status(400).json({error:'Unknown symbol'});
 try{
 const response=await fetch(`https://query2.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?range=2y&interval=1d`,{headers:{'User-Agent':'Mozilla/5.0'},signal:AbortSignal.timeout(12000)});
 if(!response.ok)throw Error('Feed unavailable');
 const raw=(await response.json()).chart.result[0];
 const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York'}).format(new Date());
 const points=raw.timestamp.map((t,i)=>({date:new Date(t*1000).toISOString().slice(0,10),close:raw.indicators.quote[0].close[i]})).filter(p=>Number.isFinite(p.close)&&p.date<today);
 if(points.length<2)throw Error('No history');
 res.setHeader('Cache-Control','s-maxage=900, stale-while-revalidate=3600');
 return res.status(200).json({points,asOf:points.at(-1).date,currency:raw.meta.currency,source:'Yahoo Finance'});
 }catch{res.status(503).json({error:'Market feed unavailable. Saved snapshot remains available.'})}
}
