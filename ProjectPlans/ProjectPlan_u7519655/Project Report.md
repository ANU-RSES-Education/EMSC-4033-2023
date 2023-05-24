## EMSC4033 - Project Report

### Instructions

This project is to apply USGS earthquake data to Australia. In this project, it shows earthquake points in different megnititude and reach their information 
 directly in a simple area sort program, and user can get the updated information of the nearest earthquake by themselves.
 
 To start this program, you need install and import some modules which list you can find in the List of dependencies later.
 The first steep is to get the data from USGS.
 
 `url = https://earthquake.usgs.gov/fdsnws/event/1/query`
 
 Then we tap in the `start_time`, the `end_time` and the `min_magnititude` one by one. (the time should in YYYY-MM-DD formation and magnititude should in 1~10.)
It will return a number of how many earthquakes happened in Australia and nearly sea area during this time.

In the second part it will show a map with scattered points of earthquakes in different colors which divided by different magnititudes.
mag in [4,4.5] is blue, [4.5,5] is orange, larger than 5 is red.

In the next part you can tap in a state name and the map will only show the earthquakes in this state.
The states list you can choose: SA(South Auistralia), ACT(Australian Capital Territory), NSW(New South Wales),
 NT(Northern Territory), QLD(Queensland), TAS(Tasmania), VIC(Victoria), and WA(Western Australia).

Next, just tap in the same state code you have done before, you can get all the information of the earthquakes in this state include magnititude, location,and time.

If you input the coordinate you are, the next part will tell you the distance of the nearest earthquake and give you information of 5 nearest earthquakes then plot them on the map.
(Rember tapping your longitude and latitude within Australia, lon:(110,160),lat:(-45,-10))

At last, it shows how to modify this program to fit other countries situation. In this part, you just need to change some coordinates and the detial instruction is in the code.

### List of dependencies

For the API requesting part, we need the `requests` package to send a request to the server, `JSON` package to format the data, `geopandas` packages to create a 
data frame, mation to format used for URL. `cartopy` package is useful to add base map, axes and data point, `datetime` package is for formatting time of the earhquake shown in the USGS data, 
`geopy` packge is for calculate distace, and `matplotlib.pyplot` package actucally does the plotting.

### Testing
In the first part, if we tap in the correct number as required, it will show like this:

`Enter the start time (YYYY-MM-DD):  2022-01-01`

`Enter the end time (YYYY-MM-DD):  2023-01-01`

`Enter the minimum magnitude:  1`

`There were 72 earthquakes in or next to Australia between 2022-01-01 and 2023-01-01.`

If we tap in something wrong, it will happen like this:

`Enter the start time (YYYY-MM-DD):  qqqq`

`Enter the end time (YYYY-MM-DD):  qqqq`

`Enter the minimum magnitude:  q`

`Invalid input. Please enter a valid floating-point number.`

`Enter the minimum magnitude:  1`

`Error: Could not retrieve earthquake data from USGS API.`

In the later part, if you tap in something outside the expect, it will show `State code not found. Please enter a valid state code.`
If tap in correct code, the map will be ploted.

### Limitations

There are still many questions in this program, especially clear in the last example of Japan,
like the area is just a square, which is suitable for large and regular countries such as Australia or 
Canada, but this is not suitable for some small or complex countries.


### Future Improvements	

As I said in limitations, the next step is to put shapefile into the program to give a better boundries for each country or each state.
It is also important to give user a way to tap in the countries they want but not modify it from code.
