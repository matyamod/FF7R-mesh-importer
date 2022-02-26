import time, os

class Logger:
    LOG_FOLDER='log'
    def __init__(self):
        os.makedirs(Logger.LOG_FOLDER, exist_ok=True)
        self.file_name = time.strftime('%Y%m%d-%H%M%S'+'.txt')
        file_path=os.path.join(Logger.LOG_FOLDER, self.file_name)
        self.f=open(file_path, 'w')

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
        self.close()
        file_path=os.path.join(Logger.LOG_FOLDER, self.file_name)
        self.file_name = 'error-'+self.file_name
        err_file_path=os.path.join(Logger.LOG_FOLDER, self.file_name)
        os.rename(file_path, err_file_path)
        raise RuntimeError(string)

class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start=time.time()

    def now(self):
        return time.time()-self.start

logger=Logger()
