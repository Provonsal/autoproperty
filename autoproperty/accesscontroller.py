from functools import wraps
import inspect
from typing import Callable

from autoproperty.autoproperty_methods.autoproperty_base import AutopropBase
from autoproperty.interfaces.autoproperty_methods import IAutopropBase
from autoproperty.prop_settings import AutoPropAccessMod
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethod, AccessModNotRecognized


class PropMethodAccessController:

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

    def __call__(self, obj: AutopropBase):

        @wraps(obj)
        def wrapper(cls, *args, **kwargs):

            frame = inspect.currentframe()

            try:

                locals = frame.f_back.f_locals

                class_caller = locals.get("self", None)

                match self.access:

                    case AutoPropAccessMod.Private:

                        cls_with_private_method = PropMethodAccessController.contain_autoprop_method(
                            class_caller.__class__.__bases__, obj)

                        if class_caller is cls and not cls_with_private_method:
                            return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj
                        else:
                            raise UnaccessiblePropertyMethod(obj)

                    case AutoPropAccessMod.Public:

                        return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj

                    case AutoPropAccessMod.Protected:

                        if class_caller is cls or isinstance(class_caller, cls.__class__):
                            return obj(cls, *args, **kwargs) if isinstance(obj, Callable) else obj
                        else:
                            raise UnaccessiblePropertyMethod(obj)
                    case _:
                        raise AccessModNotRecognized(self.access, (AutoPropAccessMod.Public, AutoPropAccessMod.Private, AutoPropAccessMod.Protected))
            finally:
                del frame

        return wrapper
