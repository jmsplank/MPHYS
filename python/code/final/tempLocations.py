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
    # omni = mp.omni(dateRange, gsm=True)
    omni = pd.read_csv('omni2.csv',
                       index_col=0, parse_dates=True)
    # pgp = mp.pgp(dateRange, gsm=True)  # Get predicted geometric position
    pgp = pd.read_csv('pgp2.csv',
                      index_col=0, parse_dates=True)

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    data = pd.merge_asof(data, omni, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE  # Units to RE
    data.x = data.x / RE
    data.y = data.y / RE

    # plot conifg
    fig, ax = plt.subplots(figsize=[6, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    # T = 20  # Temperature lower limit
    # yCut = 100
    # data_filt = data[(data.temp >= T) & (data.y <= yCut) &
    #  (data.y >= -yCut)]
    # data_filt = data[(data.temp >= T)].drop(columns=['y'])
    data_filt = data[data.temp > 0]
    # data_filt = data_filt[data_filt.y.abs() < 8]
    # print(data_filt.head())

    n = 20  # Bounds of plot in Re
    scale_x = data_filt.x.max() - data_filt.x.min()  # Width of x
    scale_z = data_filt.z.max() - data_filt.z.min()  # Width of z
    bin_width = 2.5  # Size of bins in Re
    bins_x = scale_x // bin_width
    bins_z = scale_z // bin_width

    # Bin the data. Returns 2d array of median temperature values
    binned_all = scipy.stats.binned_statistic_2d(
        data_filt.z, data_filt.x, data_filt.temp, bins=[bins_z, bins_x],
        statistic='mean')
    data_filt = data_filt[data_filt.bz > 0]
    binned_north = scipy.stats.binned_statistic_2d(
        data_filt.z, data_filt.x, data_filt.temp, bins=[bins_z, bins_x],
        statistic='mean')
    stat = binned_north.statistic - binned_all.statistic
    # Plot binned data. binned doesn't hold abs pos data so specify extents
    cm = ax.imshow(stat, extent=(data_filt.x.min(),
                                 data_filt.x.max(),
                                 data_filt.z.min(),
                                 data_filt.z.max()),
                   interpolation='nearest', cmap='seismic', aspect='equal',
                   origin='lower', vmin=-4, vmax=4)
    # ax.colorbar()  # Show colourbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=.1)
    cb = fig.colorbar(cm, cax=cax)

    ax.plot(np.sin(np.linspace(0, 2*np.pi, 20)),  # Plot Earth
            np.cos(np.linspace(0, 2*np.pi, 20)), color='k')

    ax.set_xlim(n, -n)  # Flip axis. +x points to Sun
    ax.set_ylim(-n, n)
    ax.set_xlabel(r'$X_{GSM} (R_e)$')
    ax.set_ylabel(r'$Z_{GSM} (R_e)$')
    cb.set_label(r'Ion temperature (MK)')
    ax.grid()
    plt.tight_layout()
plt.show()
