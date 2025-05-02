from autoproperty.interfaces.autoproperty_methods import IAutoProperty
from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType

class AutopropBase:

    __auto_prop__: IAutoProperty
    __prop_attr_name__: str
    __prop_access__: AutoPropAccessMod
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __init__(self, prop_name: str,  varname: str, method_access_mod: AutoPropAccessMod, belong: IAutoProperty, prop_type: AutoPropType) -> None:
        self.__auto_prop__ = belong
        self.__prop_attr_name__ = varname
        self.__prop_access__ = method_access_mod
        self.__method_type__ = prop_type
        self.__prop_name__ = prop_name
        return
    
    def __call__(self, *args, **kwds): raise NotImplementedError()