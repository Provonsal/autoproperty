from pydantic import ValidationError
from autoproperty import AutoProperty

def test_wrong_type():
    class CL1:
        def __init__(self):
            self.X = "12"
            print(self.X)
            
        @AutoProperty(annotation_type=int)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = "10"
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = "121"
            print(cls.X)
            
    # in home class
    try:
        CL1()
        assert False    
    except ValidationError:
        assert True
    
    # inside the inheritor        
    try:
        CL2()
        assert False
    except ValidationError:
        assert True
        
    # in unknown class
    try:
        cls = CL3()
        assert False
    except ValidationError:
        assert True
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = "100"
        print(cls.X)
        assert False
    except ValidationError:
        assert True

def test_correct_type():
    class CL1:
        def __init__(self):
            self.X = 12
            print(self.X)
            
        @AutoProperty(annotation_type=int)
        def X(self): ...

        def method(self):
            self.X

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
    except ValidationError:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert True
    except ValidationError:
        assert False
        
    # in unknown class
    try:
        cls = CL3()
        assert True
    except ValidationError:
        assert False
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert True
    except ValidationError:
        assert False

def test_no_validation():
    
    AutoProperty.validate_fields = False
    
    class CL1:
        def __init__(self):
            self.X = "12"
            print(self.X)
            
        @AutoProperty
        def X(self): ...

        def method(self):
            self.X

    class CL2(CL1):
        def __init__(self):
            self.X = "10"
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = "121"
            print(cls.X)
            
    # in home class
    try:
        CL1()
        assert True    
    except ValidationError:
        assert False
    
    # inside the inheritor        
    try:
        CL2()
        assert True
    except ValidationError:
        assert False
        
    # in unknown class
    try:
        cls = CL3()
        assert True
    except ValidationError:
        assert False
    
    # outside the class    
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert True
    except ValidationError:
        assert False
        
    AutoProperty.validate_fields = True