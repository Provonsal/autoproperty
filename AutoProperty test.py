from utils import AutoProperty
from utils.prop_settings import AutoPropAccessMod


class MyClass:

    _y: int = 20

    def __init__(self):
        print("Внутри родного класса. Автосвойство X до изменения: ", self.X)
        self.X = 100
        print("Внутри родного класса. Автосвойство X после изменения: ", self.X)

    @AutoProperty(int, AutoPropAccessMod.Protected)
    def X(self, lol: int = 10) -> None: ...

    @property
    def Y(self): return self._y

    @Y.setter
    def Y(self, value): self._y = value


class MyClass2(MyClass):
    def __init__(self):

        print("Внутри потомка класса. Автосвойство X до изменения: ", self.X)
        self.X = 12
        print("Внутри потомка класса. Автосвойство X после изменения: ", self.X)


def test1():
    g = MyClass()
    t = MyClass2()
    print("Снаружи классов. Автосвойство X до изменения: ", g.X)
    g.X = 12
    print("Снаружи классов. Автосвойство X после изменения: ", g.X)


test1()
