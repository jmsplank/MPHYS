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
    imf_z = cdf_imf.varget('BZ_GSM')
    imf_x = cdf_imf.varget('BX_GSE')
    imf_y = cdf_imf.varget('BY_GSM')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    imf = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]),
                       columns=['time', 'bx', 'by', 'bz'])
    #imf.time = pd.to_datetime(imf.time)
    #imf = imf.set_index('time')
    imf.bx = imf.bx.mask(imf.bx > 1000).interpolate().astype('float')
    imf.by = imf.by.mask(imf.by > 1000).interpolate().astype('float')
    imf.bz = imf.bz.mask(imf.bz > 1000).interpolate().astype('float')
    #imf['angle'] = np.arctan2(imf.by, imf.bz)
    #imf['nearestTime'] = imf.time.dt.round('5min')

with Timer('loading position data'):
    cl_locations = cdflib.CDF(cluster_loc+'{}_locations.cdf'.format(folder))
    timetags = cl_locations.varget('Epoch__CL_JP_PGP')
    pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
    gsm = cl_locations.varget('gse_gsm__CL_JP_PGP')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    locations = pd.DataFrame(np.column_stack(
        [time, pos[:, 0], pos[:, 1], pos[:, 2]]), columns=['time', 'x', 'y', 'z'])
    ##locations.time = pd.to_datetime(locations.time)
    ##locations = locations.set_index('time')
    locations.index = locations.time
    locations.z *= np.cos(np.radians(gsm))

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
    loc_imf['theta'] = np.arctan2(loc_imf.by, loc_imf.bz)
    loc_imf.z = np.abs(loc_imf.z) / 6371

    n_bins = 20
    fBin = np.linspace(-np.pi, np.pi, num=n_bins+1)
    bins = []
    for i in range(n_bins):
        bins.append([fBin[i], fBin[i+1]])
    width = 2*np.pi / n_bins

    fig = plt.figure(figsize=[12.2, 12.2])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    num_plots = 9
    radR = [[a, loc_imf.z.max()] for a in np.linspace(0, loc_imf.z.max(), num=num_plots+1)]
    for i, r in enumerate(radR[:-1]):
        means = []
        for b in bins:
            binnable = loc_imf[loc_imf.z.between(r[0], r[1])].copy()
            binnable = binnable[binnable.theta.between(b[0], b[1])]
            means.append(len(binnable))

        # print(len(bins), len(means))
        ax = fig.add_subplot(3, 3, i+1, projection='polar')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_title(r'$Z_{{GSM}}: {0:0.1f} \rightarrow {1:0.1f}$'.format(r[0], r[1]))

        ax.bar(fBin[:n_bins], means, width=width, bottom=0.0,
               edgecolor='k', color='none', linewidth=2)
        # print('doneBAR')

plt.tight_layout()
# plt.savefig('python/code/prog_rept_plots/imf_radialHist/imf_radialHistGSM.png', dpi=300)
plt.show()
# dMean = loc_imf.groupby(pd.cut(loc_imf.z,
#                        bins=pd.IntervalIndex.from_arrays(np.arange(11),
#                                                          [loc_imf.z.max()]*11))).theta.agg([dirMean, resLen])
#dMean['mid'] = pd.IntervalIndex(dMean.index).mid

#plt.plot(dMean.mid, dMean.dirMean)
