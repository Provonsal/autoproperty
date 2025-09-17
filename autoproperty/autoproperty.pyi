from types import UnionType
from typing import Any, Callable, Generic, Self, TypeVar, overload

from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter


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
                 '_found_annotations')

    annotation_type: type | UnionType | None
    setter: IAutopropSetter | None
    getter: IAutopropGetter | None
    bound_class_qualname: str
    _field_name: str | None
    prop_name: str | None
    validate_fields: bool = True
    _found_annotations: list
    
    def __init__(
        self,
        func: Callable[..., T] | None = None,
        annotation_type: type | UnionType | None = None,
    ) -> None: ...
    
    def _setup_from_func(
        self, 
        func: Callable[..., T]
    ) -> None: ...
    
    def _setup_getter(
        self, 
        prop_name: str, 
        field_name: str
    ) -> None: ...
    
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
