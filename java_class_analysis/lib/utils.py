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

