#!/usr/bin/env python3
"""Conservative current-tree publication guard. Human/history review still required."""
import json,pathlib,re,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
FORBIDDEN_DIRS={'games','generated','tools','build','private','local','artifacts','captures','logs','profiles','venv','.venv','.pi','.rea','.local','.cache','node_modules','rea','pi','evidence'}
FORBIDDEN_EXTS={'.iso','.chd','.cso','.zip','.7z','.rar','.elf','.irx','.bin','.wasm','.a','.o','.obj','.so','.dylib','.dll','.exe','.ps2','.state','.sav','.dump','.ppm','.wav','.log','.mp4','.webp','.jsonl','.jdb2','.gpr','.idb','.i64','.bndb','.sqlite','.sqlite3'}
# These four generated documentation views contain public factual metadata only,
# not generated game translations. All content/extension/secret checks still apply.
PUBLIC_DOC_VIEWS={f'docusaurus/docs/reference/generated/{name}.md'
                  for name in ('current-products','status','symbols','types')}
def forbidden_directory(name):
 return bool(set(pathlib.PurePosixPath(name).parts)&FORBIDDEN_DIRS) and name not in PUBLIC_DOC_VIEWS
SECRET=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9_]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{30,})')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def main():
 errors=[]
 for record in git('ls-files','--stage','-z').split(b'\0'):
  if record and record.split(b'\t',1)[0].split()[-1]!=b'0':errors.append('unresolved merge in index')
 paths=git('ls-files','--cached','--others','--exclude-standard','-z').split(b'\0')
 for raw in sorted(set(paths)):
  if not raw:continue
  name=raw.decode();p=ROOT/name
  if not p.exists() and not p.is_symlink():continue # deleted inherited files
  reasons=[]
  if p.is_symlink():reasons.append('symlink: review rather than follow local data')
  if forbidden_directory(name):reasons.append('private/generated directory')
  if p.suffix.lower() in FORBIDDEN_EXTS:reasons.append('binary/game/media/build artifact extension')
  if p.name.startswith('.env') or p.name in {'access-token','auth.json','mcp-auth.json','trust.json'} or 'credentials' in p.name.lower():reasons.append('private configuration')
  if not p.is_symlink() and p.is_file():
   data=p.read_bytes()
   if data.startswith((b'\x7fELF',b'MZ',b'\x00asm',b'PK\x03\x04',b'!<arch>\n')):reasons.append('compiled/archive magic')
   if SECRET.search(data) or (b'-----BEGIN '+b'PRIVATE KEY-----') in data or (b'-----BEGIN '+b'OPENSSH PRIVATE KEY-----') in data:reasons.append('possible credential')
   if len(data)>2*1024*1024:reasons.append('unexpected large file: requires provenance review')
   # Public metadata may reference private records, never embed raw provider bodies.
   if p.suffix.lower()=='.json':
    try:
     def raw_export(value):
      if isinstance(value,dict):
       return bool(set(value)&{'pseudocode','assembly','disassembly','normalized_result','provider_result'}) or any(raw_export(v) for v in value.values())
      return isinstance(value,list) and any(raw_export(v) for v in value)
     if raw_export(json.loads(data)):reasons.append('raw analysis/provider export: keep private')
    except (ValueError,UnicodeError):reasons.append('invalid JSON: requires review')
  if reasons:errors.append(name+': '+', '.join(reasons))
 if errors:
  print('Publication audit FAILED (file names/reasons only; no secret contents):',file=sys.stderr)
  for e in errors:print(' - '+e,file=sys.stderr)
  return 1
 print('Current tracked/unignored tree audit PASS. This does not certify copyright provenance or all Git history.')
 return 0
if __name__=='__main__':sys.exit(main())
