from autoproperty.autoproperty import AutoProperty
from autoproperty.events.context import EventContext
from autoproperty.events.listener import Listener
from autoproperty.prop_settings import AutoPropType


def test_event_handling_work():


    def action(context: EventContext) -> None:
        print('data: ', context.data, ' filters: ', context.filters)
        

    try:     
        get_listener = Listener(action, (AutoPropType.Getter, "X"))
        set_listener = Listener(action, (AutoPropType.Setter, "X"))
        
        class MyClass:
                        
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(events=True)
            def X(self) -> int: ...

            X.subscribe(get_listener)
            X.subscribe(set_listener)

            def method(self):
                self.X
            
        MyClass()
        
        if get_listener.trigger_count and set_listener.trigger_count:
            
            assert True
        else:
            assert False
    except:
        assert False
        

def test_event_handling_should_not_work():


    def action(context: EventContext) -> None:
        print('data: ', context.data, ' filters: ', context.filters)
        

    try:     
        get_listener = Listener(action, (AutoPropType.Getter, "X"))
        set_listener = Listener(action, (AutoPropType.Setter, "X"))
        
        class MyClass:
                        
            def __init__(self):
                self.X = 12
                print(self.X)
                
            @AutoProperty(events=False)
            def X(self) -> int: ...

            X.subscribe(get_listener)
            X.subscribe(set_listener)

            def method(self):
                self.X
            
        MyClass()
        
        if get_listener.trigger_count and set_listener.trigger_count:
            
            assert False
        else:
            assert True
    except:
        assert False    