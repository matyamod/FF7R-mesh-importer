import time

class Logger:
    def __init__(self):
        self.f=open('log.txt', 'w')
        self.start=time.time()

    def set_verbose(self, verbose):
        self.verbose=verbose

    def close(self):
        t=time.time()-self.start
        self.log('Run time (s): {}'.format(t))
        self.f.close()

    def log(self, string, ignore_verbose=False):
        self.f.write('{}\n'.format(string))
        if self.verbose or ignore_verbose:
            print(string)

    def error(self, string):
        self.log('Error: {}'.format(string))
        raise RuntimeError(string)

logger=Logger()
