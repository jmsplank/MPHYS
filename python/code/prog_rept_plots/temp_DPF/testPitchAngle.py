import matplotlib as mpl
import cdflib
import pprint
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

cwd = '/Users/jamesplank/OneDrive/Documents/Work-James’s MacBook Pro/MPHYS/Aurora/MPHYS/python/tests/colourPlot/'
cdf_file = cdflib.CDF(cwd+'pitchAngle.cdf')

timetags = cdf_file.varget('time_tags__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
diffpartflux = cdf_file.varget('Differential_Particle_Flux__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
entable = cdf_file.varget('energy_table__C1_CP_CIS-HIA_PAD_HS_MAG_IONS_PF')
offset = 62167219200000
time = np.array(timetags)
time = time - offset
time = np.array([dt.datetime.utcfromtimestamp(int(np.floor(i/1000))) for i in time])

#print(np.shape(np.transpose(y[0])[0]))
#print([np.mean(i) for i in np.transpose(y[0])])
data = []
for i in range(len(timetags)):
    data.append([np.mean(k) for k in np.transpose(diffpartflux[i])])

data = np.transpose(data)

fig, ax = plt.subplots()
ax.pcolormesh(time, entable, data, norm=mpl.colors.LogNorm())
ax.set_yscale('log')
ax.set_xticks(time[::len(time)//6]) #Only need 6 ticks
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) #Format display date

#bins = 100
#slices = np.linspace(0, len(timetags), bins+1, True).astype(int)
#counts = np.diff(slices)
#for i in range(len(entable)):
#    x.append(np.add.reduceat(data[i], slices[:-1]) / counts)
##
#plt.imshow(x)
plt.savefig('fluxenergyandtime.png')
