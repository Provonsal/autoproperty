from functools import wraps
import inspect
from types import NoneType, UnionType
from typing import Any, Callable, Iterable, Mapping
from pydantic import validate_call

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
    def create_annotations(clsobj: object) -> bool:
        
        """
        Method gets annotation from class, and if not found or empty, creates annotation.

        :return bool: True if created, False if not.
        """

        all_annotations = inspect.get_annotations(clsobj.__class__)

        # Если аннотаций в классе вообще не прописано то создаем их
        if not len(all_annotations):
            setattr(clsobj, "__annotations__", {})
            return True
        return False

    @staticmethod
    def set_annotation_to_class(clsobj: object, annotation: type | UnionType, attribute_name: str) -> None:
        
        """
        The method sets an annotation to the attribute, if the annotation already exists and matches, it does nothing.

        :param object clsobj: Class instance to set the annotation
        :param type | UnionType annotation: Annotation to set in the class
        :param str attribute_name: Name of the attribute to change the annotation

        :raises AttributeError: If dunder method __annotations__ does not exist
        :raises AnnotationOverlap: If class already has different annotation for this attribute
        """
        
        try:
            # берем все существующие аннотации
            class_annotations: dict = inspect.get_annotations(clsobj.__class__)
            
            if not len(class_annotations):
                if not hasattr(clsobj, "__annotations__"):
                    raise AttributeError("Annotations not found", name="class_annotations", obj=class_annotations)
            else:
                if class_annotations.get(attribute_name) is None:
                    clsobj.__annotations__[attribute_name] = annotation
                elif class_annotations[attribute_name] == annotation:
                    return
                else:
                    raise AnnotationOverlapError()
        except KeyError:
            clsobj.__annotations__[attribute_name] = annotation

    @staticmethod
    def get_class_annotation(clsobj: object, field_name: str) -> type | UnionType:
       
        # Пытаемся взять все существующие аннотации класса
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
            # Taking annotations
            annotations = inspect.get_annotations(func)

            if len(annotations) > 0 and annotations.get(field_name) is not None:
                return annotations[field_name]
            else:
                raise AnnotationNotFoundError("No annotation detected")

    def __call__(self, func: AutopropBase):

        @wraps(func)
        def wrapper(cls, value):

            # Получаем аннотацию для проверки поля класса
            try:
                attr_annotation = self._get_param_annotation()
            except AnnotationNotFoundError:
                try:
                    attr_annotation = self.get_class_annotation(cls, self._field_name)
                except AnnotationNotFoundError:
                    attr_annotation = self.get_func_annotation(func, self._field_name)

            func.__call__.__annotations__["value"] = attr_annotation

            return validate_call(func.__call__)(cls, value)

        return wrapper
