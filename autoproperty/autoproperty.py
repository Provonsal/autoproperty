import inspect
from types import FrameType, UnionType
from typing import Any, Callable, Generic, TypeVar, cast
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.autoproperty_methods import AutopropGetter, AutopropSetter
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

class AutoProperty(Generic[T]):

    annotationType: type | UnionType | None
    setter: IAutopropSetter
    getter: IAutopropGetter
    bound_class_qualname: str


    def __init__(
        self,
        func: Callable[..., Any] | None = None,
        annotationType: type | UnionType | None = None,
    ):
        
        self.annotationType = annotationType

        # Getting frame to get the qualname
        frame = inspect.currentframe()
        
        # Getting qualname
        self.bound_class_qualname = self.__get_class_qualname(frame)

        del frame

        if func is not None:
            # Creating name for a field that will be containing value
            self._varname = "__" + func.__name__[0].lower() + func.__name__[1:]

            # Setting a name for the property based on passed function 
            self._prop_name = func.__name__
            
            # Tring to take an annotation from passed function
            try:
                annotation = func.__annotations__.values().__iter__().__next__()
            except StopIteration:
                annotation = None

            # Creating setter and getter classes instances
            tmp1: AutopropGetter[T] = AutopropGetter[T](self._prop_name, self._varname, self)
            tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, annotation, self)

            # Assigning getter's and setter's fields with created instances before 
            self.getter = tmp1

            # Using FieldValidator decorator and casting it to AutopropSetter
            self.setter = cast(AutopropSetter, FieldValidator(self._varname, self.annotationType)(tmp2))
            #self.setter = tmp2
            

    def __get_class_qualname(self, frame: FrameType | None) -> str:

        try:

            # temp plugs
            if frame is None:
                raise Exception("Something unexpected happened! :(")
            if frame.f_back is None:
                raise Exception("Something unexpected happened! :(")
            if frame.f_back.f_back is None:
                raise Exception("Something unexpected happened! :(")
            
            # Falling back in frame 2 times
            locals = frame.f_back.f_back.f_locals

            # Getting the qualname and returning
            return cast(str, locals.get("__qualname__"))
        finally:
            # Deleting used frame
            del frame

    def __call__(
        self,
        func: Callable[..., Any]
        ) -> "AutoProperty[T]":
        
        self.__doc__ = func.__doc__

        # Creating name for a field that will be containing value
        self._varname = "__" + func.__name__[0].lower() + func.__name__[1:]

        self.__setattr__(self._varname, None)

        # Setting a name for the property based on passed function 
        self._prop_name = func.__name__

        # Tring to take an annotation from passed function
        try:
            # Getting next annotation from function annotations
            annotation = func.__annotations__.values().__iter__().__next__()
        except StopIteration:
            annotation = None
            
        # Creating setter and getter classes instances
        tmp1: AutopropGetter[T] = AutopropGetter[T](self._prop_name, self._varname, self)
        tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, annotation, self)

        # Assigning getter's and setter's fields with created instances before 
        self.getter = tmp1

        # Using FieldValidator decorator and casting it to AutopropSetter
        self.setter = cast(AutopropSetter, FieldValidator(self._varname, self.annotationType)(tmp2))
            
        return self

    
    def __set__(self, instance, obj):
        self.setter(instance, obj)

    def __get__(self, instance, owner=None):
        
        # If instance is not exist then return class type
        if instance is None:
            return self #type: ignore

        return self.getter()


