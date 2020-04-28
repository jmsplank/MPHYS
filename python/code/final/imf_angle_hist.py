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

    omni = mp.omni(dateRange)
    # omni.to_csv('omni.csv')
    # omni = pd.read_csv('omniGSE.csv',
    #    index_col=0, parse_dates=True)

    pgp = mp.pgp(dateRange)  # Get predicted geometric position
    # pgp.to_csv('pgp.csv')
    # pgp = pd.read_csv('pgpGSE.csv',
    #   index_col=0, parse_dates=True)

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
    fig = plt.figure(figsize=[12, 12])
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    data.z = data.z.abs()
    data = data.dropna()

    data["angle"] = np.arctan2(data.by, data.bz)

    # cmap = cm.get_cmap('Greys')
    # NC = 6
    # colours = [cmap(1.*i/NC) for i in range(NC)]

    # temps = np.linspace(15, 35, nrows*ncols, dtype=int)

    # width = 1
    dmin = data.z.min()
    dmax = data.z.max()
    # edges = np.arange(dmin, dmax+width, width, dtype=int)
    edges = np.linspace(dmin, dmax, 10)
    # flierprops = dict(marker='x', markerfacecolor='k', markersize=3,
    #                   alpha=0.5)
    data2 = data[data.temp > 20]
    # data2 = data2[(data2.index >= dt(2005, 9, 1)) &
    #   (data2.index < dt(2005, 10, 1))]
    for i, r in enumerate(edges[:-1]):
        data3 = data2[(data2.z >= r)]
        C = 1./len(data3) * np.sum(np.cos(data3.angle))
        S = 1./len(data3) * np.sum(np.sin(data3.angle))
        R = np.sqrt(np.power(C, 2) + np.power(S, 2))
        T = np.arctan2(S, C)
        print(
            f"Z > {r:.1f}\n   C={C:.4f}; S={S:.4f}\n  R={R:.4f}f T={np.degrees(T):.4f}")

        ax = fig.add_subplot(3, 3, i+1, projection='polar')
        ax.grid(True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.hist(data3.angle, np.linspace(-np.pi, np.pi, 20),
                edgecolor='k', fill=False, linewidth=1, density=True)

        ax.set_title(f'|Z| > {r:.1f}')
        ax.plot([T]*2, [0, R], color='r')
    # ax.set_ylabel(r'$B_z\ (nT)$')
    # ax.set_xlabel(r'$Z_{GSM}\ (R_e)$')
    # ax.set_ylim([-10, 10])
    # ax.set_xlim([dmin, dmax])

plt.tight_layout()
# plt.show()
plt.savefig('python/code/final/imf_angle_hist.png')
