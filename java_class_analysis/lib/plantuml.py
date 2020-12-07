from lib.tree import JavaClassMeta


def sequence_diagram(data: JavaClassMeta):
    # group out calls by out_calls
    out_methods = dict()
    for target, invoked_method, from_method in data.out_calls:
        line, column = from_method.position
        key = "{}__{}__{}".format(from_method.name, line, column)
        m = out_methods.get(key)
        if not m:
            m = set()
            out_methods[key] = m
        m.add((target.split(".")[-1], target, invoked_method.member))
    return "haha"

