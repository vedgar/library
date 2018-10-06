# https://mail.python.org/pipermail/python-list/2009-January/520422.html
import itertools
def sieve():
    innersieve, prevsquare, table = sieve(), 1, {}
    for i in itertools.count(2):
        try:
            nextprime, prime = i, table[i]
            while nextprime in table: nextprime += prime
            table[nextprime] = prime
            del table[i]
        except KeyError:
            yield i
            if i > prevsquare:
                j = next(innersieve)
                prevsquare = j ** 2
                table[prevsquare] = j
print(*itertools.islice(sieve(), 270), sep='\t')
