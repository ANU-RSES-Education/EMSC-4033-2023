# contains all functions used in Stage 1 of the project

# Import all relevant modules
import obspy
from obspy.core import UTCDateTime
from obspy.core.inventory.inventory import read_inventory
from obspy.core.event import read_events
from obspy.core.stream import read
from obspy.clients.fdsn import Client

from obspy.geodetics import locations2degrees
from obspy.taup import TauPyModel

from os.path import exists as file_exists
import os

import network_list as nl
import phases_list as pl

from IPython.display import clear_output


# Set up clients -> if more clients needed, add here
def set_up_clients():
    auspass = Client("http://auspass.edu.au:8080") #,user='username',password='password')
    iris = Client("IRIS")
    usgs = Client("USGS")
    return iris, usgs, auspass

# Get station metadata -> try clients in the order (1) Iris, (2) USGS, (3) AusPass
def get_station_metadata_iris(iris, network, starttime, endtime, filename):
    # first try IRIS:
    try:
        data_stations = iris.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from IRIS.")
    except: 
        print("No data available from IRIS.")
    return

def get_station_metadata_usgs(usgs, network, starttime, endtime, filename):
    # then try USGS:
    try:
        data_stations = usgs.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from USGS.")
    except: 
        print("No data available from USGS.")
    return

def get_station_metadata_auspass(auspass, network, starttime, endtime, filename):
    # lastly try AusPass:
    try:
        data_stations = auspass.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from AusPass.")
    except: 
        print("No data available from AusPass.")
    return


# Overall function, combining the different sub-functions
def get_station_metadata(iris, usgs, auspass, network, starttime, endtime):
    filename = "station_meta.xml"
    # first try iris
    get_station_metadata_iris(iris=iris, network=network, starttime=starttime, endtime=endtime, filename=filename)
    
    # if this does not work, try usgs
    if not file_exists(filename):
        get_station_metadata_usgs(usgs=usgs, network=network, starttime=starttime, endtime=endtime, filename=filename)
        
        # if this does not work, try auspass
        if not file_exists(filename):
            get_station_metadata_auspass(auspass=auspass, network=network, starttime=starttime, endtime=endtime, filename=filename)

    return filename

def choose_station(iris, usgs, auspass):
    # First create the the network df and list of dictionaries
    network_df, network_list_dict = nl.get_network_list()
    # Initialize input checker to 0
    input_checker = 0

    while input_checker == 0: # executes loop until station is successfully chosen
        clear_output(wait=True)
        # Ask the user to choose a network.
        station_name = str(input("Please choose a network (fdsn code)."))

        # Check if station is available
        no_network, network_dict = nl.look_up_station(station_name, network_list_dict)

        # If station is not available/does not exist -> restart loop
        if no_network == 1: 
            print("The chosen network is not available. Please choose one from the following list.")
            nl.display_network_list(network_df)

        else: 
            print("Please choose one of the following networks by entering the start and end time."+
            " If no end_date exists (station still running), enter None.")
            nl.display_chosen_networks(network_dict)

            # Initialize a second input checker
            input_checker_2 = 0
            
            # Execute until user specifies a valid start and end time and chooses a station.
            while input_checker_2 == 0:
                starttime = UTCDateTime(input("start_date:"))
                endtime_input = input("end_date:")
                # Get starttime and endtime from the user
                if endtime_input == "None":
                    endtime = UTCDateTime.now
                else: 
                    endtime = UTCDateTime(endtime_input)

                # Verify the start and endtime input
                input_validation = nl.start_and_endtime_check(starttime, endtime, network_dict)
                if input_validation == 1:
                    input_checker_2 = 1
                else:
                    print("Please check your date entries and try again.")

            # Now attempt to get station metadata for the chosen station
            filename = get_station_metadata(iris, usgs, auspass, station_name, starttime, endtime)

            if file_exists(filename):
                print("Successfully downloaded station metadata.")
                input_checker = 1

            else: 
                print("No data available for this station. Please choose a different one.")

            station_metadata = read_inventory(filename)
            print(station_metadata)
            network = station_name
    return station_metadata, starttime, endtime, network
 
def choose_phase():
    # Set up the list of possible phases and the corresponding processing parameters
    phases_df, phases_list_dict = pl.get_phases_list()
    # Initialize input checker
    input_checker = 0
    while input_checker == 0: # executes loop until phase is successfully chosen
        clear_output(wait=True)
        # Ask the user to choose a phase.
        phase_name = str(input("Which phase would you like to observe?"))

        # Check if phase is available
        no_phase, phase_dict = pl.look_up_phase(phase_name, phases_list_dict)

        # If station is not available/does not exist -> restart loop
        if no_phase == 1: 
            print("The chosen phase is not available. Please choose one from the following list.")
            pl.display_phases_list(phases_df)

        else:
            input_checker = 1
            min_distance = float(phase_dict['min_distance'])
            max_distance = float(phase_dict['max_distance'])
            min_filter = float(phase_dict['min_filter'])
            max_filter = float(phase_dict['max_filter'])
            print("Chosen phase: " + str(phase_name))

    return (phase_name, min_distance, max_distance, min_filter, max_filter)


