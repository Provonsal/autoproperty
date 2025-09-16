from functools import wraps
import inspect
from types import NoneType, UnionType
from typing import Any, Callable, Iterable
from pydantic import ConfigDict, validate_call

from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.exceptions.Exceptions import AnnotationNotFoundError, AnnotationOverlapError
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
        found_annotations: list,
    ) -> None:
        
        """
        :param str field_name: Name of the field in class annotation to look up.
        
        :param NoneType | UnionType | type | None annotation_type: Type for check typing.
        """

        self._field_name = field_name
        
        self._annotation_type = self._check_and_get_annotation(found_annotations)
        
    def _check_and_get_annotation(self, found_annotations: list):
        if self.all_equal(found_annotations):
            if len(found_annotations) > 0:
                return found_annotations[0]
            else:
                raise AnnotationNotFoundError("Annotation type is not provided")
        else:
            raise AnnotationOverlapError("Annotations are not the same")

    def all_equal(self, iterable: Iterable):
        iterator = iter(iterable)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(item == first for item in iterator)

    def __call__(self, func):

        
        # Tring to take annotation from any of three places
        # First trying to take from parameters
        attr_annotation = self._annotation_type

        # Adding found annotation to function's annotation
        func.__call__.__annotations__["value"] = attr_annotation

        # Decorating function by pydantic validator with parsing turned off
            
        decorated_func = validate_call(config=ConfigDict(strict=True))(func.__call__)
                

        # Calling and returning decorated function's data
        # return decorated_func(cls, value)

        #wrapper.__wrapped__ = func

        return decorated_func
