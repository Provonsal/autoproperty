from autoproperty.autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethodError
from autoproperty.prop_settings import AutoPropAccessMod


# def test_private_inherit():
#     class CL1:
#         def __init__(self):
#             self.X = 10
#             print(self.X)
            
#         @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Private)
#         def X(self): ...

#     class CL2(CL1):
#         def __init__(self):
#             super().__init__()
#             self.X = 12
#             # print(self.X)

#     class CL3:
#         def __init__(self):
#             cls = CL1()
#             cls.X = 121
#             print(cls.X)
    
#     # in home class
#     try:
#         CL1()
#         assert True    
#     except UnaccessiblePropertyMethod:
#         assert False
    
#     # inside the inheritor        
#     try:
#         CL2()
#         assert True
#     except UnaccessiblePropertyMethod:
#         assert False
        
#     # in unknown class
#     try:
#         cls = CL3()
#         assert False
#     except UnaccessiblePropertyMethod:
#         assert True
    
#     # outside the class    
#     try:
#         cls = CL1()
#         cls.X = 100
#         print(cls.X)
#         assert False
#     except UnaccessiblePropertyMethod:
#         assert True