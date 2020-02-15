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
months = ['july', 'august', 'september', 'october']
year = '05'

imf = pd.DataFrame(columns=['bx', 'by', 'bz'])
locations = pd.DataFrame(columns=['x', 'y', 'z'])

for month in months:
    with Timer('loading {}'.format(month)):
        name = 'cluster_{0}_{1}/{0}_{1}'.format(month, year)

        cdf_imf = cdflib.CDF(cluster_loc+name+'_imf.cdf')
        timetags = cdf_imf.varget('Epoch')
        imf_z = cdf_imf.varget('BZ_GSE')
        imf_x = cdf_imf.varget('BX_GSE')
        imf_y = cdf_imf.varget('BY_GSE')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        imf_month = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]),
                                 columns=['time', 'bx', 'by', 'bz'])
        imf_month.bx = imf_month.bx.mask(imf_month.bx > 1000).interpolate().astype('float')
        imf_month.by = imf_month.by.mask(imf_month.by > 1000).interpolate().astype('float')
        imf_month.bz = imf_month.bz.mask(imf_month.bz > 1000).interpolate().astype('float')
        imf_month.dropna(inplace=True)
        imf_month = imf_month.set_index('time')
        imf = imf.append(imf_month)

        cl_locations = cdflib.CDF(cluster_loc+name+'_locations.cdf')
        timetags = cl_locations.varget('Epoch__CL_JP_PGP')
        pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        locations_month = pd.DataFrame(np.column_stack(
            [time, pos[:, 0], pos[:, 1], pos[:, 2]]), columns=['time', 'x', 'y', 'z'])
        locations_month = locations_month.set_index('time')
        locations = locations.append(locations_month)

print(imf)
print(locations)

loc_imf = pd.merge_asof(imf, locations, left_index=True, right_index=True)
loc_imf['theta'] = np.abs(np.arctan2(loc_imf.by, loc_imf.bz))
loc_imf.z = np.abs(loc_imf.z) / 6371

n_bins = 25
bins = [[a, loc_imf.z.max()] for a in np.linspace(0, loc_imf.z.max(), num=n_bins)]
means = []
for b in bins:
    binnable = loc_imf[loc_imf.z.between(b[0], b[1])].copy()
    if len(binnable) > 10:
        means.append([binnable.bz.mean(), binnable.bz.std()])
    else:
        means.append([np.nan]*2)

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

fig = plt.figure(figsize=[10, 6])

plt.grid()
plt.errorbar([b[0] for b in bins], [m[0] for m in means], color='k', yerr=[m[1] for m in means])
plt.xlabel(r'$Z_{GSM} R_\oplus$')
plt.ylabel(r'$\overline{B_z}$ nT')
plt.title('july -> october 2005')
plt.tight_layout()
plt.show()
