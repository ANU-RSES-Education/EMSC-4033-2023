# contains all functions used in the project (User_Application)

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


# STAGE 1: Set up client and create folder

def set_up_clients():
    """Sets up client connection to servers. For more information: https://docs.obspy.org/packages/obspy.clients.fdsn.html
    
    Parameters
    ----------
    
    Returns
    -------
    iris : 
        client to IRIS
    usgs : 
        client to USGS
    auspass:
        client to AusPass

    """
    auspass = Client("http://auspass.edu.au:8080") #,user='username',password='password')
    iris = Client("IRIS")
    usgs = Client("USGS")
    new_folder()
    return iris, usgs, auspass


def new_folder():
    """Creates a new folder in current directory to save files in.

    Parameters
    ----------
    
    Returns
    -------

    """
    path = "./automatic_wave_processing"
    os.mkdir(path)
    return


# STAGE 2: User chooses station and station metadata is retrieved.
# Get station metadata -> try clients in the order (1) Iris, (2) USGS, (3) AusPass

# IRIS
def get_station_metadata_iris(iris, network, starttime, endtime, filename):
    """Download station metadata from IRIS and save in a file.
    
    Parameters
    ----------
    iris : 
        client to IRIS
    network : str
        network name
    starttime : UTCDateTime
        Date and time defining the start of the station search interval.
    endtime : UTCDateTime
        Date and time defining the end of the station search interval.
    filename: str
        Name of the station metadata file.
    
    Returns
    -------

    """
    try: # Try and except statement to handle exception when no data is available.
        # Level response to download instrument response, only vertical component seismogram ("BHZ")
        data_stations = iris.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from IRIS.")
    except: 
        print("No data available from IRIS.")
    return

# USGS
def get_station_metadata_usgs(usgs, network, starttime, endtime, filename):
    """Download station metadata from IRIS and save in a file.
    
    Parameters
    ----------
    usgs : 
        client to USGS
    network : str
        network name
    starttime : UTCDateTime
        Date and time defining the start of the station search interval.
    endtime : UTCDateTime
        Date and time defining the end of the station search interval.
    filename: str
        Name of the station metadata file.
    
    Returns
    -------

    """    
    try: # Try and except statement to handle exception when no data is available.
        # Level response to download instrument response, only vertical component seismogram ("BHZ")
        data_stations = usgs.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from USGS.")
    except: 
        print("No data available from USGS.")
    return

# AusPass
def get_station_metadata_auspass(auspass, network, starttime, endtime, filename):
    """Download station metadata from IRIS and save in a file.
    
    Parameters
    ----------
    auspass : 
        client to AusPass
    network : str
        network name
    starttime : UTCDateTime
        Date and time defining the start of the station search interval.
    endtime : UTCDateTime
        Date and time defining the end of the station search interval.
    filename: str
        Name of the station metadata file.
    
    Returns
    -------

    """   
    try: # Try and except statement to handle exception when no data is available.
        # Level response to download instrument response, only vertical component seismogram ("BHZ")
        data_stations = auspass.get_stations(network=network, level="response", channel="BHZ", starttime=starttime, endtime=endtime) #this downloads all station information for a network.
        data_stations.write(filename, format="STATIONXML")
        print("Data taken from AusPass.")
    except: 
        print("No data available from AusPass.")
    return


