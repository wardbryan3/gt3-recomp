#!/usr/bin/env python3
import pathlib,csv,json,statistics,re
root=pathlib.Path(__file__).resolve().parent
results={}
def pct(a,p):
 a=sorted(a); return a[min(len(a)-1,int((len(a)-1)*p))] if a else None
for path in sorted((root/'results').glob('*.csv')):
 rows=list(csv.DictReader(path.open()))
 # Skip 300 warmup requests and final sentinel; fixed window-presentation data only.
 log=path.with_suffix('.log').read_text()
 sentinel=1 if 'drain=1' in log and 'fence_only=1' not in log else 0
 sample=rows[300:len(rows)-sentinel if sentinel else len(rows)]
 if len(sample)<2: continue
 req=[int(r['begin_ns']) for r in sample]
 presented=[r for r in sample if r['status']=='1']
 t=[int(r['displayed_ns']) for r in presented]
 gaps=[(b-a)/1e6 for a,b in zip(t,t[1:])]
 unique=sorted(set(t))
 ug=[(b-a)/1e6 for a,b in zip(unique,unique[1:])]
 ri=[(b-a)/1e6 for a,b in zip(req,req[1:])]
 call=[(int(r['end_ns'])-int(r['begin_ns']))/1e6 for r in sample]
 load=json.loads(path.with_suffix('.load.json').read_text())
 s=[x for x in load['samples'] if x['t']>5]
 valid_cpu=[x for x in s if x.get('observed_comm')=='ps2run']
 cpu=[(b['cpu_seconds']-a['cpu_seconds'])/(b['t']-a['t'])*100 for a,b in zip(valid_cpu,valid_cpu[1:])]
 audio=path.with_suffix('.audio-top.txt').read_text()
 err={}
 for line in audio.splitlines():
  f=line.split()
  if len(f)>9 and f[0] in ['R','S','I','C','E'] and f[1].isdigit():
   try:
    n=f[-1]; err[n]=max(err.get(n,0),int(f[8]))
   except ValueError:pass
 d={'requests':len(sample),'presented':len(presented),'discarded':sum(r['status']=='2' for r in sample),'missing':sum(r['status']=='0' for r in sample),'surface_failures':sum(r['status']=='3' for r in sample),'request_fps':(len(req)-1)*1e9/(req[-1]-req[0]),'feedback_callback_fps':(len(t)-1)*1e9/(t[-1]-t[0]) if len(t)>1 else None,'displayed_fps':(len(unique)-1)*1e9/(unique[-1]-unique[0]) if len(unique)>1 else None,'distinct_feedback_timestamp_hz':(len(unique)-1)*1e9/(unique[-1]-unique[0]) if len(unique)>1 else None,'duplicate_feedback_timestamps':len(t)-len(unique),'unique_feedback_timestamps':len(unique),'display_gaps_ms':{'p50':pct(ug,.5),'p95':pct(ug,.95),'p99':pct(ug,.99),'max':max(ug) if ug else None,'over_25ms':sum(x>25 for x in ug)},'request_gaps_ms':{'p50':pct(ri,.5),'p95':pct(ri,.95),'p99':pct(ri,.99),'max':max(ri)},'surface_cpu_ms':{'p50':pct(call,.5),'p99':pct(call,.99),'max':max(call)},'drawable_sizes':sorted(set((int(r['width']),int(r['height'])) for r in sample)),'audio_queued_ms':{'min':min(int(r['audio_queued_bytes'])/192 for r in sample),'max':max(int(r['audio_queued_bytes'])/192 for r in sample)},'cpu_mean_percent':statistics.mean(cpu) if cpu else None,'gpu_device_mean_percent':statistics.mean(x['gpu_percent'] for x in s) if s else None,'pipewire_error_max':err,'exit':load['exit'],'audio_summary':next((l for l in log.splitlines() if l.startswith('[probe-audio]')),''),'shutdown':next((l for l in log.splitlines() if l.startswith('[shutdown]')),'single-thread return')}
 results[path.stem]=d
 print(path.stem, 'request %.3f fps'%d['request_fps'], 'unique virtual feedback %.3f Hz'%d['distinct_feedback_timestamp_hz'], 'discarded',d['discarded'],'gaps',d['display_gaps_ms'],'PWERR',err)
(root/'results/summary.json').write_text(json.dumps(results,indent=2)+'\n')
