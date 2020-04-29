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

    arcs = pd.read_csv('python/code/final/arcs.csv',
                       parse_dates=[0, 1])
    # arcs.end = pd.to_datetime(arcs.end).head()
    zs = []
    e_zs = []
    e_bz = []
    for i in range(len(arcs)):
        arc = arcs.iloc[i]
        z = data[(data.index >= arc.start) &
                 (data.index <= arc.end)]
        zs.append(z.z.mean())
        e_zs.append(z.z.std())
        e_bz.append(z.bz.std())
    arcs["zs"] = zs
    arcs["e_zs"] = e_zs
    arcs["e_bz"] = e_bz
    plt.grid()
    plt.errorbar(arcs.zs.abs(), arcs.imf_z, xerr=arcs.e_zs, yerr=arcs.e_bz,
                 color='k', linestyle='none', capsize=3, alpha=0.3)
    plt.scatter(arcs.zs.abs(), arcs.imf_z, marker='x',
                color='k', label='No Arc Observed')

    has_arc = arcs[arcs.arc == True]
    print(len(has_arc))
    plt.scatter(has_arc.zs.abs(),
                has_arc.imf_z, marker='x',
                color='r', label='Arc Observed')

    popt, pcov = curve_fit(linear, arcs.zs.abs(),
                           arcs.imf_z, sigma=arcs.e_bz)
    pcov = [pcov[0, 0]**0.5, pcov[1, 1]**0.5]
    x = np.array([arcs.zs.abs().min(), arcs.zs.abs().max()])
    plt.plot(x, linear(x, *popt), color='g',
             label=f'$B_z={popt[0]:.04f}\pm{pcov[0]:.04f}\ |Z| + {popt[1]:.04f}\pm{pcov[1]:.04f}$')
    plt.fill_between(x, linear(x, popt[0]-pcov[0], popt[1]-pcov[1]),
                     linear(x, popt[0]+pcov[0], popt[1]+pcov[1]),
                     alpha=0.1, color='g')

    popt, pcov = curve_fit(linear, has_arc.zs.abs(),
                           has_arc.imf_z, sigma=has_arc.e_bz)
    pcov = [pcov[0, 0]**0.5, pcov[1, 1]**0.5]
    x = np.array([arcs.zs.abs().min(), arcs.zs.abs().max()])
    plt.plot(x, linear(x, *popt), color='r',
             label=f'$B_z={popt[0]:.04f}\pm{pcov[0]:.04f}\ |Z| + {popt[1]:.04f}\pm{pcov[1]:.04f}$')
    # plt.fill_between(x, linear(x, popt[0]-pcov[0], popt[1]-pcov[1]),
    #                  linear(x, popt[0]+pcov[0], popt[1]+pcov[1]),
    #                  alpha=0.2, color='lightgreen')

    plt.xlabel(r'$|Z|_{GSE}\ R_e$')
    plt.ylabel(r'$IMF\ B_z\ (nT)$')
    plt.legend()
plt.tight_layout()
plt.show()
