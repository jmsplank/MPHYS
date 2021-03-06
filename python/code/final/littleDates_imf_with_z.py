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
from datetime import datetime as dt
import datetime

years = [2, 11]  # The range of years to get
months = [7, 11]  # Months within year to get
dateRange = []
for y in range(*years):
    for m in range(*months):
        # years = [2, 11]  # The range of years to get
        dateRange.append([y, m])

with mp.Timer('Timing code'):
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments.csv')
    moments = pd.read_csv('moments.csv',
                          index_col=0, parse_dates=True)

    # omni = mp.omni(dateRange)
    # omni.to_csv('omniGSE.csv')
    omni = pd.read_csv('omniGSE.csv',
                       index_col=0, parse_dates=True)

    # pgp = mp.pgp(dateRange)  # Get predicted geometric position
    # pgp.to_csv('pgpGSE.csv')
    pgp = pd.read_csv('pgpGSE.csv',
                      index_col=0, parse_dates=True)

    # data = pd.merge_asof(moments, omni, left_index=True, right_index=True)
    data = pd.merge_asof(moments, pgp, left_index=True, right_index=True)
    data = pd.merge_asof(data, omni, left_index=True, right_index=True)
    RE = 6371  # km
    data.z = data.z / RE  # Units to RE
    data.x = data.x / RE
    data.y = data.y / RE

    # plot conifg
    nrows = 2
    ncols = 3
    fig, ax = plt.subplots(figsize=[6, 4])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    data.z = data.z.abs()
    data = data.dropna()

    cmap = cm.get_cmap('Greys')
    NC = 6
    colours = [cmap(1.*i/NC) for i in range(NC)]

    temps = np.linspace(15, 35, nrows*ncols, dtype=int)

    width = 1
    dmin = data.z.min()
    dmax = data.z.max()
    edges = np.arange(dmin, dmax+width, width, dtype=int)
    flierprops = dict(marker='x', markerfacecolor='k', markersize=3,
                      alpha=0.5)
    ax.grid(True)
    data2 = data[data.temp > 20]
    data2 = data2[(data2.index >= dt(2005, 7, 1)) &
                  (data2.index < dt(2005, 11, 1))]
    for i in range(len(edges[:-1])):
        data3 = data2[(data2.z >= edges[i])]
        # ax.reshape(-1)[a].boxplot(data3.bz,
        #                           positions=[
        #                               (edges[:-1]+np.diff(edges)/2)[i]],
        #                           widths=width*0.95,
        #                           flierprops=flierprops, whis=3)
        ax.bar([edges[i]], data3.bz.mean(),
               width=width, align='edge', yerr=data3.bz.std()/np.sqrt(len(data3)),
               color='skyblue', ecolor='k', capsize=3)
        ax.hlines(data3.bz.mean(),
                  edges[i], edges[i+1], color='k')
    ax.set_title(r'$T>20$ $MK$')
    ax.set_ylabel(r'$B_z\ (nT)$')
    ax.set_xlabel(r'$|Z_{GSE}|\ (R_e)$')
    ax.set_ylim([-2.5, 10])
    ax.set_xlim([dmin, dmax])

plt.tight_layout()
plt.show()
