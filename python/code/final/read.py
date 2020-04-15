import mphys as mp
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import cm
import matplotlib as mpl
import seaborn as sns
import scipy

years = [2, 11]
months = [1, 13]
dateRange = []
for y in range(*years):
    for m in range(*months):
        dateRange.append([y, m])

with mp.Timer('Whole Code.'):
    moments = pd.read_csv('moments.csv',
                          index_col=0, parse_dates=True)
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments.csv')
    # omni = mp.omni(dateRange)
    pgp = mp.pgp(dateRange)

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE
    data.x = data.x / RE
    data.y = data.y / RE

    fig = plt.figure(figsize=[6, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    # c = ['Blues', 'Greens', 'Oranges', 'Reds']
    # for i, T in enumerate(np.linspace(20, 60, 4)):
    #     filter_by_temp = data[data.temp >= T]
    #     plt.hist2d(filter_by_temp.x, filter_by_temp.z, 20,
    #                cmap=c[i], cmin=2, norm=mpl.colors.LogNorm(), label='{:2.1f}mK')
    T = 20
    data_filt = data[(data.temp >= T) & (data.y <= 5) &
                     (data.y >= -5)].drop(columns=['y'])
    print(data_filt.head())

    n = 20
    scale_x = data_filt.x.max() - data_filt.x.min()
    scale_z = data_filt.z.max() - data_filt.z.min()
    bin_width = 0.1  # Size of bins in Re
    bins_x = scale_x // bin_width
    bins_z = scale_z // bin_width
    binned = scipy.stats.binned_statistic_2d(
        data_filt.z, data_filt.x, data_filt.temp, bins=[bins_z, bins_x],
        statistic='median')
    plt.imshow(binned.statistic, extent=(data_filt.x.min(),
                                         data_filt.x.max(),
                                         data_filt.z.min(),
                                         data_filt.z.max()),
               interpolation='nearest', cmap='viridis', aspect='equal',
               origin='lower', norm=mpl.colors.LogNorm())
    plt.colorbar()

    plt.plot(np.sin(np.linspace(0, 2*np.pi, 20)),
             np.cos(np.linspace(0, 2*np.pi, 20)), color='k')

    plt.xlim(n, -n)
    plt.ylim(-n, n)
    plt.grid()
    plt.tight_layout()
plt.show()
