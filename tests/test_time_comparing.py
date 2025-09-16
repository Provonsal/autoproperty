import line_profiler
from autoproperty import AutoProperty
import timeit

AutoProperty.validate_fields = True

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
        def X(self) -> int:
            ...

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

    @line_profiler.profile
    def func1():
        obj.X

    @line_profiler.profile
    def func2():
        obj.Y

    @line_profiler.profile
    def func3():
        obj.X = 2

    @line_profiler.profile
    def func4():
        obj.Y = 2

    execution_time_autoproperty = timeit.timeit(func1, number=100000)
    execution_time_property = timeit.timeit(func2, number=100000)
    execution_time_autoproperty_write = timeit.timeit(func3, number=10000)
    execution_time_property_write = timeit.timeit(func4, number=10000)
    execution_time_custom_descriptor = timeit.timeit(lambda: obj.Z, number=10000)

    print("autoproperty time: ", execution_time_autoproperty)
    print("property time: ", execution_time_property)
    print("autoproperty setter time: ", execution_time_autoproperty_write)
    print("property setter time: ", execution_time_property_write)
    print("descriptor time: ", execution_time_custom_descriptor)
    print("diff 1", execution_time_autoproperty/execution_time_property)
    print("diff 2", execution_time_autoproperty_write/execution_time_property_write)

#     code = """
# class A():

#     __y: int

#     @property
#     def Y(self):
#         return self.__y
    
#     @Y.setter
#     def Y(self, v):
#         self.__y = v
    
#     def __init__(self, y) -> None:
#         self.Y = y

# obj = A(3)
# obj.Y
#     """

#     code2 = """
# class A():

#     @AutoProperty[int](annotationType=int)
#     def X(self):
#         ...
    
#     def __init__(self, x) -> None:
#         self.X = x

# obj = A(3)
# print(1)
# print(1)
# print(1)
# print(1)
# print(1)
# obj.X
# """
    
    #dis(lambda: obj.X)

    # import cProfile

    # cProfile.Profile(timer=time.perf_counter_ns, timeunit=0.000001).run(code)
    # cProfile.Profile(timer=time.perf_counter_ns,timeunit=0.000001).run(code2)
    # cProfile.run(code)
    # cProfile.run(code2)

time_comparing()

"""
1 try
autoproperty time:  0.15369665699836332
property time:  0.048774095994303934
diff 3.151194376135905
"""