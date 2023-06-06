"""
The user_input.py is a module consisted of several helper function
for job_xml_generator.py program. This modules accepts several type 
of user inputs as parameters/settings that will be used to generate
XML files and configuration file.

Brief description of the some helper functions in this module are,
- exposure_model_user_input(): 
    Returns all user inputs as parameters in generating exposure_model.xml
- fragility_model_input(): 
    Generate fragility_model.csv and save it to a folder and 
    returns all user inputs as parameters in generating fragility_model.xml
- rupture_model_input(): 
    Returns all user inputs as parameters in generating rupture_model.xml
- job_ini_input(): 
    Returns all user inputs as parameters in generating job.ini
- check_number(message,int_num=False,lower_lim=None,upper_lim=None)
    Validate numeric inputs, whether it is integer or float, and check
    if the number falls within specific ranges.
- test_input(message,allow_spaces=False)
    Validate if inputs are in the expected string format.
"""
import os
import re
import pandas as pd

# Create directory for all generated file
data_folder = "data"
output_folder = "output"

if not os.path.exists(data_folder):
    os.mkdir(data_folder)
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
    
# Helper function for selecting cost_type
def cost_type_pick():
    cost_type_map = {
        "1": "aggregated",
        "2": "per_asset",
        "3": "per_area"
    }
    print("""Cost type:
    1 - Aggregated
    2 - Per Asset
    3 - Per Area""")
    cost_type_picked = input("Pick 1 to 3 for your cost type: ")
    while cost_type_picked not in cost_type_map:
        cost_type_picked = input("Not a number from 1 to 3! Pick 1 to 3 : ")
    print("Your cost type: ", cost_type_map[cost_type_picked] )
    return cost_type_map[cost_type_picked]

# Helper function for selecting area type
def area_type_pick():
    area_type_map = {
        "1": "aggregated",
        "2": "per_asset"
    }
    print("""Area type:
    1 - Aggregated
    2 - Per Asset""")
    area_type_picked = input("Pick 1 to 2 for your area type: ")
    while area_type_picked not in area_type_map:
        area_type_picked = input("Not a number from 1 or 2! Pick 1 or 2 : ")
    print("Your area type: ", area_type_map[area_type_picked] )
    return area_type_map[area_type_picked]

# Helper function for selecting loss category
def loss_cat_pick():
    loss_cat_map = {
        "1": "structural",
        "2": "nonstructural",
        "3": "business_interuption",
        "4": "contents",
        "5": "occupants"
    }
    print("""Loss type:
    1 - Structural
    2 - Non-structural
    3 - Business Interruption
    4 - Contents
    5 - Occupants""")
    loss_cat_picked = input("Pick 1 to 5 for your loss category: ")
    while loss_cat_picked not in loss_cat_map:
        loss_cat_picked = input("Not a number from 1 or 5! Pick 1 to 5 : ")
    print("Your loss category: ", loss_cat_map[loss_cat_picked] )
    return loss_cat_map[loss_cat_picked]

# Helper function for validating a number within specified limits
def check_number(message, int_num=False, lower_lim=None, upper_lim=None):
    retry_message = "Please provide a valid number: "
    if int_num is False:
        while True:
            input_var = input(message)
            try:
                check = float(input_var)
                if lower_lim is not None and check < lower_lim:
                    print(f"Number should be greater than or equal to {lower_lim}.")
                elif upper_lim is not None and check > upper_lim:
                    print(f"Number should be less than or equal to {upper_lim}.")
                else:
                    return str(check)
            except ValueError:
                message = retry_message
            message = retry_message
    else:
        while True:
            input_var = input(message)
            try:
                check = float(input_var)
                if check.is_integer():
                    if lower_lim is not None and check < lower_lim:
                        print(f"Number should be greater than or equal to {lower_lim}.")
                    elif upper_lim is not None and check > upper_lim:
                        print(f"Number should be less than or equal to {upper_lim}.")
                    else:
                        return str(int(check))
            except ValueError:
                message = retry_message
            message = retry_message

