from functools import wraps
import inspect
from typing import Callable, Generic, TypeVar

from autoproperty.interfaces.autoproperty_itself.I_autoproperty import IAutoProperty
from autoproperty.prop_settings import AutoPropAccessMod
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethod, AccessModNotRecognized

T = TypeVar('T')

class PropMethodAccessController(Generic[T]):

    def __init__(self, access: AutoPropAccessMod):
        self.access: AutoPropAccessMod = access

    @staticmethod
    def contain_autoprop_method(classes, Prop_method: Callable):
        """

        """

        for class_ in classes:

            for key in dir(class_):
                val = getattr(class_, key)

                if isinstance(val, IAutoProperty):

                    if val.getter is not None:

                        if hasattr(val.getter, "__auto_prop__"):
                            if getattr(val.getter, "__prop_name__") in getattr(Prop_method, "__prop_name__"):
                                return class_

                    if val.setter is not None:

                        if hasattr(val.setter, "__auto_prop__"):
                            if getattr(val.setter, "__prop_name__") in getattr(Prop_method, "__prop_name__"):
                                return class_
                else:
                    continue

        return None

    def __call__(self, obj) -> Callable[..., T]:
        
        @wraps(obj)
        def wrapper(cls, *args, **kwargs) -> T:

            frame = inspect.currentframe()

            try:

                # temp plugs
                if frame is None:
                    raise Exception("Something unexpected happened! :(")
                if frame.f_back is None:
                    raise Exception("Something unexpected happened! :(")
                if frame.f_back.f_back is None:
                    raise Exception("Something unexpected happened! :(")
                
                locals = frame.f_back.f_back.f_locals

                class_caller = locals.get("self", None)

                match self.access:

                    case AutoPropAccessMod.Private:

                        cls_with_private_method = PropMethodAccessController.contain_autoprop_method(
                            class_caller.__class__.__bases__, obj)

                        if class_caller is cls and not cls_with_private_method:
                            return obj(cls, *args, **kwargs)
                        else:
                            raise UnaccessiblePropertyMethod(obj)

                    case AutoPropAccessMod.Public:

                        return obj(cls, *args, **kwargs)

                    case AutoPropAccessMod.Protected:

                        if class_caller is cls or isinstance(class_caller, cls.__class__):
                            return obj(cls, *args, **kwargs)
                        else:
                            raise UnaccessiblePropertyMethod(obj)
                    case _:
                        raise AccessModNotRecognized(self.access, (AutoPropAccessMod.Public, AutoPropAccessMod.Private, AutoPropAccessMod.Protected))
            finally:
                del frame

        return wrapper
