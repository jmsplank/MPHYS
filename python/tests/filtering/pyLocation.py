import time as oohTiming
import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
from operator import itemgetter
from itertools import *

cwd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/MPHYS/python/tests/filtering/'
cdf_file = cdflib.CDF(cwd+'locationData.cdf')

timetags = cdf_file.varget('Epoch__CL_JP_PGP')
pos = cdf_file.varget('sc_r_xyz_gse__CL_JP_PGP')
offset = 62167219200000

ep = cdflib.cdfepoch.unixtime(timetags[0], to_np=True)
## print(ep)
## print(dt.datetime.utcfromtimestamp(ep[0]))

time = np.array(timetags)
time = time - offset
time = np.array([dt.datetime.utcfromtimestamp(int(np.floor(i/1000))) for i in time])

#plt.plot(time, pos[:,2])
#plt.savefig('septemberOrbits.png')

data = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2]]), columns=['time', 'x', 'y', 'z'])
data.set_index('time')
## print(dt.datetime.strftime(time[0], '%Y-%m-%d %H:%M:%S'))

def get_range(df, low, high):
    if isinstance(low, str):
        low = dt.datetime.strptime(low, '%Y-%m-%d %H:%M:%S')
        high = dt.datetime.strptime(high, '%Y-%m-%d %H:%M:%S')
    print(low, high)
    df_list = []
    for i, row in df.iterrows():
        if (row.time >= low and row.time <= high):
            df_list.append(i)
        elif (row.time > high):
            break
    return df.loc[df_list]

daterange = get_range(data, '2005-09-10 00:00:00', '2005-09-20 23:59:59')

def get_alt(df, alt=6, points=True):
    """Return dataframe filtered for points above a certain z.
    alt = altitude in Earth Radii
    """
    alt = alt * 6371
    df_list = []
    for i, row in df.iterrows():
        if (row.z >= alt or row.z <= -alt):
            df_list.append(i)
    if points:
        return df_list, df.loc[df_list]
    else:
        return df.loc[df_list]

df_list, altFilter = get_alt(daterange)

cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_september_05/'
cl_moments = cdflib.CDF(cluster_loc+'september_05_moments.cdf')
timetags = cl_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
time = cdflib.cdfepoch.unixtime(timetags)
time = [dt.datetime.utcfromtimestamp(t) for t in time]
temp = cl_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
density = cl_moments.varget('density__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
moments = pd.DataFrame(np.column_stack([time, temp, density]), columns=['time', 'temp', 'dens'])
moments.set_index('time')

## print(df_list[:50])
df_list = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(df_list), lambda x: x[0]-x[1])]
## print(df_list[:5])

for i in range(len(df_list)):
    start = altFilter.loc[df_list[i][0]].time
    end = altFilter.loc[df_list[i][-1]].time
    df_list[i] = (start, end)

## print(df_list)

fig, ax = plt.subplots(9, 1, figsize=(8,8))
for i in range(len(df_list)):
    s = oohTiming.time()
    mom = get_range(moments, *df_list[i])
    print(mom.head(10))
    ax[i].plot(mom.time, mom.temp)
    print('Done {0} of 9 in {1:02.2f}s'.format(i, oohTiming.time()-s))

plt.show()

## fs = 8
## fig, ax = plt.subplots(figsize=[fs]*2)
## t = np.linspace(0, 2*np.pi, 100)
## r = 6371
## ax.plot(r*np.sin(t), r*np.cos(t), color='k')
## ax.plot(daterange.x, daterange.z, color='skyblue')
## 
## ax.plot(altFilter.x, altFilter.z, color='maroon', linestyle='none', marker='o', fillstyle='full', markersize=2)
## 
## ax.plot(daterange['x'].iloc[-1], daterange['z'].iloc[-1], linestyle='none', marker='x', color='skyblue')
## ax.set_xlim([150000, -150000])
## ax.set_ylim([-150000, 150000])
## plt.show()
