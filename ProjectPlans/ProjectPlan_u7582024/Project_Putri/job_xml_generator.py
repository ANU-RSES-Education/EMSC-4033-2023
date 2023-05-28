"""
The program job_xml_generator.py is a program designed to 
generate NRML data model (XML-based data) and configuration file.

Brief description of the main functions in this module are,
- xml_exposure_model()
    Call exposure_model_user_input() and define it as a variable user_input,
    return create_exposure_model_xml(*user_input)
- exposure_model_user_input(): 
    Returns all user inputs as parameters in generating exposure_model.xml
- create_exposure_model_xml(*user_inputs):
    Generate exposure_model.xml and save it to a folder.
- xml_fragility_model()
    Call fragility_model_input() and define it as a variable user_input,
    return create_fragility_model_xml(*user_input)
- fragility_model_input(): 
    Generate fragility_model.csv and save it to a folder and 
    returns all user inputs as parameters in generating fragility_model.xml
- create_fragility_model_xml(*user_inputs):
    Generate fragility_model.xml and save it to a folder.
- xml_rupture_model()
    Call rupture_model_input() and define it as a variable user_input,
    return create_rupture_model_xml(*user_input)
- rupture_model_input(): 
    Returns all user inputs as parameters in generating rupture_model.xml
- create_rupture_model_xml(*user_inputs):
    Generate rupture_model.xml and save it to a folder.
- job_ini()
    Call job_ini_input() and define it as a variable user_input,
    return create_job_ini(*user_input)
- job_ini_input(): 
    Returns all user inputs as parameters in generating job.ini
- create_job_ini(*user_inputs):
    Generate job.ini and save it to a folder.
"""

import os
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
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
def checkNumber(message, int_num=False, lower_lim=None, upper_lim=None):
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
    exposure_id = input("Exposure Model ID: ")
    exposure_description = input("Exposure Model Description: ")

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
    assets_name = input("What is your name of csv file? Please include *.csv in your file name. ")

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

