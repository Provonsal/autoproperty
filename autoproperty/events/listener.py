from typing import NamedTuple

from autoproperty.events.context import EventContext
from autoproperty.events.filters import ListenerFilters
from autoproperty.interfaces.events import Action


class Listener:
    
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
    ) -> None:
        self.action = action
        self.filters = ListenerFilters._make(filters)
        self.trigger_count = 0
    
    def check_filters(self, filters: tuple) -> bool:
        if len(filters) == len(self.filters):
            
            for listener_filter, gotten_filter in zip(self.filters, filters):
                if listener_filter != gotten_filter:
                    return False
                
            return True
        else:
            return False
    
    def change_filters(self, new_filters: ListenerFilters) -> None:
        self.filters = new_filters
    
    def notify(self, context: EventContext) -> None:
        if self.check_filters(context.filters):
            self.action(context)
            self.trigger_count += 1
        else:
            return None