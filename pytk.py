import itertools, tkinter, weakref
from tkinter import ttk


def is_coord(index):
    return isinstance(index, tuple) and len(index) == 2


def rangify(coord):
    if isinstance(coord, slice):
        return range(coord.start or 0, coord.stop)
    else:
        return [coord]


def tktype(value):
    if isinstance(value, bool):
        return bool, tkinter.BooleanVar
    elif isinstance(value, int):
        return int, tkinter.IntVar
    elif isinstance(value, str):
        return str, tkinter.StringVar
    elif isinstance(value, float):
        return float, tkinter.DoubleVar
    else:
        raise TypeError(f"Unknown type {type(value)}")


class Subscriptable:
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__grid = {}

    def __getitem__(self, index):
        if is_coord(index):
            return self.__grid[index]
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        if is_coord(index):
            rows, cols = map(rangify, index)
            coords = list(itertools.product(rows, cols))
            if isinstance(value, (tuple, list)):
                assert len(value) == len(coords), 'lenghts differ'
                for (i, j), widget in zip(coords, value):
                    widget.grid(row=i, column=j, in_=self)
            else:
                opts = dict(row=min(rows), column=min(cols), in_=self)
                if isinstance(rows, range):
                    opts['rowspan'] = len(rows)
                if isinstance(cols, range):
                    opts['columnspan'] = len(cols)
                value.grid(**opts)
        else:
            super().__setitem__(index, value)

    def __delitem__(self, index):
        if is_coord(index):
            self.__grid[index].grid_forget()
        else:
            super().__delitem__(index)


class Keyable:
    def __init__(self, *args, **kw):
        self.__cached_keys = []
        super().__init__(*args, **kw)
        self.__cached_keys = self.keys()

    def __getattr__(self, attr):
        if attr in self.__cached_keys:
            return self[attr]
        raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if not attr.startswith('_') and attr in self.__cached_keys:
            self[attr] = value
        else:
            super().__setattr__(attr, value)

    def __delattr__(self, attr):
        if attr in self.__cached_keys:
            del self[attr]
        else:
            super().__delattr__(attr)


class Decoratable:
    def __call__(self, func):
        self.command = func
        func.master = self
        return func


class TextFirst:
    def __init__(self, text, **rest):
        return super().__init__(text=text, **rest)


class Descriptable:
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for dvar in vars(type(self)).values():
            if isinstance(dvar, DescriptorVariable):
                var = dvar.tktype(value=dvar.default)
                dvar.instances[self] = self[dvar.tkattr] = var


class DescriptorVariable:
    def __init__(self, tkattr, default=''):
        super().__init__()
        self.instances = weakref.WeakKeyDictionary()
        self.tkattr = tkattr
        self.default = default
        self.type, self.tktype = tktype(default)

    def instance_var(self, instance):
        if instance in self.instances:
            var = self.instances[instance]
        else:
            var = self.instances[instance] = self.tktype(value=self.default)
            setattr(instance, self.tkattr, var)
        return var

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.type(self.instances[instance].get())

    def __set__(self, instance, value):
        self.instances[instance].set(self.type(value))

    def __delete__(self, instance):
        del self.instances[instance]
        delattr(instance, self.tkattr)


class Tk(Keyable, Subscriptable, tkinter.Tk):
    pass


root = Tk()


class Frame(Keyable, Subscriptable, ttk.Frame):
    pass


class Button(Keyable, Decoratable, TextFirst, ttk.Button):
    pass


class Label(Keyable, TextFirst, ttk.Label):
    pass


class Entry(Keyable, Descriptable, ttk.Entry):
    text = DescriptorVariable('textvariable')


class Checkbox(Keyable, TextFirst, Descriptable, ttk.Checkbutton):
    on = DescriptorVariable('variable', False)


def Var(init=''):
    return tktype(init)[1](root, init)
