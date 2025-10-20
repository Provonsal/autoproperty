from autoproperty.events.context import EventContext
from autoproperty.events.data import EventData
from autoproperty.events.filters import ListenerFilters
from autoproperty.interfaces.events import IListener
from autoproperty.prop_settings import AutoPropType


class Event:

    __slots__ = (
        'listeners',
    )
    
    listeners: list[IListener]
    
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener: IListener):
        self.listeners.append(listener)

    def unsubscribe(self, listener: IListener):
        self.listeners.remove(listener)
        
    def trigger(
        self, 
        method_type: AutoPropType, 
        property_name: str | None, 
        ret_value: str | None=None,
        new_value: str | None=None, 
        time: float | None=None
    ):
        context = EventContext(
            ListenerFilters(
                method_type,
                property_name
            ),
            EventData(
                ret_value,
                new_value,
                time
            )
        )
        
        for listener in self.listeners:
            listener.notify(context)