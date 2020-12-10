from typing import List

from .tree import JavaClassMeta

caches = dict()


def find_next_class(klass, target):
    for k in klass.children:
        if k.name == target or k.name == target + "Impl":
            return k
    return None


def build_sequence_dialgram(klass: JavaClassMeta, method=None):
    # group out calls by out_calls
    out_methods = dict()
    lines = list()
    for target, invoked_method, from_method in klass.out_calls:
        line, column = from_method.position
        key = "{}__{}__{}".format(from_method.name, line, column)
        m = out_methods.get(key)
        if not m:
            m = set()
            out_methods[key] = m
        m.add((target.split(".")[-1], target, invoked_method.member))
    for key, calls in out_methods.items():
        if method is not None and key.split('__')[0] != method:
            continue
        for x in calls:
            lines.append("{} -> {}: {}()".format(klass.name, x[0], x[2]))
            nest_klass = find_next_class(klass, x[0])
            if nest_klass is not None:
                j = build_sequence_dialgram(nest_klass, method=x[2])
                lines = lines + j
    return lines


def sequence_diagram(data: JavaClassMeta):
    _str = """
@startuml
actor %s
%s
@enduml
    """ % (data.name, '\n'.join(build_sequence_dialgram(data)))
    return _str


def build_mind_diagram(klass: JavaClassMeta, deep=1) -> List[str]:
    uml = list()
    uml.append("{} {}".format('*'*deep, klass.package+"."+klass.name))
    for child in klass.children:
        uml += build_mind_diagram(child, deep + 1)
    return uml


def mind_diagram(data: JavaClassMeta):
    _str = """
@startmindmap
%s
@endmindmap
    """ % "\n".join(build_mind_diagram(data))
    return _str
