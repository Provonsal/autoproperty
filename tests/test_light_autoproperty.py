from autoproperty import LightAutoProperty


def test_basic_work():
    try:     
        class CL13:
                        
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @LightAutoProperty
            def X(self) -> int: ...

            def method(self):
                self.X
            
        CL13()
            
        assert True
    except:
        assert False