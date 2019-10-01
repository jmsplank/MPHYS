import cdflib
import pprint
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

cdf_file = cdflib.CDF('test_data.cdf')

#pprint.pprint(cdf_file.cdf_info())

y = cdf_file.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
##pprint.pprint(cdf_file.varinq('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS'))

x = cdf_file.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
offset = 62167219200000
x = np.array(x)
x = x - [offset]*len(x)
print(str(x[0])[:-5])
time = np.array([dt.datetime.utcfromtimestamp(int(np.floor(i/1000))) for i in x])
print(time)

fig, ax = plt.subplots(figsize=(10,5))
ax.grid()
ax.plot(time, y)
ax.set_xlabel('Time, 15/09/2005')
ax.set_ylabel('Temerature MK')
ax.set_xticks(time[::len(time)//6])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

plt.savefig('tempData.png')
