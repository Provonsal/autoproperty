from functools import wraps
import inspect
from typing import Callable

from utils.interfaces.autoproperty_methods import IAutoPropertyMethod
from utils.prop_settings import AutoPropAccessMod
from utils.exceptions.Exceptions import UnaccessibleProperty


class PropertyMethodAccessController:
    
    def __init__(self, access: AutoPropAccessMod):
        self.access: AutoPropAccessMod = access

    @staticmethod
    def contain_autoprop_method(classes, Prop_method: Callable):
        """
        
        """
        
        for class_ in classes:
            
            for key in dir(class_):
                val = getattr(class_, key)
            
                if isinstance(val, property):
            
                    if val.fget is not None:
            
                        if hasattr(val.fget, "__auto_prop__"):
                            if getattr(val.fget, "__name__") in Prop_method.__name__:
                                return class_
                    
                    if val.fset is not None:
            
                        if hasattr(val.fset, "__auto_prop__"):
                            if getattr(val.fset, "__name__") in Prop_method.__name__:
                                return class_
                else:
                    continue

        return None

    def __call__(self, obj: Callable):
        
        
        def  wrapper(cls, *args, **kwargs):
            
            frame = inspect.currentframe()
            
            try:
                
                locals = frame.f_back.f_locals
                
                class_caller: "IAutoPropertyMethod" = locals.get("self", None)
                
                match self.access:
                    
                    case AutoPropAccessMod.Private:
                        
                        cls_with_private_method = PropertyMethodAccessController.contain_autoprop_method(class_caller.__class__.__bases__, obj)
                        
                        if class_caller is cls and not cls_with_private_method:
                            return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj
                        else:
                            raise UnaccessibleProperty()
                    
                    case AutoPropAccessMod.Public:
                        
                        return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj
                    
                    case AutoPropAccessMod.Protected:
                        
                        if class_caller is cls or isinstance(class_caller, cls.__class__):
                            return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj
                        else:
                            raise UnaccessibleProperty()
                    case _:
                        raise Exception()
            finally:
                del frame
        
        return wrapper