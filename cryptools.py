import hashlib, itertools

def salted_md5(salt, stretch=1):
    for index in itertools.count():
        tohash = salt + str(index)
        for step in range(stretch):
            tohash = hashlib.md5(tohash.encode('ascii')).hexdigest()
        yield tohash
