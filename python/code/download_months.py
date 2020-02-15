import urllib.request as urllib
import os
import time as oohTiming
import logging


def info(s):
    logging.info(s)
    print(s)


logging.basicConfig(filename='log.txt', filemode='w',
                    format='[%(asctime)-%(name)-%(levelname)] %(message)')


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


monthDict = {'january': 1,
             'february': 2,
             'march': 3,
             'april': 4,
             'may': 5,
             'june': 6,
             'july': 7,
             'august': 8,
             'september': 9,
             'october': 10,
             'november': 11,
             'december': 12,
             }

months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'october', 'november', 'december']
year = '05'
for month in months:
    with Timer('Attempting download for {0} {1}'.format(month, year)):
        path = '../data_archive/cluster_{0}_{1}/'.format(month, year)
        try:
            os.mkdir(path)
        except FileExistsError:
            print('File Exists')

        OMNIurl = 'https://cdaweb.gsfc.nasa.gov/pub/data/omni/omni_cdaweb/hro_1min/20{0}/omni_hro_1min_20{0}{1:02}01_v01.cdf'.format(
            year, monthDict[month])
        OMNI_file = path + '{0}_{1}_imf.cdf'.format(month, year)
        urllib.urlretrieve(OMNIurl, filename=OMNI_file)
