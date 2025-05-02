
from typing import Any
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.interfaces.autoproperty_methods import IAutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType


class AutopropSetter(AutopropBase, IAutopropSetter):

    def __init__(self, prop_name: str, varname: str, s_access_mod: AutoPropAccessMod, value_type: Any, belong: IAutoProperty):
        super().__init__(prop_name, varname, s_access_mod, belong, AutoPropType.Setter)
        
        self.__value_type__ = value_type
        return

    def __call__(self, clsinst: object, value: Any):
        setattr(clsinst, self.__prop_attr_name__, value)