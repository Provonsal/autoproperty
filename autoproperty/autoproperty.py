from functools import lru_cache
from time import time
from types import UnionType
from typing import Any, Callable, Generic, Self, TypeVar, cast, get_type_hints
from warnings import warn


from autoproperty.autoproperty_methods.autoproperty_getter import AutopropGetter
from autoproperty.events.event import Event
from autoproperty.fieldvalidator import FieldValidator
from autoproperty.autoproperty_methods import AutopropSetter
from autoproperty.interfaces.autoproperty_methods import IAutopropGetter, IAutopropSetter
from autoproperty.interfaces.events import IEvent, IListener


T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

class AutoProperty(Generic[T]):

    __slots__ = ('annotation_type', 
                 'setter', 
                 'getter', 
                 '__doc__', 
                 '_field_name', 
                 'prop_name',
                 '_found_annotations',
                 'cache',
                 'operation_event')

    # fields annotation
    annotation_type: type | UnionType | None
    setter: IAutopropSetter | None
    getter: IAutopropGetter | None
    _field_name: str | None
    prop_name: str | None
    _found_annotations: list
    cache: bool
    operation_event: IEvent | None
    
    # static fields
    validate_fields: bool = True

    def __init__(
        self,
        func: Callable[..., Any] | None = None,
        annotation_type: type | UnionType | None = None,
        cache: bool = False,
        events: bool = False
    ):
        
        self.prop_name = None
        self.annotation_type = annotation_type
        self.setter = None
        self.getter = None
        self._field_name = None
        self._found_annotations = []
        self.cache = cache
        self.operation_event = Event() if events else None

        if self.annotation_type is not None:
            self._found_annotations.append(self.annotation_type)

        if func is not None:
            self._setup_from_func(func)

    def subscribe(self, listener: IListener):
        if self.operation_event is not None:
            self.operation_event.subscribe(listener)
        else:
            warn("Event system is offline. Subscriptions will no make anything.")

    def _get_debug_cache_info(self):
        """
        Retrieves debug cache information if the property has caching enabled.

        Returns:
            The cache info of the getter function if caching is enabled.
        """
        if self.cache:
            if self.getter is not None:
                return self.getter.cache_info() # pyright: ignore[reportAttributeAccessIssue]

    def _setup_from_func(self, func: Callable[..., Any]) -> None:
        """
        Initializes the AutoProperty instance from a given function.

        Extracts relevant information such as function name and annotations,
        and sets up the property accordingly.

        Args:
            func (Callable[..., Any]): The function to initialize the property with.
        """
        
        # Extracting function name and creating a 
        # name for field in the instance
        self.prop_name = func.__name__
        self._field_name = f"_{func.__name__}"

        # Extracting annotations
        hints = get_type_hints(func)
        
        # Caching annotation for return
        return_hint = hints.get('return')
        
        # If found then assigning annotation to field
        if return_hint is not None:
            self._found_annotations.append(return_hint)
            
        # Starting setting up getter, setter we will set later
        # after we get all annotations from all places
        self._setup_getter(self.prop_name, self._field_name)

    def _setup_getter(self, prop_name: str, field_name: str) -> None:
        """
        Creates a getter for the AutoProperty instance.

        Args:
            prop_name (str): The name of the property.
            field_name (str): The name of the field in the instance.
        """
        
        # Creating getter
        getter = AutopropGetter[T](prop_name, field_name, self)
        
        # If need to cache then wrapping getter with cache decorator
        if self.cache:
            decorated_getter = lru_cache()(getter)
            self.getter = decorated_getter # pyright: ignore[reportAttributeAccessIssue]
        else:
            self.getter = getter

    def _setup_setter(self, prop_name: str, _field_name: str, annotation_type: UnionType | type | None) -> None:
        """
        Creates a setter for the AutoProperty instance.

        Args:
            prop_name (str): The name of the property.
            field_name (str): The name of the field in the instance.
            annotation_type (type | None): The annotation type of the property.
        """
        
        # Creating setter
        setter = AutopropSetter(prop_name, _field_name, annotation_type, self)
        
        # If need to valdiate then wrapping setter with field validator 
        if self.validate_fields:
            setter_with_validator = FieldValidator(_field_name, self._found_annotations)(setter)
            self.setter = cast(AutopropSetter, setter_with_validator)
        else:
            # else just assigning setter
            self.setter = setter

    def _setup_getter_setter(self) -> None:
        """
        Sets up the getter and setter for the AutoProperty instance.

        This method is called after setting up the property from a function.
        """
        
        # Checking if got name from the function and have created the field name
        if self.prop_name is not None and self._field_name is not None:

            self._setup_getter(self.prop_name, self._field_name)
            self._setup_setter(self.prop_name, self._field_name, self.annotation_type)  
    
    def __set_name__(self, owner: type, name: str) -> None:
        """
        This method is called after `__init__` to allow the class to act as a descriptor.
        
        It sets up the property's name and field name based on the provided information.
        If validation fields are enabled, it attempts to retrieve annotations from the owner class
        and set up the setter function accordingly.

        Args:
            owner (type): The type of the class that owns this descriptor.
            name (str): The name of the property within the owning class.

        Returns:
            None
        """
        
        # Set up property name if not already done
        if self.prop_name is None:
            self.prop_name = name  # Store the property name for future use
        
        # Determine field name from owner's class field name if not already done
        if self._field_name is None:
            self._field_name = f"_{name}"  # Prefix with underscore for conventional naming

        # If validation fields are enabled, attempt to retrieve annotations from the owner class
        if self.validate_fields:
            
            # Get type hints (annotations) from the owning class
            hints = get_type_hints(owner)
            
            # Cache annotation for future use
            annotation = hints.get(self._field_name)
            
            # If an annotation is found, add it to the list of found annotations and set up the setter
            if annotation is not None:
                self._found_annotations.append(annotation)  # Add to list of found annotations
                self._setup_setter(self.prop_name, self._field_name, self.annotation_type)

        # Set up getter and/or setter functions based on current state
        if (self.setter is None or self.getter is None):
            self._setup_getter_setter()  # Initialize both getter and setter
        elif self.setter is None:
            self._setup_setter(self.prop_name, self._field_name, self.annotation_type)  # Only set up setter
        elif self.getter is None:
            self._setup_getter(self.prop_name, self._field_name)  # Only set up getter

    def __call__(
        self,
        func: Callable[..., Any]
    ) -> Self:
        """
        Initializes the AutoProperty instance from a function.

        Args:
            func: The function to initialize the property with. Its docstring will be used as the property's docstring.

        Returns:
            A reference to the initialized AutoProperty instance.
        """
        
        # Set the property's docstring
        self.__doc__ = func.__doc__
        
        # Initialize the property from the given function
        self._setup_from_func(func)
        
        return self

    def __set__(self, instance, obj: object) -> None:
        """
        Sets the value of an attribute on an instance.

        Args:
            instance: The instance that owns the attribute being set.
            obj: The new value to be assigned to the attribute.

        Raises:
            RuntimeError: If the property was not properly initialized.
        """
        
        # Check if the setter function has been provided
        if self.setter is None:
            raise RuntimeError(f"AutoProperty '{self.prop_name}' was not properly initialized.")
            
        if self.operation_event is not None:
            
            method_type = self.setter.__wrapped__.__self__.__method_type__ if hasattr(self.setter, '__wrapped__') else self.setter.__method_type__ # pyright: ignore[reportAttributeAccessIssue]
            
            self.operation_event.trigger(
                method_type, 
                self.prop_name, 
                new_value=obj.__repr__(), 
                time=time()
            )
            
        # Call the setter function with the instance and object as arguments
        self.setter(instance, obj)

    def __get__(self, instance, owner=None) -> T | None:
        """
        Gets the value of an attribute from an instance.

        Args:
            instance: The instance that owns the attribute being accessed.
            owner: The type of the class that defines the property (default is None).

        Returns:
            The value of the attribute if the instance exists, otherwise the property itself.

        Raises:
            RuntimeError: If the property was not properly initialized.
        """
        
        # If the instance does not exist, return the property itself
        if instance is None:
            return self # pyright: ignore[reportReturnType]
        
        try:
            # Attempt to get the attribute value using the getter function
            gotten_value = self.getter(instance, owner=owner) # pyright: ignore[reportOptionalCall]
            
            if self.operation_event is not None:
                
                self.operation_event.trigger(
                    self.getter.__method_type__,  # pyright: ignore[reportOptionalMemberAccess]
                    self.prop_name, 
                    gotten_value, 
                    time=time()
                ) # pyright: ignore[reportOptionalMemberAccess]
            
            return gotten_value
        except:
            # If an error occurs, raise a RuntimeError with a descriptive message
            raise RuntimeError(f"AutoProperty '{self.prop_name}' was not properly initialized.")

        
