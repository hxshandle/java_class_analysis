from collections import namedtuple

from javalang import tree
import javalang

from lib.tree import JavaClassMeta

ParseContext = namedtuple("ParseContext", ["package", "compilationUnit"])
MethodContext = namedtuple("MethodContext", ["method", "local_variables"])


class Analyzer:
    parse_context_stack = []
    context = None
    klass_stack = []
    klass: tree.ClassDeclaration = None
    method_context = None
    deep = 0

    def __init__(self, file_path):
        self.root_java_file = file_path
        self.root_ast = javalang.parse.parse(open(file_path, 'r').read())

    def push_context(self, ctx: ParseContext):
        self.parse_context_stack.append(ctx)
        self.context = ctx

    def parse(self):
        """ process java file """
        for path, node in self.root_ast.filter(tree.CompilationUnit):
            self.push_context(ParseContext(node.package.name, node))
            self.parse_class()
            print(self.klass)

            print(self.klass.out_class_method_calls())
            for out_class, methods in self.klass.out_class_method_calls().items():
                self.deep += 1
                print("nest parse class {} with {} ".format(out_class, methods))

    def parse_class(self):
        for path, node in self.context.compilationUnit.filter(tree.ClassDeclaration):
            # only deal with sf code
            imports = dict(
                ((lambda p: p.split(".")[-1])(x.path), x.path) for x in self.context.compilationUnit.imports if
                x.path.startswith(("com.successfactors", "com.sf")))

            self.push_klass(JavaClassMeta(package=self.context.package, imports=imports, name=node.name, ast=node))
            self.parse_class_variable()
            self.parse_class_methods()

    def push_klass(self, klazz: JavaClassMeta):
        self.klass_stack.append(klazz)
        self.klass = klazz

    def parse_class_variable(self):
        variable_type_map = dict()
        for field in self.klass.ast.fields:
            for variable in field.declarators:
                variable_type_map[variable.name] = field.type.name
        self.klass["fields"] = variable_type_map

    def parse_class_methods(self):
        for path, node in self.klass.ast.filter(tree.MethodDeclaration):
            self.parse_method(path, node)

    def parse_method(self, path, node):
        # print("parse Method " + node.name, node.position)
        ## current method local variables
        local_variable_map = dict()
        for p, lv in node.filter(tree.LocalVariableDeclaration):
            for v in lv.declarators:
                local_variable_map[v.name] = lv.type.name
        self.method_context = MethodContext(node, local_variable_map)
        for statement in node.body:
            self.parse_out_call(path, statement)

    def parse_out_call(self, path, node: tree.Statement):
        for p, n in node.filter(tree.MethodInvocation):
            if not n.qualifier:
                continue
            # if is local variable call chain
            out_type = self.klass.imports.get(self.method_context.local_variables.get(n.qualifier))
            if out_type:
                self.push_out_call(out_type, n, path)

    def push_out_call(self, out_class, out_method_call, call_from):
        self.klass.out_calls.append((out_class, out_method_call, self.method_context.method))
