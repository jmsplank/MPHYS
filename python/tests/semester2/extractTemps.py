import logging
import time as oohTiming
import pandas as pd
import matplotlib as mpl
import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import seaborn as sns


cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/'
months = ['july', 'august', 'september', 'october']
year = '05'

temps = pd.DataFrame(columns=['temp'])

for month in months:
    name = 'cluster_{0}_{1}/{0}_{1}'.format(month, year)

    cl_moments = cdflib.CDF(cluster_loc+name+'_moments.cdf')
    timetags = cl_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    temp = cl_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    moments = pd.DataFrame(np.column_stack([time, temp]), columns=['time', 'temp'])
    moments.set_index('time', inplace=True)
    temps = temps.append(moments)

print(temps)
temps.to_csv(cluster_loc+name+'_temps.csv')
