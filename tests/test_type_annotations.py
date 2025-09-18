from autoproperty.autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import AnnotationNotFoundError, AnnotationOverlapError


def test_annotation_overlap_one():
    
    # First combination
    try:   
        class CL1:
            
            _X: str 
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=int)
            def X(self) -> int: ...

            def method(self):
                self.X
    
        assert False
    except AnnotationOverlapError:
        assert True
def test_annotation_overlap_two():    
    # Second combination
    try:       
        class CL2:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=str)
            def X(self) -> int: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
def test_annotation_overlap_three():    
    # Third combination
    try:     
        class CL3:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=int)
            def X(self) -> str: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_four():        
    # fourth combination
    try:     
        class CL4:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty
            def X(self) -> str: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_five():
    # fourth combination
    try:     
        class CL5:
            
            _X: str
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty
            def X(self) -> int: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_six():
    # fourth combination
    try:     
        class CL6:
            
            
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=str)
            def X(self) -> int: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_seven():
    # fourth combination
    try:     
        class CL7:
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=int)
            def X(self) -> str: ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_eight():
    # fourth combination
    try:     
        class CL8:
            
            _X: str
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=int)
            def X(self): ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_overlap_nine():
    # fourth combination
    try:     
        class CL9:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=str)
            def X(self): ...

            def method(self):
                self.X
            
        assert False
    except AnnotationOverlapError:
        assert True
        
def test_annotation_right():
    # fourth combination
    try:     
        class CL10:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(annotation_type=int)
            def X(self) -> int: ...

            def method(self):
                self.X
            
        assert True
    except AnnotationOverlapError:
        assert False
        
def test_with_no_annotation():
    # fourth combination
    try:     
        class CL11:
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty
            def X(self): ...

            def method(self):
                self.X
            
        assert False
    except AnnotationNotFoundError:
        assert True
        
        
def test_with_generic_without_validation():
    # fourth combination
    
    AutoProperty.validate_fields = False
    
    try:     
        class CL12:
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty[int]
            def X(self): ...

            def method(self):
                self.X
            
        assert True
    except AnnotationNotFoundError:
        assert False
    except:
        assert False
    finally:
        AutoProperty.validate_fields = True
        
def test_with_generic_with_validation():
    # fourth combination
    
    try:     
        class CL13:
            
            _X: int
            
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty[int]
            def X(self): ...

            def method(self):
                self.X
            
        assert True
    except AnnotationNotFoundError:
        assert False
