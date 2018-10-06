def primes(to=None):
    n=2
    while n!=to:
        for d in primes(n):
            if not n%d: break
        else: yield n
        n+=1
for p in primes(100):
    print(p)
