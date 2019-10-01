import cdflib
import pprint
import numpy as np
import matplotlib.pyplot as plt

cdf_file = cdflib.CDF('C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050915_140000_20050915_200000_V161018.cdf')

#pprint.pprint(cdf_file.cdf_info())

y = cdf_file.varget('temperature__C1_CP_CIS-HIA_ONBOARD_MOMENTS')
x = cdf_file.varget('time_tags__C1_CP_CIS-HIA_ONBOARD_MOMENTS')

plt.plot(x, y)
plt.show()
