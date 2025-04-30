
from typing import Any, Generic, TypeVar
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.prop_settings import AutoPropType


T = TypeVar('T')

class AutopropGetter(Generic[T],AutopropBase):

    def __init__(self, prop_name: str,  varname: str, g_access_mod):
        super().__init__()
        self.varname = varname
        self.g_access_mod = g_access_mod

        self.__auto_prop__ = True
        self.__prop_name__ = prop_name
        self.__prop_attr_name__ = varname
        self.__prop_access__ = g_access_mod
        self.__method_type__ = AutoPropType.Getter

    def __call__(self, clsinst) -> T|None:
        return getattr(clsinst, self.varname, None)
