class MetaNode(type):
    def __new__(mcs, name, bases, dict):
        attrs = list(dict['attrs'])
        dict['attrs'] = list()

        for base in bases:
            if hasattr(base, 'attrs'):
                dict['attrs'].extend(base.attrs)

        dict['attrs'].extend(attrs)

        return type.__new__(mcs, name, bases, dict)


class Node(object, metaclass=MetaNode):
    attrs = ()

    def __init__(self, **kwargs):
        values = kwargs.copy()

        for attr_name in self.attrs:
            value = values.pop(attr_name, None)
            setattr(self, attr_name, value)

        if values:
            raise ValueError('Extraneous arguments')

    def __repr__(self):
        attr_values = []
        for attr in sorted(self.attrs):
            attr_values.append('%s=%s' % (attr, getattr(self, attr)))
        return '%s(%s)' % (type(self).__name__, ', '.join(attr_values))

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class NamedNode(Node):
    attrs = ("name", "children")


class JavaFileMeta(Node):
    attrs = ("path", "types", "ast")


class JavaClassMeta(NamedNode):
    attrs = ("package", "imports", "ast", "repo")
    # out call ast details from source code

    def __init__(self, **kwargs):
        super(JavaClassMeta, self).__init__(**kwargs)
        self.out_calls = list()
        self.children = list()

    def out_class_method_calls(self):
        """ grouped out method calls """
        _out_calls = dict()
        for out_class, out_method, call_from in self.out_calls:
            _out_class_methods = _out_calls.get(out_class)
            if not _out_class_methods:
                _out_class_methods = list()
                _out_calls[out_class] = _out_class_methods
            if out_method.member not in _out_class_methods:
                _out_class_methods.append(out_method.member)
        return _out_calls
