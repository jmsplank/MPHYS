import cdflib
import numpy as np
import datetime as dt
import pandas as pd

def loadCdf(cdf, timeVar, zVars, cwd = ''):
    cdf_file = cdflib.CDF(cwd+cdf)
    timetags = cdf_file.varget(timeVar)
    time = cdflib.cdfepoch.unixtime(timetags)
    time = [dt.datetime.utcfromtimestamp(t) for t in time]
    df = pd.DataFrame({'time': time})
    df.set_index('time')
    for i in zVars:
        print(i)
        print(zVars[i])
        df = df.assign(i=pd.Series(cdf_file.varget(zVars[i])).values)
    return df
