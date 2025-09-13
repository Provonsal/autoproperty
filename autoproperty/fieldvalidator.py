from functools import wraps
import inspect
from types import NoneType, UnionType
from typing import Callable, Iterable
from pydantic import ConfigDict, validate_call

from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.exceptions.Exceptions import AnnotationNotFoundError
from autoproperty.interfaces.autoproperty_methods import IAutopropSetter


class FieldValidator:
    
    """
    This class's goal is to check type of accepted object.  
    
    This class is actually a class-decorator, no other using method accepted.  
    
    It scanning for type annotation inside given function's class,
    then inside given parameters from constructor,
    then inside function's first parameter after "self".  
    
    Otherwise throws "AnnotationNotFound"
    """
    
    def __init__(
        self,
        field_name: str,
        annotation_type: NoneType | UnionType | type | None = None
    ) -> None:
        
        """
        :param str field_name: Name of the field in class annotation to look up.
        
        :param NoneType | UnionType | type | None annotation_type: Type for check typing.
        """

        self._field_name = field_name if isinstance(field_name, Iterable) else (field_name)

        if isinstance(annotation_type, (NoneType, UnionType, type)):
            self._annotation_type = annotation_type
        else:
            raise TypeError("Annotation type is invalid")

    @staticmethod
    def get_class_annotation(clsobj: object, field_name: str) -> type | UnionType:
       
        # Taking annotations from class
        annotations = inspect.get_annotations(clsobj.__class__)
        
        if len(annotations) > 0 and annotations.get(field_name) is not None:
            return annotations[field_name]
        else:
            raise AnnotationNotFoundError("No annotation detected")
        
    def _get_param_annotation(self) -> type | UnionType:
        
        if self._annotation_type is not None:
            return self._annotation_type
        else:
            raise AnnotationNotFoundError("No annotation detected")

    @staticmethod
    def get_func_annotation(func: Callable, field_name: str):

        # Checking if the passed function is a setter for autoprop
        if isinstance(func, IAutopropSetter):
            
            # If value type is written in the field __value_type__ then returning it
            if func.__value_type__ is not None:
                return func.__value_type__
            else:
                # otherwise raising an error
                raise AnnotationNotFoundError("No annotation detected")
        else:
            # Taking annotations from callable
            annotations = inspect.get_annotations(func)

            # Checking if annotations are not None
            if len(annotations) > 0 and annotations.get(field_name) is not None:
                return annotations[field_name]
            else:
                # If annotation is empty throw an error
                raise AnnotationNotFoundError("No annotation detected")

    def __call__(self, func: AutopropBase):

        @wraps(func)
        def wrapper(cls, value):

            # Tring to take annotation from any of three places
            try:
                # First trying to take from parameters
                attr_annotation = self._get_param_annotation()
            except AnnotationNotFoundError:
                try:
                    # Second trying to take from class annotations
                    attr_annotation = self.get_class_annotation(cls, self._field_name)
                except AnnotationNotFoundError:
                    # Third tring to take from function's arguments annotations
                    attr_annotation = self.get_func_annotation(func, self._field_name)

            # Adding found annotation to function's annotation
            func.__call__.__annotations__["value"] = attr_annotation

            decorated_func = validate_call(config=ConfigDict(strict=True))(func.__call__)

            return decorated_func(cls, value)

        return wrapper
