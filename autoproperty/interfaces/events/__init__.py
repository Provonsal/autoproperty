from typing import Callable, NamedTuple, Protocol

from autoproperty.events.context import EventContext
from autoproperty.events.filters import ListenerFilters
from autoproperty.prop_settings import AutoPropType


class IListener(Protocol):
    __slots__ = (
        'action',
        'filters'
    )
    
    action: Callable[[EventContext], None]
    filters: NamedTuple
    
    def __init__(
        self, 
        action: Callable[[EventContext], None],
        filters: tuple
    ): ...
    def check_filters(self, filters: tuple) -> bool: ...
    def change_filters(self, new_filters: ListenerFilters): ...
    def notify(self, context: EventContext) -> None: ...

class IEvent(Protocol):
    __slots__ = (
        'listeners',
    )
    
    listeners: list[IListener]
    
    def __init__(self): ...
    def subscribe(self, listener) -> None: ...
    def unsubscribe(self, listener) -> None: ...
    def trigger(
        self, 
        method_type: AutoPropType, 
        property_name: str | None, 
        ret_value: str | None=None,
        new_value: str | None=None, 
        time: float | None=None
    ) -> None: ...