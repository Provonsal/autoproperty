from typing import Any, Protocol

from utils.interfaces.autoproperty_methods.I_autoproperty_method import IAutoPropertyMethod
from utils.prop_settings import AutoPropAccessMod


class IAutoPropertyMethodSetter(IAutoPropertyMethod, Protocol):
    
    def __init__(self, varname: str, s_access_mod: AutoPropAccessMod) -> None: ...
    
    def __call__(self, clsinst: object, value: Any) -> None: ...