# Overall function, combining the different sub-functions
def get_station_metadata(iris, usgs, auspass, network, starttime, endtime):
    """Download station metadata from IRIS, USGS or AusPass and save in a file.
    If no server contains data, the function will return an error.
    
    Parameters
    ----------
    iris : 
        client to IRIS
    usgs: 
        client to USGS
    auspass : 
        client to AusPass
    network : str
        network name
    starttime : UTCDateTime
        Date and time defining the start of the station search interval.
    endtime : UTCDateTime
        Date and time defining the end of the station search interval.
 
    Returns
    -------
    filename: str
        Name of the station metadata file.


    """  
    # Define file name and location to save.
    filename = "automatic_wave_processing/station_meta.xml"

    # First try IRIS
    get_station_metadata_iris(iris=iris, network=network, starttime=starttime, endtime=endtime, filename=filename)
    
    # If this does not work, try USGS:
    if not file_exists(filename):
        get_station_metadata_usgs(usgs=usgs, network=network, starttime=starttime, endtime=endtime, filename=filename)
        
        # If this does not work, try AusPass.
        if not file_exists(filename):
            get_station_metadata_auspass(auspass=auspass, network=network, starttime=starttime, endtime=endtime, filename=filename)

    return filename

# Final function for STAGE 2

def choose_station(iris, usgs, auspass):
    """Let the user choose a station and download station meta data from IRIS, USGS or AusPass.
    
    Parameters
    ----------
    iris : 
        client to IRIS
    usgs: 
        client to USGS
    auspass : 
        client to AusPass
 
    Returns
    -------
    station_metadata:
        Meta data for network and all stations and channels.
    starttime: UTCDateTime
        Date and time of the start of the station recording interval.
    endtime: UTCDateTime
        Date and time of the end of the station recording interval.
    network: str
        Chosen network.


    """  
    
    # First create the the network df and list of dictionaries
    # For function, see "network_list.py"
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
            # Display the list of all networks as a pandas dataframe.
            # For function, see "network_list.py"
            nl.display_network_list(network_df)

        else: 
            print("Please choose one of the following networks by entering the start and end time."+
            " If no end_date exists (station still running), enter None.")
            
            # Display the networks/arrays available for chosen network code
            # For function, see "network_list,py"
            nl.display_chosen_networks(network_dict)

            # Initialize a second input checker
            input_checker_2 = 0
            
            # Execute until user specifies a valid start and end time and chooses a station.
            while input_checker_2 == 0:
                try:
                    starttime = UTCDateTime(input("start_date:"))
                except:
                    print("Starttime must be in valid format (YYYY-MM-DD)")
                    continue

                endtime_input = input("end_date:")
            
                # Get starttime and endtime from the user
                if endtime_input == "None":
                    endtime = UTCDateTime.now
                else:
                    try:
                        endtime = UTCDateTime(endtime_input)
                    except:
                        print("Endtime must be in valid format (YYYY-MM-DD)")
                        continue

                # Verify the start and endtime input
                # For function, see "network_list.py"
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
            # Print station metadata to give user overview of available stations.
            print(station_metadata)
            network = station_name
    return station_metadata, starttime, endtime, network
 

# STAGE 3: User chooses a seismic phase.
def choose_phase():
    """Let the user choose a seismic phase.
    
    Parameters
    ----------
 
    Returns
    -------
    phase_name: str
        Name of the chosen seismic phase
    min_distance: float
        Minimum epicentral distance at which the phase can be observed.
    max_distance: float
        Maximum epicentral distance at which the phase can be observed.
    min_filter: float
        Minimum frequency for bandpass filter.
    max_filter: float
        Maximum frequency for bandpass filter.

        
    """     
    # Set up the list of possible phases and the corresponding processing parameters
    # For function, see "phases_list.py"
    phases_df, phases_list_dict = pl.get_phases_list()
    
    # Initialize input checker
    input_checker = 0

    while input_checker == 0: # executes loop until phase is successfully chosen
        clear_output(wait=True) # clear output (table)
        
        # Ask the user to choose a phase.
        phase_name = str(input("Which phase would you like to observe?"))

        # Check if phase is available
        no_phase, phase_dict = pl.look_up_phase(phase_name, phases_list_dict)

        # If station is not available/does not exist -> restart loop
        if no_phase == 1: 
            print("The chosen phase is not available. Please choose one from the following list.")
            # display the list of possible phases
            # for function, see "phases_list.py"
            pl.display_phases_list(phases_df)

        else:
            # set parameters as defined in "phase_parameters.json"
            input_checker = 1
            min_distance = float(phase_dict['min_distance'])
            max_distance = float(phase_dict['max_distance'])
            min_filter = float(phase_dict['min_filter'])
            max_filter = float(phase_dict['max_filter'])
            print("Chosen phase: " + str(phase_name))

    return (phase_name, min_distance, max_distance, min_filter, max_filter)

