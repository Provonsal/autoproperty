from autoproperty import AutoProperty
from autoproperty.exceptions.Exceptions import UnaccessiblePropertyMethod
from autoproperty.prop_settings import AutoPropAccessMod


def test_str_public_parse():
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, 'public')
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # in unknown class
    try:
        cls = CL3()
        assert True
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert True
    except UnaccessiblePropertyMethod:
        assert True


def test_str_protected_parse():
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, "protected")
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessiblePropertyMethod:
        assert True


def test_str_private_parse():

    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, "private")
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessiblePropertyMethod:
        assert True


def test_int_public_parse():
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, 0)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # in unknown class
    try:
        cls = CL3()
        assert True
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert True
    except UnaccessiblePropertyMethod:
        assert True


def test_int_protected_parse():
    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, 1)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessiblePropertyMethod:
        assert True


def test_int_private_parse():

    class CL1:
        def __init__(self):
            self.X = 10
            print(self.X)

        @AutoProperty(int, 2)
        def X(self): ...

    class CL2(CL1):
        def __init__(self):
            self.X = 10
            print(self.X)

    class CL3:
        def __init__(self):
            cls = CL1()
            cls.X = 121
            print(cls.X)

    # in home class
    try:
        CL1()
        assert True
    except UnaccessiblePropertyMethod:
        assert False

    # inside the inheritor
    try:
        CL2()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # in unknown class
    try:
        cls = CL3()
        assert False
    except UnaccessiblePropertyMethod:
        assert True

    # outside the class
    try:
        cls = CL1()
        cls.X = 100
        print(cls.X)
        assert False
    except UnaccessiblePropertyMethod:
        assert True
