# light_autoproperty.pxd

from typing import Any, Callable

ctypedef class light_autoproperty.LightAutoProperty:
    
    cdef object __doc__
    cdef object _field_name
    cdef object prop_name
    
    cpdef void __init__(self, func: Callable[..., Any])
    
   

    cpdef object __get__(self, object instance, object owner = None)

    cpdef void __set__(self, object instance, object obj)
    
    cpdef void __set_name__(self, object owner, str name)