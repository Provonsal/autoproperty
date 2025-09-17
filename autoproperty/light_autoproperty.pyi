from typing import Any, Callable, TypeVar, Generic, overload, Self

T = TypeVar('T')

# It is not actually generic!!!
# just for correct type highlight, 
# do not place brackets like
# to generic one
class LightAutoProperty(Generic[T]):
    
    __slots__ = ( 
                 '__doc__', 
                 '_field_name', 
                 'prop_name',
                 'stored_value'
                )
    
    def __init__(self, func: Callable[[Any], T] = ...) -> None: ...
    def __set_name__(self, owner: type, name: str) -> None: ...
    
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type | None = ..., /) -> T: ...

    def __set__(self, instance: Any, obj: T, /) -> None: ...