from dataclasses import dataclass

from autoproperty.events.data import EventData
from autoproperty.events.filters import ListenerFilters


@dataclass
class EventContext:
    filters: ListenerFilters
    data: EventData