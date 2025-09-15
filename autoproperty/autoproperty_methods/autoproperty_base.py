from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.prop_settings import AutoPropType

class AutopropBase:

    __slots__ = ('__auto_prop__', '__prop_attr_name__', '__method_type__', '__prop_name__')

    __auto_prop__: IAutoProperty
    __prop_attr_name__: str
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __init__(self, prop_name: str,  attr_name: str, belong: IAutoProperty, prop_type: AutoPropType) -> None:
        self.__auto_prop__ = belong
        self.__prop_attr_name__ = attr_name
        self.__method_type__ = prop_type
        self.__prop_name__ = prop_name
        return
    
    def __call__(self, *args, **kwds): raise NotImplementedError()