# STAGE 4: Get event list

def get_lat_and_lon(station_metadata):
    """Get longitude and latitude of station.
    
    Parameters
    station_metadata:
        Metadata for network and all stations and channels.
    ----------
 
    Returns
    -------
    latitude : float
        latitude of the network/station
    longitude : float
        longitude of the network/station

        
    """     
    latitude = station_metadata[0][0].latitude
    longitude = station_metadata[0][0].longitude

    return latitude, longitude


def choose_min_magnitude():
    """Let the user choose a minimum magnitude.
    
    Parameters
    ----------
 
    Returns
    -------
    min_magnitude : float
        Minimum magnitude of events.
        
    """ 

    # initialize an input check variable    
    min_magnitude_check = 0

    while min_magnitude_check == 0: # exectue until input requirements are met
        min_magnitude = input("Choose a minimum magnitude (MW) for events.")
        try:
            min_magnitude = float(min_magnitude)
        except:
            print("Minimum magnitude must be a number between 0 and 10.")
            continue
        if min_magnitude < 0 or min_magnitude > 10: 
            print("Minimum magnitude must be between 0 and 10.")
            continue
        else: 
            min_magnitude_check = 1

    return min_magnitude

def choose_max_magnitude(min_magnitude):
    """Let the user choose a maximum magnitude.
    
    Parameters
    ----------
 
    Returns
    -------
    max_magnitude : float
        Maximum magnitude of events.
        
    """ 

    # initialize an input check variable.
    max_magnitude_check = 0

    while max_magnitude_check == 0: # execute until input requirements are met.
        max_magnitude = input("Choose a maximum magnitude (MW) for events.")
        try:
            max_magnitude = float(max_magnitude)
        except:
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
    """Refine the start and end date of station operations for more accurate results.
    
    Parameters
    ----------
    station_metadata :
        Metadata for network and all stations and channels.
    starttime : UTCDateTime
        Starttime as defined in the network list.
    endtime: UTCDateTime
        Starttime as defined in the network list.
 
    Returns
    -------
    start_time : UTCDateTime
        Refined starttime.
    end_time : UTCDateTime
        Refined endtime.
        
    """ 

    # create a list to store all station starttimes.
    creation_date_list =[]
    for station in station_metadata[0]:
        creation_date_list.append(station.creation_date)
    # find the earliest starttime (if possible)
    try:
        start_time = min(creation_date_list)
    except:
        start_time = starttime
    
    # create a list to store all station endtimes.
    termination_date_list = []
    for station in station_metadata[0]:
        termination_date_list.append(station.termination_date)
    # find the latest endtime (if possible)
    try: 
        end_time = max(termination_date_list)
    except:
        end_time = endtime
        
    return start_time, end_time

def get_eventdata_iris(iris, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename):
    """Download an event catalogue using IRIS.
    
    Parameters
    ----------
    iris: 
        client to IRIS
    start_time: UTCDateTime
        start time of the event search interval.
    end_time: UTCDateTime
        end time of the event search interval.
    latitude: float
        latitude of station/network
    longitude: float
        longitude of station/network
    min_distance: float
        minimum epicentral distance between station and event
    max_distance: float
        maximum epicentral distance between station and event
    min_magnitude: float
        minimum magnitude of events
    max_magnitude: float
        maximum magnitude of events
    filename: str
        filename for event catalogue
 
    Returns
    -------
        
    """ 
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
    
    """Download an event catalogue using USGS.
    
    Parameters
    ----------
    usgs: 
        client to USGS
    start_time: UTCDateTime
        start time of the event search interval.
    end_time: UTCDateTime
        end time of the event search interval.
    latitude: float
        latitude of station/network
    longitude: float
        longitude of station/network
    min_distance: float
        minimum epicentral distance between station and event
    max_distance: float
        maximum epicentral distance between station and event
    min_magnitude: float
        minimum magnitude of events
    max_magnitude: float
        maximum magnitude of events
    filename: str
        filename for event catalogue
 
    Returns
    -------
        
    """
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

