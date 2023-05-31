## EMSC4033 - Project Report

### Instructions

This project is to apply USGS earthquake data to Australia. In this project, it shows earthquake points in different megnitude and reach their information 
 directly in a simple area sort program, and user can get the updated information of the nearest earthquake by themselves.
 
 To start this program, you need install and import some modules which list you can find in the List of dependencies later.
 The first steep is to get the data from USGS.
 
 `url = https://earthquake.usgs.gov/fdsnws/event/1/query`
 
 Then we tap in the `start_time`, the `end_time` and the `min_magnitude` one by one. (the time should in YYYY-MM-DD formation and magnititude should in 1~10.)
It will return a number of how many earthquakes happened in Australia and nearly sea area during this time.

In the second part it will show a map with scattered points of earthquakes in different colors which divided by different magnitudes.
mag in [4,4.5] is blue, [4.5,5] is orange, larger than 5 is red.

In the next part you can tap in a state name and the map will only show the earthquakes in this state.
The states list you can choose: SA(South Auistralia), ACT(Australian Capital Territory), NSW(New South Wales),
 NT(Northern Territory), QLD(Queensland), TAS(Tasmania), VIC(Victoria), and WA(Western Australia).

Next, just tap in the same state code you have done before, you can get all the information of the earthquakes in this state include magnitude, location,and time.

If you input the coordinate you are, the next part will tell you the distance of the nearest earthquake and give you information of 5 nearest earthquakes then plot them on the map.
(Rember tapping your longitude and latitude within Australia, lon:(110,160),lat:(-45,-10))

At last, it shows how to modify this program to fit other countries situation. In this part, you just need to change some coordinates and the detial instruction is in the code.

### List of dependencies

For the API requesting part, we need the `requests` package to send a request to the server, `JSON` package to format the data, `geopandas` packages to create a 
data frame, mation to format used for URL. `cartopy` package is useful to add base map, axes and data point, `datetime` package is for formatting time of the earhquake shown in the USGS data, 
`geopy` packge is for calculate distace, and `matplotlib.pyplot` package actucally does the plotting.

### Testing

For the `obtain_earthquake_data` function:

Test the function by passing different combinations of parameters, such as varying start and end dates, different minimum magnitudes, and different geographical coordinates.
Check if the function returns a valid response from the earthquake data API.
Verify if the returned data contains the expected fields and format.

For the `map_plotting` part:

Test the map creation by checking if the plot is generated successfully using `plt.figure()` or `plt.subplots()`.
Test the addition of earthquake data points by providing test earthquake data and verifying if the points are correctly plotted on the map using plt.scatter() or similar functions.
Check if the map is displayed or saved correctly using `plt.show()` or `plt.savefig()`.

For the `input_validation` functions:

Test the input validation functions by providing valid and invalid inputs and checking if the functions correctly identify them.
Verify if the error messages or exceptions are raised as expected for invalid inputs.

For the program as a whole:

Test the overall functionality by running the program with different inputs and verifying if the expected output is generated or if the program handles errors gracefully.

### Limitations

There are still many questions in this program, especially clear in the last example of Japan,
like the area is just a square, which is suitable for large and regular countries such as Australia or 
Canada, but this is not suitable for some small or complex countries.


### Future Improvements	

As I said in limitations, the next step is to put shapefile into the program to give a better boundries for each country or each state.
It is also important to give user a way to tap in the countries they want but not modify it from code.
