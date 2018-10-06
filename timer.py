from sys import modules
from types import ModuleType
from time import perf_counter as pc
from importlib.util import module_from_spec
from datetime import timedelta


class Stopwatch:
    __slots__ = ['start']
    
    def __get__(self, owner, cls, *, _pc=pc):
        self.start = _pc()
        return self

    def __call__(self, timed, *, _pc=pc):
        delta = _pc() - self.start
        print(f"Elapsed: {timedelta(seconds=delta)}")
        return timed


class Substitute(ModuleType):
    time = Stopwatch()


substitute = module_from_spec(__spec__)
substitute.__all__ = ['time']
substitute.__class__ = Substitute
modules[__name__] = substitute
