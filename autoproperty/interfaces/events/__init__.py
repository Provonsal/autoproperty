from typing import NamedTuple, Protocol

from autoproperty.events.context import EventContext
from autoproperty.events.filters import ListenerFilters
from autoproperty.prop_settings import AutoPropType


class Action(Protocol):
    def __call__(self, context: EventContext) -> None: ...

class IListener(Protocol):
    __slots__ = (
        'action',
        'filters',
        'trigger_count'
    )
    
    action: Action
    filters: NamedTuple
    trigger_count: int
    
    def __init__(
        self, 
        action: Action,
        filters: tuple
    ) -> None: ...
    def check_filters(self, filters: tuple) -> bool: ...
    def change_filters(self, new_filters: ListenerFilters) -> None: ...
    def notify(self, context: EventContext) -> None: ...

class IEvent(Protocol):
    __slots__ = (
        'listeners',
    )
    
    listeners: list[IListener]
    
    def __init__(self) -> None: ...
    def subscribe(self, listener: IListener) -> None: ...
    def unsubscribe(self, listener: IListener) -> None: ...
    def trigger(
        self, 
        method_type: AutoPropType, 
        property_name: str | None, 
        ret_value: str | None=None,
        new_value: str | None=None, 
        time: float | None=None
    ) -> None: ...