# Create XML file for exposure model
def create_exposure_model_xml(
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
    assets_name):

    # Create the root element
    root_exposure_model = ET.Element("nrml")
    root_exposure_model.attrib = {}
    root_exposure_model.attrib["xmlns:gml"] = "http://www.opengis.net/gml"
    root_exposure_model.attrib["xmlns"] = "http://openquake.org/xmlns/nrml/0.4"
    
    # Create sub-elements and add to the root
    exp_model = ET.SubElement(root_exposure_model, "exposureModel")
    exp_model.attrib = {}
    exp_model.attrib["id"] = "ex1"
    exp_model.attrib["category"] = "buildings"
    exp_model.attrib["taxonomySource"] = "GEM taxonomy"

    exp_description = ET.SubElement(exp_model, "description")
    exp_description.text = exposure_description
    
    conversions = ET.SubElement(exp_model, "conversions")
    cost_types = ET.SubElement(conversions, "costTypes")
    
    # Structural cost type
    if structural_type is not None:
        structural_cost_types = ET.SubElement(cost_types, "costType")

        structural_cost_types.attrib = {}
        structural_cost_types.attrib["name"] = "structural"
        structural_cost_types.attrib["type"] = structural_type
        structural_cost_types.attrib["unit"] = unit_cost
        
        #if is_retrofitted is not None:
         #   structural_cost_types.attrib["retrofittedType"] = is_retrofitted
          #  structural_cost_types.attrib["retrofittedUnit"] = unit_cost
        
        types_to_boolean_map = {"absolute": "true", "relative": "false"}

        if limit_types is not None:
            limit = ET.SubElement(conversions, "insuranceLimit")
            limit.attrib = {}
            limit.attrib["isAbsolute"] = types_to_boolean_map[limit_types]
        if deductible_types is not None:
            limit = ET.SubElement(conversions, "deductible")
            limit.attrib = {}
            limit.attrib["isAbsolute"] = types_to_boolean_map[deductible_types]

    # Non-structural cost type
    if non_structural_type is not None:
        nonstructural_cost_types = ET.SubElement(cost_types, "costType")
        nonstructural_cost_types.attrib = {}
        nonstructural_cost_types.attrib["name"] = "non_structural"
        nonstructural_cost_types.attrib["type"] = non_structural_type
        nonstructural_cost_types.attrib["unit"] = unit_cost
        
    # Contents cost type
    if contents_type is not None:
        contents_cost_types = ET.SubElement(cost_types, "costType")
        contents_cost_types.attrib = {}
        contents_cost_types.attrib["name"] = "contents"
        contents_cost_types.attrib["type"] = contents_type
        contents_cost_types.attrib["unit"] = unit_cost

    # Business cost type
    if business_type is not None:
        business_cost_types = ET.SubElement(cost_types, "costType")
        business_cost_types.attrib = {}
        business_cost_types.attrib["name"] = "business"
        business_cost_types.attrib["type"] = business_type
        business_cost_types.attrib["unit"] = unit_cost

    # Area type
    if area_type is not None:
        area = ET.SubElement(conversions, "Area")
        area.attrib = {}
        area.attrib["type"] = area_type
        area.attrib["unit"] = unit_area

    # Occupancy periods
    occupancy_periods_se = ET.SubElement(exp_model, "occupancyPeriods")
    if occupancy_periods is not None:
        occupancy_periods_se.text = occupancy_periods
    
    # Tag names
    tag_names_se = ET.SubElement(exp_model, "tagNames")
    if tag_names is not None:
        tag_names_se.text = tag_names

    # Assets
    assets = ET.SubElement(exp_model, "assets")
    assets.text = assets_name
    
    print("\n========================================================")
    print("\nHere is your XML file!")
    
    # Convert the XML to a pretty-printed string
    exposure_model = ET.tostring(root_exposure_model, encoding="utf8", method="xml")
    print(BeautifulSoup(exposure_model, "xml").prettify())
    
    # Create the XML file
    tree_exposure_model = ET.ElementTree(root_exposure_model)
    file = os.path.join(data_folder, "exposure_model" + ".xml")
    tree_exposure_model.write(file)
     
    print("\n================= Process Completed ====================")
    print("Saved " + file)
    
    #return "exposure_model.xml"

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
    num_of_frag_func = int(checkNumber("How many fragility function do you have? ", int_num=True, lower_lim=0))
    
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
        no_damage_lim[i] = checkNumber("Damage Limit: ", lower_lim=0)
        min_IML[i] = checkNumber("Minimum Intensity Measure Level: ", lower_lim=0)
        max_IML[i] = checkNumber("Maximum Intensity Measure Level: ", lower_lim=0)
        slight_mean[i] = checkNumber("Slight damage - Mean: ", lower_lim=0)
        slight_stddev[i] = checkNumber("Slight damage - Standard deviation: ", lower_lim=0)
        moderate_mean[i] = checkNumber("Moderate damage - Mean: ", lower_lim=0)
        moderate_stddev[i] = checkNumber("Moderate damage - Standard deviation: ", lower_lim=0)
        extensive_mean[i] = checkNumber("Extensive damage - Mean: ", lower_lim=0)
        extensive_stddev[i] = checkNumber("Extensive damage - Standard deviation: ", lower_lim=0)
        complete_mean[i] = checkNumber("Complete damage - Mean: ", lower_lim=0)
        complete_stddev[i] = checkNumber("Complete damage - Standard deviation: ", lower_lim=0)
    
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

