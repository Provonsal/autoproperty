import inspect
from types import FrameType, UnionType
from typing import Any, Callable, Generic, TypeVar, cast, get_type_hints

from line_profiler import profile

from autoproperty.autoproperty_methods.autoproperty_getter import AutopropGetter
from autoproperty.exceptions.Exceptions import AnnotationOverlapError
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.autoproperty_methods import AutopropSetter
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter


T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

class AutoProperty(Generic[T]):

    __slots__ = ('annotation_type', 
                 'setter', 'getter', 
                 'bound_class_qualname', 
                 'value', 
                 '__doc__', 
                 '_field_name', 
                 'prop_name')

    annotation_type: type | UnionType | None
    setter: IAutopropSetter | None
    getter: IAutopropGetter | None
    bound_class_qualname: str
    value: Any
    _field_name: str | None
    prop_name: str | None
    validate_fields: bool = True

    def __init__(
        self,
        func: Callable[..., Any] | None = None,
        annotation_type: type | UnionType | None = None,
    ):
        
        self.prop_name = None
        self.annotation_type = annotation_type
        self.setter = None
        self.getter = None
        self._field_name = None

        if func is not None:
            self._setup_from_func(func)

    def _setup_from_func(self, func: Callable[..., Any]):

        # Extracting function name and creating a 
        # name for field in the instance
        self.prop_name = func.__name__
        self._field_name = f"_{func.__name__}"

        # Checking if annotation type 
        # is not passed in arguments
        if self.annotation_type is None:
            try:
                # Extracting annotations
                hints = get_type_hints(func)
                
                # Caching annotation for return
                return_hint = hints.get('return')
                
                # If found then assigning annotation to field
                if return_hint is not None:
                    self.annotation_type = return_hint
            except Exception:
                pass

        # Starting setting up setter and getter
        self._setup_getter_setter()

    def _setup_getter(self, prop_name: str, field_name: str):
        
        """Method for creating getter of autoproperty"""
        
        # Creating getter
        self.getter = AutopropGetter[T](prop_name, field_name, self)

    def _setup_setter(self, prop_name, _field_name, annotation_type):
        
        """Method for creating setter of autoproperty"""
        
        # Creating setter
        setter = AutopropSetter(prop_name, _field_name, annotation_type, self)
        
        # If need to valdiate then wrapping setter with field validator 
        if self.validate_fields:
            setter_with_validator = FieldValidator(_field_name, annotation_type)(setter)
            self.setter = cast(AutopropSetter, setter_with_validator)
        else:
            # else just assigning setter
            self.setter = setter

    def _setup_getter_setter(self):
        
        """Method for setting up setter and getter of auto property."""
        
        # Checking if got name from the function and have created the field name
        if self.prop_name is not None and self._field_name is not None:

            self._setup_getter(self.prop_name, self._field_name)
            self._setup_setter(self.prop_name, self._field_name, self.annotation_type)
            
    
    def __set_name__(self, owner: type, name: str) -> None:
        
        """Method that calling after __init__ cause this class is also a descriptor."""
        
        # If didnt get name yet then assing new name from the owner's class field name
        if self.prop_name is None:
            self.prop_name = name
        
        # If didnt make field name then make it from the owner's class field name
        if self._field_name is None:
            self._field_name = f"_{name}" 

        if self.validate_fields:

            # Getting annotations from owner class
            hints = get_type_hints(owner)
            
            # If no annotation provided in parameters of decorator
            # then trying to get annotations from the owner class now
            if self.annotation_type is None:
                
                self.annotation_type = hints.get(name)
                
                if self.annotation_type is None:
                    raise TypeError("Annotation for validation are not provided.")    
                else:
                    self._setup_setter(self.prop_name, self._field_name, self.annotation_type)
                    return
                    
            # If annotation is provided after all then compare with existing in the
            # owner class and if they are different then raise an error
            elif self.annotation_type is not hints.get(name):
                raise AnnotationOverlapError("Type annotation is different")
            
        else:
            if self.setter is None and self.getter is None:
                self._setup_getter_setter()
            elif self.setter is None:
                self._setup_setter(self.prop_name, self._field_name, self.annotation_type)
            elif self.getter is None:
                self._setup_getter(self.prop_name, self._field_name)

    def __call__(
        self,
        func: Callable[..., Any]
        ) -> "AutoProperty[T]":
        
        self.__doc__ = func.__doc__
        self._setup_from_func(func)
        return self
    
    def __set__(self, instance, obj):
        if self.setter is None:
            raise RuntimeError(f"AutoProperty '{self.prop_name}' was not properly initialized.")
        self.setter.__set__(instance, obj)

    def __get__(self, instance, owner=None):
        
        try:
            return self.getter.__get__(instance, owner=owner) # type: ignore
        except AttributeError:

            # If instance is not exist then return class type
            if instance is None:
                return self #type: ignore
            else:
                raise RuntimeError(f"AutoProperty '{self.prop_name}' was not properly initialized.")
        