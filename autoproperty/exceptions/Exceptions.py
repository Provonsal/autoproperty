from typing import Any, Iterable
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutopropBase
from autoproperty.prop_settings import AutoPropAccessMod


class UnaccessiblePropertyMethodError(Exception):
    def __init__(self, method: IAutopropBase):
        self.method_type = method.__method_type__.name
        self.msg = f"This autoproperty {method.__prop_name__} {self.method_type} method is not allowed in this scope"
        super().__init__(self.msg)


class AnnotationNotFoundError(Exception):
    ...


class AnnotationOverlapError(Exception):
    def __init__(self, msg="Annotation in class and in property are not the same"):
        super().__init__(msg)


class AccessModNotRecognizedError(Exception):
    def __init__(self, mod: AutoPropAccessMod | Any, expectations: Iterable[AutoPropAccessMod]):
        self.access_mod = mod.name if isinstance(mod, AutoPropAccessMod) else str(mod)
        self.msg = f"Access modificator is not recognized. Got: '{self.access_mod}'. Expected: {tuple(i.name for i in expectations)}"
        super().__init__(self.msg)
