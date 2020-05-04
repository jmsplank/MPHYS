## Structure
`Final Report` Contains source code and image files for the final report tex document.  
`Progress Report` Contains source code and image files for the progress report tex document.  
`python` Contains all python code  

`*.csv` Are csv files containing data extracted from `cdf` files (not stored here due to excessively large filsizes).  
 
### python folder
All code for this project was written in python.  
  
`code` contains:  
`final` -> All code used to generate the plots used in final report are stored here. This is the most up-to-date codebase.  
`prog_rept_plots` -> Code used to generate plots used in progress report.  
`tests` contains:  
`semester 1` -> Analysis of data not tied to specific report done during Sem 1 19/20  
`semester2` -> Analysis of data not ties to specific report done during Sem 2 19/20  
`cdflook.py` -> Self-contained script for analysing the contents of a cdf file  
  
## Dependencies
`MPHYS/python/code/final/mphys.py`  
`logging`  
`numpy`  
`pandas`  
`matplotlib.pyplot`  
`matplotlib.dates`  
`matplotlib.cm`  
`matplotlib`  
`seaborn`  
`scipy`  
`datetime`  

## CDF data
CDF data not kept in github due to filesizes.
Code assumes the presence of an archive folder with structure:  
MPHYS_ARCHIVE  
├── MOMENTS  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020101_000000_20020131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020201_000000_20020228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020301_000000_20020331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020401_000000_20020430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020501_000000_20020531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020601_000000_20020630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020701_000000_20020731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020801_000000_20020831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20020901_000000_20020930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20021001_000000_20021031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20021101_000000_20021130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20021201_000000_20021231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030101_000000_20030131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030201_000000_20030228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030301_000000_20030331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030401_000000_20030430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030501_000000_20030531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030601_000000_20030630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030701_000000_20030731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030801_000000_20030831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20030901_000000_20030930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20031001_000000_20031031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20031101_000000_20031130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20031201_000000_20031231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040101_000000_20040131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040201_000000_20040228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040301_000000_20040331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040401_000000_20040430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040501_000000_20040531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040601_000000_20040630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040701_000000_20040731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040801_000000_20040831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20040901_000000_20040930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20041001_000000_20041031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20041101_000000_20041130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20041201_000000_20041231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050101_000000_20050131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050201_000000_20050228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050301_000000_20050331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050401_000000_20050430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050501_000000_20050531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050601_000000_20050630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050701_000000_20050731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050801_000000_20050831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20050901_000000_20050930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20051001_000000_20051031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20051101_000000_20051130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20051201_000000_20051231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060101_000000_20060131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060201_000000_20060228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060301_000000_20060331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060401_000000_20060430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060501_000000_20060531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060601_000000_20060630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060701_000000_20060731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060801_000000_20060831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20060901_000000_20060930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20061001_000000_20061031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20061101_000000_20061130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20061201_000000_20061231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070101_000000_20070131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070201_000000_20070228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070301_000000_20070331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070401_000000_20070430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070501_000000_20070531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070601_000000_20070630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070701_000000_20070731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070801_000000_20070831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20070901_000000_20070930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20071001_000000_20071031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20071101_000000_20071130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20071201_000000_20071231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080101_000000_20080131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080201_000000_20080228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080301_000000_20080331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080401_000000_20080430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080501_000000_20080531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080601_000000_20080630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080701_000000_20080731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080801_000000_20080831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20080901_000000_20080930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20081001_000000_20081031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20081101_000000_20081130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20081201_000000_20081231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090101_000000_20090131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090201_000000_20090228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090301_000000_20090331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090401_000000_20090430_235959_V170421.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090501_000000_20090531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090601_000000_20090630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090701_000000_20090731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090801_000000_20090831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20090901_000000_20090930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20091001_000000_20091031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20091101_000000_20091130_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20091201_000000_20091231_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100101_000000_20100131_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100201_000000_20100228_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100301_000000_20100331_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100401_000000_20100430_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100501_000000_20100531_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100601_000000_20100630_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100701_000000_20100731_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100801_000000_20100831_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20100901_000000_20100930_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20101001_000000_20101031_235959_V161018.cdf  
│   ├── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20101101_000000_20101130_235959_V161018.cdf  
│   └── C1_CP_CIS-HIA_ONBOARD_MOMENTS__20101201_000000_20101231_235959_V161018.cdf  
├── OMNI  
│   ├── omni_hro_1min_20010101_v01.cdf  
│   ├── omni_hro_1min_20010201_v01.cdf  
│   ├── omni_hro_1min_20010301_v01.cdf  
│   ├── omni_hro_1min_20010401_v01.cdf  
│   ├── omni_hro_1min_20010501_v01.cdf  
│   ├── omni_hro_1min_20010601_v01.cdf  
│   ├── omni_hro_1min_20010701_v01.cdf  
│   ├── omni_hro_1min_20010801_v01.cdf  
│   ├── omni_hro_1min_20010901_v01.cdf  
│   ├── omni_hro_1min_20011001_v01.cdf  
│   ├── omni_hro_1min_20011101_v01.cdf  
│   ├── omni_hro_1min_20011201_v01.cdf  
│   ├── omni_hro_1min_20020101_v01.cdf  
│   ├── omni_hro_1min_20020201_v01.cdf  
│   ├── omni_hro_1min_20020301_v01.cdf  
│   ├── omni_hro_1min_20020401_v01.cdf  
│   ├── omni_hro_1min_20020501_v01.cdf  
│   ├── omni_hro_1min_20020601_v01.cdf  
│   ├── omni_hro_1min_20020701_v01.cdf  
│   ├── omni_hro_1min_20020801_v01.cdf  
│   ├── omni_hro_1min_20020901_v01.cdf  
│   ├── omni_hro_1min_20021001_v01.cdf  
│   ├── omni_hro_1min_20021101_v01.cdf  
│   ├── omni_hro_1min_20021201_v01.cdf  
│   ├── omni_hro_1min_20030101_v01.cdf  
│   ├── omni_hro_1min_20030201_v01.cdf  
│   ├── omni_hro_1min_20030301_v01.cdf  
│   ├── omni_hro_1min_20030401_v01.cdf  
│   ├── omni_hro_1min_20030501_v01.cdf  
│   ├── omni_hro_1min_20030601_v01.cdf  
│   ├── omni_hro_1min_20030701_v01.cdf  
│   ├── omni_hro_1min_20030801_v01.cdf  
│   ├── omni_hro_1min_20030901_v01.cdf  
│   ├── omni_hro_1min_20031001_v01.cdf  
│   ├── omni_hro_1min_20031101_v01.cdf  
│   ├── omni_hro_1min_20031201_v01.cdf  
│   ├── omni_hro_1min_20040101_v01.cdf  
│   ├── omni_hro_1min_20040201_v01.cdf  
│   ├── omni_hro_1min_20040301_v01.cdf  
│   ├── omni_hro_1min_20040401_v01.cdf  
│   ├── omni_hro_1min_20040501_v01.cdf  
│   ├── omni_hro_1min_20040601_v01.cdf  
│   ├── omni_hro_1min_20040701_v01.cdf  
│   ├── omni_hro_1min_20040801_v01.cdf  
│   ├── omni_hro_1min_20040901_v01.cdf  
│   ├── omni_hro_1min_20041001_v01.cdf  
│   ├── omni_hro_1min_20041101_v01.cdf  
│   ├── omni_hro_1min_20041201_v01.cdf  
│   ├── omni_hro_1min_20050101_v01.cdf  
│   ├── omni_hro_1min_20050201_v01.cdf  
│   ├── omni_hro_1min_20050301_v01.cdf  
│   ├── omni_hro_1min_20050401_v01.cdf  
│   ├── omni_hro_1min_20050501_v01.cdf  
│   ├── omni_hro_1min_20050601_v01.cdf  
│   ├── omni_hro_1min_20050701_v01.cdf  
│   ├── omni_hro_1min_20050801_v01.cdf  
│   ├── omni_hro_1min_20050901_v01.cdf  
│   ├── omni_hro_1min_20051001_v01.cdf  
│   ├── omni_hro_1min_20051101_v01.cdf  
│   ├── omni_hro_1min_20051201_v01.cdf  
│   ├── omni_hro_1min_20060101_v01.cdf  
│   ├── omni_hro_1min_20060201_v01.cdf  
│   ├── omni_hro_1min_20060301_v01.cdf  
│   ├── omni_hro_1min_20060401_v01.cdf  
│   ├── omni_hro_1min_20060501_v01.cdf  
│   ├── omni_hro_1min_20060601_v01.cdf  
│   ├── omni_hro_1min_20060701_v01.cdf  
│   ├── omni_hro_1min_20060801_v01.cdf  
│   ├── omni_hro_1min_20060901_v01.cdf  
│   ├── omni_hro_1min_20061001_v01.cdf  
│   ├── omni_hro_1min_20061101_v01.cdf  
│   ├── omni_hro_1min_20061201_v01.cdf  
│   ├── omni_hro_1min_20070101_v01.cdf  
│   ├── omni_hro_1min_20070201_v01.cdf  
│   ├── omni_hro_1min_20070301_v01.cdf  
│   ├── omni_hro_1min_20070401_v01.cdf  
│   ├── omni_hro_1min_20070501_v01.cdf  
│   ├── omni_hro_1min_20070601_v01.cdf  
│   ├── omni_hro_1min_20070701_v01.cdf  
│   ├── omni_hro_1min_20070801_v01.cdf  
│   ├── omni_hro_1min_20070901_v01.cdf  
│   ├── omni_hro_1min_20071001_v01.cdf  
│   ├── omni_hro_1min_20071101_v01.cdf  
│   ├── omni_hro_1min_20071201_v01.cdf  
│   ├── omni_hro_1min_20080101_v01.cdf  
│   ├── omni_hro_1min_20080201_v01.cdf  
│   ├── omni_hro_1min_20080301_v01.cdf  
│   ├── omni_hro_1min_20080401_v01.cdf  
│   ├── omni_hro_1min_20080501_v01.cdf  
│   ├── omni_hro_1min_20080601_v01.cdf  
│   ├── omni_hro_1min_20080701_v01.cdf  
│   ├── omni_hro_1min_20080801_v01.cdf  
│   ├── omni_hro_1min_20080901_v01.cdf  
│   ├── omni_hro_1min_20081001_v01.cdf  
│   ├── omni_hro_1min_20081101_v01.cdf  
│   ├── omni_hro_1min_20081201_v01.cdf  
│   ├── omni_hro_1min_20090101_v01.cdf  
│   ├── omni_hro_1min_20090201_v01.cdf  
│   ├── omni_hro_1min_20090301_v01.cdf  
│   ├── omni_hro_1min_20090401_v01.cdf  
│   ├── omni_hro_1min_20090501_v01.cdf  
│   ├── omni_hro_1min_20090601_v01.cdf  
│   ├── omni_hro_1min_20090701_v01.cdf  
│   ├── omni_hro_1min_20090801_v01.cdf  
│   ├── omni_hro_1min_20090901_v01.cdf  
│   ├── omni_hro_1min_20091001_v01.cdf  
│   ├── omni_hro_1min_20091101_v01.cdf  
│   ├── omni_hro_1min_20091201_v01.cdf  
│   ├── omni_hro_1min_20100101_v01.cdf  
│   ├── omni_hro_1min_20100201_v01.cdf  
│   ├── omni_hro_1min_20100301_v01.cdf  
│   ├── omni_hro_1min_20100401_v01.cdf  
│   ├── omni_hro_1min_20100501_v01.cdf  
│   ├── omni_hro_1min_20100601_v01.cdf  
│   ├── omni_hro_1min_20100701_v01.cdf  
│   ├── omni_hro_1min_20100801_v01.cdf  
│   ├── omni_hro_1min_20100901_v01.cdf  
│   ├── omni_hro_1min_20101001_v01.cdf  
│   ├── omni_hro_1min_20101101_v01.cdf  
│   └── omni_hro_1min_20101201_v01.cdf  
├── PGP  
│   ├── CL_JP_PGP_20010201_V19.cdf  
│   ├── CL_JP_PGP_20010301_V23.cdf  
│   ├── CL_JP_PGP_20010401_V31.cdf  
│   ├── CL_JP_PGP_20010501_V36.cdf  
│   ├── CL_JP_PGP_20010601_V35.cdf  
│   ├── CL_JP_PGP_20010701_V42.cdf  
│   ├── CL_JP_PGP_20010801_V44.cdf  
│   ├── CL_JP_PGP_20010901_V45.cdf  
│   ├── CL_JP_PGP_20011001_V49.cdf  
│   ├── CL_JP_PGP_20011101_V52.cdf  
│   ├── CL_JP_PGP_20011201_V50.cdf  
│   ├── CL_JP_PGP_20020101_V51.cdf  
│   ├── CL_JP_PGP_20020201_V53.cdf  
│   ├── CL_JP_PGP_20020301_V51.cdf  
│   ├── CL_JP_PGP_20020401_V55.cdf  
│   ├── CL_JP_PGP_20020501_V53.cdf  
│   ├── CL_JP_PGP_20020601_V50.cdf  
│   ├── CL_JP_PGP_20020701_V47.cdf  
│   ├── CL_JP_PGP_20020801_V47.cdf  
│   ├── CL_JP_PGP_20020901_V45.cdf  
│   ├── CL_JP_PGP_20021001_V47.cdf  
│   ├── CL_JP_PGP_20021101_V49.cdf  
│   ├── CL_JP_PGP_20021201_V47.cdf  
│   ├── CL_JP_PGP_20030101_V47.cdf  
│   ├── CL_JP_PGP_20030201_V48.cdf  
│   ├── CL_JP_PGP_20030301_V51.cdf  
│   ├── CL_JP_PGP_20030401_V56.cdf  
│   ├── CL_JP_PGP_20030501_V58.cdf  
│   ├── CL_JP_PGP_20030601_V61.cdf  
│   ├── CL_JP_PGP_20030701_V60.cdf  
│   ├── CL_JP_PGP_20030801_V58.cdf  
│   ├── CL_JP_PGP_20030901_V52.cdf  
│   ├── CL_JP_PGP_20031001_V52.cdf  
│   ├── CL_JP_PGP_20031101_V49.cdf  
│   ├── CL_JP_PGP_20031201_V52.cdf  
│   ├── CL_JP_PGP_20040101_V52.cdf  
│   ├── CL_JP_PGP_20040201_V51.cdf  
│   ├── CL_JP_PGP_20040301_V50.cdf  
│   ├── CL_JP_PGP_20040401_V49.cdf  
│   ├── CL_JP_PGP_20040501_V45.cdf  
│   ├── CL_JP_PGP_20040601_V45.cdf  
│   ├── CL_JP_PGP_20040701_V41.cdf  
│   ├── CL_JP_PGP_20040801_V41.cdf  
│   ├── CL_JP_PGP_20040901_V42.cdf  
│   ├── CL_JP_PGP_20041001_V42.cdf  
│   ├── CL_JP_PGP_20041101_V41.cdf  
│   ├── CL_JP_PGP_20041201_V41.cdf  
│   ├── CL_JP_PGP_20050101_V40.cdf  
│   ├── CL_JP_PGP_20050201_V38.cdf  
│   ├── CL_JP_PGP_20050301_V40.cdf  
│   ├── CL_JP_PGP_20050401_V37.cdf  
│   ├── CL_JP_PGP_20050501_V38.cdf  
│   ├── CL_JP_PGP_20050601_V36.cdf  
│   ├── CL_JP_PGP_20050701_V34.cdf  
│   ├── CL_JP_PGP_20050801_V33.cdf  
│   ├── CL_JP_PGP_20050901_V34.cdf  
│   ├── CL_JP_PGP_20051001_V35.cdf  
│   ├── CL_JP_PGP_20051101_V34.cdf  
│   ├── CL_JP_PGP_20051201_V33.cdf  
│   ├── CL_JP_PGP_20060101_V34.cdf  
│   ├── CL_JP_PGP_20060201_V31.cdf  
│   ├── CL_JP_PGP_20060301_V31.cdf  
│   ├── CL_JP_PGP_20060401_V31.cdf  
│   ├── CL_JP_PGP_20060501_V34.cdf  
│   ├── CL_JP_PGP_20060601_V32.cdf  
│   ├── CL_JP_PGP_20060701_V34.cdf  
│   ├── CL_JP_PGP_20060801_V33.cdf  
│   ├── CL_JP_PGP_20060901_V32.cdf  
│   ├── CL_JP_PGP_20061001_V32.cdf  
│   ├── CL_JP_PGP_20061101_V33.cdf  
│   ├── CL_JP_PGP_20061201_V33.cdf  
│   ├── CL_JP_PGP_20070101_V31.cdf  
│   ├── CL_JP_PGP_20070201_V33.cdf  
│   ├── CL_JP_PGP_20070301_V29.cdf  
│   ├── CL_JP_PGP_20070401_V29.cdf  
│   ├── CL_JP_PGP_20070501_V25.cdf  
│   ├── CL_JP_PGP_20070601_V28.cdf  
│   ├── CL_JP_PGP_20070701_V32.cdf  
│   ├── CL_JP_PGP_20070801_V31.cdf  
│   ├── CL_JP_PGP_20070901_V30.cdf  
│   ├── CL_JP_PGP_20071001_V33.cdf  
│   ├── CL_JP_PGP_20071101_V31.cdf  
│   ├── CL_JP_PGP_20071201_V27.cdf  
│   ├── CL_JP_PGP_20080101_V29.cdf  
│   ├── CL_JP_PGP_20080201_V30.cdf  
│   ├── CL_JP_PGP_20080301_V28.cdf  
│   ├── CL_JP_PGP_20080401_V27.cdf  
│   ├── CL_JP_PGP_20080501_V28.cdf  
│   ├── CL_JP_PGP_20080601_V29.cdf  
│   ├── CL_JP_PGP_20080701_V31.cdf  
│   ├── CL_JP_PGP_20080801_V31.cdf  
│   ├── CL_JP_PGP_20080901_V30.cdf  
│   ├── CL_JP_PGP_20081001_V32.cdf  
│   ├── CL_JP_PGP_20081101_V28.cdf  
│   ├── CL_JP_PGP_20081201_V26.cdf  
│   ├── CL_JP_PGP_20090101_V28.cdf  
│   ├── CL_JP_PGP_20090201_V27.cdf  
│   ├── CL_JP_PGP_20090301_V26.cdf  
│   ├── CL_JP_PGP_20090401_V29.cdf  
│   ├── CL_JP_PGP_20090501_V28.cdf  
│   ├── CL_JP_PGP_20090601_V28.cdf  
│   ├── CL_JP_PGP_20090701_V29.cdf  
│   ├── CL_JP_PGP_20090801_V29.cdf  
│   ├── CL_JP_PGP_20090901_V25.cdf  
│   ├── CL_JP_PGP_20091001_V28.cdf  
│   ├── CL_JP_PGP_20091101_V30.cdf  
│   ├── CL_JP_PGP_20091201_V28.cdf  
│   ├── CL_JP_PGP_20100101_V27.cdf  
│   ├── CL_JP_PGP_20100201_V20.cdf  
│   ├── CL_JP_PGP_20100301_V21.cdf  
│   ├── CL_JP_PGP_20100401_V18.cdf  
│   ├── CL_JP_PGP_20100501_V19.cdf  
│   ├── CL_JP_PGP_20100601_V20.cdf  
│   ├── CL_JP_PGP_20100701_V22.cdf  
│   ├── CL_JP_PGP_20100801_V22.cdf  
│   ├── CL_JP_PGP_20100901_V24.cdf  
│   ├── CL_JP_PGP_20101001_V25.cdf  
│   ├── CL_JP_PGP_20101101_V24.cdf  
│   └── CL_JP_PGP_20101201_V25.cdf  
└── Reference  
  
4 directories, 347 files  
