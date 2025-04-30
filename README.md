# AutoProperty library

## What it used for?

I wrote this library for my own uses and points. I think it is very comfy to use and less code to write.  

I just have enough of writting millions and trillions of "@property" and setters for them. It also have type validation, just like a bonus.

## How does this work?

Basically it is just a common **property** or **data descriptor** (if you feel better to call it like that) but instead of storing the providing **private** (optionally) class attribute inside itself, it creating the attribute by itself inside the containing class instance. 

You **do not need** to do anything - only smoke the cigarrete, throw legs on a table and rest. Let it keep all hard boring work. You are the **king** and you **deserve** no other treatment.

Jokes aside, it do all hard work, let me show you.

```python
class Exmpl:
    @AutoProperty[int] # <-- it will check type it accepting in getter
    def SomeProp(self): ... # <-- no need to implement, it won't change anything
                            # only thing is matter is the name of a method
```

In runtime it turns construction above to construction below:

```python
class Exmpl:
    __someProp: int

    @AutoProperty[int]
    def SomeProp(self): ...
```

By default autoproperty has private access:

```python
class Exmpl:
    @AutoProperty[int]
    def SomeProp(self): ...

    def __init__(self):
        self.SomeProp = 42 # ok

example = Exmpl()
print(example.SomeProp) # Error: UnaccessiblePropertyMethod
```

>I dont know how to fix it but even python debugger in VSCode cant go against it, if you do know please open an issue and **tell me**. I'll appreciate that.



## Full example

```python
from autoproperty import AutoProperty


class Point:
    def __init__(self, *args, **kwargs):
        ... # do smth

    # by default it has private access
    @AutoProperty[int](access_mod="public")
    def X(self): ...

    @AutoProperty[int](access_mod="public")
    def Y(self): ...

    def __repr__(self) -> str:
        return f"[{self.X};{self.Y}]"

myPointOne = Point()

myPointOne.X = 2
myPointOne.Y = 6

print(myPointOne) # [2; 6]
```