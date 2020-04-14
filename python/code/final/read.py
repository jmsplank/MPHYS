import mphys as mp
import logging
import numpy as np
import pandas as pd

# url = "https://csa.esac.esa.int/csa/aio/product-action?"
# months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# DATASET_ID = 'DATASET_ID=C1_CP_CIS-HIA_ONBOARD_MOMENTS'
# DELIVERY_FORMAT = '&DELIVERY_FORMAT=CDF_2_7'
# CSACOOKIE = '&CSACOOKIE=21185F6025034F56792E7352233247497D257E477C394F6238091D6F7A0C52752A465F60251459717E0F02370B1B5C7524061D602846466A'
# DELIVERY_INTERVAL = '&DELIVERY_INTERVAL=All'
# for y in [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]:
#     for i, m in enumerate(months):
#         START_DATE = f"&START_DATE={y}-{i+1:02d}-01T00:00:00Z"
#         END_DATE = f"&END_DATE={y}-{i+1:02d}-{m:02d}T23:59:59Z"
#         with open('get.sh', 'a') as file:
#             file.write("wget --content-disposition '"+url+DATASET_ID+START_DATE+END_DATE +
#                        DELIVERY_FORMAT+DELIVERY_INTERVAL+CSACOOKIE+"'\n")
