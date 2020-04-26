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
months = [7, 13]  # Months within year to get
dateRange = []
for y in range(*years):
    for m in [5, 6, 7, 8, 9, 10, 11, 12]:
        dateRange.append([y, m])  # Make list of months & years

with mp.Timer('Timing code'):
    moments = pd.read_csv('moments2.csv',
                          index_col=0, parse_dates=True)
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments2.csv')
    omni = pd.read_csv('omni2.csv',
                       index_col=0, parse_dates=True)
    # omni = mp.omni(dateRange, gsm=True)
    # omni.to_csv('omni2.csv')
    pgp = pd.read_csv('pgp2.csv',
                      index_col=0, parse_dates=True)
    # pgp = mp.pgp(dateRange, gsm=True)  # Get predicted geometric position
    # pgp.to_csv('pgp2.csv')

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    data = pd.merge_asof(data, omni, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE  # Units to RE
    data.x = data.x / RE
    data.y = data.y / RE

    data = data[data.temp > 0]

    # plot conifg
    fig, ax = plt.subplots(figsize=[8, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    scale_z = data.z.max() - data.z.min()  # Width of z
    bin_width = 1  # Size of bins in Re
    bins_z = scale_z // bin_width
    binned_all = scipy.stats.binned_statistic(
        data.z, data.temp, bins=bins_z, statistic='mean')
    err_binned_all = scipy.stats.binned_statistic(
        data.z, data.temp, bins=bins_z, statistic='std')
    binned_north = scipy.stats.binned_statistic(
        data[data.bz > 0].z, data[data.bz > 0].temp, bins=bins_z, statistic='mean')
    err_binned_north = scipy.stats.binned_statistic(
        data[data.bz > 0].z, data[data.bz > 0].temp, bins=bins_z, statistic='std')
    diff = binned_north.statistic - binned_all.statistic
    x = np.linspace(data.z.min(), data.z.max(), len(diff))
    plt.plot(x, diff, c='k', marker='x', linestyle='none')
    yerr = np.sqrt(np.power(err_binned_all.statistic, 2) +
                   np.power(err_binned_north.statistic, 2))
    plt.errorbar(x, diff, c='k', marker='x', linestyle='none', yerr=yerr)
    plt.plot([x[0], x[-1]], [0]*2, color='y')
plt.show()
