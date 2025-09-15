# Basic usage example

## Table of content

- [Example](#start)
- [Annotation](#annotations)  
    - [Annotation overlap](#annotation-overlap)
- [Validation](#validation)
    - [Turn off validation](#turn-off-validation) 

## Example

Here is an example. Wait a minute, look at it, remember and then we will go further.

```python
from autoproperty import AutoProperty


class Book:
    def __init__(self, title):
        self.title = title

    @AutoProperty[str]
    def title(self) -> str: ...
```

## Annotations

Lets take a look closer, first we'll look at annotations. It is pretty important if the field validation is on.

Here it is. You can put type annotation into one of 3 different places (as you like to):

1. In **class body annotation**.
2. In **parameters** of autoproperty.
3. In **function return** annotation.

```python
from autoproperty import AutoProperty


class Book:
    
    title: str # <- Class body annotation

    def __init__(self, title):
        self.title = title

    @AutoProperty[str](annotation_type=str)# <- Parameters annotation
    def title(self) -> str: ...
                      # ^ Return annotation
```

### Annotation overlap

All annotation in any of these **3 places** should be the same as in exmaple above. Otherwise if **at least one** of the annotations will be different on creating phase autoproperty **will raise** an "AnnotationOverlapError" error.  

Be careful with that. Better to define annotation in one place or just turn off the validation and error will never appear.

```python
from autoproperty import AutoProperty


class Book:
    
    title: bytearray # <- Different class body annotation

    def __init__(self, title):
        self.title = title

    @AutoProperty[str](annotation_type=str)# <- Parameters annotation
    def title(self) -> str: ...
                      # ^ Return annotation

book = Book("a book") # AnnotationOverlapError: "Type annotation is different"
```

## Validation

Validation is provided by **pydantic** module. Especially library using **validate_call** with **parsing turned off**. 

So if **validation is on** and you trying to assign **a new value** with **wrong type** that will **raise a ValidationError**.

```python
from autoproperty import AutoProperty


class Book:
    
    title: str # Class body annotation

    def __init__(self, title):
        self.title = title

    @AutoProperty[str]
    def title(self): ...

book = Book("a book")
book.title = "a different book" # Fine
book.title = 42 # ValidationError
```

### Turn off validation

If you want to, you can turn off validation and setters will turn faster like ~x20 times. And of course no errors.

```python
from autoproperty import AutoProperty


# Change this static value to change the behavior.
AutoProperty.validate_fields = False

class Book:
    
    title: bytearray # <- Different class body annotation

    def __init__(self, title):
        self.title = title

    @AutoProperty[str](annotation_type=str)
    def title(self) -> str: ...

book = Book() # no error
```