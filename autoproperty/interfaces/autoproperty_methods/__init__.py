

from types import UnionType
from typing import Any, Protocol, runtime_checkable
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType




class IAutopropBase(Protocol):
    __auto_prop__: "IAutoProperty"
    __prop_attr_name__: str
    __prop_access__: AutoPropAccessMod
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __call__(self, *args, **kwds) -> Any: ...
    
@runtime_checkable
class IAutopropGetter(IAutopropBase, Protocol):
    
    def __init__(self, prop_name: str, varname: str, g_access_mod: AutoPropAccessMod, belong: "IAutoProperty") -> None: ...
    
    def __call__(self, clsinst: object) -> object | None: ...
    
@runtime_checkable
class IAutopropSetter(IAutopropBase, Protocol):
    
    __value_type__: Any
    
    def __init__(self,prop_name: str, varname: str, s_access_mod: AutoPropAccessMod, value_type: Any, belong: "IAutoProperty") -> None: ...
    
    def __call__(self, clsinst: object, value: Any) -> None: ...
    
@runtime_checkable
class IAutoProperty(Protocol):
    annotationType: type | UnionType | None
    access_mod: AutoPropAccessMod
    g_access_mod: AutoPropAccessMod
    s_access_mod: AutoPropAccessMod
    docstr: str | None = None
    setter: IAutopropSetter
    getter: IAutopropGetter
    bound_class_qualname: str