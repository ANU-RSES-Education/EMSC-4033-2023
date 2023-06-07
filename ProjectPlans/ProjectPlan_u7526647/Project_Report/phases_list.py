# Import all relevant modules
import json
import pandas as pd
from obspy.core import UTCDateTime

# Read the phase_parameters json file
# This file can be updated to accommodate more stations or to change processing parameters

def get_phases_list(): 
    """Create a dictionary of lists from phases file.

    Parameters
    ----------
    
    Returns
    -------
    phases_df: 
        pandas dataframe for list of dictionaries
    phases_list_dict:
        list of dictionaries for all phases

    """
# Create a list of dictionaries (one for each phase)
    with open('phase_parameters.json', encoding='utf-8') as json_file:
        phases_list_dict = json.load(json_file)

# Create a dataframe with new column order    
    df = pd.DataFrame(phases_list_dict).reindex(columns=["phase_name","min_distance","max_distance", "min_filter", "max_filter" ])
    phases_df = df
    return phases_df, phases_list_dict

# Set display options to display the whole table in a nice format
def display_phases_list(phases_df):
    """Display a list with all available phases.

    Parameters
    ----------
    
    Returns
    -------

    """
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 3000)
    pd.set_option('max_colwidth', 40)
    pd.set_option('display.colheader_justify', 'left')

    display(phases_df) # Note: don't know why it is underlined...works fine
    return

# look up phase
def look_up_phase(phase_name, phases_list_dict):
    """Look up the phase and check if it matches with a phase list entry.

    Parameters
    ----------
    phase_name: str
        name of seismic phase
    phases_list_dict:
        list of dictionaries for all phases
        
    Returns
    -------
    no_phase: int
        verificatation variable indicating if phase is in list
    phase_dict: dictionary
        dictionary for phase
    

    """
    # phase name should be a string
    # create empty dictionary as a string
    phase_dict = {}
    no_phase = 1
    for phase in phases_list_dict: 
        if str(phase["phase_name"]) == phase_name: 
            phase_dict = phase
            no_phase = 0
            
    return no_phase, phase_dict

