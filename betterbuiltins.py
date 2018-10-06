import builtins, itertools, operator, numbers, functools
from math import inf


old_reversed = builtins.reversed
old_divmod = builtins.divmod
old_zip = builtins.zip
old_map = builtins.map
old_enumerate = builtins.enumerate
old_filter = builtins.filter
old_range = builtins.range

old_chain = itertools.chain
old_product = itertools.product
old_cycle = itertools.cycle
old_compress = itertools.compress
old_repeat = itertools.repeat
old_count = itertools.count


class _UANE:
    "Universal additive neutral element"

    def __add__(uane, other):
        return other

    def __sub__(uane, other):
        return -other

    def __mul__(uane, other):
        return uane

    __rsub__ = __radd__ = __add__
    __rmul__ = __mul__

    def __neg__(uane):
        return uane

    def __pos__(uane):
        return uane

    def __repr__(uane):
        return 'uane'


uane = _UANE()


class Sentinel:
    """A simple named sentinel."""
    
    def __init__(self, description=''):
        self.description = description

    def __str__(self):
        return str(self.description)

    def __repr__(self):
        return f'{type(self).__name__}({self.description!r})'


SAME = Sentinel('SAME')
NOT_GIVEN = Sentinel('NOT GIVEN')


def normalize_index(index, len):
    """Handle negative indices and slices, including Seq slices."""
    if isinstance(index, slice):
        return type(index)(*index.indices(len)), True
    elif isinstance(index, Seq):
        return normalize_index(index.slice, len)
    elif isinstance(index, int):
        if 0 <= index < len:
            return index, False
        elif 0 > index >= -len:
            return index + len, False
        else:
            raise IndexError(f'Invalid index {index!r}')
    else:
        raise TypeError(f"can't index by {type(index)}")


class reversed:
    """Representation of reversed sequence."""
    def __init__(self, sequence):
        self.sequence = sequence

    def __contains__(self, value):
        return value in self.sequence

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, i):
        i, isslice = normalize_index(~i, len(self))        
        if isslice:
            raise NotImplementedError('yet')
        return self.sequence[i]

    def __iter__(self):
        return old_reversed(self.sequence)

    def __reversed__(self):
        yield from self.sequence


def product(factors, start=1):
    """Product of a start value (default: 1) times an iterable of factors."""
    return functools.reduce(operator.mul, factors, start)


def divmod(dividend, *divisors):
    """Digits in a generalized positional system with divisors as bases."""
    def gen(quotient):
        for d in reversed(divisors):
            quotient, modulo = old_divmod(quotient, d)
            yield modulo
        yield quotient
    return tuple(gen(dividend))[::-1]


class zip:
    """Representation of parallel sequences."""
    def __init__(self, *iters):
        self.iters = iters

    def __iter__(self):
        return old_zip(*self.iters)

    def __len__(self):
        return min(map(len, self.iters), default=0)

    def __getitem__(self, i):
        i, isslice = normalize_index(i, len(self))
        gen = (it[i] for it in self.iters)
        if isslice:
            return type(self)(*gen)
        return tuple(gen)


class map:
    """Sequence obtained by mapping a function over one or more sequences."""
    def __init__(self, func, iter1, *iters):
        self.func, self.iters = func, (iter1,) + iters

    def __iter__(self):
        return old_map(self.func, *self.iters)

    def __len__(self):
        return min(map(len, self.iters))

    def __getitem__(self, i):
        i, isslice = normalize_index(i, len(self))
        gen = (it[i] for it in self.iters)
        if isslice:
            return type(self)(self.func, *gen)
        return self.func(*gen)


class enumerate:
    """Sequence obtained by enumerating another sequence."""
    def __init__(self, it, start=0, step=1):
        self.it, self.start, self.step = it, start, step

    def __iter__(self):
        if self.step == 1:
            return old_enumerate(self.it, self.start)
        else:
            return zip(count(self.start, self.step), self.it)

    def __getitem__(self, i):
        i, isslice = normalize_index(i, len(self))
        if isinstance(i, slice):
            return type(self)(self.it[i],
                        self.start + self.step*i.start, self.step*i.step)
        return self.start + i*self.step, self.it[i]

    def __len__(self):
        return len(self.it)

    def __contains__(self, needle):
        if not isinstance(needle, tuple) or len(needle) != 2:
            return False
        ordinal, elem = needle
        if self.step is uane or not self.step:
            return ordinal == self.start and elem in self.it
        else:
            try:
                index = Seq(len(self.it), self.start, self.step).index(ordinal)
            except ValueError:
                return False
            else:
                return self.it[index] == elem


class filter:
    """Sequence obtained by filtering via predicate (default bool)."""
    def __init__(self, pred, it=NOT_GIVEN):
        if it is NOT_GIVEN:
            self.pred, self.it = bool, pred
        else:
            self.pred, self.it = pred, it

    def __iter__(self):
        return old_filter(self.pred, self.it)

    def __contains__(self, value):
        return self.pred(value) and value in self.it


class direct_sum:
    """Sequence obtained by concatenating sequences."""
    def __init__(self, *iters):
        self.iters = iters

    def __contains__(self, value):
        return any(value in it for it in self.iters)

    def __len__(self):
        return sum(map(len, self.iters))

    def __iter__(self):
        return old_chain(*self.iters)

    def __getitem__(self, i):
        i, isslice = normalize_index(i, len(self))
        if isslice:
            raise NotImplementedError('yet')
        ...


