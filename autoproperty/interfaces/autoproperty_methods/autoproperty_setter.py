from typing import Any, Protocol

from autoproperty.interfaces.autoproperty_methods.autoproperty_base import IAutopropBase
from autoproperty.prop_settings import AutoPropAccessMod


class IAutopropSetter(IAutopropBase, Protocol):
    
    def __init__(self,prop_name: str, varname: str, s_access_mod: AutoPropAccessMod) -> None: ...
    
    def __call__(self, clsinst: object, value: Any) -> None: ...