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

    # omni = mp.omni(dateRange, gsm=True)
    # omni.to_csv('omni.csv')
    omni = pd.read_csv('omni.csv',
                       index_col=0, parse_dates=True)

    # pgp = mp.pgp(dateRange, gsm=True)  # Get predicted geometric position
    # pgp.to_csv('pgp.csv')
    pgp = pd.read_csv('pgp.csv',
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
    fig, ax = plt.subplots(nrows, ncols, figsize=[12, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    cmap = cm.get_cmap('Greys')
    NC = 6
    colours = [cmap(1.*i/NC) for i in range(NC)]

    T = 20  # Temperature lower limit

    for r in np.arange(0, 12, 0.5):
        data2 = data[(data.z >= r) | (data.z <= -r)]
        # https://stackoverflow.com/q/24281936
        data2['tag'] = data2['temp'] > T
        fst = data2.index[data2.tag & ~ data2.tag.shift(1).fillna(False)]
        lst = data2.index[data2.tag & ~ data2.tag.shift(-1).fillna(False)]

        dates = [[j, i] for i, j in zip(fst, lst)
                 if j > i + pd.DateOffset(minutes=5)]

        events = pd.DataFrame()
        for i in range(len(dates)):
            event = {'start': ,
                     'end': ,
                     'imf_avg':,
                     'err_imf_avg': ,
                     'z_avg':,


plt.tight_layout()
plt.show()
