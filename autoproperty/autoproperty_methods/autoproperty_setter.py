
from typing import Any
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods.autoproperty_setter import IAutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType


class AutopropSetter(AutopropBase):

    def __init__(self, prop_name: str, varname: str, s_access_mod: AutoPropAccessMod, value_type: Any):
        self.varname = varname
        self.s_access_mod = s_access_mod

        self.__auto_prop__ = True
        self.__prop_name__ = prop_name
        self.__prop_attr_name__ = varname
        self.__prop_access__ = s_access_mod
        self.__method_type__ = AutoPropType.Setter
        self.__value_type__ = value_type

    def __call__(self, clsinst: object, value: Any):
        setattr(clsinst, self.varname, value)