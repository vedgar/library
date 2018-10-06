import itertools

def primes():
    p = [2]
    yield 2
    for n in itertools.count(3, 2):
        if all(map(n.__mod__, p)):
            p.append(n)
            yield n

N = 10 ** 5
result = itertools.islice(primes(), N, N + 1)
print(*result, sep="\t")
