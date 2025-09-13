from typing import Generic, TypeVar
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.prop_settings import AutoPropType


T = TypeVar('T')

class AutopropGetter(Generic[T], AutopropBase):

    def __init__(self, prop_name: str,  varname: str, belong: IAutoProperty):
        super().__init__(prop_name, varname, belong, AutoPropType.Getter)
        return

    def __call__(self) -> T|None:
        
        return getattr(self.__auto_prop__, self.__prop_attr_name__, None)

        