# Note: no need to try AusPass as it does not provide event data

def get_event_metadata(iris, usgs, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                        min_magnitude, max_magnitude):
    """Download an event catalogue using IRIS or USGS.
    
    Parameters
    ----------
    iris: 
        client to IRIS
    usgs:
        client to USGS
    start_time: UTCDateTime
        start time of the event search interval.
    end_time: UTCDateTime
        end time of the event search interval.
    latitude: float
        latitude of station/network
    longitude: float
        longitude of station/network
    min_distance: float
        minimum epicentral distance between station and event
    max_distance: float
        maximum epicentral distance between station and event
    min_magnitude: float
        minimum magnitude of events
    max_magnitude: float
        maximum magnitude of events
    filename: str
        filename for event catalogue
 
    Returns
    -------
    filename: str
        filename for event catalogue
    
        
    """

    filename = "automatic_wave_processing/event_cat.xml"
    
    # first try iris
    get_eventdata_iris(iris, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename)
    
    # if this does not work, try usgs
    if not file_exists(filename):
        get_eventdata_usgs(usgs, start_time, end_time, latitude, longitude, min_distance, max_distance, 
                       min_magnitude, max_magnitude, filename)

    return filename

# Final Function for STAGE 4, combining all previous functions
def choose_events(iris, usgs, station_metadata, starttime, endtime, min_distance, max_distance):
    """Get all events for given parameters using IRIS or USGS.
    
    Parameters
    ----------
    iris: 
        client to IRIS
    usgs:
        client to USGS
    station_metadata:
        Metadata for network and all stations/channels.
    starttime: UTCDateTime
        start time of the event search interval.
    endtime: UTCDateTime
        end time of the event search interval.
    min_distance: float
        minimum epicentral distance between station and event
    max_distance: float
        maximum epicentral distance between station and event
 
    Returns
    -------
    latitude: float
        latitude of the station
    longitude: float
        longitude of the station
    event_metadata:
        metadata for all events
    
        
    """  
    # get latitude and longitude of station  
    latitude, longitude = get_lat_and_lon(station_metadata)
    # ask user to choose minimum magnitude
    min_magnitude = choose_min_magnitude()
    # ask user to choose maximum magnitude
    max_magnitude = choose_max_magnitude(min_magnitude)
    # refine start and endtime
    start_time, end_time = refine_start_and_end(station_metadata, starttime, endtime)

    # get the event catalogue from iris or usgs
    event_catalogue = get_event_metadata(iris, usgs, start_time, end_time, latitude, longitude, min_distance,
                                         max_distance, min_magnitude, max_magnitude)
    
    # save event_metadata in variable
    event_metadata = read_events(event_catalogue)

    print(event_metadata.__str__(print_all=True))
    event_metadata.plot()
    
    # only allow a maximum of 50 entries
    if len(event_metadata) > 50: 
        raise Exception("The maximum number of events is 50. Please refine the magnitude window or choose a different station.")
    
    return latitude, longitude, event_metadata

