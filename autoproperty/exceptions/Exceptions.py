from typing import Any, Iterable
from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutopropBase


class AnnotationNotFoundError(Exception):
    ...

class AnnotationOverlapError(Exception):
    def __init__(self, msg="Provided annotations are not the same."):
        super().__init__(msg)

