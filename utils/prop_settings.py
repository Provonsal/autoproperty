from enum import Enum


class AutoPropAccessMod(int, Enum):
    Public = 0
    Protected = 1
    Private = 2
    
class AutoPropMod(str, Enum):
    Required = "required"
    ReadOnly = "readonly"  