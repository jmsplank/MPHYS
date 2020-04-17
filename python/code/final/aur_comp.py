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
    nrows = 2
    ncols = 3
    fig, ax = plt.subplots(nrows, ncols, figsize=[12, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    cmap = cm.get_cmap('Greys')
    NC = 6
    colours = [cmap(1.*i/NC) for i in range(NC)]

    T = 10  # Temperature lower limit

    for i, r in enumerate(range(0, 2*NC, 2)):
        data2 = data[(data.z > r) | (data.z < -r)]
        data2 = data2[data2.index > dt(2005, 1, 1, 0, 0, 0)]
        # https://stackoverflow.com/q/24281936
        data2['tag'] = data2['temp'] > T
        fst = data2.index[data2.tag & ~ data2.tag.shift(1).fillna(False)]
        lst = data2.index[data2.tag & ~ data2.tag.shift(-1).fillna(False)]

        fmtUrl = 'https://ssusi.jhuapl.edu/dataN/f16/apl/l1b/images/{0}/f16_StripDisk_{1}.png'
        dates = [j-i for i, j in zip(fst, lst)]
        # dates = [(fmtUrl.format(i.strftime("%Y/%j"),
        #                         i.strftime("%Y%j")),
        #           f"{i.strftime('%Y-%m-%d:%j')} for {str(j-i)}") for i, j in zip(fst, lst)
        #          if ((j >= i + pd.DateOffset(hours=1.5)) & (j <= i + pd.DateOffset(days=2)))]
        deltas = pd.DataFrame(dates)

        (deltas/pd.Timedelta(minutes=1)).hist(bins=range(1, 800, 15),
                                              ax=ax.reshape(-1)[i], color=colours[3],
                                              label=f">{r} Re",
                                              edgecolor='k', linewidth=1)
        ax.reshape(-1)[i].set_yscale('log')
        ax.reshape(-1)[i].set_title(f">{r} Re")
        if i > 2:
            ax.reshape(-1)[i].set_xlabel("Duration (minutes)")
        if i % 3 == 0:
            ax.reshape(-1)[i].set_ylabel(
                f"(log) No. events with T>{T} MK")
        # ax.reshape(-1)[i].legend()
        ax.reshape(-1)[i].set_ylim([0, 2e3])

plt.tight_layout()
plt.show()
