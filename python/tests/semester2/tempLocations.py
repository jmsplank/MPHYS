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
from matplotlib import cm


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

with Timer('Getting temperatures'):
    temps = pd.read_csv(
        '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_october_05/october_05_temps.csv',
        index_col=0, parse_dates=True)

loc_imf = pd.merge_asof(imf, locations, left_index=True, right_index=True)
loc_imf = pd.merge_asof(loc_imf, temps, left_index=True, right_index=True)
loc_imf['theta'] = np.arctan2(loc_imf.by, loc_imf.bz)
print(min(loc_imf.theta), max(loc_imf.theta))
# loc_imf.z = np.abs(loc_imf.z) / 6371
loc_imf.z = loc_imf.z / 6371
loc_imf.x = loc_imf.x / 6371

fig = plt.figure(figsize=[6, 6])
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

c = ['Blues', 'Greens', 'Oranges', 'Reds']
for i, T in enumerate(np.linspace(20, 60, 4)):
    filter_by_temp = loc_imf[loc_imf.temp >= T]
    plt.hist2d(filter_by_temp.x, filter_by_temp.z, 100,
               cmap=c[i], cmin=2, norm=mpl.colors.LogNorm(), label='{:2.1f}mK')
plt.plot(np.sin(np.linspace(0, 2*np.pi, 20)), np.cos(np.linspace(0, 2*np.pi, 20)), color='k')

n = 20
plt.xlim(n, -n)
plt.ylim(-n, n)
plt.grid()
plt.tight_layout()
plt.show()


# fig = plt.figure(figsize=[12.2, 12.2])
# plt.rc('font', family='serif')
# plt.rc('xtick', labelsize='x-small')
# plt.rc('ytick', labelsize='x-small')
#
# n_bins = 20
# fBin = np.linspace(-np.pi, np.pi, num=n_bins+1)
# bins = []
# for i in range(n_bins):
#     bins.append([fBin[i], fBin[i+1]])
# width = 2*np.pi / n_bins
#
# num_plots = 9
# radR = [[a, loc_imf.z.max()] for a in np.linspace(0, loc_imf.z.max(), num=num_plots+1)]
# colours = [cm.rainbow(i) for i in np.linspace(0, 1, 5)]
# for i, r in enumerate(radR[:-1]):
#     ax = fig.add_subplot(3, 3, i+1, projection='polar')
#     ax.set_theta_zero_location('N')
#     ax.set_theta_direction(-1)
#     ax.set_title(r'$Z_{{GSM}}: {0:0.1f} \rightarrow {1:0.1f}$'.format(r[0], r[1]))
#
#     for j, T in enumerate([20, 30, 40, 50, 60]):
#         filter_by_temp = loc_imf[loc_imf.temp >= T]
#         means = []
#         for b in bins:
#             binnable = filter_by_temp[filter_by_temp.z.between(r[0], r[1])].copy()
#             binnable = binnable[binnable.theta.between(b[0], b[1])]
#             means.append(len(binnable))
#         print(means)
#         ax.bar(fBin[:n_bins], means, width=width, bottom=0.0,
#                edgecolor=colours[j], color='none', linewidth=2)
#
# plt.tight_layout()
# plt.savefig('temp_hists.png')
