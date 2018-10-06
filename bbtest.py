from builtins import reversed

r = reversed([2, 5, 3])
# print(r[2])
# print(reversed(r))
print(5 in r, 2 in r, 5 in r)

from betterbuiltins import reversed

r = reversed([2, 5, 3])
print(5 in r, 2 in r, 5 in r, 7 in r)
print(r[2])
print(*reversed(r))

from builtins import zip

i1, i2, i3, i4 = iter('ABCDE'), iter('ghi'), iter('abc'), iter('FGHIJ')
z = zip(i1, i2, i3, i4)
print(*z)
print(next(i2, None), next(i4, None), next(i1, None))

from betterbuiltins import zip

z = zip('ABCDE', 'ghi', 'abc', 'FGHIJ')
print(z[1], z[-1])
print(*reversed(z))

from builtins import map

m = map(pow, [2, 3, 1, 8, 3], [6, 3, 9, 7], [12, 9, 45, 99])
# print(m[:2])
numbers = map(int, '123 456 678'.split())
# print(max(numbers) - min(numbers))

from betterbuiltins import map

m = map(pow, [2, 3, 1, 8, 3], [6, 3, 9, 7], [12, 9, 45, 99])
print(*m)
print(*m[-2:])
numbers = map(int, '123 456 678'.split())
print(max(numbers) - min(numbers))

from builtins import filter

f = filter(callable, [7, print, ..., SyntaxError])
print(SyntaxError in f, print in f)

from betterbuiltins import filter

f = filter(callable, [7, print, ..., SyntaxError])
print(SyntaxError in f, print in f)

from builtins import enumerate

...