# Create XML file for fragility model
def create_fragility_model_xml(frag_model_id, loss_cat, description, num_of_frag_func, frag_func_id,
                               no_damage_lim, min_IML, max_IML, slight_mean, slight_stddev,
                               moderate_mean, moderate_stddev, extensive_mean, extensive_stddev,
                               complete_mean, complete_stddev):
    
    """ 
    Return XML file for building fragility model
    
    """
    
    # Create the root element
    root_frag_model = ET.Element('nrml')
    root_frag_model.attrib = {"xmlns":"http://openquake.org/xmlns/nrml/0.5"}

    # Create sub-elements and add to the root
    frag_model = ET.SubElement(root_frag_model, 'fragilityModel')
    frag_model.attrib = {}
    frag_model.attrib["id"] = frag_model_id
    frag_model.attrib["assetCategory"] = "buildings"
    frag_model.attrib["lossCategory"] = loss_cat
    
    desciption = ET.SubElement(frag_model, "description")
    desciption.text = description
    
    limit_states = ET.SubElement(frag_model, "limitStates")
    limit_states.text = "slight moderate extensive complete"
    
    for i in range(num_of_frag_func):
        frag_function = ET.SubElement(frag_model, "fragilityFunction")
        frag_function.attrib = {}
        frag_function.attrib["id"] = frag_func_id[i]
        frag_function.attrib["format"] = "continuous"
        frag_function.attrib["shape"] = "logncdf"

        imls = ET.SubElement(frag_function, "imls")
        imls.attrib = {}
        imls.attrib["imt"] = "PGA"
        imls.attrib["noDamageLimit"] = no_damage_lim[i]
        imls.attrib["minIML"] = min_IML[i]
        imls.attrib["maxIML"] = max_IML[i]

        slight = ET.SubElement(frag_function, "param")
        slight.attrib = {}
        slight.attrib["ls"] = "slight"
        slight.attrib["mean"] = slight_mean[i]
        slight.attrib["stddev"] = slight_stddev[i]

        moderate = ET.SubElement(frag_function, "param")
        moderate.attrib = {}
        moderate.attrib["ls"] = "moderate"
        moderate.attrib["mean"] = moderate_mean[i]
        moderate.attrib["stddev"] = moderate_stddev[i]

        extensive = ET.SubElement(frag_function, "param")
        extensive.attrib = {}
        extensive.attrib["ls"] = "extensive"
        extensive.attrib["mean"] = extensive_mean[i]
        extensive.attrib["stddev"] = extensive_stddev[i]
        
        complete = ET.SubElement(frag_function, "param")
        complete.attrib = {}
        complete.attrib["ls"] = "complete"
        complete.attrib["mean"] = complete_mean[i]
        complete.attrib["stddev"] = complete_stddev[i]
    
    print("\n========================================================")
    print("\nHere is your xml file for fragility model!\n")
    
    # Convert the XML to a pretty-printed string
    fragility_model = ET.tostring(root_frag_model, encoding='utf8', method='xml')
    print(BeautifulSoup(fragility_model, "xml").prettify())
    
    # Create the XML file
    tree_fragility_model = ET.ElementTree(root_frag_model)
    file = os.path.join(data_folder, "fragility_model" + ".xml")
    tree_fragility_model.write(file)
    
    print("\n================= Process Completed ====================")
    print("Saved " + file)

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
    eq_magnitude = checkNumber("Earthquake magnitude: ", lower_lim=0)
    eq_rake = checkNumber("Earthquake rake (-180 <= float <= 180): ", lower_lim=-180, upper_lim=180)
    hypo_lat = checkNumber("Hypocenter latitude (-90 <= float <= 90): ", lower_lim=-90, upper_lim=90)
    hypo_lon = checkNumber("Hypocenter longitude (-180 <= float <= 180): ", lower_lim=-180, upper_lim=180)
    hypo_depth = checkNumber("Hypocenter depth (km) (float >= 0): ", lower_lim=0)
    fault_dip = checkNumber("Fault dip (0 < float <= 90): ", lower_lim=0, upper_lim=90)
    fault_upper_depth = checkNumber("Fault upper depth (float >= 0): ", lower_lim=0)
    fault_lower_depth = checkNumber("Fault lower depth (float >= 0): ", lower_lim=0)
    
    print_line_break()
    
    print("Simple Fault Geometry")
    num_of_coord = int(checkNumber("How many coordinates of the faults do you have? ", int_num=True, lower_lim=0 ))
    lat = []
    lon = []
    for i in range(num_of_coord):
        print("\nCoordinate ", i+1)
        lat_i = checkNumber("latitude: ", lower_lim=-90, upper_lim=90)
        lon_i = checkNumber("longitude: ", lower_lim=-180, upper_lim=180)
        lat.append(lat_i)
        lon.append(lon_i)
    fault_coord = ""
    for n in range (len(lat)):
        fault_coord += lon[n] + " " + lat[n] + "\n"
        
    return eq_magnitude, eq_rake, hypo_lat, hypo_lon, hypo_depth, fault_dip, fault_upper_depth, fault_lower_depth, fault_coord

