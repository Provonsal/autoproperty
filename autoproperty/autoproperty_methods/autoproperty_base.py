from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType

class AutopropBase:

    __auto_prop__: IAutoProperty
    __prop_attr_name__: str
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __init__(self, prop_name: str,  varname: str, belong: IAutoProperty, prop_type: AutoPropType) -> None:
        self.__auto_prop__ = belong
        self.__prop_attr_name__ = varname
        self.__method_type__ = prop_type
        self.__prop_name__ = prop_name
        return
    
    def __call__(self, *args, **kwds): raise NotImplementedError()