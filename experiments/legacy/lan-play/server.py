#!/usr/bin/env python3
"""Private LAN WebRTC video/audio + game-specific controls; no filesystem serving."""
import asyncio, fractions, json, logging, mmap, os, pathlib, secrets, signal, socket, struct, time
import av
from aiohttp import web
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription, RTCRtpSender, MediaStreamTrack, RTCBundlePolicy
from aiortc.codecs import vpx
from aiortc.mediastreams import MediaStreamError
import aioice.ice
# One LAN candidate and one BUNDLE transport: no broad UDP firewall allowance.
os.environ['GT3_ICE_PORT']='8766'
aioice.ice.get_host_addresses=lambda use_ipv4,use_ipv6: ['10.6.65.10'] if use_ipv4 else []

ROOT=pathlib.Path(__file__).resolve().parent
TOKEN_FILE=ROOT/'run/access-token'
if not TOKEN_FILE.exists(): TOKEN_FILE.write_text(secrets.token_urlsafe(24)); TOKEN_FILE.chmod(0o600)
TOKEN=TOKEN_FILE.read_text().strip()
vpx.DEFAULT_BITRATE=8_000_000; vpx.MAX_BITRATE=12_000_000; vpx.MIN_BITRATE=2_000_000; vpx.MAX_FRAME_RATE=60
WIDTH,HEIGHT=1920,1080
SIZE=4096+WIDTH*HEIGHT*4
neutral=0x808080800000
udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
pc=None; game=None; game_log=None; audio=None; video=None; last_input=0.; control_state=neutral
restart_lock=asyncio.Lock()

def send_input(value):
 global control_state
 control_state=value
 udp.sendto(struct.pack('<Q',value),('127.0.0.1',19876))

def auth(request):
 if not secrets.compare_digest(request.headers.get('Authorization',''), 'Bearer '+TOKEN): raise web.HTTPUnauthorized()

async def start_game():
 global game,game_log
 if game and game.returncode is None: return
 env=os.environ.copy()
 for k in ['PS2_ONE_THREAD','PS2_NO_VU_THREAD','PS2_WINDOW_BENCH','PS2_PRESENT_CSV','PS2_PRESENT_HOLD_MS','PS2_TIME']: env.pop(k,None)
 env.update(PS2_LAN_VIDEO=str(ROOT/'run/video.bgra'), PS2_PRESENT_MODE='fifo', PS2_SCRIPTED_INPUT='1')
 game_log=open(ROOT/'logs/game.log','ab',buffering=0)
 args=[str(ROOT/'repo/build/lan/ps2run'),'games/gt3-usa-v110/core-triple.elf','--disc','games/gt3-usa-v110/disc.iso',
       '--load-state',str(ROOT.parent/'validation/race-start.state'),'--ntsc','--gt3-triple','--render-scale','9',
       '--render-scale-y','3','--output-size','5760x1080','--fullscreen']
 game=await asyncio.create_subprocess_exec(*args,cwd=ROOT/'repo',env=env,stdout=game_log,stderr=game_log)
 for _ in range(150):
  if game.returncode is not None: raise RuntimeError('Native game exited; see game.log')
  p=ROOT/'run/video.bgra'
  if p.exists() and p.stat().st_size==SIZE:
   with p.open('rb') as f: seq=struct.unpack('<Q',f.read(8))[0]
   if seq>0 and not seq&1: return
  await asyncio.sleep(.1)
 raise RuntimeError('Video capture did not become ready')

async def stop_game():
 global game,game_log
 send_input(neutral)
 if game and game.returncode is None:
  game.terminate()
  try: await asyncio.wait_for(game.wait(),10)
  except asyncio.TimeoutError: game.kill(); await game.wait()
 game=None
 if game_log: game_log.close(); game_log=None

class Video(MediaStreamTrack):
 kind='video'
 def __init__(self):
  super().__init__(); self.file=open(ROOT/'run/video.bgra','rb'); self.mm=mmap.mmap(self.file.fileno(),SIZE,access=mmap.ACCESS_READ)
  self.seq=-1; self.epoch=time.monotonic(); self.next=self.epoch; self.count=0
 async def recv(self):
  while self.readyState=='live':
   now=time.monotonic()
   if now<self.next: await asyncio.sleep(self.next-now)
   if self.readyState!='live': raise MediaStreamError
   seq=struct.unpack_from('<Q',self.mm)[0]
   if not seq or seq&1 or seq==self.seq: await asyncio.sleep(.002); continue
   # Native metadata reports WebGPU format; never assume BGRA byte order.
   surface_format=struct.unpack_from('<I',self.mm,16)[0]
   pixel_format={0x16:'rgba',0x17:'rgba',0x1b:'bgra',0x1c:'bgra'}.get(surface_format)
   if pixel_format is None: await asyncio.sleep(.002); continue
   raw=self.mm[4096:]
   if struct.unpack_from('<Q',self.mm)[0]!=seq: await asyncio.sleep(.001); continue
   self.seq=seq; self.next+=1/60
   if self.next<time.monotonic()-.05: self.next=time.monotonic()
   frame=av.VideoFrame(WIDTH,HEIGHT,pixel_format); frame.planes[0].update(raw)
   frame.pts=int((time.monotonic()-self.epoch)*90000); frame.time_base=fractions.Fraction(1,90000)
   self.count+=1; return frame
  raise MediaStreamError
 def stop(self):
  if self.readyState=='live': self.mm.close(); self.file.close()
  super().stop()

