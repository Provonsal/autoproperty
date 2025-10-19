from typing import NamedTuple
from autoproperty.prop_settings import AutoPropType


class ListenerFilters(NamedTuple):
    method_type: AutoPropType
    property_name: str | None