# Helper function for validating text input
def text_input(message, allow_spaces=False):
    if allow_spaces is False:
        pattern = re.compile("^[A-Za-z0-9_]*$")
        retry_message = "Please provide a text that only consists of alphanumeric characters (letters A-Z, a-z, numbers 0-9), and underscores (_): "
        input_var = input(message)
        while pattern.fullmatch(input_var) is None:
            input_var = input(retry_message)
    else:
        pattern = re.compile("^[A-Za-z0-9_ ]*$")
        retry_message = "Please provide a text that consists of alphanumeric characters (letters A-Z, a-z, numbers 0-9), underscores (_), and spaces: "
        input_var = input(message)
        while pattern.fullmatch(input_var) is None:
            input_var = input(retry_message)
    return input_var

# Helper function for validating csv filename
def csv_input(message):
    pattern = re.compile("^[A-Za-z0-9_]*\.csv$")
    retry_message = "Please provide a filename that only consists of alphanumeric characters, underscore, and has *.csv extension): "
    input_var = input(message)
    while pattern.fullmatch(input_var) is None:
        input_var = input(retry_message)
    return input_var

# Helper function to print a line break
def print_line_break():
    print("--------------------------------------------------------")

# Helper function for validating yes/no input
def yes_no_input(message):
    retry_message = "Please provide Y/N answer: "
    input_var = input(message).lower()
    while input_var not in ("y","n"):
        input_var = input(retry_message).lower()
    return input_var

# Helper function for validating absolute/relative input
def absolute_relative_input(message):
    retry_message = "Please provide Absolute/Relative answer: "
    input_var = input(message).lower()
    while input_var not in ("absolute", "relative"):
        input_var = input(retry_message).lower()
    return input_var

# Helper function for user input for structural cost
def structural_cost_input():
    print_line_break()
    print("STRUCTURAL COST")
    structural_type, is_retrofitted, limit_types, deductible_types = [None]*4
    
    # Check if structural cost exists
    if yes_no_input("Do you have structural cost? (Y/N): ") == "y":
        structural_type = cost_type_pick()
        is_retrofitted = yes_no_input("Is retrofitting? (Y/N): ")

         # Check if insurance limit exists
        if yes_no_input("Is limit? (Y/N): ") == "y":
            limit_types = absolute_relative_input("Insurance Limit Type (Absolute/Relative): ")
            
        # Check if deductible cost exists
        if yes_no_input("Is deductible? (Y/N): ") == "y":
            deductible_types = absolute_relative_input("Deductible Cost Type (Absolute/Relative): ")

    return structural_type, is_retrofitted, limit_types, deductible_types

# Helper function for user input for non_structural cost
def non_structural_cost_input():
    print_line_break()
    print("NONSTRUCTURAL COST")
    non_structural_type = None
    
    # Check if nonstructural cost exists
    if yes_no_input("Do you have nonstructural Cost (Y/N): ") == "y":
        non_structural_type = cost_type_pick()
    
    return non_structural_type

# Helper function for user input for business cost
def business_cost_input():
    print_line_break()
    print("BUSINESS COST")
    business_type = None
    
    # Check if business cost exists
    if yes_no_input("Do you have business Cost (Y/N): ") == "y":
        business_type = cost_type_pick()
    
    return business_type

# Helper function for user input for non_structural cost
def content_cost_input():
    print_line_break()
    print("CONTENTS COST")
    contents_type = None

    # Check if content cost exists
    if yes_no_input("Do you have contents Cost (Y/N): ") == "y":
        contents_type = cost_type_pick()

    return contents_type

