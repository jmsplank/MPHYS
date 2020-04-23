import time as oohTiming
import logging
import glob
import cdflib
import datetime as dt
import pandas as pd
import numpy as np
import progress.bar as progress


logging.basicConfig(filename='mphys_project_log.log', level=logging.DEBUG,
                    format='\n[%(asctime)s: Fname - %(filename)s: Function - %(funcName)s: %(levelname)s]\n%(message)s')


def info(s):
    logging.info(str(s))
    print(s)


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


def moments(dateRange, source='/home/james/Documents/MPHYS_ARCHIVE/MOMENTS'):
    """
    Loads moments cdf data and returns DateTime object.

    Inputs:
        dateRange ->
    Outputs:
        DataFrame
    """
    dates = [f"20{i[0]:02d}{i[1]:02d}" for i in dateRange]
    files = sorted(glob.glob(source+'/*.cdf'))
    filesRef = [s.split('/')[-1].split('_')[6][:-2] for s in files]
    files = dict(zip(filesRef, files))

    df = pd.DataFrame(columns=['temp'])
    with Timer('Timing MOMENTS'):
        bar = progress.Bar('Loading MOMENTS', max=len(dates))
        for d in dates:
            logging.info(files[d])
            moments = cdflib.CDF(files[d])
            timetags = moments.varget(
                'time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
            time = cdflib.cdfepoch.unixtime(timetags)
            time = [dt.datetime.utcfromtimestamp(t) for t in time]
            temp = moments.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
            moments = pd.DataFrame(np.column_stack(
                [time, temp]), columns=['time', 'temp'])
            moments.set_index('time', inplace=True)
            moments.temp = moments.temp.astype(float)
            moments = moments.resample("5T").mean().clip(lower=-2e3, upper=2e3)
            moments.temp = moments.temp.mask(
                moments.temp > 140).astype(float)
            moments.temp = moments.temp.mask(
                moments.temp < -20).astype(float)
            df = df.append(moments)
            bar.next()
        bar.finish()
    return df


def omni(dateRange, source='/home/james/Documents/MPHYS_ARCHIVE/OMNI', gsm=False):
    dates = [f"20{i[0]:02d}{i[1]:02d}" for i in dateRange]
    files = sorted(glob.glob(source+'/*.cdf'))
    filesRef = [s.split('/')[-1].split('_')[-2][:-2] for s in files]
    files = dict(zip(filesRef, files))

    df = pd.DataFrame(columns=['bx', 'by', 'bz'])
    with Timer('Timing OMNI'):
        bar = progress.Bar('Loading OMNI', max=len(dates))
        for d in dates:
            logging.info(files[d])
            omni = cdflib.CDF(files[d])
            timetags = omni.varget('Epoch')
            imf_x = omni.varget('BX_GSE')
            if gsm:
                imf_z = omni.varget('BZ_GSM')
                imf_y = omni.varget('BY_GSM')
            else:
                imf_z = omni.varget('BZ_GSE')
                imf_y = omni.varget('BY_GSE')
            time = cdflib.cdfepoch.unixtime(timetags)
            time = [dt.datetime.utcfromtimestamp(t) for t in time]
            imf_month = pd.DataFrame(np.column_stack([time, imf_x, imf_y, imf_z]),
                                     columns=['time', 'bx', 'by', 'bz'])
            imf_month.bx = imf_month.bx.mask(
                imf_month.bx > 1000).interpolate().astype('float')
            imf_month.by = imf_month.by.mask(
                imf_month.by > 1000).interpolate().astype('float')
            imf_month.bz = imf_month.bz.mask(
                imf_month.bz > 1000).interpolate().astype('float')
            imf_month.dropna(inplace=True)
            imf_month = imf_month.set_index('time')
            imf_month = imf_month.resample("5T").mean()
            df = df.append(imf_month)
            bar.next()
        bar.finish()
    return df


def pgp(dateRange, source='/home/james/Documents/MPHYS_ARCHIVE/PGP', gsm=False):
    dates = [f"20{i[0]:02d}{i[1]:02d}" for i in dateRange]
    files = sorted(glob.glob(source+'/*.cdf'))
    filesRef = [s.split('/')[-1].split('_')[-2][:-2] for s in files]
    files = dict(zip(filesRef, files))

    df = pd.DataFrame(columns=['x', 'y', 'z'])
    with Timer('Timing PGP'):
        bar = progress.Bar('Loading PGP', max=len(dates))
        for d in dates:
            logging.info(files[d])
            pgp = cdflib.CDF(files[d])
            timetags = pgp.varget('Epoch__CL_JP_PGP')
            pos = pgp.varget('sc_r_xyz_gse__CL_JP_PGP')
            if gsm:
                conv = pgp.varget('gse_gsm__CL_JP_PGP')
                pos[:, 1] *= np.cos(np.radians(-conv))
                pos[:, 2] *= np.cos(np.radians(-conv))
            time = cdflib.cdfepoch.unixtime(timetags)
            time = [dt.datetime.utcfromtimestamp(t) for t in time]
            locations_month = pd.DataFrame(np.column_stack(
                [time, pos[:, 0], pos[:, 1], pos[:, 2]]), columns=['time', 'x', 'y', 'z'])
            locations_month.x = locations_month.x.astype(float)
            locations_month.z = locations_month.z.astype(float)
            locations_month.y = locations_month.y.astype(float)
            locations_month = locations_month.set_index('time')
            df = df.append(locations_month)
            bar.next()
        bar.finish()
    return df
