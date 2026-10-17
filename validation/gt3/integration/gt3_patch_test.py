#!/usr/bin/env python3
"""Synthetic ELF only: check patch mechanics without distributing game bytes."""
import contextlib,hashlib,importlib.util,io,pathlib,struct,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('gt3_triple',ROOT/'scripts/gt3_triple.py')
patch=importlib.util.module_from_spec(spec);spec.loader.exec_module(patch)
class PatchTests(unittest.TestCase):
 def invoke(self,source,out,manifest):
  args=sys.argv;sys.argv=['gt3_triple',str(source),str(out),'--manifest',str(manifest)]
  try:
   with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):patch.main()
  finally:sys.argv=args
 def test_synthetic_elf(self):
  base=0x170000;size=0x350000-base
  data=bytearray(84+size);data[:4]=b'\x7fELF';struct.pack_into('<I',data,28,52);struct.pack_into('<HH',data,42,32,1)
  struct.pack_into('<8I',data,52,1,84,base,base,size,size,5,4096)
  for address,expected,_,_ in patch.CHANGES:struct.pack_into('<I',data,84+address-base,expected)
  original_hash=patch.CORE_SHA256;patch.CORE_SHA256=hashlib.sha256(data).hexdigest()
  try:
   with tempfile.TemporaryDirectory() as d:
    source=pathlib.Path(d)/'synthetic.elf';out=pathlib.Path(d)/'patched.elf';manifest=pathlib.Path(d)/'manifest.json';source.write_bytes(data)
    self.invoke(source,out,manifest);self.assertEqual(source.read_bytes(),data)
    result=out.read_bytes()
    for address,_,value,_ in patch.CHANGES:self.assertEqual(struct.unpack_from('<I',result,84+address-base)[0],value)
    self.assertTrue(manifest.exists())
    with self.assertRaises(SystemExit):self.invoke(source,source,manifest)
    source.write_bytes(b'not the supported input')
    with self.assertRaises(SystemExit):self.invoke(source,out,manifest)
  finally:patch.CORE_SHA256=original_hash
if __name__=='__main__':unittest.main()
