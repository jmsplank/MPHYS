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

progStartTime = oohTiming.time()
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

    def __exit__(self, *args):
        self.end = oohTiming.time()
        self.interval = self.end - self.start
        info(self.message+' completed in {0:.2f}s'.format(self.interval))
info('Starting script: {}'.format(progStartTime))

with Timer('Load cluster moments'):
    cwd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/MPHYS/python/tests/filt_by_temp/'
    cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_september_05/'
    cl_moments = cdflib.CDF(cluster_loc+'september_05_moments.cdf')
    timetags = cl_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    temp = cl_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    density = cl_moments.varget('density__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    moments = pd.DataFrame(np.column_stack([time, temp, density]), columns=['time', 'temp', 'dens'])
    info('moments data loaded')

with Timer('Searching for high temperatures'):
    high_temp = []
    for i, row in moments.iterrows():
        if row.temp >= 30:
            high_temp.append(i)
    #high_temp = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(high_temp), lambda x: x[0]-x[1])]
    temp_groups = [[high_temp[0]]]
    for x in high_temp[1:]:
        if x - temp_groups[-1][-1] < 100:
            temp_groups[-1].append(x)
        else:
            temp_groups.append([x])
    info('Found {} zones'.format(len(temp_groups)))

with Timer('Loading cluster locations'):
    cl_locations = cdflib.CDF(cwd+'locationData.cdf')
    timetags = cl_locations.varget('Epoch__CL_JP_PGP')
    pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP') 
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    locations = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2]]), columns=['time', 'x', 'y', 'z'])
    locations.time = pd.to_datetime(locations.time)
    locations = locations.set_index('time')

with Timer('Associating index to time'):
    for i in range(len(temp_groups)):
        start = moments.loc[temp_groups[i][0]].time
        end = moments.loc[temp_groups[i][-1]].time
        temp_groups[i] = (start, end)

with Timer('Associating with IMF'):
    cdf_imf = cdflib.CDF(cwd+'omni_hro_1min_20050901_v01.cdf')
    timetags = cdf_imf.varget('Epoch')
    imf = cdf_imf.varget('BZ_GSM')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    imf = pd.DataFrame(np.column_stack([time, imf]), columns=['time', 'IMF'])
    imf.time = pd.to_datetime(imf.time)
    imf = imf.set_index('time')
    imf.IMF = imf.IMF.replace(imf.IMF.max(), np.NAN).interpolate()

    imf_tf = []
    for j in range(len(temp_groups)):
        begin = temp_groups[j][0].replace(second=0, microsecond=0)
        end = temp_groups[j][1].replace(second=0, microsecond=0)
        imf_tf.append(imf.loc[begin:end].IMF.mean() < 0)
    

with Timer('Extracting locations of high temp'):
    #moments.time = pd.to_datetime(moments.time)
    #moments = moments.set_index('time')
    fig, ax = plt.subplots(figsize=[8]*2)
    t = np.linspace(0, 2*np.pi, 100)
    r = 6371
    ax.plot(r*np.sin(t), r*np.cos(t), color='k')
    ax.set_xlim([150000, -150000])
    ax.set_ylim([-150000, 150000])
    for i in range(len(temp_groups)):
        temp_interval = temp_groups[i]
        loc = locations.loc[temp_interval[0]:temp_interval[1]]
        if imf_tf[i]:
            c = 'seagreen'
        else:
            c = 'skyblue'
        if len(loc.index) > 1:
            ax.plot(loc.x, loc.z, color=c)
        elif len(loc.index) == 1:
            ax.plot(loc.x, loc.z, color=c, marker='x')

plt.show()
