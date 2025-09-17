import line_profiler
from autoproperty import AutoProperty
from autoproperty import LightAutoProperty
import timeit

AutoProperty.validate_fields = False

def time_comparing():
    
    class Descriptor():
        value: int

        def __init__(self, value) -> None:
            self.value = value

        def __set__(self, instance, obj):
            self.value = obj

        def __get__(self, instance, owner=None):
            
            # If instance is not exist then return class type
            if instance is None:
                return self #type: ignore
            
            return self.value
        
    class A():

        __y: int
        

        @AutoProperty
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
            self.Z = Descriptor(z)

    

    obj = A(3,3,3)

    #@line_profiler.profile
    def autoproperty_get():
        obj.X

    #@line_profiler.profile
    def light_autoproperty_get():
        obj.G
        
    
    def basic_property_get():
        obj.Y
        
    #@line_profiler.profile
    def autoproperty_set():
        obj.X = 2

    #@line_profiler.profile
    def light_autoproperty_set():
        obj.G = 2
        
    def basic_property_set():
        obj.Y = 2

    execution_time_autoproperty_write   = timeit.timeit(autoproperty_set, number=1_000_000_0)
    execution_time_autoproperty         = timeit.timeit(autoproperty_get, number=1_000_000_0)
    execution_time_light_property_write = timeit.timeit(light_autoproperty_set, number=1_000_000_0)
    execution_time_light_property       = timeit.timeit(light_autoproperty_get, number=1_000_000_0)
    execution_time_basic_property_write = timeit.timeit(basic_property_set, number=1_000_000_0)
    execution_time_basic_property       = timeit.timeit(basic_property_get, number=1_000_000_0)

    print("autoproperty time: ", execution_time_autoproperty)
    print("autoproperty setter time: ", execution_time_autoproperty_write)
    print("light autoproperty time: ", execution_time_light_property)
    print("light autoproperty setter time: ", execution_time_light_property_write)
    print("basic property", execution_time_basic_property)
    print("basic property write", execution_time_basic_property_write)
    print("diff 1", execution_time_autoproperty/execution_time_light_property)
    print("diff 2", execution_time_autoproperty_write/execution_time_light_property_write)



time_comparing()

"""
1 try
autoproperty time:  0.15369665699836332
property time:  0.048774095994303934
diff 3.151194376135905
"""