import time

def timing(f):
    def call(*args):
        start = time.time()
        ret = f(*args)
        print("Time taken:", f.__name__, (time.time() - start))
        return ret
    return call