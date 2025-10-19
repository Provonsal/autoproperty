from dataclasses import dataclass


@dataclass
class EventData:
    ret_value: str | None = None
    new_value: str | None = None
    time: float | None = None