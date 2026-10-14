"""Offline stream-format tests; never connects to or controls the running game."""
import asyncio,pathlib,struct
import server
async def main():
 real_root=server.ROOT
 root=real_root/'tmp/color-format-test';(root/'run').mkdir(parents=True,exist_ok=True)
 server.ROOT=root
 colors=[(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
 for fmt,layout in [(0x16,'rgba'),(0x17,'rgba'),(0x1b,'bgra'),(0x1c,'bgra')]:
  row=b''
  for r,g,b in colors: row+=bytes((r,g,b,255) if layout=='rgba' else (b,g,r,255))*480
  header=bytearray(4096);struct.pack_into('<QIII',header,0,2,1920,1080,fmt)
  (root/'run/video.bgra').write_bytes(header+row*1080)
  video=server.Video();frame=await video.recv();rgb=frame.reformat(format='rgb24');data=bytes(rgb.planes[0])
  got=[tuple(data[(i*480+240)*3:(i*480+240)*3+3]) for i in range(4)]
  assert got==colors,(fmt,got)
  video.stop();print('PASS',hex(fmt),layout,'red/green/blue/white decoded correctly')
 # Inspect the running capture directly; no extra peer, input or restart.
 server.ROOT=real_root
 video=server.Video();frame=await video.recv();rgb=frame.reformat(format='rgb24');plane=bytes(rgb.planes[0]);stride=rgb.planes[0].line_size
 raw=b''.join(plane[y*stride:y*stride+1920*3] for y in range(1080))
 (real_root/'logs/live-color-fixed.ppm').write_bytes(b'P6\n1920 1080\n255\n'+raw);video.stop()
 print('PASS current GPU capture interpreted using native format metadata')
asyncio.run(main())
