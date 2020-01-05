from mpl_toolkits.axes_grid1 import make_axes_locatable
import logging
import time as oohTiming
import pandas as pd
import matplotlib as mpl
import cdflib
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

def info(s):
    logging.info(s)
    print(s)
logging.basicConfig(filename='log.txt', filemode='w',
                    format='[%(asctime)-%(name)-%(levelname)] %(message)')

class Timer:
    def __init__(self, message):
        self.message = message
    def __enter__(self):
        self.start = oohTiming.time()
        info(self.message)

    def __exit__(self, *args):
        self.end = oohTiming.time()
        self.interval = self.end - self.start
        info(self.message+' completed in {0:.2f}s'.format(self.interval))

cwd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/MPHYS/python/tests/hist/'
folder = 'september_05'
cluster_loc = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/cluster_{}/'.format(folder)

with Timer('Loading ion data'):
    cdf_ions = cdflib.CDF(cluster_loc+'{}_ions.cdf'.format(folder))
    timetags = cdf_ions.varget('time_tags__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
    ion_time = cdflib.cdfepoch.unixtime(timetags)
    ion_time = [dt.datetime.utcfromtimestamp(t) for t in ion_time]
    diffpartflux = cdf_ions.varget('Differential_Particle_Flux__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
    energy_table = cdf_ions.varget('energy_table__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
    dpf = []
    for i in range(len(ion_time)):
        dpf.append([np.mean(k) for k in np.transpose(diffpartflux[i])])
    dpf = np.transpose(dpf)
    print(np.shape(dpf))
    #ions = pd.DataFrame(np.column_stack([time, energy_table, diffpartflux]), columns=['time', 'energy', 'dpf'])

with Timer('Loading moments data'):
    cdf_moments = cdflib.CDF(cluster_loc+'{}_moments.cdf'.format(folder))
    timetags = cdf_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    temp = cdf_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    density = cdf_moments.varget('density__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
    moments = pd.DataFrame(np.column_stack([time, temp, density]), columns=['time', 'temp', 'dens'])
    moments.temp = moments.temp.mask(moments.temp < 0).interpolate()
    moments.temp = moments.temp.mask(moments.temp > 1000).interpolate()

with Timer('Plotting'):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=[15, 8])

    ax[0].set_ylabel('Energy (eV)')
    ax[0].set_title('Differential particle flux')
    cm = ax[0].pcolormesh(ion_time, energy_table, dpf, norm=mpl.colors.LogNorm())
    ax[0].set_yscale('log')
    ax[0].set_xticks(ion_time[::len(ion_time)//8])
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    divider0 = make_axes_locatable(ax[0])
    cax = divider0.append_axes("right", size="5%", pad=.05)
    cb = fig.colorbar(cm, cax=cax)
    cb.set_label(r'Ions - DPF $keV/cm^2/s/str$', rotation=90)
    ax[0].set_xlim([pd.to_datetime('2005-09-10 00:00:00'), pd.to_datetime('2005-09-20 00:00:00')])
    
    ax[1].set_ylabel('Ion temp (MK)')
    ax[1].set_title('Ion temperature')
    ax[1].plot(moments.time, moments.temp)
    ax[1].set_xticks(moments.time[::len(moments.time)//16])
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M:%S'))
    ax[1].set_xlabel('UTC for the month of September 2005')
    divider1 = make_axes_locatable(ax[1])
    cax2 = divider1.append_axes("right", size="5%", pad=.05)
    cax2.remove()

    ax[1].plot([dt.datetime.strptime('2005-09-15 14:00:00', '%Y-%m-%d %H:%M:%S')]*2,
               [moments.temp.min(), moments.temp.max()], color='g')
    ax[1].plot([dt.datetime.strptime('2005-09-15 22:00:00', '%Y-%m-%d %H:%M:%S')]*2,
               [moments.temp.min(), moments.temp.max()], color='g')
    
    ax[0].set_xlim([pd.to_datetime('2005-09-10 00:00:00'), pd.to_datetime('2005-09-20 00:00:00')])

plt.tight_layout()
plt.show()
