from typing import Protocol
from utils.interfaces.autoproperty_methods.I_autoproperty_method import IAutoPropertyMethod


class IAutoPropertyMethodGetter(IAutoPropertyMethod, Protocol):
    
    def __init__(self, varname: str, g_access_mod) -> None: ...
    
    def __call__(self, clsinst: object) -> None: ...