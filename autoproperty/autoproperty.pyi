from types import UnionType
from typing import Any, Callable, Generic, Self, TypeVar, overload

from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter
from autoproperty.interfaces.events import IEvent, IListener


T = TypeVar('T')

# It is not actually generic!!!
# just for correct type highlight, 
# do not place brackets like
# to generic one
class AutoProperty(Generic[T]):

    __slots__ = ('annotation_type', 
                 'setter', 
                 'getter', 
                 '__doc__', 
                 '_field_name', 
                 'prop_name',
                 '_found_annotations',
                 'cache',
                 'operation_event')

    # fields annotation
    annotation_type: type | UnionType | None
    setter: IAutopropSetter | None
    getter: IAutopropGetter | None
    _field_name: str | None
    prop_name: str | None
    _found_annotations: list
    cache: bool
    operation_event: IEvent | None
    
    # static fields
    validate_fields: bool = True
    
    def __init__(
        self,
        func: Callable[..., T] | None = None,
        annotation_type: type | UnionType | None = None,
        cache: bool = False,
        events: bool = False
    ) -> None: ...
    
    def subscribe(self, listener: IListener): ...
    
    def _setup_from_func(
        self, 
        func: Callable[..., T]
    ) -> None: ...
    
    def _setup_getter(
        self, 
        prop_name: str, 
        field_name: str
    ) -> None: ...
    
    def _get_debug_cache_info(self) -> tuple: ...
    
    def _setup_setter(
        self, 
        prop_name: str, 
        _field_name: str, 
        annotation_type: type | None
    ) -> None: ...
    
    def _setup_getter_setter(
        self
    ) -> None: ...
    
    def __set_name__(
        self, 
        owner: type, 
        name: str
    ) -> None: ...
    
    def __call__(
        self,
        func: Callable[..., Any]
    ) -> Self: ...

    def __set__(
        self, 
        instance,
        obj
    ) -> None: ...
    
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type | None = ..., /) -> T: ...
