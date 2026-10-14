import asyncio,json,pathlib,time,struct
import aiohttp
from aiortc import RTCPeerConnection,RTCConfiguration,RTCSessionDescription
ROOT=pathlib.Path(__file__).resolve().parent
async def main():
 token=(ROOT/'run/access-token').read_text().strip();headers={'Authorization':'Bearer '+token}
 pc=RTCPeerConnection(RTCConfiguration(iceServers=[]));counts={'video':0,'audio':0};info={};tasks=[]
 async def consume(track):
  try:
   while True:
    frame=await track.recv();counts[track.kind]+=1
    if track.kind=='video':
     info['video_size']=[frame.width,frame.height]
     if counts['video']==120:
      rgb=frame.reformat(format='rgb24');plane=bytes(rgb.planes[0]);stride=rgb.planes[0].line_size
      raw=b''.join(plane[y*stride:y*stride+frame.width*3] for y in range(frame.height))
      (ROOT/'logs/loopback-frame.ppm').write_bytes(f'P6\n{frame.width} {frame.height}\n255\n'.encode()+raw)
    else:
     raw=bytes(frame.planes[0]); x=struct.unpack('<'+'h'*(len(raw)//2),raw); info['audio_peak']=max(info.get('audio_peak',0),max(abs(v) for v in x))
  except Exception: pass
 @pc.on('track')
 def on_track(track): tasks.append(asyncio.create_task(consume(track)))
 pc.addTransceiver('video',direction='recvonly');pc.addTransceiver('audio',direction='recvonly')
 channel=pc.createDataChannel('input',ordered=False,maxRetransmits=0)
 await pc.setLocalDescription(await pc.createOffer())
 async with aiohttp.ClientSession() as http:
  r=await http.post('http://10.6.65.10:8765/offer',headers=headers,json={'sdp':pc.localDescription.sdp,'type':pc.localDescription.type});answer=await r.json()
  await pc.setRemoteDescription(RTCSessionDescription(**answer))
  for _ in range(200):
   if pc.connectionState=='connected' and channel.readyState=='open': break
   await asyncio.sleep(.05)
  start=time.monotonic()
  for i in range(360):
   buttons=(1<<14) if 60<=i<240 else 0
   if 250<=i<256: buttons|=1<<11
   channel.send(json.dumps({'buttons':buttons,'axes':[128]*4}));await asyncio.sleep(1/60)
  info.update(counts=counts,seconds=time.monotonic()-start,connection=pc.connectionState)
  await pc.close()
  for t in tasks:t.cancel()
  await asyncio.sleep(.5)
  r=await http.post('http://10.6.65.10:8765/restart',headers=headers,json={});info['restart_status']=r.status
  r=await http.post('http://10.6.65.10:8765/offer',json={});info['unauthorized_status']=r.status
  r=await http.get('http://10.6.65.10:8765/repo/games/gt3-usa-v110/disc.iso');info['asset_route_status']=r.status
  (ROOT/'logs/loopback-result.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
asyncio.run(main())
