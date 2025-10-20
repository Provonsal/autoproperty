from types import UnionType
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
from autoproperty.prop_settings import AutoPropType


T = TypeVar("T", covariant=True)

class IAutopropBase(Protocol):
    __auto_prop__: "IAutoProperty"
    __prop_attr_name__: str
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __init__(self, prop_name: str,  attr_name: str, belong: "IAutoProperty", prop_type: AutoPropType) -> None: ...
    
    def __call__(self, *args, **kwds) -> Any: ...
    
@runtime_checkable
class IAutopropGetter(IAutopropBase, Protocol):
    
    def __init__(self, prop_name: str, attr_name: str, belong: "IAutoProperty") -> None: ...
    
    def __call__(self,  cls: object, owner: None = None): ...
    
    def __get__(self, instance, owner=None) -> Any | None: ...
    
@runtime_checkable
class IAutopropSetter(IAutopropBase, Protocol):
    
    __value_type__: Any
    
    def __init__(self,prop_name: str, attr_name: str, value_type: Any, belong: "IAutoProperty") -> None: ...
    
    def __call__(self,  cls: object, value: Any): ...
    
    def __set__(self, cls: object, value: Any) -> None: ...
    
@runtime_checkable
class IAutoProperty(Generic[T], Protocol):

    __slots__ = ('annotation_type', 
                 'setter', 
                 'getter', 
                 '__doc__', 
                 '_field_name', 
                 'prop_name')

    annotation_type: type | UnionType | None
    setter: IAutopropSetter | None
    getter: IAutopropGetter | None
    _field_name: str | None
    prop_name: str | None