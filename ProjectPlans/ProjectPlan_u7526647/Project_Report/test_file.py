# Test everything with an example: 
import obspy
from obspy.core import UTCDateTime
from obspy.core.inventory.inventory import read_inventory
from obspy.core.event import read_events
from obspy.core.stream import read
from obspy.clients.fdsn import Client

from obspy.geodetics import locations2degrees
from obspy.taup import TauPyModel

import functions.py as fun
import network_list.py as nl
import phases_list.py as pl

from os.path import exists as file_exists
import os

import network_list as nl
import phases_list as pl

from IPython.display import clear_output

# NOTES: This file tests almost all individual function for the following example.
# If a specific line of code will raise an error, the run will stop.
# If everything worked fine, it will print a success message.
station_name = "1E"
start_time = UTCDateTime("2013-01-01")
end_time = UTCDateTime("2014-12-31")
phase_name = "PKIKP"
min_magnitude = 6
max_magnitude = 7

# Set up client 
iris, usgs, auspass = fun.set_up_client()

# Create new folder 
fun.new_folder()

# get station metadata -> use overall function which includes the individual ones:
filename = fun.get_station_metadata(iris, usgs, auspass, station_name, start_time, end_time)
station_metadata = read_inventory(filename)

# Note: user input cannot be tested here -> needs individual tests (maybe just try different options?)

# Choose phase
phases_df, phases_list_dict = pl.get_phases_list()
no_phase, phase_dict = pl.look_up_phase(phase_name, phases_list_dict)

assert no_phase == 0
# again, input cannot be tested here

# get input parameters
min_distance = float(phase_dict['min_distance'])
max_distance = float(phase_dict['max_distance'])
min_filter = float(phase_dict['min_filter'])
max_filter = float(phase_dict['max_filter'])

# get latitude and longitude
latitude, longitude = fun.get_lat_and_lon(station_metadata)

# refine start and endtime
starttime, endtime = fun.refine_start_and_end(station_metadata, start_time, end_time)

# get event data
event_catalogue = fun.get_event_metadata(iris, usgs, starttime, endtime, latitude, longitude, min_distance, max_distance, 
                        min_magnitude, max_magnitude)

# save event_metadata in variable
event_metadata = read_events(event_catalogue)

print(event_metadata.__str__(print_all=True))
event_metadata.plot()
    
# only allow a maximum of 50 entries
if len(event_metadata) > 50: 
    raise Exception("The maximum number of events is 50. Please refine the magnitude window or choose a different station.")


# Get event list and event data
event_data = fun.create_event_list(event_metadata, latitude, longitude, phase_name)

# Create raw waveform folder
fun.create_raw_waveforms_folder()

# Get raw waveforms
fun.get_raw_waveforms(iris, usgs, auspass, station_name, event_data)


# Process waveforms
fun.process_waveforms(station_metadata, event_data, min_filter, max_filter)


# Create folder and get waveforms
fun.get_phase_waveforms(event_data)

print("Successful test run.")