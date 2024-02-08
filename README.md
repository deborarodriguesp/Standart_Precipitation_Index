# run_precipitation_SPI
Scripts developed to calculate the SPI and to be applied to FillMatrix of MOHID.

This script was developed based on the Standard Precip package:
- Author - Eric Nussbaumer (ebaumer@gmail.com)
- Website: https://github.com/e-baumer/standard_precip/tree/master

The run_SPI.py script uses a data frame with a format of:
  Date        Station1       Station2
  01/01/1990  PrecipValue1    PrecipValue1

The script opens this data frame and calculates the SPI based on Normal, Dry, and Wet years for at least 30 years.
Then, a precipitation average is done for each category (Dry, Normal, and Wet years). In the end, a time series with three precipitations is saved for each station. 

The run_find_station_fillmatrix.py script opens a specific Excel file, which has the station name, latitude, and longitude information. The script finds the stations and copies the coordinates information into a .dat file. This .dat file has a format to be applied to the Fillmatrix of the MOHID Model (http://wiki.mohid.com/index.php?title=FillMatrix). 



