import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd

cwd = '/Users/jamesplank/OneDrive/Documents/Work-James’s MacBook Pro/MPHYS/Aurora/MPHYS/python/tests/location/'
cdf_file = cdflib.CDF(cwd+'locationData.cdf')

timetags = cdf_file.varget('Epoch__CL_JP_PGP')
pos = cdf_file.varget('sc_r_xyz_gse__CL_JP_PGP')
offset = 62167219200000

ep = cdflib.cdfepoch.unixtime(timetags[0], to_np=True)
print(ep)
print(dt.datetime.utcfromtimestamp(ep[0]))

time = np.array(timetags)
time = time - offset
time = np.array([dt.datetime.utcfromtimestamp(int(np.floor(i/1000))) for i in time])

#plt.plot(time, pos[:,2])
#plt.savefig('septemberOrbits.png')

data = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2]]), columns=['time', 'x', 'y', 'z'])
data.set_index('time')
print(dt.datetime.strftime(time[0], '%Y-%m-%d %H:%M:%S'))

def get_range(df, low, high):
    low = dt.datetime.strptime(low, '%Y-%m-%d %H:%M:%S')
    high = dt.datetime.strptime(high, '%Y-%m-%d %H:%M:%S')
    df_list = []
    for i, row in df.iterrows():
        if (row.time >= low and row.time <= high):
            df_list.append(i)
        elif (row.time > high):
            break
    return df.loc[df_list]

daterange = get_range(data, '2005-09-15 00:00:00', '2005-09-15 23:59:59')

fs = 8
fig, ax = plt.subplots(figsize=[fs]*2)
t = np.linspace(0, 2*np.pi, 100)
r = np.sqrt(6371)
ax.plot(r*np.sin(t), r*np.cos(t), color='k')
ax.plot(daterange.x, daterange.z, color='skyblue')
ax.plot(daterange['x'].iloc[-1], daterange['z'].iloc[-1], linestyle='none', marker='x', color='skyblue')
ax.set_xlim([-150000, 150000])
ax.set_ylim([-150000, 150000])
plt.savefig(cwd+'xz.png')
