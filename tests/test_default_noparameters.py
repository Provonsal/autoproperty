from autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethodError
from autoproperty.prop_settings import AutoPropAccessMod


def test_no_parameters_passed():
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)
            
        @AutoProperty[int]
        def X(self, v: int): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)
    
    # in home class
    try:
        CL1()
        assert True    
    except UnaccessiblePropertyMethodError:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert False
    except UnaccessiblePropertyMethodError:
        assert True
        
    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessiblePropertyMethodError:
        assert True
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessiblePropertyMethodError:
        assert True