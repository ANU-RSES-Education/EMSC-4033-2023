## EMSC4033 - Project Report

### Instructions

This code enables the visualization of the parameters of the Gaussian diffusion model and the concentration diffusion. During the running process, the program will ask you to enter some content, don't worry, there are detailed instructions. In addition to realizing visualization, two csv files will be produced, which are related to the parameter calculation link. The purpose is to present some important information more intuitively to readers for easy understanding.


### List of dependencies + short description

requests: The requests package is used for making HTTP requests. It allows you to send HTTP requests to a specified URL and handle the responses.
datetime: It allows you to work with dates, times, and time intervals, and perform various operations like formatting, parsing, and arithmetic calculations on dates and times.
pysolar.solar: Provides functions to calculate the solar position (altitude and azimuth) for a given location and time. 
pytz: Provides functionality to localize and convert datetime objects to different time zones.
numpy: Realize complex operations.
csv: It provides functionality to parse CSV data into Python data structures and vice versa.
mpl_toolkits.mplot3d: It enables the creation of 3D visualizations, including 3D scatter plots.


### Testing

By putting some simple 'print()' functions in the code, it is possible to verify that the entered value is valid. At the same time, for different input content, the result of the code output and the generated image also change accordingly. The output results shown in text and images are reasonable. Finally, the code runs without bugs.



### Limitations

The code is too lengthy. In fact, some of the codes that define functions can be generated into py files, and then put into the same directory and called by the import command. But for the logic of the code, I chose to put all the code into the ipynb file, so that it is easier for readers to understand.



### Future Improvements	

How to incorporate more factors affecting the atmosphere and pollutants into the concentration calculation and apply it to the simulation of daily pollutant emissions is the next step.
