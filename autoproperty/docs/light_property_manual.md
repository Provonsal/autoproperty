# Light AutoProperty info

## Table of content

- [Info](#info)
- [Example](#example)
- [Annotations](#annotations)
- [Validation](#validation)

## Info

This light version of autoproperty was developed for high load projects. It dont have most fields that basic autoproperty has for more speed and light weight and less memory costs.

By the way it is build with Cython, that's why it is faster than the regular autoproperty.

## Example

```python
from autoproperty import LightAutoProperty


class Book:
    def __init__(self, title):
        self.title = title

    @LightAutoProperty # Never use brackets like [type] as for generic
    def title(self) -> str: ... # For type annotation use
                                # only return type hint
```

## Annotations

Actually you dont need to write annotations, LightAutoProperty has no type validation, so you need to pass only one type hint: in function's return hint like as in example above.

## Validation

Due absence of validation, you have to control types by yourself.