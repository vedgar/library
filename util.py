class _Arg:
    def __getitem__(self, index):
        return _Var(index, kw=False)

    def __getattr__(self, attr):
        return _Var(attr, kw=True)


class _Var:
    def __init__(self, arg, *, kw):
        self.kw = kw
        self.arg = arg

    def __call__(self, *args, **kwargs):
        return (kwargs if self.kw else args)[self.arg]


arg = _Arg()
item = arg[0]
