import time as oohTiming
import logging


logging.basicConfig(filename='mphys_project_log.log', level=logging.DEBUG,
                    format='\n[%(asctime)s: Fname - %(filename)s: Function - %(funcName)s: %(levelname)s]\n%(message)s')


def info(s):
    logging.info(str(s))
    print(s)


class Timer:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        self.start = oohTiming.time()
        info(self.message)

    def __exit__(self, *args):
        self.end = oohTiming.time()
        self.interval = self.end - self.start
        info(self.message+' completed in {0:.2f}s'.format(self.interval))
