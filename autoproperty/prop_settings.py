from enum import Enum


class AutoPropAccessMod(int, Enum):
    Public = 0
    Protected = 1
    Private = 2 
    
class AutoPropType(int, Enum):
    Setter = 0
    Getter = 1