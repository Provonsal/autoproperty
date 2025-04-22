from functools import wraps
from types import NoneType, UnionType
from typing import Any, Callable, Iterable, Mapping

from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.exceptions.Exceptions import AnnotationNotFound
from autoproperty.interfaces.autoproperty_methods.autoproperty_base import IAutopropBase


class FieldValidator:
    def __init__(
        self, 
        fieldName: str, 
        annotationType: type | UnionType | None = None
    ) -> None:
        
        self._fieldName: str = fieldName if isinstance(fieldName, Iterable) else (fieldName)
        
        if isinstance(annotationType, (NoneType, UnionType, type)):
            self._annotationType = annotationType
        else:
            raise TypeError("Annotation type is invalid")
        
    def _create_annotations(self, cls) -> bool:
        
        all_annotations = getattr(cls, "__annotations__", None)
        
        # Если аннотаций в классе вообще не прописано то создаем их
        if all_annotations is None:
            setattr(cls, "__annotations__", {})
            return True
        return False
    
    def _set_annotation_to_class(self, cls, annotation: type | UnionType) -> None:
        try:
            
            # берем все существующие аннотации
            class_annotations: dict = getattr(cls, "__annotations__")
            assert class_annotations[self._fieldName] == annotation or class_annotations.get(self._fieldName) is None
            cls.__annotations__[self._fieldName] = annotation
            
        except AttributeError:
            raise AttributeError("Annotations not found", name="class_annotations", obj=class_annotations)
        except AssertionError:
            raise Exception("Annotation overload")
        except KeyError:
            cls.__annotations__[self._fieldName] = annotation
    
    def _get_field_annotation(self, cls, func: Callable) -> type | UnionType:
        try:
            # Пытаемся взять все существующие аннотации класса
            annotations: Mapping[str, type] = getattr(cls, "__annotations__")
            assert annotations.get(self._fieldName) is not None
            return annotations[self._fieldName]
        except AssertionError:
            return self._get_param_annotation(func)
    
    def _get_param_annotation(self, func: Callable) -> type | UnionType:
        try:
            # В первую очередь смотрим на переданные аннотации в параметрах декоратора
            assert self._annotationType is not None
            return self._annotationType
                
        except AssertionError:
            return self._get_func_annotation(func)
    
    def _get_func_annotation(self, func: Callable):
        # если не найдено то смотрим в аннотациях метода
        # Пытаемся взять все существующие аннотации параметров функции
        annotations: dict[str, type | UnionType] = getattr(func, "__annotations__")
        
        if len(annotations) > 0 and annotations.get(self._fieldName) is not None:
            return annotations[self._fieldName]
        else:
            raise AnnotationNotFound("No annotation detected")
           
    
    def _check_args(self, args: Iterable, kwargs: Mapping[str, Any], attr_type: type | UnionType):
        
        if attr_type is not None:
            for arg in args:
                if not isinstance(arg, attr_type):
                    raise TypeError(f"Wrong field type. Type should be {attr_type}, but got {type(arg)} instead")
                
            for value in kwargs.values():
                if not isinstance(value, attr_type):
                    raise TypeError(f"Wrong field type. Type should be {attr_type}, but got {type(value)} instead")
        else:
            raise ValueError("Type is none")
    
    def __call__(self, func: AutopropBase):
        
        @wraps(func) 
        def wrapper(cls, *args, **kwargs):
            
            self._create_annotations(cls)

            # Получаем аннотацию для проверки поля класса
            attr_annotation = self._get_field_annotation(cls, func)
            
            self._set_annotation_to_class(cls, attr_annotation)

            self._check_args(args, kwargs, attr_annotation)
            
            return func(cls, *args)
        
        return wrapper