# Main function for user input for exposure model
def exposure_model_user_input():
    """ 
    Returns all input variable that is needed to create exposure_model.xml
    
    """
    print("\n========================================================")
    print("Welcome to Exposure Model Generator!")
    print("========================================================")
    print("Please fill in all of these parameters.")
    
    # Default values
    unit_cost = "EUR"
    unit_area = "SQM"

    # User input
    exposure_id = text_input("Exposure Model ID: ", allow_spaces=False)
    exposure_description = text_input("Exposure Model Description: ", allow_spaces=True)

    # Get all input variable from output of helper function
    structural_type, is_retrofitted, limit_types, deductible_types = structural_cost_input()
    non_structural_type = non_structural_cost_input()
    business_type = business_cost_input()
    contents_type = content_cost_input() 

    print_line_break()

    # Check if any cost type requires area type
    if any(
        variable == "per_area" for variable in (
            structural_type, non_structural_type, contents_type, business_type)):
        print("AREA TYPE")
        area_type = area_type_pick()
    else:
        area_type = None

    # Get additional user inputs
    occupancy_periods = None
    if yes_no_input("Do you have occupancy data? (Y/N): ") == "y":
        occupancy_periods = text_input("Occupancy Periods: ", allow_spaces=True)
    tag_names = None
    if yes_no_input("Do you have tag names? (Y/N): ") == "y":
        tag_names = text_input("Tag Names: ", allow_spaces=True)
    
    print_line_break()

    # Get csv file name
    assets_name = csv_input("What is your name of csv file? Please include *.csv in your file name. ")

    return (
        unit_cost,
        unit_area,
        exposure_id,
        exposure_description,
        structural_type,
        is_retrofitted,
        limit_types,
        deductible_types,
        non_structural_type,
        business_type,
        contents_type,
        area_type,
        occupancy_periods,
        tag_names,
        assets_name
    )

# Main function for user input for fragility model
def fragility_model_input():
    """ 
    Returns all input variable that is needed to create fragility_model.xml
    
    """
    print("\n========================================================")
    print("Welcome to Fragility Model for Continuous Function Generator!")
    print("========================================================")
    print("Please fill in all of these parameters.")
    
    # User input
    frag_model_id = text_input("Fragility Model ID: ")
    loss_cat = loss_cat_pick()
    description = text_input("Description of your fragility model: ")
    num_of_frag_func = int(check_number("How many fragility function do you have? ", int_num=True, lower_lim=0))
    
    # Create None list
    frag_func_id = [None]*num_of_frag_func
    no_damage_lim = [None]*num_of_frag_func
    min_IML = [None]*num_of_frag_func
    max_IML = [None]*num_of_frag_func
    slight_mean = [None]*num_of_frag_func
    slight_stddev = [None]*num_of_frag_func
    moderate_mean = [None]*num_of_frag_func
    moderate_stddev = [None]*num_of_frag_func
    extensive_mean = [None]*num_of_frag_func
    extensive_stddev = [None]*num_of_frag_func
    complete_mean = [None]*num_of_frag_func
    complete_stddev = [None]*num_of_frag_func
    
    # Get value from user input for each list
    for i in range(num_of_frag_func):
        print("\nFragility Function No ", i+1)
        frag_func_id[i] = text_input("\nFragility Function ID: ")
        no_damage_lim[i] = check_number("Damage Limit: ", lower_lim=0)
        min_IML[i] = check_number("Minimum Intensity Measure Level: ", lower_lim=0)
        max_IML[i] = check_number("Maximum Intensity Measure Level: ", lower_lim=0)
        slight_mean[i] = check_number("Slight damage - Mean: ", lower_lim=0)
        slight_stddev[i] = check_number("Slight damage - Standard deviation: ", lower_lim=0)
        moderate_mean[i] = check_number("Moderate damage - Mean: ", lower_lim=0)
        moderate_stddev[i] = check_number("Moderate damage - Standard deviation: ", lower_lim=0)
        extensive_mean[i] = check_number("Extensive damage - Mean: ", lower_lim=0)
        extensive_stddev[i] = check_number("Extensive damage - Standard deviation: ", lower_lim=0)
        complete_mean[i] = check_number("Complete damage - Mean: ", lower_lim=0)
        complete_stddev[i] = check_number("Complete damage - Standard deviation: ", lower_lim=0)
    
    # Create table of fragility functions and save it to csv
    csv_path = os.path.join(os.getcwd(), output_folder, "fragility_model" + ".csv")
    frag_table = pd.DataFrame(data=[slight_mean, slight_stddev, moderate_mean, moderate_stddev,
                                    extensive_mean, extensive_stddev, complete_mean, complete_stddev]).transpose()
    frag_table.columns = ["slight_mean", "slight_stddev", "moderate_mean", "moderate_stddev",
                          "extensive_mean", "extensive_stddev", "complete_mean", "complete_stddev"]
    frag_table.insert(0,"frag_func_id",frag_func_id)
    frag_table.to_csv(csv_path)

    return frag_model_id, loss_cat, description, num_of_frag_func, frag_func_id, \
        no_damage_lim, min_IML, max_IML, slight_mean, slight_stddev, \
        moderate_mean, moderate_stddev, extensive_mean, extensive_stddev, \
        complete_mean, complete_stddev

