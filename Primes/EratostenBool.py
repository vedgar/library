N = 10**6 + 1
isPrime = [True] * N
isPrime[0] = isPrime[1] = False
p = 0
while p ** 2 <= N:
    while not isPrime[p]:
        p += 1
    seq = 2*p, N, p
    isPrime[slice(*seq)] = [False] * len(range(*seq))
    p += 1
import math
truepi = sum(isPrime)
approx = N / math.log(N)
print("={} ~{:.2f} (err {:.2%})".format(truepi, approx, approx/truepi - 1))
