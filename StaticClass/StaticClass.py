__author__ = 'toadicus'

from types import FunctionType


class StaticClass(type):
    def __new__(mcs, cls, b=None, d=None):
        if b is not None and d is not None:
            cls = type(cls, b, d)
        cls.__new__ = classmethod(StaticClass.raise_on_new)

        for k, v in cls.__dict__.items():
            if isinstance(v, FunctionType):
                raise TypeError("Error creating static class '{0}': "
                                "member function '{1}' is not a class or static method".format(cls.__name__, k))

        return cls

    @staticmethod
    def raise_on_new(cls, *args, **kwargs):
        raise TypeError("Cannot create new object of type '{0}': '{0}' is a static class".format(cls.__name__))
