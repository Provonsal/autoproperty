from typing import Any, TypeVar, Callable
import cython

T = TypeVar('T')

@cython.cclass
cdef class LightAutoProperty:
    

    # Объявляем атрибуты — они будут полями C-структуры
    cdef object __doc__
    cdef object _field_name
    cdef object prop_name

    def __init__(self, func: Callable[..., T] = ...):
        self.__doc__ = func.__doc__
        self.prop_name = func.__name__
        self._field_name = f"_{func.__name__}"
        
    def __set_name__(self, owner, name):
        if self.prop_name is None and self._field_name is None:
            self.prop_name = name
            self._field_name = f"_{name}"


    def __get__(self, instance, owner) -> T:
        
        if instance is None:
            return self

        # Оптимизация: используем PyObject_GetAttrString напрямую
        return getattr(instance, self._field_name, None)

    def __set__(self, instance, obj):
        # Оптимизация: используем PyObject_SetAttrString напрямую
        setattr(instance, self._field_name, obj)
