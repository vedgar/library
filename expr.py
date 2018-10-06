import collections, operator, fractions, contextlib, decimal, math, abc


Operator = collections.namedtuple('Operator',
                                  'symbol name dunder func prec arity assoc')
opdict = {name: Operator(symbol, name, f"__{name.strip('_')}__",
                getattr(operator, name), prec, 1 if prec == 8 else 2,
                'left' if prec < 8 else 'right')
        for prec, prec_ops in enumerate([
            dict(or_='|'), dict(xor='^'), dict(and_='&'),
            dict(lshift='<<', rshift='>>'),
            dict(add='+', sub='-'),
            dict(mul='*', truediv='/', mod='%', floordiv='//', matmul='@'),
            dict(invert='~', pos='+', neg='-'),
            dict(pow='**'),
        ], 2) for name, symbol in prec_ops.items()}
ops = frozenset(opdict.values())
op = type('operator', (), opdict)


def sub(expr, parenthesize):
    """Parenthesizes the subexpression if necessary."""
    return f"({expr})" if parenthesize else f"{expr}"


class Expr(abc.ABC):
    """Mixin class whose operators build simple trees."""
    for op in ops:
        if op.arity == 1:
            ar = 'unary'
            def _impl(self, *, _op=op):
                return Compound(_Null(), _op, self)
        else:
            ar = 'binary'
            def _impl(self, other, *, _op=op):
                return Compound(self, _op, other)
        _impl.__name__ = op.dunder
        _impl.__doc__ = f"Implements {ar} operator {op.symbol!r}."
        vars()[op.dunder] = _impl
    del op, ar, _impl

    @abc.abstractmethod
    def at(self, depth):
        """Formats the expression at a given depth (precedence)."""

    @abc.abstractmethod
    def value(self):
        """Value of an expression (when evaluated)."""


class _Null(Expr):
    def at(self, depth):
        return ''

    def value(self):
        pass


class Compound(Expr, collections.namedtuple('Tree', 'left op right')):
    """Compound expression."""
    def at(self, depth):
        prec = lprec = rprec = self.op.prec
        if self.op.assoc == 'left':
            rprec += .1
        elif self.op.assoc == 'right':
            lprec += .1
        if self.op is op.pow:
            rprec -= 1
        items = self.left.at(lprec), self.op.symbol, self.right.at(rprec)
        sep = ' ' * (prec <= 6)
        return sub(sep.join(items), prec < depth)

    def value(self):
        args = (self.left.value(), self.right.value())[2 - self.op.arity :]
        return self.op.func(*args)

    def __str__(self):
        return self.at(0).strip()


def Const(T, group=None):
    """Factory for constants of type T at given precedence grouping."""
    prec = math.inf if group is None else group.prec
    class _result(Expr, T):
        def value(self):
            return T(self)

        def at(self, depth):
            result = str(T(self)).strip('()')
            return sub(result, prec < depth and not result.isdigit())

    _result.__name__ = T.__name__
    return _result


Fraction = Const(fractions.Fraction, op.truediv)
Integer = Const(int, op.neg)
Complex = Const(complex, op.add)
Decimal = Const(decimal.Decimal, op.neg)
