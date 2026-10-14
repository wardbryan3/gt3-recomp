#!/usr/bin/env python3
"""Verified GT3 v1.10 triple-width adaptation, applied BEFORE recompilation.
Address leads: Silentwarior112, PCSX2-patches/Gran Turismo 3/USA PBPX-95503/8AA991B0.pnach.
Names below describe verified instructions or candidate data roles, not recovered original symbols.
Does not modify the ISO or input ELF. Refuses other executables.
"""
import argparse, hashlib, json, struct
from pathlib import Path
CORE_SHA256 = 'b6351d1c67a3ac1205d118c9041bfad88e2711235e67ca11d1056c4103cde763'
# (address, original word, replacement word, semantic name)
CHANGES = [
 (0x17e88c,0x10400007,0,'race_projection_skip_4_3_branch'),
 (0x17e89c,0x3c013f40,0x3c013e80,'race_projection_horizontal_scale_0_25'),
 (0x17e9ec,0x3c014348,0x3c014391,'mirror_rectangle_x_290'),
 (0x17ea04,0x3c014370,0x3c014270,'mirror_rectangle_width_60'),
 (0x193658,0x10600003,0,'hud_text_skip_4_3_branch'),
 (0x193660,0x3c013f40,0x3c013e80,'hud_text_horizontal_scale_0_25'),
 (0x18a950,0x3c013f40,0x3c013e80,'license_text_horizontal_scale_candidate'),
 (0x22a190,0x3c013f40,0x3c013e80,'license_model_horizontal_scale_candidate'),
 (0x21ed20,0x45010008,0x10000008,'visibility_branch_1_bypass'),
 (0x21f9ac,0x45010002,0x10000002,'visibility_branch_2_bypass'),
 (0x222278,0x4501000c,0x1000000c,'visibility_branch_3_bypass'),
 (0x224238,0x45010002,0x10000002,'visibility_branch_4_bypass'),
 (0x34fd04,0x3fb6d98c,0x3eb6d98c,'mirror_projection_scale'),
 (0x34fd74,0xc2d55556,0xc46e0000,'hud_canvas_left_minus_952'),
 (0x34fd78,0x443aaaaa,0x44c70000,'hud_canvas_right_1592'),
 (0x34ffc8,0xc2d4dd70,0xc46e0000,'pause_canvas_left_minus_952'),
 (0x34ffcc,0x443a9bae,0x44c70000,'pause_canvas_right_1592'),
]
def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--manifest',required=True);a=p.parse_args()
 source=Path(a.source);out=Path(a.output)
 if source.resolve()==out.resolve():p.error('output must differ from source')
 data=bytearray(source.read_bytes())
 if hashlib.sha256(data).hexdigest()!=CORE_SHA256:p.error('unsupported core ELF SHA-256')
 ph=struct.unpack_from('<I',data,28)[0];size,count=struct.unpack_from('<HH',data,42)
 def offset(address):
  for i in range(count):
   kind,off,va,_,length,*_=struct.unpack_from('<8I',data,ph+i*size)
   if kind==1 and va<=address and address+4<=va+length:return off+address-va
  raise ValueError(f'unmapped {address:x}')
 manifest=[]
 for address,expected,value,name in CHANGES:
  at=offset(address);actual=struct.unpack_from('<I',data,at)[0]
  if actual!=expected:raise ValueError(f'{name}: expected {expected:08x}, got {actual:08x}')
  struct.pack_into('<I',data,at,value)
  manifest.append(dict(address=f'{address:08x}',expected=f'{expected:08x}',value=f'{value:08x}',name=name))
 out.write_bytes(data);Path(a.manifest).write_text(json.dumps(dict(source_sha256=CORE_SHA256,output_sha256=hashlib.sha256(data).hexdigest(),aspect='16:3',patches=manifest),indent=2)+'\n')
 print(f'Applied {len(manifest)} verified changes to separate output ELF')
if __name__=='__main__':main()
