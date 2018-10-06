from itertools import count
from functools import partial
from operator import mod
print(2,end=" ")
primes=[]
for candidate in count(3,2):
    if all(map(partial(mod,candidate),primes)):
        print(candidate,end=" ")
        primes.append(candidate)
