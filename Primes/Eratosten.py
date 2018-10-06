def gp1():
    D,q={},2
    while True:
        if q in D:
            for p in D[q]:
                D.setdefault(p+q,[]).append(p)
            del D[q]
        else:
            yield q
            D[q*q]=[q]
        q+=1
def gp2():
    D,q={},2
    while True:
        p=D.pop(q,None)
        if p:
            x=p+q
            while x in D: x+=p
            D[x]=p
        else:
            D[q*q]=q
            yield q
        q+=1
def gp3():
    D,q,p={},3,(yield 2)
    while True:
        if p:
            x=q+p+p
            while x in D: x+=p+p
            D[x]=p
        else:
            D[q*q]=q
            yield q
        q+=2
        p=D.pop(q,None)            
primes=gp3()
print([next(primes) for _ in range(50)])