class Audio(MediaStreamTrack):
 kind='audio'
 def __init__(self,process): super().__init__(); self.process=process; self.pts=0
 async def recv(self):
  raw=await self.process.stdout.readexactly(960*4)
  frame=av.AudioFrame(format='s16',layout='stereo',samples=960); frame.planes[0].update(raw)
  frame.sample_rate=48000; frame.pts=self.pts; frame.time_base=fractions.Fraction(1,48000); self.pts+=960
  return frame

async def close_peer():
 global pc,audio,video
 send_input(neutral)
 old=pc; pc=None
 if old: await old.close()
 if video: video.stop(); video=None
 if audio and audio.returncode is None:
  audio.terminate()
  try: await asyncio.wait_for(audio.wait(),3)
  except asyncio.TimeoutError: audio.kill(); await audio.wait()
 audio=None

async def index(request):
 return web.Response(text=(ROOT/'index.html').read_text(),content_type='text/html',headers={'Cache-Control':'no-store','Referrer-Policy':'no-referrer'})

async def offer(request):
 global pc,audio,video,last_input
 auth(request)
 params=await request.json()
 async with restart_lock:
  # A new authenticated connection takes over; never run two drivers at once.
  await close_peer(); await start_game()
  pc=RTCPeerConnection(RTCConfiguration(iceServers=[],bundlePolicy=RTCBundlePolicy.MAX_BUNDLE)); peer=pc
  @peer.on('datachannel')
  def on_channel(channel):
   @channel.on('message')
   def on_message(message):
    global last_input
    if pc is not peer or not isinstance(message,str) or len(message)>1024: return
    try:
     data=json.loads(message)
     mask=int(data.get('buttons',0))&0xffff
     axes=data.get('axes',[128]*4)
     if len(axes)!=4: return
     value=mask
     for i,x in enumerate(axes): value|=max(0,min(255,int(x)))<<(16+8*i)
     send_input(value); last_input=time.monotonic()
     if 'ping' in data and channel.readyState=='open': channel.send(json.dumps({'pong':data['ping']}))
    except (ValueError,TypeError,KeyError): pass
  @peer.on('connectionstatechange')
  async def state():
   logging.info('WebRTC %s',peer.connectionState)
   if peer.connectionState in ['failed','closed','disconnected'] and pc is peer: await close_peer()
  await peer.setRemoteDescription(RTCSessionDescription(sdp=params['sdp'],type=params['type']))
  video=Video(); peer.addTrack(video)
  audio_log=open(ROOT/'logs/audio-capture.log','ab',buffering=0)
  audio=await asyncio.create_subprocess_exec('ffmpeg','-hide_banner','-loglevel','warning','-f','pulse','-sample_rate','48000',
     '-channels','2','-fragment_size','3840','-i','gt3-null.monitor','-f','s16le','-ac','2','-ar','48000','pipe:1',
     stdout=asyncio.subprocess.PIPE,stderr=audio_log)
  audio_log.close(); peer.addTrack(Audio(audio))
  # VP8 avoids H.264 profile/level limits for 1080p60; modern Safari/Chrome support it.
  codecs=RTCRtpSender.getCapabilities('video').codecs
  preferred=[c for c in codecs if c.mimeType=='video/VP8']
  for t in peer.getTransceivers():
   if t.kind=='video': t.setCodecPreferences(preferred)
  await peer.setLocalDescription(await peer.createAnswer())
  last_input=time.monotonic()
  return web.json_response({'sdp':peer.localDescription.sdp,'type':peer.localDescription.type})

async def restart(request):
 auth(request)
 async with restart_lock:
  await stop_game(); await start_game()
 return web.json_response({'ok':True})

async def status(request):
 auth(request)
 return web.json_response({'game_running':bool(game and game.returncode is None),'connection':pc.connectionState if pc else None,
   'video_frames_sent':video.count if video else 0,'size':[WIDTH,HEIGHT],'view':'center of full 5760x1080 render',
   'path':'parallel + SSE4.1 + FIFO','audio':'private null-sink monitor, 48kHz stereo'})

async def watchdog():
 while True:
  if time.monotonic()-last_input>.35 and control_state!=neutral: send_input(neutral)
  await asyncio.sleep(.1)

async def startup(app):
 await start_game(); app['watchdog']=asyncio.create_task(watchdog())
async def cleanup(app):
 app['watchdog'].cancel(); await close_peer(); await stop_game(); udp.close()

if __name__=='__main__':
 logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
 app=web.Application(client_max_size=65536)
 app.router.add_get('/',index); app.router.add_post('/offer',offer); app.router.add_post('/restart',restart); app.router.add_get('/status',status)
 app.on_startup.append(startup); app.on_cleanup.append(cleanup)
 web.run_app(app,host='0.0.0.0',port=8765,access_log=None)
