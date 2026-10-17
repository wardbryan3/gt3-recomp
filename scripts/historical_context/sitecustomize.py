"""Source-only historical verification view, enabled ONLY by run_historical.py.

No runtime hook, generated-code substitution, artifact remapping or copied checkout.
Public source reads/imports resolve from one explicit Git revision. Private paths,
executables, fixture bytes and their original immutable expectations are untouched.
"""
import importlib.machinery
import importlib.abc
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys

CONTEXT_READY = None

if os.environ.get("GT3_HISTORY_ROOT") and os.environ.get("GT3_HISTORY_REVISION"):
    root = Path(os.environ["GT3_HISTORY_ROOT"]).resolve()
    revision = os.environ["GT3_HISTORY_REVISION"]
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise RuntimeError("historical source view requires a full immutable Git revision")
    names = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "-z", revision], cwd=root
    ).decode().split("\0")
    allowed = {name for name in names if name and not name.startswith(("local/", "build/"))}
    original_open = Path.open
    original_is_file = Path.is_file
    original_get_code = importlib.machinery.SourceFileLoader.get_code
    cache = {}

    def logical(path):
        try:
            name = str(Path(path).absolute().relative_to(root))
        except ValueError:
            return None
        return name if name in allowed else None

    def source(name):
        if name not in cache:
            cache[name] = subprocess.check_output(
                ["git", "show", revision + ":" + name], cwd=root
            )
        return cache[name]

    def historical_open(self, mode="r", buffering=-1, encoding=None, errors=None,
                        newline=None):
        name = logical(self)
        if name is None:
            return original_open(self, mode, buffering, encoding, errors, newline)
        if mode not in ("r", "rb", "rt"):
            raise PermissionError("historical public source is read-only: " + name)
        data = source(name)
        if "b" in mode:
            return io.BytesIO(data)
        return io.TextIOWrapper(io.BytesIO(data), encoding=encoding or "utf-8",
                                errors=errors, newline=newline)

    def historical_is_file(self):
        return True if logical(self) is not None else original_is_file(self)

    def historical_get_code(self, fullname):
        name = logical(self.path)
        if name is not None and name.endswith(".py"):
            return compile(source(name), str(root / name), "exec", dont_inherit=True)
        return original_get_code(self, fullname)

    class HistoricalImports(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            leaf = fullname.rsplit('.', 1)[-1] + '.py'
            for directory in (path if path is not None else sys.path):
                candidate = Path(directory or os.getcwd()) / leaf
                name = logical(candidate)
                if name is not None:
                    loader = importlib.machinery.SourceFileLoader(fullname, str(candidate))
                    return importlib.util.spec_from_loader(fullname, loader)
            return None

    sys.meta_path.insert(0, HistoricalImports())
    Path.open = historical_open
    Path.is_file = historical_is_file
    importlib.machinery.SourceFileLoader.get_code = historical_get_code
    sys.dont_write_bytecode = True
    CONTEXT_READY = (str(root), revision)
