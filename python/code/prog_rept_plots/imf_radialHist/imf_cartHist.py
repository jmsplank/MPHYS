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


cwd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/MPHYS/python/tests/hist/'
folder = 'september_05'
cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_{}/'.format(
    folder)

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
    imf_z = cdf_imf.varget('BZ_GSE')
    imf_x = cdf_imf.varget('BX_GSE')
    imf_y = cdf_imf.varget('BY_GSE')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    imf = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]),
                       columns=['time', 'bx', 'by', 'bz'])
    # imf.time = pd.to_datetime(imf.time)
    # imf = imf.set_index('time')
    imf.bx = imf.bx.mask(imf.bx > 1000).interpolate().astype('float')
    imf.by = imf.by.mask(imf.by > 1000).interpolate().astype('float')
    imf.bz = imf.bz.mask(imf.bz > 1000).interpolate().astype('float')
    # imf['angle'] = np.arctan2(imf.by, imf.bz)
    # imf['nearestTime'] = imf.time.dt.round('5min')

with Timer('loading position data'):
    cl_locations = cdflib.CDF(cluster_loc+'{}_locations.cdf'.format(folder))
    timetags = cl_locations.varget('Epoch__CL_JP_PGP')
    pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    locations = pd.DataFrame(np.column_stack(
        [time, pos[:, 0], pos[:, 1], pos[:, 2]]), columns=['time', 'x', 'y', 'z'])
    # locations.time = pd.to_datetime(locations.time)
    # locations = locations.set_index('time')
    locations.index = locations.time

with Timer('Searching for high temperatures'):
    mk = 20
    temps = moments[moments.temp >= mk]
    times = temps.time.tolist()
    times = np.unique([x.replace(second=0, microsecond=0) for x in times])


def dirMean(series):
    C = 1./len(series) * np.sum(np.cos(series))
    S = 1./len(series) * np.sum(np.sin(series))
    return np.arctan2(S, C)


def resLen(series):
    C = 1./len(series) * np.sum(np.cos(series))
    S = 1./len(series) * np.sum(np.sin(series))
    return np.sqrt(C**2 + S**2)


def in_ranges(x, bins):
    return [((x >= y[0]) & (x <= y[1])) for y in bins]


with Timer('Generating plot'):
    imf.set_index(imf.time, inplace=True)
    # print(locations.head())
    # print(imf.head())
    loc_imf = pd.merge_asof(imf, locations, left_index=True, right_index=True)
    loc_imf = loc_imf.loc[times].copy()
    # print(loc_imf.head(10))
    loc_imf['theta'] = np.arctan2(loc_imf.bz, loc_imf.by)
    loc_imf['r'] = np.sqrt(loc_imf.by**2 + loc_imf.bz**2)
    loc_imf.z = np.abs(loc_imf.z) / 6371

    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    binnable = loc_imf[loc_imf.z.between(6, 20)].copy()
    binnable = binnable.dropna()
    sns.jointplot(binnable.by, binnable.bz, kind='kde', cmap='viridis', n_levels=60)
    # ax1 = sns.jointplot(binnable.by, binnable.bz, marginal_kws=dict(bins=60), color='k')
    # ax1.fig.set_size_inches(5, 4)
    # ax1.ax_joint.cla()
    # plt.sca(ax1.ax_joint)
    # plt.hist2d(binnable.by, binnable.bz, 100, norm=mpl.colors.LogNorm(), cmap='viridis')
    # cbar_ax = ax1.fig.add_axes([1, 0.1, .03, .7])
    # cb = plt.colorbar(cax=cbar_ax)
    # plt.grid()
    # plt.xlabel(r'$Y_{GSM}$')
    # plt.ylabel(r'$Y_{GSM}$')


# plt.tight_layout()
plt.show()
# plt.savefig('python/code/prog_rept_plots/imf_radialHist/imf_cartHist2.png', dpi=300)

# dMean = loc_imf.groupby(pd.cut(loc_imf.z,
#                        bins=pd.IntervalIndex.from_arrays(np.arange(11),
#                                                          [loc_imf.z.max()]*11))).theta.agg([dirMean, resLen])
# dMean['mid'] = pd.IntervalIndex(dMean.index).mid

# plt.plot(dMean.mid, dMean.dirMean)
