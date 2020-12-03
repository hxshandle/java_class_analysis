from typing import List

from javalang.tree import ClassDeclaration, InterfaceDeclaration, EnumDeclaration

from lib import utils
from lib.tree import JavaClassMeta, JavaFileMeta


def process_enum(clazz: EnumDeclaration, ast) -> JavaClassMeta:
    return JavaClassMeta(name=clazz.name, package=ast.package.name, type="Enum")


def process_interface(clazz: InterfaceDeclaration, ast) -> JavaClassMeta:
    return JavaClassMeta(name=clazz.name, package=ast.package.name, type="Interface")


def look_constructors(clazz):
    for c in clazz.constructors:
        for s in c.body:
            print(s)
        pass


def look_fields(clazz):
    pass


def process_class(clazz: ClassDeclaration, ast) -> JavaClassMeta:
    class_meta = JavaClassMeta(name=clazz.name, package=ast.package.name, type="Class")
    # fields
    for field in clazz.fields:
        # 1. constructors
        look_constructors(clazz)
        # 2. fields
        look_fields(clazz)
        # 3. methods
        look_fields(clazz)
        pass
    return class_meta


def _process(clazz_type, ast):
    """ process each class """
    if isinstance(clazz_type, ClassDeclaration):
        return process_class(clazz_type, ast)
    if isinstance(clazz_type, InterfaceDeclaration):
        return process_interface(clazz_type, ast)
    if isinstance(clazz_type, EnumDeclaration):
        return process_enum(clazz_type, ast)
    return None


def analysis(path) -> List[JavaFileMeta]:
    """ Absolute path for the given java class """
    ast = utils.get_ast_for_java_file(path)
    if not ast:
        return None
    result = JavaFileMeta(path=path,
                          types=[_process(_t, ast) for _t in ast.types], ast=ast)

    return result
