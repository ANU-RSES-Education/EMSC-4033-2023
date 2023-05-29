# Module to generate a table with all network names and start and end dates 
# This will help the user to choose a valid input in Stage 1 "User chooses station"

# Import all relevant modules
import json
import pandas as pd
from obspy.core import UTCDateTime

# Read the network_names json file
# -> This file should be updated regularly to accommodate for changes and new networks
# url: https://www.fdsn.org/ws/networks/1/query

def get_network_list(): 
# Create a list of dictionaries (one for each station)
    with open('network_names.json', encoding='utf-8') as json_file:
        network_list_dict = json.load(json_file)

# Create a dataframe with new column order    
    df = pd.DataFrame(network_list_dict).reindex(columns=["fdsn_code","start_date","end_date", "name", "doi" ])
    network_df = df
    return network_df, network_list_dict

# Set display options to display the whole table in a nice format
def display_network_list(network_df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 3000)
    pd.set_option('max_colwidth', 40)
    pd.set_option('display.colheader_justify', 'left')

    display(network_df) # Note: don't know why it is underlined...works fine
    return

# look up stations
def look_up_station(station_name, network_list_dict): 
    # station name should be a string
    no_network = 1
    network_dict = []
    for network in network_list_dict: 
        if str(network["fdsn_code"]) == station_name: 
            network_dict.append(network)
            no_network = 0
    
    return no_network, network_dict

# Display chosen networks
def display_chosen_networks(network_dict):
    df = pd.DataFrame(network_dict).reindex(columns=["fdsn_code","start_date","end_date", "name", "doi" ])
    station_df = df
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 3000)
    pd.set_option('max_colwidth', 40)
    pd.set_option('display.colheader_justify', 'left')

    display(station_df)

    return

def start_and_endtime_check(starttime, endtime, network_dict):
    input_validation = 0
    if endtime == UTCDateTime.now:
        for network in network_dict:
            if starttime == UTCDateTime(network["start_date"]) and network["end_date"] is None:
                input_validation = 1
    else: 
        for network in network_dict: 
            if starttime == UTCDateTime(network["start_date"]) and str(endtime) == UTCDateTime(network["end_date"]):
                input_validation = 1

    return input_validation