# Create XML file for fragility model
def create_rupture_model_xml(eq_magnitude, eq_rake, hypo_lat, hypo_lon, hypo_depth, fault_dip, fault_upper_depth, fault_lower_depth, fault_coord):
    """ 
    Return xml file for earthquake rupture model
    
    """
    # Create the root elemet
    root_rupture_model = ET.Element('nrml')
    root_rupture_model.attrib = {}
    root_rupture_model.attrib["xmlns:gml"] = "http://www.opengis.net/gml"
    root_rupture_model.attrib["xmlns"] = "http://openquake.org/xmlns/nrml/0.4"
    
    # Create sub-elements and add to the root
    simple_fault = ET.SubElement(root_rupture_model, 'simpleFaultRupture')
    
    magnitude = ET.SubElement(simple_fault, "magnitude")
    magnitude.text = eq_magnitude

    rake = ET.SubElement(simple_fault, "rake")
    rake.text = eq_rake

    hypocenter = ET.SubElement(simple_fault, "hypocenter")
    hypocenter.attrib = {}
    hypocenter.attrib["lat"] = hypo_lat
    hypocenter.attrib["lon"] = hypo_lon
    hypocenter.attrib["depth"] = hypo_depth
    
    simple_fault_geom = ET.SubElement(simple_fault, "simpleFaultGeometry")            
    gml_linestring = ET.SubElement(simple_fault_geom, "gml:LineString")
    gml_poslist = ET.SubElement(gml_linestring, "gml:posList")
    gml_poslist.text = fault_coord

    dip = ET.SubElement(simple_fault_geom, "dip")  
    dip.text =fault_dip

    upper_depth = ET.SubElement(simple_fault_geom, "upperSeismoDepth")  
    upper_depth.text =fault_upper_depth

    lower_depth = ET.SubElement(simple_fault_geom, "lowerSeismoDepth")  
    lower_depth.text =fault_lower_depth
    
    print("\n========================================================")
    print("\nHere is your xml file!\n")    

    # Convert the XML to a pretty-printed string   
    rupture_model = ET.tostring(root_rupture_model, encoding='utf8', method='xml')
    print(BeautifulSoup(rupture_model, "xml").prettify())
    
    # Create the XML file
    tree_rupture_model = ET.ElementTree(root_rupture_model)
    file = os.path.join(data_folder, "rupture_model" + ".xml")
    tree_rupture_model.write(file)
    
    print("\n================= Process Completed ====================")
    print("Saved " + file)

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
    rupture_mesh_spacing = checkNumber("Rupture mesh spacing: ", lower_lim=0)
    
    print_line_break()
    print("Site conditions")
    ref_vs30 = checkNumber("Reference vs30 value (m/s): ", lower_lim=0)
    depth_2pt5 = checkNumber("Minimum depth (km) at which vs30 ≥ 2.5 km/s (z2.5): ", lower_lim=0)
    depth_1pt0 = checkNumber("Minimum depth (m) at which vs30 ≥ 1.0 km/s (z1.0): ", lower_lim=0)
    
    print_line_break()
    print("Calculation Parameters")
    gmpe = text_input("Ground Motion Prediction Equation (GMPE): ")
    trunc_level = checkNumber("Level of trunction: ", lower_lim=0)
    max_distance = checkNumber("Maximum source-to-site distance (km): ", lower_lim=0)
    num_gmf = checkNumber("Number of ground motion fields: ", int_num=True, lower_lim=0)
    
    return job_desc, rupture_mesh_spacing, ref_vs30, depth_2pt5, depth_1pt0, gmpe, trunc_level, max_distance, num_gmf 

