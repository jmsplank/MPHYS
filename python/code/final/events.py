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
from scipy.optimize import curve_fit

years = [2, 11]  # The range of years to get
months = [7, 11]  # Months within year to get
dateRange = []
for y in range(*years):
    for m in range(*months):
        # years = [2, 11]  # The range of years to get
        dateRange.append([y, m])


def linear(x, m, c):
    return m*x + c


with mp.Timer('Timing code'):
    # moments = mp.moments(dateRange)  # Regen moments data. Takes > 90s
    # moments.to_csv('moments.csv')
    moments = pd.read_csv('moments.csv',
                          index_col=0, parse_dates=True)

    # omni = mp.omni(dateRange, gsm=True)
    # omni.to_csv('omni.csv')
    omni = pd.read_csv('omniGSE.csv',
                       index_col=0, parse_dates=True)

    # pgp = mp.pgp(dateRange, gsm=True)  # Get predicted geometric position
    # pgp.to_csv('pgp.csv')
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
    fig, ax = plt.subplots(figsize=[12, 6])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    cmap = cm.get_cmap('Greys')
    NC = 6
    colours = [cmap(1.*i/NC) for i in range(NC)]

    T = 20  # Temperature lower limit

    data.z = data.z.abs()
    # data = data[data.y.abs() <= 5]
    # for i, r in enumerate(np.arange(0, 12, 0.5)):
    r = 0
    data2 = data[(data.z >= r)]
    # https://stackoverflow.com/q/24281936
    data2['tag'] = data2['temp'] > T
    fst = data2.index[data2.tag & ~ data2.tag.shift(1).fillna(False)]
    lst = data2.index[data2.tag & ~ data2.tag.shift(-1).fillna(False)]

    dates = [[j, i] for i, j in zip(fst, lst)
             if j > i + pd.DateOffset(minutes=5)]

    events = pd.DataFrame()
    with mp.Timer('Generating events dataframe'):
        for i in range(len(dates)):
            event = {'start': dates[i][1],
                     'end': dates[i][0],
                     'imf_avg': data2[(data2.index >= dates[i][1]) & (data2.index <= dates[i][0])].bz.mean(),
                     'err_imf_avg': data2[(data2.index >= dates[i][1]) & (data2.index <= dates[i][0])].bz.std(),
                     'z_avg': data2[(data2.index >= dates[i][1]) & (data2.index <= dates[i][0])].z.mean(),
                     'x_avg': data2[(data2.index >= dates[i][1]) & (data2.index <= dates[i][0])].x.mean(),
                     'y_avg': data2[(data2.index >= dates[i][1]) & (data2.index <= dates[i][0])].y.mean()}
            events = events.append(event, ignore_index=True)
        events = events.dropna()
        print(events.describe())
        events.to_csv('events.csv')
    ax.errorbar(events.y_avg, events.imf_avg,
                yerr=events.err_imf_avg, color='k',
                linestyle='none', alpha=0.2)
    ax.plot(events.y_avg, events.imf_avg, color='k',
            marker='x', alpha=0.5, linestyle='none')

    popt, pcov = curve_fit(
        linear, events.y_avg, events.imf_avg, sigma=events.err_imf_avg)
    err_popt = [pcov[0, 0]**0.5, pcov[1, 1]**0.5]
    x = np.array([events.y_avg.min(), events.y_avg.max()])
    ax.plot(x, linear(x, *popt), color='r',
            label=f'$B_z={popt[0]:.03f}\pm{err_popt[0]:.03f}\ |Z| +{popt[1]:.03f}\pm{err_popt[1]:.03f}$')
    ax.grid()
    ax.legend()
    ax.set_xlabel(r"|Z|_{GSE}")
    ax.set_ylabel(r"IMF B_z")
    print(popt, err_popt)
plt.tight_layout()
plt.show()
