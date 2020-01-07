import logging
import time as oohTiming
import pandas as pd
import matplotlib as mpl
import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

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

cwd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/MPHYS/python/tests/hist/'
folder = 'september_05'
cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_{}/'.format(folder)

with Timer('Loading IMF data'):
    cdf_imf = cdflib.CDF(cluster_loc+'{}_imf.cdf'.format(folder))
    timetags = cdf_imf.varget('Epoch')
    imf_z = cdf_imf.varget('BZ_GSE')
    imf_x = cdf_imf.varget('BX_GSE')
    imf_y = cdf_imf.varget('BY_GSE')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    imf = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]), columns=['time', 'bx', 'by', 'bz'])
    imf.time = pd.to_datetime(imf.time)
    #imf = imf.set_index('time')
    imf.bx = imf.bx.mask(imf.bx > 1000).interpolate()
    imf.by = imf.by.mask(imf.by > 1000).interpolate()
    imf.bz = imf.bz.mask(imf.bz > 1000).interpolate()

with Timer('Plotting'):
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=[4, 4])

    ax[0].plot(imf.time, imf.bz, color='k', linewidth=0.5)
    ax[0].set_ylabel(r'IMF $B_z (nT)$')

    ax[1].plot(imf.time, imf.by, color='k', linewidth=0.5)
    ax[1].set_ylabel(r'IMF $B_y (nT)$')
    ax[1].set_xlabel('UTC for the month of September 2005')
    ax[1].set_xticks(imf.time[::len(imf.time)//4])
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))

print(np.mean(imf.bz), np.std(imf.bz))
print(np.mean(imf.by), np.std(imf.by))

plt.tight_layout()
#plt.savefig('python/code/prog_rept_plots/imf_ts/imf_ts.png', dps=300)
