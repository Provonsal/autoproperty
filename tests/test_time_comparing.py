import time
from autoproperty import AutoProperty
import timeit
from dis import dis

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

        @AutoProperty[int](annotationType=int)
        def X(self):
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

    execution_time_autoproperty = timeit.timeit(lambda: obj.X, number=10000000)
    execution_time_property = timeit.timeit(lambda: obj.Y, number=10000000)
    execution_time_custom_descriptor = timeit.timeit(lambda: obj.Z, number=10000000)

    print("autoproperty time: ", execution_time_autoproperty)
    print("property time: ", execution_time_property)
    print("descriptor time: ", execution_time_custom_descriptor)
    print("diff", execution_time_autoproperty/execution_time_property)

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