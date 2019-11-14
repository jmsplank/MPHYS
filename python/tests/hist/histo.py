from itertools import *
from mpl_toolkits.mplot3d import Axes3D
from operator import itemgetter
import cdflib
import datetime as dt
import logging
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time as oohTiming

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

with Timer('Load cluster moments'):
    cl_moments = cdflib.CDF(cluster_loc+'{}_moments.cdf'.format(folder))
    timetags = cl_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    temp = cl_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    density = cl_moments.varget('density__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    moments = pd.DataFrame(np.column_stack([time, temp, density]), columns=['time', 'temp', 'dens'])

with Timer('Loading IMF data'):
    cdf_imf = cdflib.CDF(cluster_loc+'{}_imf.cdf'.format(folder))
    timetags = cdf_imf.varget('Epoch')
    imf_z = cdf_imf.varget('BZ_GSM')
    imf_x = cdf_imf.varget('BX_GSE')
    imf_y = cdf_imf.varget('BY_GSM')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    imf = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]), columns=['time', 'bx', 'by', 'bz'])
    imf.time = pd.to_datetime(imf.time)
    imf = imf.set_index('time')
    imf.bx = imf.bx.replace(imf.bx.max(), np.NAN).interpolate()
    imf.by = imf.by.replace(imf.by.max(), np.NAN).interpolate()
    imf.bz = imf.bz.replace(imf.bx.max(), np.NAN).interpolate()

with Timer('loading position data'):
    cl_locations = cdflib.CDF(cluster_loc+'{}_locations.cdf'.format(folder))
    timetags = cl_locations.varget('Epoch__CL_JP_PGP')
    pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    locations = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2]]), columns=['time', 'x', 'y', 'z'])
    ##locations.time = pd.to_datetime(locations.time)
    ##locations = locations.set_index('time')

with Timer('Searching for high temperatures'):
    mk = 20
    temps = moments[moments.temp >= mk]
    times = temps.time.tolist()
    times = np.unique([x.replace(second=0, microsecond=0) for x in times])

with Timer('Generating plot'):
    avg_ang = []
    for alt in np.linspace(0, 7, 50):
        alt_filter = locations.loc[locations.z >= alt*6371]

        with Timer('creating angles'):
            imf_filt = imf.loc[times].copy()
            imf_filt = imf.loc[alt_filter.time.tolist()].copy()
            imf_filt['ang_xz'] = np.arctan(imf.bz/imf.bx)
            imf_filt['ang_yz'] = np.arctan(imf.bz/imf.by)
        avg_ang.append(imf_filt['ang_xz'].mean())
    plt.plot(np.linspace(0,7,50), avg_ang)
    plt.xlabel(r'$r R_\oplus$')
    plt.ylabel(r'Average angle $\overline{B_{xz}}$')


##with Timer('plotting'):
    ##num_bars = 20
    ##_, bins = pd.cut(imf.ang_yz, num_bars, retbins=True)
    ##n, _, _ = plt.hist(imf.ang_yz, bins)
    ##plt.clf()
##
    ##width = bins[1]-bins[0]
    ##ax = plt.subplot(1, 1, 1, projection='polar')
    ##bars = ax.bar(bins[:num_bars], n, width=width, bottom=0.0)
    ##for bar in bars:
        ##bar.set_alpha(0.5)

##plt.savefig(cwd+'radial_xz_{0}MK.png'.format(mk))
plt.show()
