from autoproperty import AutoProperty
from autoproperty.prop_settings import AutoPropAccessMod


class MyClass:

    _y: int = 20

    def __init__(self):
        print("Внутри родного класса. Автосвойство X до изменения: ", self.X)
        self.X = 100
        print("Внутри родного класса. Автосвойство X после изменения: ", self.X)

    @AutoProperty(int, access_mod=AutoPropAccessMod.Public, g_access_mod = AutoPropAccessMod.Public, s_access_mod=AutoPropAccessMod.Private)
    def X(self, lol: int = 10) -> None: ...

    @property
    def Y(self): return self._y

    @Y.setter
    def Y(self, value): self._y = value


class MyClass2(MyClass):
    def __init__(self):

        # print("Внутри потомка класса. Автосвойство X до изменения: ", self.X)
        print("Внутри потомка класса. Автосвойство X после изменения: ", self.X)
        self.X = 12


def test1():
    g = MyClass()
    t = MyClass2()
    print("Снаружи классов. Автосвойство X до изменения: ", g.X)
    g.X = 12
    print("Снаружи классов. Автосвойство X после изменения: ", g.X)


test1()
