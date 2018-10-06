"""Tools for enforcing types of class attributes.

Usage:
>>> from enforce import Restricted
>>> class A(Restricted, x=int, y=str): pass

>>> a = A()
>>> a.x = 4
>>> a.y = 2
TypeError: A.y should be str, not int
>>> a.z = 3
AttributeError: 'A' object has no attribute 'z'
"""


import unittest


__all__ = ['Restricted']


class RestrictedMeta(type):
    def __new__(meta, *args, **_):
        return super().__new__(meta, *args)

    def __init__(cls, *_, **attrs):
        cls._attrs = attrs


def tname(value):
    """Name of value's type (or value itself if it is a type)."""
    if not isinstance(value, type):
        value = type(value)
    return value.__name__


class Restricted(metaclass=RestrictedMeta):
    """Mixin for classes with restricted attributes.

    Usage: class MyClass(Restricted, attr1=type1, attr2=type2,...): ...
    """
    def __setattr__(self, attr, value):
        try:
            required_type = self._attrs[attr]
            assert isinstance(value, required_type)
            super().__setattr__(attr, value)
        except KeyError:
            msg = '{!r} object has no attribute {!r}'.format(tname(self), attr)
            raise AttributeError(msg) from None
        except AssertionError:
            msg = '{}.{} should be {}, not {}'.format(
                tname(self), attr, tname(required_type), tname(value))
            raise TypeError(msg) from None


class TestRestricted(unittest.TestCase):
    def setUp(self):
        class A(Restricted, x=int, y=str):
            pass

        self.a = A()

    def test_normal_operation(self):
        self.a.x = 4
        self.assertEqual(self.a.x, 4)

    def test_attribute_missing(self):
        with self.assertRaisesRegex(AttributeError, "object has no attribute"):
            self.a.z = 3

    def test_wrong_type(self):
        with self.assertRaisesRegex(TypeError, '^A.y should be str, not int$'):
            self.a.y = 2
