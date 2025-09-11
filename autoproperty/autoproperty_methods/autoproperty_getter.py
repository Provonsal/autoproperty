
from typing import Any, Generic, TypeVar
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType


T = TypeVar('T')

class AutopropGetter(Generic[T], AutopropBase):

    def __init__(self, prop_name: str,  varname: str, belong: IAutoProperty):
        super().__init__(prop_name, varname, belong, AutoPropType.Getter)
        return

    def __call__(self, clsinst: object) -> T|None:
        return getattr(clsinst, self.__prop_attr_name__, None)