def get_lat_and_lon(station_metadata):
    latitude = station_metadata[0][0].latitude
    longitude = station_metadata[0][0].longitude

    return latitude, longitude

def choose_min_magnitude():
    min_magnitude_check = 0
    while min_magnitude_check == 0:
        min_magnitude = input("Choose a minimum magnitude (MW) for events.")
        try:
            min_magnitude = float(min_magnitude)
        except ValueError:
            print("Minimum magnitude must be a number between 0 and 10.")
            continue
        if min_magnitude < 0 or min_magnitude > 10: 
            print("Minimum magnitude must be between 0 and 10.")
            continue
        else: 
            min_magnitude_check = 1
    return min_magnitude

def choose_max_magnitude(min_magnitude):
    max_magnitude_check = 0
    while max_magnitude_check == 0:
        max_magnitude = input("Choose a maximum magnitude (MW) for events.")
        try:
            max_magnitude = float(max_magnitude)
        except ValueError:
            print("Maximum magnitude must be a number between 0 and 10.")
            continue
        if min_magnitude < 0 or min_magnitude > 10: 
            print("Maximum magnitude must be between 0 and 10.")
            continue
        elif max_magnitude <= min_magnitude: 
            print("Maximum magnitude must be larger than minimum magnitude ("+ str(min_magnitude)+")")
            continue
        else: 
            max_magnitude_check = 1
    return max_magnitude

def refine_start_and_end(station_metadata, starttime, endtime):

    creation_date_list =[]
    for station in station_metadata[0]:
        creation_date_list.append(station.creation_date)
    try:
        start_time = min(creation_date_list)
    except:
        start_time = starttime
        
    termination_date_list = []
    for station in station_metadata[0]:
        termination_date_list.append(station.termination_date)
    try: 
        end_time = max(termination_date_list)
    except:
        end_time = endtime
        
    return start_time, end_time

def get_eventdata_iris(iris, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename):
    # first try IRIS:
    try:
        event_cat = iris.get_events(starttime=start_time, endtime=end_time, latitude=latitude, longitude=longitude,
                                minradius = min_distance, maxradius = max_distance,
                                minmagnitude = min_magnitude, maxmagnitude = max_magnitude, magnitudetype="MW",
                                orderby="magnitude")
    
        event_cat.write(filename, format="QUAKEML")
        print("IRIS was successful.")
    except: 
        print("No events available for these parameters from IRIS.")
    return

def get_eventdata_usgs(usgs, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename):
    # next try usgs:
    try:
        event_cat = usgs.get_events(starttime=start_time, endtime=end_time, latitude=latitude, longitude=longitude,
                                minradius = min_distance, maxradius = max_distance,
                                minmagnitude = min_magnitude, maxmagnitude = max_magnitude, magnitudetype="MW",
                                orderby="magnitude")
    
        event_cat.write(filename, format="QUAKEML")
        print("USGS was successful.")
    except: 
        print("No events available for these parameters from USGS.")
    return

def get_event_metadata(iris, usgs, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                        min_magnitude, max_magnitude):
    filename = "event_cat.xml"
    
    # first try iris
    get_eventdata_iris(iris, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename)
    
    # if this does not work, try usgs
    if not file_exists(filename):
        get_eventdata_usgs(usgs, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename)

    return filename

def choose_events(iris, usgs, station_metadata, starttime, endtime, min_distance, max_distance):
    
    latitude, longitude = get_lat_and_lon(station_metadata)
    min_magnitude = choose_min_magnitude()
    max_magnitude = choose_max_magnitude(min_magnitude)
    start_time, end_time = refine_start_and_end(station_metadata, starttime, endtime)

    event_catalogue = get_event_metadata(iris, usgs, start_time, end_time, latitude, longitude, min_distance,
                                         max_distance, min_magnitude, max_magnitude)
    
    event_metadata = read_events(event_catalogue)

    print(event_metadata.__str__(print_all=True))
    event_metadata.plot()

    if len(event_metadata) > 50: 
        raise Exception("The maximum number of events is 50. Please refine the magnitude window or choose a different station.")
    
    return latitude, longitude, event_metadata
    
