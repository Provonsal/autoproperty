from autoproperty.prop_settings import AutoPropAccessMod, AutoPropType

class AutopropBase:

    __auto_prop__: bool
    __prop_attr_name__: str
    __prop_access__: AutoPropAccessMod
    __method_type__: AutoPropType
    __prop_name__: str
    
    def __call__(self, *args, **kwds): raise NotImplementedError()