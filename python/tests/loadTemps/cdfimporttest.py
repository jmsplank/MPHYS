import cdflib #Python cdf file importer
import pprint #Pretty printing
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

cdf_file = cdflib.CDF('test_data.cdf') #Load the cdf file

y = cdf_file.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS') #Temperature data as np array

x = cdf_file.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS') #Time data as milliseconds since some epoch
offset = 62167219200000 #Required to format the date data to utc timestamp
x = np.array(x) #Confirm data type
x = x - [offset]*len(x) #Offset the data
time = np.array([dt.datetime.utcfromtimestamp(int(np.floor(i/1000))) for i in x]) #create datetime objects from x

#Plotting
fig, ax = plt.subplots(figsize=(10,5))
ax.grid()
ax.plot(time, y)
ax.set_xlabel('Time, 15/09/2005')
ax.set_ylabel('Temerature MK')
ax.set_xticks(time[::len(time)//6]) #Only need 6 ticks
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) #Format display date

plt.savefig('tempData.png')
