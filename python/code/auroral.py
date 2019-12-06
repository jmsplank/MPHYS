from itertools import *
from mpl_toolkits.mplot3d import Axes3D
from operator import itemgetter
import cdflib
import datetime as dt
import logging
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time as oohTiming


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

def load_moments(fname):
    with Timer('Load cluster moments'):
        cl_moments = cdflib.CDF(fname)
        timetags = cl_moments.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        temp = cl_moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
        moments = pd.DataFrame(np.column_stack([time, temp]), columns=['time', 'temp'])
    return moments

def load_IMF(fname):
    with Timer('Loading IMF data'):
        cdf_imf = cdflib.CDF(fname)
        timetags = cdf_imf.varget('Epoch')
        imf_z = cdf_imf.varget('BZ_GSE')
        imf_x = cdf_imf.varget('BX_GSE')
        imf_y = cdf_imf.varget('BY_GSE')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        imf = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]), columns=['time', 'bx', 'by', 'bz'])
        imf.time = pd.to_datetime(imf.time)
        imf = imf.set_index('time')
        imf.bx = imf.bx.replace(imf.bx.max(), np.NAN).interpolate()
        imf.by = imf.by.replace(imf.by.max(), np.NAN).interpolate()
        imf.bz = imf.bz.replace(imf.bx.max(), np.NAN).interpolate()
    return imf

def load_position(fname):
    with Timer('loading position data'):
        cl_locations = cdflib.CDF(fname)
        timetags = cl_locations.varget('Epoch__CL_JP_PGP')
        pos = cl_locations.varget('sc_r_xyz_gse__CL_JP_PGP')
        time = cdflib.cdfepoch.unixtime(timetags)
        time = [dt.datetime.utcfromtimestamp(t) for t in time]
        locations = pd.DataFrame(np.column_stack([time, pos[:,0], pos[:,1], pos[:,2]]), columns=['time', 'x', 'y', 'z'])
    return locations
