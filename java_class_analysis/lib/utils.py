import os
from pathlib import Path
import javalang

_cwd = Path.cwd()
_java_files = list()


def cwd():
    return _cwd


def _walk_to_root(path):
    print(_cwd)
    return _cwd


def workspace_root():
    return _walk_to_root(cwd())


def get_ast_for_java_file(path):
    """ Return AST tree for the given absolute for java class"""
    try:
        _c = open(path, 'r')
        s = _c.read()
        return javalang.parse.parse(s)
    except:
        return None


def init_workspace_files(root_workspace):
    all_java_files = dict()
    for root, dirs, files in os.walk(root_workspace):
        for f in files:
            if f.endswith(".java"):
                full_path = Path(root).joinpath(f)
                package = root.split("{0}java{0}".format(os.sep))[-1].replace(os.sep, ".") + "." + f.split(".")[0]
                s = all_java_files.get(package)
                if not s:
                    s = [full_path]
                    all_java_files[package] = s
                else:
                    s.append(full_path)
    return all_java_files
