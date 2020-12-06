import os
from collections import namedtuple
from typing import List

from javalang import tree
import javalang
from pathlib import Path

from lib.tree import JavaClassMeta
from lib.utils import init_workspace_files

ParseContext = namedtuple("ParseContext", ["package", "compilationUnit", "file_path"])
MethodContext = namedtuple("MethodContext", ["method", "local_variables"])
all_java_files = dict()
parse_marker = dict()


class Analyzer:
    root_ast = None
    root_workspace = Path.cwd()
    parse_context_stack = []
    context = None
    klass_stack = []
    klass: tree.ClassDeclaration = None
    method_context = None
    class_methods_filter = None
    deep = 0

    def log(self, msg):
        print("%s %s" % ('  ' * self.deep, msg))

    def __init__(self, workspace=Path.cwd(), max_deep=5):
        global all_java_files
        self.max_deep = max_deep
        self.root_workspace = Path(workspace) if isinstance(workspace, str) else workspace
        self.log("📂 [{}]".format(self.root_workspace))
        # init file list
        all_java_files = init_workspace_files(self.root_workspace)

    def set_workspace_path(self, path: str):
        self.root_workspace = Path(path)

    def push_context(self, ctx: ParseContext):
        self.log("⬇ push parse_context %s" % ctx.file_path)
        self.parse_context_stack.append(ctx)
        self.context = ctx

    def parse(self, java_class=None, methods=None) -> List[JavaClassMeta]:
        """ process java file
        :param java_class:
        :param methods: the methods filter
        :return:
        """
        ret = []
        self.class_methods_filter = methods
        if self.get_ast(java_class):
            for path, node in self.root_ast.filter(tree.CompilationUnit):
                self.deep += 1
                self.push_context(ParseContext(node.package.name, node, java_class))
                java_meta = self.parse_class()
                self.method_context = None
                self.push_klass(java_meta)
                self.parse_class_variable()
                self.parse_class_methods()
                ret.append(java_meta)
                self.parse_nest_out_call_classes()
                self.pop_context()
                self.pop_klass()
                self.deep -= 1
        return ret

    def parse_nest_out_call_classes(self):
        if self.deep < self.max_deep:
            for out_class, methods in self.klass.out_class_method_calls().items():

                o = self.parse(out_class, methods=methods)
                if len(o) > 0:
                    self.klass.children.extend(o)
                    self.log("nest parse class {} with {} ".format(out_class, methods))

    def pop_context(self):
        p = self.parse_context_stack.pop()
        self.log("⬆ pop context " + p.file_path)
        if len(self.parse_context_stack) > 0:
            self.context = self.parse_context_stack[-1]
        else:
            self.context = None

    def get_ast(self, java_class: str):
        paths = all_java_files.get(java_class)
        # TODO need deal with same package in different repos
        if not paths:
            return False
        if len(paths) > 1:
            self.log("🚨 Warning: Multi java files found")
        for p in paths:
            self.root_ast = javalang.parse.parse(open(p, 'r').read())
            self.log("🏴󠁩󠁤󠁪󠁷󠁿 %s" % java_class)
        return True

    def parse_class(self) -> JavaClassMeta:
        for path, node in self.context.compilationUnit.filter(tree.ClassDeclaration):
            # only deal with sf code
            imports = dict(
                ((lambda p: p.split(".")[-1])(x.path), x.path) for x in self.context.compilationUnit.imports if
                x.path.startswith(("com.successfactors", "com.sf")))
            java_meta = JavaClassMeta(package=self.context.package, imports=imports, name=node.name, ast=node)
            return java_meta

    def push_klass(self, klazz: JavaClassMeta):
        self.klass_stack.append(klazz)
        self.klass = klazz

    def pop_klass(self):
        self.klass_stack.pop()
        if len(self.parse_context_stack) > 0:
            self.klass = self.klass_stack[-1]
        else:
            self.klass = None

    def parse_class_variable(self):
        variable_type_map = dict()
        for field in self.klass.ast.fields:
            for variable in field.declarators:
                variable_type_map[variable.name] = field.type.name
        self.klass["fields"] = variable_type_map

    def parse_class_methods(self):
        for path, node in self.klass.ast.filter(tree.MethodDeclaration):
            if self.class_methods_filter is None or node.name in self.class_methods_filter:
                self.parse_method(path, node)

    def parse_method(self, path, node):
        # self.log("parse Method " + node.name, node.position)
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
