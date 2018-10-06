def primes():
    yield 2
    d, n, i = [2], 3, 0
    while True:
        if not n % d[i]:
            n, i = n + 2, 0
        elif d[i] ** 2 > n:
            yield n
            d.append(n)
            n, i = n + 2, 0
        else: i += 1
for p in primes():
    if p>700: break
    print(p,end=" ");
