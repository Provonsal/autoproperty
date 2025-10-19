


from typing import Callable, NamedTuple

from autoproperty.events.context import EventContext
from autoproperty.events.filters import ListenerFilters


class Listener:
    
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
    ):
        self.action = action
        self.filters = ListenerFilters._make(filters)
    
    def check_filters(self, filters: tuple) -> bool:
        if len(filters) == len(self.filters):
            
            for listener_filter, gotten_filter in zip(self.filters, filters):
                if listener_filter != gotten_filter:
                    return False
                
            return True
        else:
            return False
    
    def change_filters(self, new_filters: ListenerFilters):
        self.filters = new_filters
    
    def notify(self, context: EventContext):
        if self.check_filters(context.filters):
            self.action(context)
        else:
            return None