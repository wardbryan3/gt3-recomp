"""Explicit current/historical source versioning, never a permissive hash skip.
Old expectations stay unchanged; replaced source must have a separately pinned
historical artifact AND a current source hash in the new closure authority.
Private verifiers check the archived bytes; public checks need no private files.
"""
import hashlib
import json

def source_version(root,name,expected):
    actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
    path=root/'decomp/gt3/pedal-closure.json'
    if path.is_file():
        closure=json.loads(path.read_text())
        assert closure['id']=='pedal-v1-observed-context-closure'
        if name in closure['historical_sources']:
            assert closure['historical_sources'][name]['sha256']==expected,'Historical expectation changed'
            assert closure['source_hashes'][name]==actual,'Unvalidated current source change'
            assert closure['historical_sources'][name] in closure['artifacts'],'Missing historical source artifact'
            return
    assert actual==expected,'Source changed without explicit current/historical version authority'
