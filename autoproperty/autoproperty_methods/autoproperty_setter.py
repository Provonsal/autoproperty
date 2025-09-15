from typing import Any
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.interfaces.autoproperty_methods import IAutopropSetter
from autoproperty.prop_settings import AutoPropType


class AutopropSetter(AutopropBase):

    __slots__ = ('__auto_prop__', '__prop_attr_name__', '__method_type__', '__prop_name__', '__value_type__')

    def __init__(self, prop_name: str, attr_name: str, value_type: Any, belong: IAutoProperty):
        super().__init__(prop_name, attr_name, belong, AutoPropType.Setter)
        
        self.__value_type__ = value_type
        
    def __set__(self, cls, value):
        setattr(cls, self.__prop_attr_name__, value)