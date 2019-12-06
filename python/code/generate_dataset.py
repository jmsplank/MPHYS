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
import auroral as au
import subprocess

dl = '/Users/jamesplank/Downloads/'
wd = '/Users/jamesplank/OneDrive/Documents/Work/University/MPHYS/Aurora/data_archive/'
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