# STAGE 5: Create an event list file for future use 
def create_event_list(event_metadata, latitude, longitude, phase_name):
    """Create an event list textfile for a given event catalogue,
        including the theoretical arrival time for a given phase.
    
    Parameters
    ----------
    event_metadata:
        metadata for all events
    latitude: float
        latitude of station
    longitude: float
        longitude of station
    phase_name: str
        chosen seismic phase
    station_metadata: inventory(obspy)
        Metadata for network and all stations/channels.
    starttime: UTCDateTime
        start time of the event search interval.
    endtime: UTCDateTime
        end time of the event search interval.
    min_distance: float
        minimum epicentral distance between station and event
    max_distance: float
        maximum epicentral distance between station and event
 
    Returns
    -------
    event_data:
        list of lists containing all event data
    
        
    """     
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
    
    # create a file containing all the data
    outputfile = "automatic_wave_processing/events_data.txt"
    fp = open(outputfile, 'w')
    fp.write("ID, Time, Magnitude(MW), Depth, Epicentral Distance, Phase theor. traveltime, " +
        "Phase theor. arrival\n")
    for i in event_data:
        fp.write(str(i) + "\n")
    fp.close()

    return event_data


# STAGE 6: Get raw waveform data
def create_raw_waveforms_folder():
    """Creates a new folder to save raw waveforms in.

    Parameters
    ----------
    
    Returns
    -------

    """
    path = "automatic_wave_processing/raw_waveforms"
    os.mkdir(path)
    return

def iris_get_raw_waveforms(iris, network, event_data): 
    """Get the raw waveforms for all events from iris.
    
    Parameters
    ----------
    iris: 
        client to IRIS
    network: str
        network name
    event_data:
        List of lists containing all event data.
 
    Returns
    -------
        
    """  
    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        # for each event get a 1 hour time window
        tend = tstart + 3600 # get one hour after origin time

        filename = "automatic_wave_processing/raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                # get waveforms
                st = iris.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def usgs_get_raw_waveforms(usgs, network, event_data):
    """Get the raw waveforms for all events from usgs.
    
    Parameters
    ----------
    usgs: 
        client to USGS
    network: str
        network name
    event_data:
        List of lists containing all event data.
 
    Returns
    -------
        
    """  
    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        # for each event get a one hour time window
        tend = tstart + 3600 # get one hour after origin time

        filename = "automatic_wave_processing/raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                # get raw waveforms
                st = usgs.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def auspass_get_raw_waveforms(auspass, network, event_data):
    """Get the raw waveforms for all events from AusPass.
    
    Parameters
    ----------
    auspass: 
        client to Auspass
    network: str
        network name
    event_data:
        List of lists containing all event data.
 
    Returns
    -------
        
    """  
    event_id = 0

    for event in event_data:
        event_id += 1
        tstart = UTCDateTime(float(event[1]))
        # for each event get a 1 hour time window
        tend = tstart + 3600 # get one hour after origin time

        filename = "automatic_wave_processing/raw_waveforms/raw_event_" + str(event_id)+".mseed"
    
        try: # use try statement because for some stations, no data will be available
            if not file_exists(filename):
                # get raw waveforms
                st = auspass.get_waveforms(network=str(network), location = "*", station = "*", channel="BHZ", starttime=tstart, endtime=tend)
                st.write(filename, format="MSEED")

        except: 
            continue
    return

def get_raw_waveforms(iris, usgs, auspass, network, event_data): 
    """Get the raw waveforms for all events from either IRIS, USGS or AusPass.
    
    Parameters
    ----------
    iris:
        client to IRIS
    usgs: 
        client to USGS
    auspass:
        client to AusPass
    network: str
        network name
    event_data:
        List of lists containing all event data.
 
    Returns
    -------
        
    """  
    path = "automatic_wave_processing/raw_waveforms"

    # first try IRIS
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

# Last function of STAGE 6, combining all the previous ones
def download_raw_waveforms(event_metadata, latitude, longitude, iris, usgs, auspass, network, phase_name):
    """Download the raw waveforms and save them in a folder.
    
    Parameters
    ----------
    event_metadata: 
        metadata for all events
    latitude: float
        latitude of station
    longitude: float
        longitude of station
    iris: 
        client to IRIS
    usgs: 
        client to USGS
    auspass:
        client to AusPass
    network: str
        network name
    phase_name: str
        name of the seismic phase
 
    Returns
    event_data: 
        list of lists containing all event data
    -------
        
    """  
    event_data = create_event_list(event_metadata, latitude, longitude, phase_name)
    create_raw_waveforms_folder()
    get_raw_waveforms(iris, usgs, auspass, network, event_data)

    return event_data

