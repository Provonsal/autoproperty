from autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethodError
from autoproperty.prop_settings import AutoPropAccessMod


def test_private_public_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Private, s_access_mod=AutoPropAccessMod.Public)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert True
            except UnaccessiblePropertyMethodError:
                assert False

            try:
                print(self.X)
                assert False
            except:
                assert True

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert True
            except:
                assert False

            try:
                print(cls.X)
                assert False
            except:
                assert True

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert True
    except:
        assert False

    try:
        print(cls.X)
        assert False
    except:
        assert True


def test_private_protected_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Private, s_access_mod=AutoPropAccessMod.Protected)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert True
            except UnaccessiblePropertyMethodError:
                assert False

            try:
                print(self.X)
                assert False
            except:
                assert True

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert False
            except:
                assert True

            try:
                print(cls.X)
                assert False
            except:
                assert True

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert False
    except:
        assert True

    try:
        print(cls.X)
        assert False
    except:
        assert True

def test_public_private_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Public, s_access_mod=AutoPropAccessMod.Private)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert False
            except UnaccessiblePropertyMethodError:
                assert True

            try:
                print(self.X)
                assert True
            except:
                assert False

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert False
            except:
                assert True

            try:
                print(cls.X)
                assert True
            except:
                assert False

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert False
    except:
        assert True

    try:
        print(cls.X)
        assert True
    except:
        assert False
        
def test_public_protected_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Public, s_access_mod=AutoPropAccessMod.Protected)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert True
            except UnaccessiblePropertyMethodError:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert False
            except:
                assert True

            try:
                print(cls.X)
                assert True
            except:
                assert False

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert False
    except:
        assert True

    try:
        print(cls.X)
        assert True
    except:
        assert False
        
def test_protected_private_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Protected, s_access_mod=AutoPropAccessMod.Private)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert False
            except UnaccessiblePropertyMethodError:
                assert True

            try:
                print(self.X)
                assert True
            except:
                assert False

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert False
            except:
                assert True

            try:
                print(cls.X)
                assert False
            except:
                assert True

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert False
    except:
        assert True

    try:
        print(cls.X)
        assert False
    except:
        assert True
        
        
def test_protected_public_access():

    class CL1:
        def __init__(self):
            try:
                self.X = 10
                assert True
            except:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

        @AutoProperty[int](annotationType=int, access_mod=AutoPropAccessMod.Public, g_access_mod=AutoPropAccessMod.Protected, s_access_mod=AutoPropAccessMod.Public)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            try:
                self.X = 10
                assert True
            except UnaccessiblePropertyMethodError:
                assert False

            try:
                print(self.X)
                assert True
            except:
                assert False

    class CL3:
        def __init__(self):
            cls = CL1()
            try:
                cls.X = 10
                assert True
            except:
                assert False

            try:
                print(cls.X)
                assert False
            except:
                assert True

    # in home class
    CL1()

    # inside the inheritor

    CL2()

    # in unknown class
    cls = CL3()

    # outside the class

    cls = CL1()

    try:
        cls.X = 10
        assert True
    except:
        assert False

    try:
        print(cls.X)
        assert False
    except:
        assert True