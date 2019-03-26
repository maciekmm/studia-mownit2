import time


def timing(f):
    def call(*args):
        start = time.time()
        ret = f(*args)
        print(time.time() - start, end=' | ')
        # print("Time taken:", f.__module__, f.__name__, (time.time() - start))
        return ret

    return call
