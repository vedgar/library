def Erathostenes(m=10**4):
    s = set(range(2, m))
    while s:
        n = min(s)
        s.difference_update(range(n, m, n))
        yield n

checkio = lambda n: n in Erathostenes(n + 1)

print(list(Erathostenes(100)))
