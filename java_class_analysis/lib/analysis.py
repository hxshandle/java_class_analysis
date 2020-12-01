from typing import List

from javalang.tree import ClassDeclaration, InterfaceDeclaration, EnumDeclaration

from lib import utils
from lib.tree import JavaClassMeta, JavaFileMeta


def process_enum(clazz: EnumDeclaration, package=None) -> JavaClassMeta:
    return JavaClassMeta(name=clazz.name, package=package, type="Enum")


def process_interface(clazz: InterfaceDeclaration, package=None) -> JavaClassMeta:
    return JavaClassMeta(name=clazz.name, package=package, type="Interface")


def process_class(clazz: ClassDeclaration, package=None) -> JavaClassMeta:
    return JavaClassMeta(name=clazz.name, package=package, type="Class")


def _process(clazz_type, package):
    if isinstance(clazz_type, ClassDeclaration):
        return process_class(clazz_type, package)
    if isinstance(clazz_type, InterfaceDeclaration):
        return process_interface(clazz_type, package)
    if isinstance(clazz_type, EnumDeclaration):
        return process_enum(clazz_type, package)
    return None


def analysis(path) -> List[JavaFileMeta]:
    """ Absolute path for the given java class """
    ast = utils.get_ast_for_java_file(path)
    if not ast:
        return None
    package = ast.package.name
    return JavaFileMeta(path=path,
                        types=[_process(_t, package) for _t in ast.types])
