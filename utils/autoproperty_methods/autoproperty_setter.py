
from utils.autoproperty_methods.autoproperty_base import AutoPropertyMethodBase
from utils.prop_settings import AutoPropAccessMod


class AutoPropSetterMethod(AutoPropertyMethodBase):

    def __init__(self, varname: str, s_access_mod):
        self.varname = varname
        self.s_access_mod = s_access_mod

        self.__auto_prop__ = True
        self.__prop_attr_name__ = varname
        self.__prop_access__ = s_access_mod
        self.__belongs__ = None

    def __call__(self, clsinst, value):
        self.__belongs__ = clsinst
        setattr(clsinst, self.varname, value)