import collections, itertools, operator, functools


def gcd_ex(a, b):
    Qs = *_, r = [collections.deque(s, 2) for s in ([1,0], [0,1], [a,b])]
    try:
        while True:
            q = r[-2] // r[-1]
            for Q in Qs:
                Q.append(Q[-2] - q*Q[-1])
    except ZeroDivisionError:
        (ac, br), (bc, ar), (d, zero) = Qs
        if d < 0:
            ac, bc, d = -ac, -bc, -d
        return (ac, bc), (abs(ar), abs(br)), d

def gcd_ex_test(a, b):
    (ac, bc), (ar, br), d = gcd_ex(a, b)
    assert a*ac + b*bc == d and abs(a) == d * ar and abs(b) == d * br


def product(numbers):
    return functools.reduce(operator.mul, numbers, 1)

def avoiding_products(numbers: list) -> list:
    raise_ = [1, *itertools.accumulate(numbers, operator.mul)][:-1]
    fall = [1, *itertools.accumulate(reversed(numbers), operator.mul)][-2::-1]
    return list(map(operator.mul, raise_, fall))


def chinese_remainder(ns_as: dict) -> int:
    def gen_terms(ns, as_):
        for a, m, n in zip(as_, avoiding_products(list(ns)), ns):
            (mc, nc), _, d = gcd_ex(m, n)
            assert d == 1
            yield a * mc * m
    return sum(gen_terms(*zip(*ns_as.items()))) % product(map(abs, ns_as))


def factor(number: int) -> list:
    if number == 0:
        return [0]
    elif number < 0:
        fac = [-1]
        number *= -1
    elif number > 0:
        fac = []
    while not number % 2:
        fac.append(2)
        number //= 2
    for div in itertools.count(3, 2):
        if div ** 2 > number:
            if number > 1:
                fac.append(number)
            return fac
        while not number % div:
            fac.append(div)
            number //= div
