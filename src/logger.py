import time

class Logger:
    def __init__(self):
        self.f=open('log.txt', 'w')

    def set_verbose(self, verbose):
        self.verbose=verbose

    def close(self):
        self.f.close()

    def log(self, string, ignore_verbose=False):
        self.f.write('{}\n'.format(string))
        if self.verbose or ignore_verbose:
            print(string)

    def error(self, string):
        self.log('Error: {}'.format(string))
        raise RuntimeError(string)

class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start=time.time()

    def now(self):
        return time.time()-self.start

logger=Logger()
