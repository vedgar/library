# https://gist.github.com/vrajivk/c505310fb79d412afcd5

import collections, types, contextlib, itertools, sys

class Channel1:
    @types.coroutine
    def transmit(self, i):
        yield self, 'w'
        assert not self
        self.value = i

    @types.coroutine
    def receive(self):
        yield self, 'r'
        try:
            return self.value
        finally:
            del self.value

    def __bool__(self):
        return hasattr(self, 'value')

Waiting = collections.namedtuple('Waiting', 'function channel mode')
ready = lambda w: w.mode == 'wr'[bool(w.channel)]

class Deadlock(Exception):
    pass

class Loop(set):
    def run(self, f):
        args = f.send(None)
        self.add(Waiting(f, *args))

    def _pick(self):
        candidates = set(filter(ready, self))
        if not candidates:
            raise Deadlock
        picked = candidates.pop()
        self.remove(picked)
        return picked

    def run_until_complete(self, f):
        self.run(f)
        while any(func is f for func, chan, mode in self):
            picked = self._pick()
            with contextlib.suppress(StopIteration):
                self.run(picked.function)

async def generate(ch):
    for i in itertools.count(2):
        await ch.transmit(i)

async def cfilter(cin, cout, prime):
    while True:
        i = await cin.receive()
        if i % prime:
            await cout.transmit(i)

async def main(n, loop):
    ch = Channel1()
    loop.run(generate(ch))
    for i in range(n):
        prime = await ch.receive()
        print(prime)
        ch1 = Channel1()
        loop.run(cfilter(ch, ch1, prime))
        ch = ch1

if __name__ == '__main__':
    loop = Loop()
    n = int(input('How many primes to generate: '))
    loop.run_until_complete(main(n, loop))
