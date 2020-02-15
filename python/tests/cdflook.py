import cdflib
import pprint
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='Input the filename.')

args = parser.parse_args()

cdf_file = cdflib.CDF(args.filename)

pprint.pprint(cdf_file.cdf_info())

