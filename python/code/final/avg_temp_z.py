from mpl_toolkits import mplot3d
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
from mpl_toolkits.axes_grid1 import make_axes_locatable

years = [2, 11]  # The range of years to get
months = [7, 11]  # Months within year to get
dateRange = []
for y in range(*years):
    for m in range(*months):
        dateRange.append([y, m])  # Make list of months & years

with mp.Timer('Timing code'):
    moments = pd.read_csv('moments.csv',
                          index_col=0, parse_dates=True)
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments.csv')
    omni = pd.read_csv('omni.csv',
                       index_col=0, parse_dates=True)
    # omni = mp.omni(dateRange)
    # omni.to_csv('omni.csv')
    pgp = mp.pgp(dateRange)  # Get predicted geometric position

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    data = pd.merge_asof(data, omni, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE  # Units to RE
    data.x = data.x / RE
    data.y = data.y / RE

    # plot conifg
    fig, ax = plt.subplots(figsize=[8, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    # T = 20  # Temperature lower limit
    # yCut = 100
    # data_filt = data[(data.temp >= T) & (data.y <= yCut) &
    #                  (data.y >= -yCut)]
    # data_filt = data[(data.temp >= T)].drop(columns=['y'])
    # data_filt = data[data.temp > 0]
    # print(data_filt.head())

    data = data[(data.temp >= 0) & (data.x <= 0)]
    n = 20  # Bounds of plot in Re
    bin_width = 1  # Size of bins in Re
    bin_edges = np.arange(0, data.z.abs().max(), bin_width)
    flierprops = dict(marker='x', markerfacecolor='k', markersize=3,
                      alpha=0.5)
    for i in range(len(bin_edges[:-1])):
        filt = data[(data.z.abs() >= bin_edges[i]) &
                    (data.z.abs() <= bin_edges[i+1])]
        print(len(filt))
        ax.boxplot(filt.temp, positions=[(
            bin_edges[:-1]+np.diff(bin_edges)/2)[i]],
            widths=bin_width*0.95, flierprops=flierprops, whis=3)

    # bins = scipy.stats.binned_statistic(
    #     data.z, data.temp, bins=bin_edges, statistic='mean')
    # stds = scipy.stats.binned_statistic(
    #     data.z, data.temp, bins=bin_edges, statistic='std')

    # print(bins.bin_edges, bins.statistic)
    # ax.hlines(bins.statistic,
    #           bins.bin_edges[:-1], bins.bin_edges[1:], color='k', lw=5)
    # ax.errorbar(bins.bin_edges[:-1]+np.diff(bins.bin_edges)/2,
    #             bins.statistic, yerr=stds.statistic, color='r')
    ax.set_ylabel(r'Temperature (MK)')
    ax.set_xlabel(r'$Z_{GSM}$ Position $(R_e)$')
    ax.grid()
    plt.tight_layout()
plt.show()
