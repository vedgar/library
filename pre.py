import functools
from re import (I, compile, escape as lit, findall, finditer,
                fullmatch, match, search, split, sub)

_enclosed = lambda r, d: (r.rfind(d[0]), r.find(d[~0])) == (0, len(r) - 1)
atomic = lambda r: any((
    len(r) <= 1, len(r) == 2 and r.startswith('\\'),
    _enclosed(r, '[]'), _enclosed(r, '()'),
))
group = lambda r: f'(?:{r})'
atom = lambda r: r if atomic(r) else group(r)
_name = lambda name: '' if name is None else f'?P<{lit(name)}>'
capture = lambda r, name=None: f'({_name(name)}{r})'

anychar, start, end = '.^$'
starts, ends, digit, wordchar, space, wordboundary = map('\\'.__add__, 'AZdwsb')
nondigit, nonwordchar = digit.upper(), wordchar.upper()
nonspace, nonwordboundary = space.upper(), wordboundary.upper()
ascii_lowercase, ascii_letter = '[a-z]', '[a-zA-Z]'
ascii_uppercase = ascii_lowercase.upper()

def digitrange(start, stop=None):
    if stop is None: start, stop = 0, start
    from string import digits, ascii_lowercase, ascii_uppercase
    row = (digits + ascii_lowercase)[start:stop]
    def pretty(sel):
        res = list(filter(sel, row))
        if len(res) < 4: return ''.join(res)
        return f'{res[0]}-{res[~0]}'
    digs, lets = pretty(str.isdigit), pretty(str.isalpha)
    return f'[{digs}{lets}{lets.upper()}]'

def repeat(r, min=0, max=None, *, greedy=True):
    min, max = str(int(min or 0)), '' if max is None else str(int(max))
    rep = min if min == max else min + ',' + max
    if rep == '0,1': rep = '?'
    elif rep == '0,': rep = '*'
    elif rep == '1,': rep = '+'
    else: rep = rep.join('{}')
    return f'{atom(r)}{rep}{"?" * (not greedy)}'

minimal = functools.partial(repeat, greedy=False)
optional = functools.partial(repeat, max=1)
anyof = lambda *rs: f'[{lit(*rs)}]' if len(rs) == 1 else atom('|'.join(rs))
noneof = lambda s: f'[^{lit(s)}]'

flag = lambda f: '(?{lit(f)})'
again = lambda g: f'\\{g}' if isinstance(g, int) else f'(?P={g})'
lookassert = lambda r, occur=True, *, reverse=False: \
    f'(?{"<" * bool(reverse)}{"=" if occur else "!"}{r})'
conditional = lambda g, yes='', no='': f'(?({lit(g)}){atom(yes)}|{atom(no)})'
put = lambda g: f'\\g<{lit(str(g))}>'
