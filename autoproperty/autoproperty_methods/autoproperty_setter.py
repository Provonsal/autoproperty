from typing import Any
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.interfaces.autoproperty_methods import IAutopropSetter
from autoproperty.prop_settings import AutoPropType


class AutopropSetter(AutopropBase, IAutopropSetter):

    def __init__(self, prop_name: str, varname: str, value_type: Any, belong: IAutoProperty):
        super().__init__(prop_name, varname, belong, AutoPropType.Setter)
        
        self.__value_type__ = value_type
        return

    def __call__(self, cls: object, value: Any):
        setattr(self.__auto_prop__, self.__prop_attr_name__, value)