from typing import Generic, TypeVar

from line_profiler import profile
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.prop_settings import AutoPropType
from numba import jit

T = TypeVar('T')

class AutopropGetter(Generic[T], AutopropBase):

    __slots__ = ('__auto_prop__', '__prop_attr_name__', '__method_type__', '__prop_name__')

    def __init__(self, prop_name: str,  attr_name: str, belong: IAutoProperty):
        super().__init__(prop_name, attr_name, belong, AutoPropType.Getter)
        return
   
    
    def __get__(self, instance, owner=None):
        return getattr(instance, self.__prop_attr_name__, None)
        
