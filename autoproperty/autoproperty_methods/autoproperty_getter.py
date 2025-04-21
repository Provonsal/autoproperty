from warnings import warn

from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.prop_settings import AutoPropAccessMod


class AutopropGetter(AutopropBase):

    def __init__(self, varname: str, g_access_mod) -> None:
        super().__init__()
        self.varname = varname
        self.g_access_mod = g_access_mod

        self.__auto_prop__ = True
        self.__prop_attr_name__ = varname
        self.__prop_access__ = g_access_mod
        self.__belongs__ = None

    def __call__(self, clsinst: object) -> None:
        self.__belongs__ = clsinst
        
        try:
            return getattr(clsinst, self.varname)
        except:
            return None