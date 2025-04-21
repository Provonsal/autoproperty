from functools import wraps
from types import UnionType
from typing import Callable
from warnings import warn
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.accesscontroller import PropMethodAccessController
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter
from autoproperty.autoproperty_methods import AutopropGetter, AutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod


class AutoProperty:
    def __init__(
        self,
        annotationType: type | UnionType | None = None,
        access_mod=AutoPropAccessMod.Private,
        g_access_mod=None,
        s_access_mod=None,
        docstr: str | None = None
    ):

        self._annotationType = annotationType
        self.docstr = docstr
        self.access_mod = access_mod

        default = access_mod

        self.g_access_mod = default if g_access_mod is None else g_access_mod
        self.s_access_mod = default if s_access_mod is None else s_access_mod

        if self.g_access_mod < access_mod:
            warn("Invalid getter access level. Getter level can't be higher than property's", SyntaxWarning)
            self.g_access_mod = default

        if self.s_access_mod < access_mod:
            warn("Invalid setter access level. Setter level can't be higher than property's", SyntaxWarning)
            self.s_access_mod = default

    def _get_docstring(self, func: Callable, attr_type):

        try:
            assert self.docstr is not None
            return self.docstr
        except AssertionError:
            try:
                assert func.__doc__ is not None
                return func.__doc__
            except AssertionError:
                return f"Auto property. Name: {func.__name__}, type: {attr_type}, returns: {func.__annotations__.get('return')}"

    def __call__(self, func: Callable):
        
        varname = "__" + func.__name__[0].lower() + func.__name__[1:]

        tmp1: AutopropGetter = AutopropGetter(varname, self.g_access_mod)
        tmp2: AutopropSetter = AutopropSetter(varname, self.s_access_mod)

        self.getter: AutopropGetter = wraps(tmp1)(PropMethodAccessController(self.g_access_mod)(tmp1)) # type: ignore
        self.setter: AutopropSetter = wraps(tmp2)(PropMethodAccessController(self.s_access_mod)(FieldValidator(varname, self._annotationType)(tmp2))) # type: ignore

        return property(self.getter, self.setter, doc=self._get_docstring(func, self._annotationType))
