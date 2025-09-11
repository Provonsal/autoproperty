import inspect
import traceback
from types import FrameType, NoneType, UnionType
from typing import Any, Callable, Generic, TypeVar, cast
from warnings import warn
from autoproperty.exceptions.Exceptions import AccessModNotRecognizedError
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.accesscontroller import PropMethodAccessController
from autoproperty.autoproperty_methods import AutopropGetter, AutopropSetter
from autoproperty.interfaces.autoproperty_methods import IAutopropBase, IAutopropGetter, IAutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

class AutoProperty(Generic[T]):

    annotationType: type | UnionType | None
    docstr: str | None = None
    setter: IAutopropSetter
    getter: IAutopropGetter
    bound_class_qualname: str

    def __new__(
        cls,
        *args,
        **kwargs
        ):
        
        return super().__new__(cls)

    def __init__(
        self,
        func: Callable[..., Any] | None = None,
        annotationType: type | UnionType | None = None,
        docstr: str | None = None
    ):

        self.docstr = docstr
        self.annotationType = annotationType

        frame = inspect.currentframe()
        
        self.bound_class_qualname = self.__get_class_qualname(frame)

        if func is not None:
            self._varname = "__" + func.__name__[0].lower() + func.__name__[1:]

            self._prop_name = func.__name__
            
            try:
                annotation = func.__annotations__.values().__iter__().__next__()
            except StopIteration:
                annotation = None

            tmp1: AutopropGetter[T] = AutopropGetter[T](self._prop_name, self._varname, self)
            tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, annotation, self)

            self.getter = tmp1
            self.setter = cast(AutopropSetter, PropMethodAccessController[NoneType](self.s_access_mod)(cast(IAutopropBase, FieldValidator(self._varname, self.annotationType)(tmp2))))
            

    def __get_class_qualname(self, frame: FrameType | None) -> str:

        try:

            # temp plugs
            if frame is None:
                raise Exception("Something unexpected happened! :(")
            if frame.f_back is None:
                raise Exception("Something unexpected happened! :(")
            if frame.f_back.f_back is None:
                raise Exception("Something unexpected happened! :(")
            
            locals = frame.f_back.f_back.f_locals

            return cast(str, locals.get("__qualname__"))
        finally:
            del frame

    def __call__(
        self,
        func: Callable[..., Any]
        ) -> "AutoProperty[T]":
        
        self._varname = "__" + func.__name__[0].lower() + func.__name__[1:]

        self._prop_name = func.__name__
        
        try:
            annotation = func.__annotations__.values().__iter__().__next__()
        except StopIteration:
            annotation = None
            
        tmp1: AutopropGetter[T] = AutopropGetter[T](self._prop_name, self._varname, self.g_access_mod, self)
        tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, self.s_access_mod, annotation, self)

        self.getter = cast(AutopropGetter, PropMethodAccessController[T](self.g_access_mod)(tmp1))
        self.setter = cast(AutopropSetter, PropMethodAccessController[NoneType](self.s_access_mod)(cast(IAutopropBase, FieldValidator(self._varname, self.annotationType)(tmp2))))
            
        return self

    
    def __set__(self, instance, obj):
        self.setter(instance, obj)

    def __get__(self, instance, owner=None) -> T:
        if instance is None:
            return self #type: ignore
        return self.getter(instance) #type: ignore

    def __parse_access_str_int(self, access: str):
        match access:
            case "public":
                return 0
            case "protected":
                return 1
            case "private":
                return 2
            case _:
                raise AccessModNotRecognizedError(access, (AutoPropAccessMod))

    def _get_docstring(self, func: Callable, attr_type):

        try:
            assert self.docstr is not None
            return self.docstr
        except AssertionError:
            try:
                assert func.__doc__ is not None
                return func.__doc__
            except AssertionError:
                return f"Auto property. Name: {func.__name__}, type: {attr_type}, returns: {func.__annotations__.get('return')}"

# class AutoPropertyVar(Generic[T]):
#     annotationType: type | UnionType | None
#     access_mod: AutoPropAccessMod
#     g_access_mod: AutoPropAccessMod
#     s_access_mod: AutoPropAccessMod
#     docstr: str | None = None

