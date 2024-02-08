# run_precipitation_SPI
Scripts developed to calculate the SPI and to be applied to FillMatrix of MOHID.

This script was developed based on the Standard Precip package:
- Author - Eric Nussbaumer (ebaumer@gmail.com)
- Website: https://github.com/e-baumer/standard_precip/tree/master


**The run_SPI.py script uses a data frame with a format of:**

|Date|Station1|Station2|
|----|--------|--------|
|01/01/1990|PrecipValue1|PrecipValue2|
|02/01/1990|PrecipValue1|PrecipValue2|
------------------------

The script opens this data frame and calculates the SPI based on Normal, Dry, and Wet years for at least 30 years.
Then, a precipitation average is done for each category (Dry, Normal, and Wet years). In the end, a time series with three precipitations is saved for each station. 

> SERIE_INITIAL_DATA :  2022 01 01 00 00 00
>
> TIME_UNITS         : DAYS
>
> !time dry wet normal
> 
> <BeginTimeSerie>
  
> Values Calculated by the run_SPI.py script
>
> <EndTimeSerie>
>

The **run_find_station_fillmatrix.py** script opens a specific Excel file, which has the station name, latitude, and longitude information: 

|Station Name|Latitude|Longitude|
|----|--------|--------|
|Station 1|x|y|
|Station 2|x|y|
------------------------

The script finds the stations and copies the coordinates information into a .dat file. This .dat file has a format to be applied to the Fillmatrix of the MOHID Model (http://wiki.mohid.com/index.php?title=FillMatrix). 

> PROPERTY_NAME           : precipitation
> 
> PROPERTY_UNITS          : mm
> 
> VARIABLE_IN_TIME        : 1
> 
> START                   : 2022 01 01 00 00 00
> 
> END                     : 2023 01 01 00 00 00
> 
> OUTPUT_TIME             : 0 86400
> 
> OUTPUT_FILE             : Precip_.hdf5
> 
> GRID_DATA_FILE          : dtm_para_v1_edit.dat
> 
> FILL_OUTSIDE_POINTS     : 1
> 
> MAX_TIME_SPAN           : 86400
> 
> INTERPOLATION_METHOD    : 2
> 
> MAX_DISTANCE            : 1000
> 
> IWD_N                   : 4.0
> 
> SKIP_NULLVALUES         : 0
> 
>
> <begin_station>
>
> NAME                    : 1045006
>
> X                       : -45.695
> 
> Y                       : -10.5622
>
> VALUE_TYPE              : TIMESERIE
> 
> FILENAME                :
> E:\METEOROLOGIA\Precipitation_scenarious\Precipitation_time_series\daily_mean_precipitation_1045006.txt
> 
> DATA_COLUMN             : 2
> 
> <end_station>

