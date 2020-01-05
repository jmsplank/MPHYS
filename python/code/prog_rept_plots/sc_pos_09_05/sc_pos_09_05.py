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

with Timer('loading position data'):
    cl_locations = cdflib.CDF(cluster_loc+'{}_locations.cdf'.format(folder))
    timetags = cl_locations.varget('Epoch__CL_JP_PGP')
    pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
    gsm = cl_locations.varget('gse_gsm__CL_JP_PGP')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    locations = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2], gsm]), columns=['time', 'x', 'y', 'z', 'gsm'])
    print(locations.gsm.head())

with Timer('Loading boundaries'):
    bounds = pd.read_csv('python/code/prog_rept_plots/sc_pos_09_05/wpd_datasets.csv')
    print(bounds.head())

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
fig, ax = plt.subplots(1, 1, sharex=True, figsize=[4, 4])
ax.set_xlabel(r'$X_{GSM} (R_{\oplus})$')
ax.set_ylabel(r'$Z_{GSM} (R_{\oplus})$')

t = np.linspace(0, 2*np.pi, 100)
r = 6371
locations.x = locations.x / r
locations.z = locations.z * np.cos(np.radians(gsm)) / r

for line in ['l1', 'l2', 'l3', 'bs']:
    ax.plot(bounds['{}X'.format(line)], bounds['{}Y'.format(line)], color='k', ls='none', marker='o', markersize=1)

ax.plot(np.sin(t), np.cos(t), color='k', ls='none', marker='x', markersize=1)
ax.plot(locations.x, locations.z, color='k')
ax.set_xlim([20, -20])
ax.set_ylim([-20, 20])
plt.show()
#plt.savefig('python/code/prog_rept_plots/sc_pos_09_05/sc_pos_09_05.png', dpi=400)