class direct_product:
    """Sequence obtained by Cartesian multiplying of sequences."""
    def __init__(self, *iters):
        self.iters = iters

    def __contains__(self, value):
        return isinstance(value, tuple) and len(value) == len(self.iters) \
                and all(map(operator.contains, self.iters, value))

    def __iter__(self):
        return old_product(*self.iters)

    def __len__(self):
        return product(map(len, self.iters))

    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError('slicing products is not supported')
        elif isinstance(i, int):
            lens = itertools.islice(map(len, self.iters), 1, None)
            return self[divmod(i, *lens)]
        elif isinstance(i, tuple):
            if len(self.iters) != len(i):
                raise ValueError(f'Wrong dimension, expected {len(self.iters)}')
            gen = map(operator.getitem, self.iters, i)
            if all(isinstance(j, slice) for j in i):
                return type(self)(*gen)
            elif all(isinstance(j, int) for j in i):
                return tuple(gen)
            else:
                raise TypeError('mixing slicing and indexing is not allowed')
        else:
            raise TypeError('cannot index by {!r}'.format(type(i)))


def direct_power(base, exponent):
    """A Cartesian product with exponent factors all equal to base."""
    if exponent >= 0:
        return direct_product(*[base]*exponent)
    raise ValueError('exponent must be nonnegative')


class cycle:
    """Sequence obtained by cycling through another sequence."""
    def __init__(self, p):
        self.p = p

    def __iter__(self):
        return old_cycle(self.p)

    def __getitem__(self, i):
        if isinstance(i, int) and i >= 0:
            return self.p[i % len(self.p)]
        else:
            raise IndexError('invalid index {}'.format(i))

    def __contains__(self, value):
        return value in self.p


class compress:
    """Sequence obtained by compressing another sequence."""
    def __init__(self, data, selectors):
        self.data, self.selectors = data, selectors

    def __iter__(self):
        return old_compress(self.data, self.selectors)

    def __contains__(self, value):
        ... #TODO: .indices (generator or sequence, singledispatch)
        raise NotImplementedError('yet')


class Seq:
    """Universal arithmetical sequence."""
    def __init__(self, len=inf, start=0, step=1):
        if not len:
            start, step = None, uane
        elif step is None:
            step = uane
        self.len, self.start, self.step = len, start, step

    @property
    def stop(self):
        if self.len == inf:
            return None
        else:
            return self.start + self.step*self.len

    @property
    def range(self):
        return old_range(self.start, self.stop, self.step)

    @property
    def slice(self):
        if self.step is uane:
            raise ValueError('repeats cannot be represented as slices')
        return slice(self.start, self.stop, self.step)

    @classmethod
    def fromrange(cls, range):
        return cls(len(range), range.start, range.step)

    @classmethod
    def fromslice(cls, slice):
        start = slice.start or 0
        step = slice.step or 1
        if slice.stop is None:
            len_ = inf
        else:
            len_ = len(range(start, slice.stop, step))
        return cls(len_, start, step)        

    def __call__(self, len, start=0, step=1):
        len_ = min(len, self.len - start)
        if len_ <= 0:
            return Seq(0, None, uane)
        return Seq(len_, self[start], self.step * step)

    def __len__(self):
        if self.len == inf:
            raise ValueError('infinite seq has no representable len')
        else:
            return self.len

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self[self.fromslice(i)]
        elif isinstance(i, int):
            if 0 <= i < self.len:
                return self.start + self.step*i
            elif 0 > i >= -self.len:
                return self[self.len + i]
            else:
                raise IndexError('seq index out of range')
        elif isinstance(i, Seq):
            return self(i.len, i.start, i.step)
        else:
            raise TypeError('cannot slice seq by {}'.format(type(i)))

    def __contains__(self, needle):
        candidate, rest = divmod(needle - self.start, self.step)
        return rest == 0 and 0 <= candidate < self.len

    def __add__(self, other):
        if isinstance(other, Seq):
            if self.len == other.len:
                return type(self)(self.len, self.start + other.start,
                                            self.step + other.step)
            else:
                raise ValueError('Seqs with unequal lengths cannot be added')
        return type(self)(self.len, self.start + other, self.step)

    def __mul__(self, other):
        if isinstance(other, Seq):
            raise TypeError('multiplying seqs mutually is not allowed')
        else:
            return type(self)(self.len, self.start * other, self.step * other)

    __radd__ = __add__
    __rmul__ = __mul__

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __and__(self, other):
        #TODO: homework! Intersection of two Arseqs is also an ArSeq.
        ...

    def __repr__(self):
        current = [self.len, self.start, self.step]
        default = self.__init__.__defaults__
        while current and current[-1] == default[len(current) - 1]:
            del current[-1]
        return type(self).__name__ + ', '.join(map(repr, current)).join('()')

    def replace(self, *, len=SAME, start=SAME, step=SAME):
        newlen = self.len if len is SAME else len
        newstart = self.start if start is SAME else start
        newstep = self.step if step is SAME else step
        return type(self)(newlen, newstart, newstep)
            

nats = Seq(inf, 0, 1)


def repeat(elem, n=inf):
    """Sequence of n elements all equal to elem."""
    return Seq(n, elem, uane)


def count(start=0, step=1):
    """Arithmetical infinite sequence starting at start and with delta=step."""
    return Seq(inf, start, step)


def range(*args):
    """Arithmetical finite sequence."""
    return Seq.fromrange(old_range(*args))
