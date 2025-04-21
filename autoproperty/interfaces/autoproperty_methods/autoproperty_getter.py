from typing import Protocol
from autoproperty.interfaces.autoproperty_methods.autoproperty_base import IAutopropBase
from autoproperty.prop_settings import AutoPropAccessMod


class IAutopropGetter(IAutopropBase, Protocol):
    
    def __init__(self, varname: str, g_access_mod: AutoPropAccessMod) -> None: ...
    
    def __call__(self, clsinst: object) -> None: ...