#     def __init__(
#         self,
#         access_mod: AutoPropAccessMod | int | str = AutoPropAccessMod.Private,
#         g_access_mod: AutoPropAccessMod | int | str | None = None,
#         s_access_mod: AutoPropAccessMod | int | str | None = None,
#         name: str | None = None,
#         docstr: str | None = None
#     ):

#         self.docstr = docstr

#         if isinstance(access_mod, AutoPropAccessMod):
#             self.access_mod = access_mod
#         elif isinstance(access_mod, int):
#             self.access_mod = AutoPropAccessMod(access_mod)
#         else:
#             self.access_mod = AutoPropAccessMod(
#                 self.__parse_access_str_int(access_mod))

#         default = self.access_mod

#         if g_access_mod is None:
#             self.g_access_mod = default
#         elif isinstance(g_access_mod, AutoPropAccessMod):
#             self.g_access_mod = g_access_mod
#         elif isinstance(g_access_mod, int):
#             self.g_access_mod = AutoPropAccessMod(g_access_mod)
#         else:
#             self.g_access_mod = AutoPropAccessMod(
#                 self.__parse_access_str_int(g_access_mod))

#         if s_access_mod is None:
#             self.s_access_mod = default
#         elif isinstance(s_access_mod, AutoPropAccessMod):
#             self.s_access_mod = s_access_mod
#         elif isinstance(s_access_mod, int):
#             self.s_access_mod = AutoPropAccessMod(s_access_mod)
#         else:
#             self.s_access_mod = AutoPropAccessMod(
#                 self.__parse_access_str_int(s_access_mod))

#         if self.g_access_mod < self.access_mod:
#             warn("Invalid getter access level. Getter level can't be higher than property's", SyntaxWarning)
#             self.g_access_mod = default

#         if self.s_access_mod < self.access_mod:
#             warn("Invalid setter access level. Setter level can't be higher than property's", SyntaxWarning)
#             self.s_access_mod = default

#         if name is not None:
#             self._varname = "__" + name[0].lower() + name[1:]

#             self._prop_name = name
#         else:
#             (_, _, _, text) = traceback.extract_stack()[-2]

#             name = cast(str, text[:text.find('=')].strip())

#             self._varname = "__" + name[0].lower() + name[1:]

#             self._prop_name = name

#         tmp1: AutopropGetter = AutopropGetter[T](self._prop_name, self._varname, self.g_access_mod)
#         tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, self.s_access_mod, func.__annotations__.values().__iter__().__next__())

#         self.getter = PropMethodAccessController[T](self.g_access_mod)(tmp1)
#         self.setter = PropMethodAccessController[NoneType](self.s_access_mod)(FieldValidator(self._varname, getattr(self, "__orig_class__").__args__[0])(tmp2))

#     def __call__(
#         self,
#         func: Callable[..., Any]
#         ) -> "AutoPropertyVar[T]":
        
#         self._varname = "__" + func.__name__[0].lower() + func.__name__[1:]

#         self._prop_name = func.__name__
        
#         tmp1: AutopropGetter[T] = AutopropGetter[T](self._prop_name, self._varname, self.g_access_mod)
#         tmp2: AutopropSetter = AutopropSetter(self._prop_name, self._varname, self.s_access_mod)

#         self.getter = PropMethodAccessController[T](self.g_access_mod)(tmp1)
#         self.setter = PropMethodAccessController[NoneType](self.s_access_mod)(FieldValidator(self._varname, getattr(self, "__orig_class__").__args__[0])(tmp2))
        
#         return self

#     def __set__(self, instance, obj):
#         self.setter(instance, obj)

#     def __get__(self, instance, owner=None) -> T:
#         return self.getter(instance)

#     def __parse_access_str_int(self, access: str):
#         match access:
#             case "public":
#                 return 0
#             case "protected":
#                 return 1
#             case "private":
#                 return 2
#             case _:
#                 raise AccessModNotRecognized(access, (AutoPropAccessMod))

#     def _get_docstring(self, func: Callable, attr_type):

#         try:
#             assert self.docstr is not None
#             return self.docstr
#         except AssertionError:
#             try:
#                 assert func.__doc__ is not None
#                 return func.__doc__
#             except AssertionError:
#                 return f"Auto property. Name: {func.__name__}, type: {attr_type}, returns: {func.__annotations__.get('return')}"