# Main function for user input for rupture model
def rupture_model_input():
    """ 
    Returns all input variable that is needed to create rupture_model.xml

    """
    print("\n========================================================")
    print("Welcome to Simple Rupture Model Generator!")
    print("========================================================")
    print("Please fill in all of these parameters.")
    
    # User input
    eq_magnitude = check_number("Earthquake magnitude: ", lower_lim=0)
    eq_rake = check_number("Earthquake rake (-180 <= float <= 180): ", lower_lim=-180, upper_lim=180)
    hypo_lat = check_number("Hypocenter latitude (-90 <= float <= 90): ", lower_lim=-90, upper_lim=90)
    hypo_lon = check_number("Hypocenter longitude (-180 <= float <= 180): ", lower_lim=-180, upper_lim=180)
    hypo_depth = check_number("Hypocenter depth (km) (float >= 0): ", lower_lim=0)
    fault_dip = check_number("Fault dip (0 < float <= 90): ", lower_lim=0, upper_lim=90)
    fault_upper_depth = check_number("Fault upper depth (float >= 0): ", lower_lim=0)
    fault_lower_depth = check_number("Fault lower depth (float >= 0): ", lower_lim=0)
    
    print_line_break()
    
    print("Simple Fault Geometry")
    num_of_coord = int(check_number("How many coordinates of the faults do you have? ", int_num=True, lower_lim=0 ))
    lat = []
    lon = []
    for i in range(num_of_coord):
        print("\nCoordinate ", i+1)
        lat_i = check_number("latitude: ", lower_lim=-90, upper_lim=90)
        lon_i = check_number("longitude: ", lower_lim=-180, upper_lim=180)
        lat.append(lat_i)
        lon.append(lon_i)
    fault_coord = ""
    for n in range (len(lat)):
        fault_coord += lon[n] + " " + lat[n] + "\n"
        
    return eq_magnitude, eq_rake, hypo_lat, hypo_lon, hypo_depth, fault_dip, fault_upper_depth, fault_lower_depth, fault_coord

# Main function for user input for job.ini
def job_ini_input():
    """
    Returns all input variable that is needed to create job.ini
    
    """
    print("\n========================================================")
    print("Welcome to job.ini Generator!")
    print("========================================================")
    print("Please fill in all of these parameters.")
    
    # User input
    print_line_break()
    print("General")
    job_desc = text_input("Description of your calculation: ",True) 
    
    print_line_break()
    print("Rupture Information")
    rupture_mesh_spacing = check_number("Rupture mesh spacing: ", lower_lim=0)
    
    print_line_break()
    print("Site conditions")
    ref_vs30 = check_number("Reference vs30 value (m/s): ", lower_lim=0)
    depth_2pt5 = check_number("Minimum depth (km) at which vs30 ≥ 2.5 km/s (z2.5): ", lower_lim=0)
    depth_1pt0 = check_number("Minimum depth (m) at which vs30 ≥ 1.0 km/s (z1.0): ", lower_lim=0)
    
    print_line_break()
    print("Calculation Parameters")
    gmpe = text_input("Ground Motion Prediction Equation (GMPE): ")
    trunc_level = check_number("Level of trunction: ", lower_lim=0)
    max_distance = check_number("Maximum source-to-site distance (km): ", lower_lim=0)
    num_gmf = check_number("Number of ground motion fields: ", int_num=True, lower_lim=0)
    
    return job_desc, rupture_mesh_spacing, ref_vs30, depth_2pt5, depth_1pt0, gmpe, trunc_level, max_distance, num_gmf

 