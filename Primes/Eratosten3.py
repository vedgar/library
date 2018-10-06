n = 1000
p = range(2, n + 1)
for b in range(2, int(n**.5 + 1)):
    p = filter(lambda a, b=b: a == b or a % b != 0, p)
print(list(p))
