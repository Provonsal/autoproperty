from types import UnionType
from typing import Callable
from warnings import warn
from autoproperty.exceptions.Exceptions import AccessModNotRecognized
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.accesscontroller import PropMethodAccessController
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter
from autoproperty.autoproperty_methods import AutopropGetter, AutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod


class AutoProperty:
    
    annotationType: type | UnionType | None
    access_mod: AutoPropAccessMod
    g_access_mod: AutoPropAccessMod
    s_access_mod: AutoPropAccessMod
    docstr: str | None = None
    
    
    def __init__(
        self,
        annotationType: type | UnionType | None = None,
        access_mod: AutoPropAccessMod | int | str = AutoPropAccessMod.Private,
        g_access_mod: AutoPropAccessMod | int | str | None = None,
        s_access_mod: AutoPropAccessMod | int | str | None = None,
        docstr: str | None = None
    ):

        self._annotationType = annotationType
        self.docstr = docstr
        
        if isinstance(access_mod, AutoPropAccessMod):
            self.access_mod = access_mod
        elif isinstance(access_mod, int):
            self.access_mod = AutoPropAccessMod(access_mod)
        else:
            self.access_mod = AutoPropAccessMod(self.__parse_access_str_int(access_mod))
        
        default = self.access_mod
        
        if g_access_mod is None:
            self.g_access_mod = default
        elif isinstance(g_access_mod, AutoPropAccessMod):
            self.g_access_mod = g_access_mod
        elif isinstance(g_access_mod, int):
            self.g_access_mod = AutoPropAccessMod(g_access_mod)
        else:
            self.g_access_mod = AutoPropAccessMod(self.__parse_access_str_int(g_access_mod))
        
        if s_access_mod is None:
            self.s_access_mod = default
        elif isinstance(s_access_mod, AutoPropAccessMod):
            self.s_access_mod = s_access_mod
        elif isinstance(s_access_mod, int):
            self.s_access_mod = AutoPropAccessMod(s_access_mod)
        else:
            self.s_access_mod = AutoPropAccessMod(self.__parse_access_str_int(s_access_mod))

        if self.g_access_mod < self.access_mod:
            warn("Invalid getter access level. Getter level can't be higher than property's", SyntaxWarning)
            self.g_access_mod = default

        if self.s_access_mod < self.access_mod:
            warn("Invalid setter access level. Setter level can't be higher than property's", SyntaxWarning)
            self.s_access_mod = default

    def __parse_access_str_int(self, access: str):
        match access:
            case "public":
                return 0
            case "protected":
                return 1
            case "private":
                return 2
            case _:
                raise AccessModNotRecognized(access, (AutoPropAccessMod))

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
        
        prop_name = func.__name__
        
        tmp1: AutopropGetter = AutopropGetter(prop_name, varname, self.g_access_mod)
        tmp2: AutopropSetter = AutopropSetter(prop_name, varname, self.s_access_mod)

        self.getter: AutopropGetter = PropMethodAccessController(
            self.g_access_mod)(tmp1)
        self.setter: AutopropSetter = PropMethodAccessController(
            self.s_access_mod)(FieldValidator(varname, self._annotationType)(tmp2))

        return property(self.getter, self.setter, doc=self._get_docstring(func, self._annotationType))
