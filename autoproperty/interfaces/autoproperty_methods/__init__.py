

from types import UnionType
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType


T = TypeVar("T", covariant=True)

class IAutopropBase(Protocol):
    __auto_prop__: "IAutoProperty"
    __prop_attr_name__: str
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __call__(self, *args, **kwds) -> Any: ...
    
@runtime_checkable
class IAutopropGetter(IAutopropBase, Protocol):
    
    def __init__(self, prop_name: str, varname: str, belong: "IAutoProperty") -> None: ...
    
    def __call__(self, clsinst: object) -> object | None: ...
    
@runtime_checkable
class IAutopropSetter(IAutopropBase, Protocol):
    
    __value_type__: Any
    
    def __init__(self,prop_name: str, varname: str, value_type: Any, belong: "IAutoProperty") -> None: ...
    
    def __call__(self, clsinst: object, value: Any) -> None: ...
    
@runtime_checkable
class IAutoProperty(Generic[T], Protocol):
    annotationType: type | UnionType | None
    docstr: str | None = None
    setter: IAutopropSetter
    getter: IAutopropGetter
    bound_class_qualname: str