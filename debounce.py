import time


class Debounce(object):
    def __init__(self, f):
        self.f = f
        self.last_endtime = 0

    def __call__(self, *args, **kwargs):
        now = time.time()
        delta = now - self.last_endtime
        if delta > 1:
            self.f(*args, **kwargs)
            self.last_endtime = time.time()
        else:
            print 'Debouncing...'

