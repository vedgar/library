import enum, operator
from functools import partial, reduce

def compose(*functions):
    def composition(*args, **kw):
        it = reversed(functions)
        result = next(it)(*args, **kw)
        for function in it:
            result = function(result)
        return result
    return composition

curry = partial(partial, partial)
curry3 = curry(partial)
aggregate = curry(compose)
classaggregate = compose(aggregate(classmethod), aggregate)
bettersum = partial(reduce, operator.add)
decorator = classaggregate(bettersum)
