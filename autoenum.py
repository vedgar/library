# comment that started it all:
#  http://www.acooke.org/cute/Pythonssad0.html
#  Date: Fri, 17 May 2013 15:19:04 +0100

import enum, itertools, contextlib, collections

if False:
    class AutoEnumMeta(type):
        @classmethod
        def __prepare__(meta, *whatever):
            return collections.defaultdict(itertools.count().__next__)
    class MyClass(metaclass=AutoEnumMeta):
        a, b, c
    print(MyClass.a, MyClass.b, MyClass.c)

class AutoEnumMeta(enum.EnumMeta):
    @classmethod
    def __prepare__(meta, *args, **kw):
        namespace = super().__prepare__(*args, **kw)
        assert isinstance(namespace, dict)
        count = itertools.count(1)
        class AutoDict(type(namespace)):
            def __missing__(self, key):
                if not key.startswith('__'):
                    value = next(count)
                    self[key] = value
                    return value
        namespace.__class__ = AutoDict
        return namespace

class AutoEnum(enum.Enum, metaclass=AutoEnumMeta):
    pass

class Color(AutoEnum):
    red, green, blue

    def f(self):
        print(self.name, '=', self.value)

# Color.blue.f()

def flagger(enumtype):
    assert issubclass(enumtype, enum.Enum)
    class FlagsHelper(Flags):
        _fh_enum = enumtype
        def __new__(cls, value):
            with contextlib.suppress(ValueError):
                return enumtype(value)
            self = super(FlagsHelper, cls).__new__(cls)
            self.enum, self._value_ = enumtype, value
            inv = self.inverted = value < 0
            if inv:
                value = ~value
            constituents = list()
            while value:
                current = 1 << value.bit_length()-1
                constituents.append(enumtype(current))
                value &=~ current
            self.set = frozenset(constituents)
            cnames = '|'.join(c.name for c in reversed(constituents))
            self._name_ = '~'*inv + cnames.join('()')
            return self
        __str__ = enum.Enum.__str__
        __repr__ = enum.Enum.__repr__
    FlagsHelper.__name__ = enumtype.__name__
    return FlagsHelper

def get_enum(v):
    t = type(v)
    return getattr(t, '_fh_enum', t)

def common_enum(v1, v2):
    t1 = get_enum(v1)
    t2 = get_enum(v2)
    if t1 is t2:
        return t1
    raise TypeError(f"Incompatible enum types {t1} and {t2}")
    
class Flags:
    def __or__(self, other):
        common = flagger(common_enum(self, other))
        return common(self._value_ | other._value_)

    def __and__(self, other):
        common = flagger(common_enum(self, other))
        return common(self._value_ & other._value_)

    def __invert__(self):
        return flagger(get_enum(self))(~self._value_)

class FlagEnum(Flags, enum.Enum):
    pass

class Move(FlagEnum):
    UP = 0b100
    DOWN = 0b1000
    LEFT = 0b1
    RIGHT = 0b10

print((Move.LEFT | Move.UP) | (Move.DOWN | Move.UP))

#TODO:
# probably simpler solution: every enum has its own flaghelper
# whose instances remember enumtype, frozenset and bool inv

#TODO:
# combine this with AutoEnum, so bits are given
# values 1, 2, 4, 8, 16... automatically