# Create job.ini file
def create_job_ini(job_desc, rupture_mesh_spacing, ref_vs30, depth_2pt5, depth_1pt0, gmpe, trunc_level, max_distance, num_gmf):
    """ 
    Return job.ini file for scenario damage calculation
    
    """
    file = os.path.join(data_folder, "job" + ".ini")
    output_path= os.path.join(os.getcwd(), output_folder)
    f = open(file,'w')
    f.write('[general]\n')
    f.write(f"description = {job_desc}\n")
    f.write('calculation_mode = scenario_damage\n')
    f.write('random_seed = 3\n')    
    
    f.write("\n[Rupture information]\n")
    f.write("rupture_model_file = rupture_model.xml\n")
    f.write(f"rupture_mesh_spacing = {rupture_mesh_spacing}\n")
    
    f.write("\n[Hazard sites]\n")
    
    f.write("\n[Exposure model]\n")
    f.write("exposure_file = exposure_model.xml\n")
    
    f.write("\n[Fragility model]\n")
    f.write("structural_fragility_file = fragility_model.xml\n")
    
    f.write('\n[Site conditions]\n')
    f.write('reference_vs30_type = measured\n')
    f.write(f'reference_vs30_value = {ref_vs30}\n')
    f.write(f'reference_depth_to_2pt5km_per_sec = {depth_2pt5}\n')
    f.write(f'reference_depth_to_1pt0km_per_sec = {depth_1pt0}\n')
    
    f.write('\n[Calculation parameters]\n')
    f.write(f'truncation_level = {trunc_level}\n')
    f.write(f'maximum_distance = {max_distance}\n')
    f.write(f'gsim = {gmpe}\n')
    f.write(f'number_of_ground_motion_fields = {num_gmf}\n')
    
    f.write('\n[output]\n')
    f.write(f'export_dir = {output_path}\n')
    f.close()
    print("\n========================================================")
    print("================= Process Completed ====================")
    print("Saved " + file)
    return

# Function to generate the XML file for the exposure model
def xml_exposure_model():
    user_inputs = exposure_model_user_input()

    return create_exposure_model_xml(*user_inputs)

# Function to generate the XML file for the fragility model
def xml_fragility_model():
    user_inputs = fragility_model_input()

    return create_fragility_model_xml(*user_inputs)

# Function to generate the XML file for the rupture model
def xml_rupture_model():
    user_inputs = rupture_model_input()

    return create_rupture_model_xml(*user_inputs)

# Function to generate the job.ini file
def job_ini():
    user_inputs = job_ini_input()

    return create_job_ini(*user_inputs)

# Function to clear the screen
def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

# Function to exit the program
def exit():
    return None

# Function to display the main menu and handle user selection
def main_menu():
    clear_screen()
    print("""Welcome to 'XML & job.ini File Generator'. Pick a file that you want to generate!
    0 - Main menu (this menu)
    1 - Exposure Model
    2 - Fragility Model
    3 - Earthquake Rupture Model
    4 - job.ini""")
    return program_pick()

# Function to handle user input and execute the selected program
def program_pick():
    file_map = {
        'c': exit,
        '0': main_menu,
        '1': xml_exposure_model,
        '2': xml_fragility_model,
        '3': xml_rupture_model,
        '4': job_ini
    }

    # Get user input for program selection
    user_pick = input("Pick 1 to 4 or 0 to go back to menu (or enter c to exit) : ")
    
    # Validate user input and execute the selected program
    while user_pick not in file_map:
        user_pick = input("Not a number from 0 to 4! (or enter c to exit) : ")
    return file_map[user_pick]()

# Entry point of the program, displays the main menu
if __name__ == '__main__':
    main_menu()