# STAGE 7: Process waveforms
def create_processed_waveforms_folder():
    """Creates a new folder to save processed waveforms in.

    Parameters
    ----------
    
    Returns
    -------

    """
    path = "automatic_wave_processing/processed_waveforms"
    os.mkdir(path)
    return

def process_waveforms(station_metadata, event_data, min_filter, max_filter):
    """Process the waveforms.
    
    Parameters
    ----------
    station_metadata:
        metadata for network and all stations and channels
    event_data:
        list of lists containing all event data
    min_filter:
        minimum for bandpass filter in Hertz
    max_filter:
        maximum for bandpass filter in Hertz
 
    Returns
    -------
        
    """ 
    # create folder for processed waveforms 
    create_processed_waveforms_folder()
    event_id = 1

    # for each event in the event list, check if a raw waveform exists and if yes, process it.
    for id in range(1,(len(event_data)+1)):

        filename = "automatic_wave_processing/raw_waveforms/raw_event_"+str(event_id)+".mseed"
    
        if file_exists(filename):
            st = read(filename)
            wave = st.copy()
            # remove instrument response
            wave.remove_response(inventory=station_metadata, output='VEL')
            # detrent it
            wave.detrend() # Note!!! this operation will modify the st
            # taper to account for discontinuities
            wave.taper(max_percentage=0.01, max_length=100) 
            # apply the filter specified in parameters
            wave.filter("bandpass", freqmin=min_filter, freqmax=max_filter, zerophase=True, corners=4) # filter

            # save processed waveform
            wave.write("automatic_wave_processing/processed_waveforms/processed_event_" + str(event_id) + ".mseed", format="MSEED")
    

        event_id+=1
    return

def create_phase_waveforms_folder():
    """Creates a folder to save trimmed waveforms in.

    Parameters
    ----------
    
    Returns
    -------

    """
    path = "automatic_wave_processing/phase_waveforms"
    os.mkdir(path)
    return

def create_stack_waveforms_folder():
    """Creates a folder to save waveform stacks in.

    Parameters
    ----------
    
    Returns
    -------

    """
    path = "automatic_wave_processing/stack_waveforms"
    os.mkdir(path)

def get_phase_waveforms(event_data):
    """Get the waveforms trimmed to theoretical arrival and stacks.
    
    Parameters
    ----------
    event_data:
        List of lists containing all event data.
 
    Returns
    -------
        
    """  
    # create folders
    create_phase_waveforms_folder()
    create_stack_waveforms_folder()

    event_id = 1
    for i in range(1,(len(event_data)+1)):

        filename = "automatic_wave_processing/processed_waveforms/processed_event_"+str(event_id)+".mseed"

        # Phase arrival time
        event_list = event_data[(i-1)]
        # theoretical arrival of phase
        theoretical_arrival_Phase = UTCDateTime(float(event_list[6]))
        # get a 60 second time window
        starttime = theoretical_arrival_Phase - 30 
        endtime = theoretical_arrival_Phase + 30

        if file_exists(filename):
            st2 = read(filename)
            # trim to 60 second window around theoretical arrival time of PKIKP
            st2.trim(starttime, endtime)
            # create a new file
            try:
                st2.write("automatic_wave_processing/phase_waveforms/phase_event_" + str(event_id) + ".mseed", format="MSEED")
                st2.plot()
            except:
                print("No data for this trace.")
            # create a stack over all stations
            try:
                stack = st2.stack()
                stack.write("automatic_wave_processing/stack_waveforms/phase_stack_event_" + str(event_id) + ".mseed", format="MSEED")
                stack.plot()
            except:
                print("No stack for this trace")
                
        event_id+=1
    return