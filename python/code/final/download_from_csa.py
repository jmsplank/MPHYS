# Base url. Add args separated by '&' to configure
url = "https://csa.esac.esa.int/csa/aio/product-action?"
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Days in each month
# Use web GUI to download a sample, then copy fmt of .cdf filename
DATASET_ID = 'DATASET_ID=C1_CP_CIS-HIA_ONBOARD_MOMENTS'
DELIVERY_FORMAT = '&DELIVERY_FORMAT=CDF_2_7'  # Want cdf so can use cdflib
# Change cookie if anyone other than JP is using.
# Get cookie from: https://csa.esac.esa.int/csa/aio/html/howto.shtml#loginOptions
CSACOOKIE = '&CSACOOKIE=21185F6025034F56792E7352233247497D257E477C394F6238091D6F7A0C52752A465F60251459717E0F02370B1B5C7524061D602846466A'
# Grab all data, other options TenMin, hour, hour6, daily, etc... default daily
DELIVERY_INTERVAL = '&DELIVERY_INTERVAL=All'
for y in [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]:  # hardcode because lazy
    if y % 4 == 0:
        months[1] = 29  # Leap year
    else:
        months[1] = 28
    for i, m in enumerate(months):  # i+1 = month no. m = days in month
        START_DATE = f"&START_DATE={y}-{i+1:02d}-01T00:00:00Z"
        END_DATE = f"&END_DATE={y}-{i+1:02d}-{m:02d}T23:59:59Z"
        # Create wget shell script. Expect this to take > 1hr (LINUX ONLY)
        with open('get.sh', 'a') as file:
            file.write("wget --content-disposition '"+url+DATASET_ID+START_DATE+END_DATE +
                       DELIVERY_FORMAT+DELIVERY_INTERVAL+CSACOOKIE+"'\n")
