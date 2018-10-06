def pbs(cond, start=0):
    """last int after start satisfying cond
    Precondition: cond(n)=>cond(n-1) & cond(start) & exists n>start not cond(n)
    Complexity: max. 2*ld(result-start), calls cond on distinct numbers only"""
    step = 1
    while cond(start + step): step <<= 1
    start += step >> 1
    step >>= 2
    while step:
        if cond(start + step): start += step
        step >>= 1
    return start