def create_event_list(event_metadata, latitude, longitude, phase_name):
    # Choose a theoretical model to get expected arrival times at certain distances
    model = TauPyModel(model="prem") # uses prem model but other models would be possible

    event_id = 1  # initialize event id

    # Create lists with: Time, Magnitude (MW), Depth, Epicentral Distance, Travel time and Theoretical arrival:
    event_data = []

    for event in event_metadata:
        event_list = []
        event_list.append(event_id)
        # Time
        event_time = event.origins[0].time
        event_list.append(event_time.timestamp)

        # Magnitude
        event_magnitude = event.magnitudes[0].mag
        event_list.append(event_magnitude)

        # Depth
        event_depth = event.origins[0].depth
        event_depth_in_km = event_depth/1000
        event_list.append(event_depth) # Is depth in m???

        # Epicentral Distance
        event_latitude = event.origins[0].latitude
        event_longitude = event.origins[0].longitude
        epicentral_distance = locations2degrees(latitude, longitude, event_latitude, event_longitude)
        event_list.append(epicentral_distance)

        # Travel Time Phase
        travel_time_Phase = model.get_travel_times(source_depth_in_km = event_depth_in_km, distance_in_degree = epicentral_distance, phase_list = [str(phase_name)])
        travel_time_seconds_Phase = travel_time_Phase[0].time
        event_list.append(travel_time_seconds_Phase)

        # Theoretical Arrival Phase 
        theoretical_arrival_Phase = event_time + travel_time_seconds_Phase
        event_list.append(theoretical_arrival_Phase.timestamp)
    
        event_data.append(event_list)
        event_id+=1
    
    outputfile = "events_data.txt"
    fp = open(outputfile, 'w')
    fp.write("ID, Time, Magnitude(MW), Depth, Epicentral Distance, Phase theor. traveltime, " +
        "Phase theor. arrival\n")
    for i in event_data:
        fp.write(str(i) + "\n")
    fp.close()

    return event_data


def create_raw_waveforms_folder():
    path = "./raw_waveforms"
    os.mkdir(path)
    return

def iris_get_raw_waveforms(iris, network, event_data): 

    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        tend = tstart + 3600 # get one hour after origin time

        filename = "raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                st = iris.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def usgs_get_raw_waveforms(usgs, network, event_data):

    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        tend = tstart + 3600 # get one hour after origin time

        filename = "raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                st = usgs.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def auspass_get_raw_waveforms(auspass, network, event_data):

    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        tend = tstart + 3600 # get one hour after origin time

        filename = "raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                st = auspass.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def get_raw_waveforms(iris, usgs, auspass, network, event_data): 
    path = "raw_waveforms"
    iris_get_raw_waveforms(iris, network, event_data)

    # if folder is empty -> try usgs
    if os.listdir(path) == []:
        print("No data found for IRIS.")

        usgs_get_raw_waveforms(usgs, network, event_data)

        # check if folder is still empty -> try auspass
        if os.listdir(path) == []:
            print("No data found for USGS.")

            auspass_get_raw_waveforms(auspass, network, event_data)

            # If folder still empty, return error message
            if os.listdir(path) == []:
                print("No data found for AusPass.")
                print("No data available on any of the servers. Choose a different station.")

            else: 
                print("Raw waveforms successfully downloaded.")

        else: 
            print("Raw waveforms successfully downloaded")

    else: 
        print("Raw waveforms successfully downloaded.")
    
    return

def download_raw_waveforms(event_metadata, latitude, longitude, iris, usgs, auspass, network, phase_name):
    event_data = create_event_list(event_metadata, latitude, longitude, phase_name)
    create_raw_waveforms_folder()
    get_raw_waveforms(iris, usgs, auspass, network, event_data)

    return event_data

def create_processed_waveforms_folder():
    path = "./processed_waveforms"
    os.mkdir(path)
    return

def process_waveforms(station_metadata, event_data, min_filter, max_filter):
    create_processed_waveforms_folder()
    event_id = 1

    for id in range(1,(len(event_data)+1)):

        filename = "raw_waveforms/raw_event_"+str(event_id)+".mseed"
    
        if file_exists(filename):
            st = read(filename)
            wave = st.copy()
            wave.remove_response(inventory=station_metadata, output='VEL')
            wave.detrend() # Note!!! this operation will modify the st
            wave.taper(max_percentage=0.01, max_length=100) 
            wave.filter("bandpass", freqmin=min_filter, freqmax=max_filter, zerophase=True, corners=4) # filter

            wave.write("processed_waveforms/processed_event_" + str(event_id) + ".mseed", format="MSEED")
    

        event_id+=1
    return

def create_phase_waveforms_folder():
    path = "./phase_waveforms"
    os.mkdir(path)
    return

def create_stack_waveforms_folder():
    path = "./stack_waveforms"
    os.mkdir(path)

def get_phase_waveforms(event_data):
    create_phase_waveforms_folder()
    create_stack_waveforms_folder()

    event_id = 1
    for i in range(1,(len(event_data)+1)):

        filename = "processed_waveforms/processed_event_"+str(event_id)+".mseed"

        # Phase arrival time
        event_list = event_data[(i-1)]
   
        theoretical_arrival_Phase = UTCDateTime(float(event_list[6]))

        starttime = theoretical_arrival_Phase - 30 
        endtime = theoretical_arrival_Phase + 30

        if file_exists(filename):
            st2 = read(filename)
            # trim to 60 second window around theoretical arrival time of PKIKP
            st2.trim(starttime, endtime)
            # create a new file
            try:
                st2.write("phase_waveforms/phase_event_" + str(event_id) + ".mseed", format="MSEED")
                st2.plot()
            except:
                print("No data for this trace.")
            # create a stack over all stations
            try:
                stack = st2.stack()
                stack.write("stack_waveforms/phase_stack_event_" + str(event_id) + ".mseed", format="MSEED")
                stack.plot()
            except:
                print("No stack for this trace")
                
        event_id+=1
    return