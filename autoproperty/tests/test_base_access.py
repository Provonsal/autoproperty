from autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import UnaccessibleProperty
from autoproperty.prop_settings import AutoPropAccessMod


def test_private_access():
    
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)
            
        @AutoProperty(int, AutoPropAccessMod.Private)
        def X(self): ...

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
    except UnaccessibleProperty:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert False
    except UnaccessibleProperty:
        assert True
        
    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessibleProperty:
        assert True
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessibleProperty:
        assert True
        
def test_protected_access():
    
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)
            
        @AutoProperty(int, AutoPropAccessMod.Protected)
        def X(self): ...

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
    except UnaccessibleProperty:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert True
    except UnaccessibleProperty:
        assert False
        
    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessibleProperty:
        assert True
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessibleProperty:
        assert True
        
def test_public_access():
    
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)
            
        @AutoProperty(int, AutoPropAccessMod.Public)
        def X(self): ...

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
    except UnaccessibleProperty:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert True
    except UnaccessibleProperty:
        assert False
        
    # in unknown class
    try:
        cls = CL3()
        assert True
    except UnaccessibleProperty:
        assert True
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert True
    except UnaccessibleProperty:
        assert True
        
