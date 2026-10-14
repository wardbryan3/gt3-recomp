#!/usr/bin/env python3
import subprocess, time, pathlib, json, sys, os
log=pathlib.Path(sys.argv[1]); samples=[]
with log.open('w') as out:
 p=subprocess.Popen(sys.argv[2:],stdout=out,stderr=subprocess.STDOUT)
 t=time.monotonic()
 while p.poll() is None:
  try:
   pid=p.pid
   # timeout is a supervisor, not the game. Sample its ps2run child.
   children=pathlib.Path(f'/proc/{p.pid}/task/{p.pid}/children').read_text().split()
   for child in children:
    if pathlib.Path(f'/proc/{child}/comm').read_text().strip()=='ps2run': pid=int(child); break
   stat=pathlib.Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()
   gpu=pathlib.Path('/sys/class/drm/card0/device')
   samples.append({'observed_pid':pid,'observed_comm':pathlib.Path(f'/proc/{pid}/comm').read_text().strip(),'t':time.monotonic()-t,'cpu_seconds':(int(stat[11])+int(stat[12]))/os.sysconf('SC_CLK_TCK'),'rss_bytes':int(stat[21])*os.sysconf('SC_PAGE_SIZE'),'gpu_percent':int((gpu/'gpu_busy_percent').read_text()),'vram_bytes':int((gpu/'mem_info_vram_used').read_text())})
  except (FileNotFoundError,ProcessLookupError): pass
  time.sleep(1)
 code=p.wait()
log.with_suffix('.load.json').write_text(json.dumps({'exit':code,'wall_seconds':time.monotonic()-t,'samples':samples},indent=2)+'\n')
sys.exit(code)
