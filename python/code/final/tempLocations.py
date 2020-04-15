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

years = [2, 11]  # The range of years to get
months = [7, 13]  # Months within year to get
dateRange = []
for y in range(*years):
    for m in range(*months):
        dateRange.append([y, m])  # Make list of months & years

with mp.Timer('Timing code'):
    moments = pd.read_csv('moments.csv',
                          index_col=0, parse_dates=True)
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments.csv')
    # omni = mp.omni(dateRange)
    pgp = mp.pgp(dateRange)  # Get predicted geometric position

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE  # Units to RE
    data.x = data.x / RE
    data.y = data.y / RE

    # plot conifg
    fig = plt.figure(figsize=[6, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    T = 20  # Temperature lower limit
    data_filt = data[(data.temp >= T) & (data.y <= 5) &
                     (data.y >= -5)].drop(columns=['y'])
    # data_filt = data[(data.temp >= T)].drop(columns=['y'])
    print(data_filt.head())

    n = 20  # Bounds of plot in Re
    scale_x = data_filt.x.max() - data_filt.x.min()  # Width of x
    scale_z = data_filt.z.max() - data_filt.z.min()  # Width of z
    bin_width = 1.5  # Size of bins in Re
    bins_x = scale_x // bin_width
    bins_z = scale_z // bin_width

    # Bin the data. Returns 2d array of median temperature values
    binned = scipy.stats.binned_statistic_2d(
        data_filt.z, data_filt.x, data_filt.temp, bins=[bins_z, bins_x],
        statistic='median')
    # Plot binned data. binned doesn't hold abs pos data so specify extents
    plt.imshow(binned.statistic, extent=(data_filt.x.min(),
                                         data_filt.x.max(),
                                         data_filt.z.min(),
                                         data_filt.z.max()),
               interpolation='nearest', cmap='Reds', aspect='equal',
               origin='lower', norm=mpl.colors.LogNorm())
    plt.colorbar()  # Show colourbar

    plt.plot(np.sin(np.linspace(0, 2*np.pi, 20)),  # Plot Earth
             np.cos(np.linspace(0, 2*np.pi, 20)), color='k')

    plt.xlim(n, -n)  # Flip axis. +x points to Sun
    plt.ylim(-n, n)
    plt.grid()
    plt.tight_layout()
plt.show()
