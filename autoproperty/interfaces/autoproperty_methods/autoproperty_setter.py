from typing import Any, Protocol, runtime_checkable

from autoproperty.interfaces.autoproperty_methods.autoproperty_base import IAutopropBase
from autoproperty.prop_settings import AutoPropAccessMod

@runtime_checkable
class IAutopropSetter(IAutopropBase, Protocol):
    
    __value_type__: Any
    
    def __init__(self,prop_name: str, varname: str, s_access_mod: AutoPropAccessMod, value_type: Any) -> None: ...
    
    def __call__(self, clsinst: object, value: Any) -> None: ...