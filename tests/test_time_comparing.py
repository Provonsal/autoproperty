from autoproperty import AutoProperty
from autoproperty import LightAutoProperty
import timeit

AutoProperty.validate_fields = False

def time_comparing():
        
    class A():

        __y: int

        @AutoProperty(cache=True)
        def X(self) -> int: ...

        @LightAutoProperty
        def G(self) -> int: ...

        @property
        def Y(self):
            return self.__y
        
        @Y.setter
        def Y(self, v):
            self.__y = v
        
        def __init__(self, x, y, z) -> None:
            self.X = x
            self.Y = y

    obj = A(3,3,3)

    def autoproperty_get():
        obj.X

    def light_autoproperty_get():
        obj.G
        
    def basic_property_get():
        obj.Y
        
    def autoproperty_set():
        obj.X = 2

    def light_autoproperty_set():
        obj.G = 2
        
    def basic_property_set():
        obj.Y = 2

    try_count = 1_000_000_000

    execution_time_autoproperty         = timeit.timeit(autoproperty_get, number=try_count)
    execution_time_light_property       = timeit.timeit(light_autoproperty_get, number=try_count)
    execution_time_basic_property       = timeit.timeit(basic_property_get, number=try_count)
    
    execution_time_autoproperty_write   = timeit.timeit(autoproperty_set, number=try_count)
    execution_time_light_property_write = timeit.timeit(light_autoproperty_set, number=try_count)
    execution_time_basic_property_write = timeit.timeit(basic_property_set, number=try_count)

    print("autoproperty getter time: ", execution_time_autoproperty)
    print("autoproperty setter time: ", execution_time_autoproperty_write)
    print()
    print("light autoproperty getter time: ", execution_time_light_property)
    print("light autoproperty setter time: ", execution_time_light_property_write)
    print()
    print("basic property getter time", execution_time_basic_property)
    print("basic property setter time", execution_time_basic_property_write)
    print()
    print("diff between getters of autoproperty and it light version", execution_time_autoproperty/execution_time_light_property)
    print("diff between setters of autoproperty and it light version", execution_time_autoproperty_write/execution_time_light_property_write)
    print()
    print("diff between getters of autoproperty and basic solution", execution_time_autoproperty/execution_time_basic_property)
    print("diff between setters of autoproperty and basic solution", execution_time_autoproperty_write/execution_time_basic_property_write)
    
    light_autoproperty_percent_getter = (((execution_time_autoproperty-execution_time_light_property)/execution_time_light_property)*100)+100
    basic_property_percent_getter = (((execution_time_autoproperty-execution_time_basic_property)/execution_time_basic_property)*100)+100
    
    light_autoproperty_percent_setter = (((execution_time_autoproperty_write-execution_time_light_property_write)/execution_time_light_property_write)*100)+100
    basic_property_percent_setter = (((execution_time_autoproperty_write-execution_time_basic_property_write)/execution_time_basic_property_write)*100)+100
    
    print()
    print("Lets find out who is faster. More percent - faster")
    print("getters")
    print(f"If AutoProperty result = 100%, then LightAutoProperty = {light_autoproperty_percent_getter:.0f}%, and basic property = {basic_property_percent_getter:.0f}%")
    print()
    print("setters")
    print(f"If AutoProperty result = 100%, then LightAutoProperty = {light_autoproperty_percent_setter:.0f}%, and basic property = {basic_property_percent_setter:.0f}%")
    

time_comparing()
