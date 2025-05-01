
from types import UnionType
from typing import Protocol, runtime_checkable

from autoproperty.autoproperty_methods.autoproperty_getter import AutopropGetter
from autoproperty.autoproperty_methods.autoproperty_setter import AutopropSetter
from autoproperty.prop_settings import AutoPropAccessMod

@runtime_checkable
class IAutoProperty(Protocol):
    annotationType: type | UnionType | None
    access_mod: AutoPropAccessMod
    g_access_mod: AutoPropAccessMod
    s_access_mod: AutoPropAccessMod
    docstr: str | None = None
    setter: AutopropSetter
    getter: AutopropGetter