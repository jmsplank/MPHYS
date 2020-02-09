import logging
import time as oohTiming
import pandas as pd
import matplotlib as mpl
import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import seaborn as sns


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


cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/'
year = '05'
months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

imf = pd.DataFrame(columns=['bx', 'by', 'bz'])
for month in months:
    with Timer('Loading IMF for {}'.format(month)):
        file = 'cluster_{0}_{1}/{0}_{1}_imf.cdf'.format(month, year)
        cdf_imf = cdflib.CDF(cluster_loc+file)
        print(cluster_loc+file)
        timetags = cdf_imf.varget('Epoch')
        imf_z = cdf_imf.varget('BZ_GSM')
        imf_x = cdf_imf.varget('BX_GSE')
        imf_y = cdf_imf.varget('BY_GSM')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        imf_temp = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]),
                                columns=['time', 'bx', 'by', 'bz'])
        imf_temp = imf_temp.set_index('time')
        # imf_temp.bx = imf_temp.bx.mask(imf.bx > 1000).interpolate().astype('float')
        # imf_temp.by = imf_temp.by.mask(imf.by > 1000).interpolate().astype('float')
        # imf_temp.bz = imf_temp.bz.mask(imf.bz > 1000).interpolate().astype('float')
        imf = imf.append(imf_temp)
        print(imf)
        # imf.time = pd.to_datetime(imf.time)

# imf = imf.set_index('time')


imf.bx = imf.bx.mask(imf.bx > 1000).interpolate().astype('float')
imf.by = imf.by.mask(imf.by > 1000).interpolate().astype('float')
imf.bz = imf.bz.mask(imf.bz > 1000).interpolate().astype('float')
imf = imf.dropna()
print(imf)

# sns.jointplot(imf.by, imf.bz, kind='kde', cmap='viridis', n_levels=60)
fig = plt.figure(figsize=(8, 5))
plt.hist(imf.by, bins=100)
plt.yscale('log')
plt.xlabel('by')
plt.ylabel('log count')
# plt.xlim(-40, 40)
# plt.ylim(-40, 40)
plt.show()
