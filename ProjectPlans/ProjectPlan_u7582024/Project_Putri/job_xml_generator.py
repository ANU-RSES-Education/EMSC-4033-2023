"""
The program job_xml_generator.py is a program designed to 
generate NRML data model (XML-based data) and configuration file.

Brief description of the main functions in this module are,
- xml_exposure_model()
    Call exposure_model_user_input() and define it as a variable user_input,
    return create_exposure_model_xml(*user_input)
- create_exposure_model_xml(*user_inputs):
    Generate exposure_model.xml and save it to a folder.
- xml_fragility_model()
    Call fragility_model_input() and define it as a variable user_input,
    return create_fragility_model_xml(*user_input)
- create_fragility_model_xml(*user_inputs):
    Generate fragility_model.xml and save it to a folder.
- xml_rupture_model()
    Call rupture_model_input() and define it as a variable user_input,
    return create_rupture_model_xml(*user_input)
- create_rupture_model_xml(*user_inputs):
    Generate rupture_model.xml and save it to a folder.
- job_ini()
    Call job_ini_input() and define it as a variable user_input,
    return create_job_ini(*user_input)
- create_job_ini(*user_inputs):
    Generate job.ini and save it to a folder.
"""

import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import user_input as ipt

# Declare directory for all generated file
data_folder = "data"
output_folder = "output"

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
    exp_model.attrib["id"] = exposure_id
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
    
    return end_of_process()

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

    return end_of_process()

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

    return end_of_process()

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
    
    return end_of_process()

# Function to generate the XML file for the exposure model
def xml_exposure_model():
    user_inputs = ipt.exposure_model_user_input()

    return create_exposure_model_xml(*user_inputs)

# Function to generate the XML file for the fragility model
def xml_fragility_model():
    user_inputs = ipt.fragility_model_input()

    return create_fragility_model_xml(*user_inputs)

# Function to generate the XML file for the rupture model
def xml_rupture_model():
    user_inputs = ipt.rupture_model_input()

    return create_rupture_model_xml(*user_inputs)

# Function to generate the job.ini file
def job_ini():
    user_inputs = ipt.job_ini_input()

    return create_job_ini(*user_inputs)

# Function to clear the screen
def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")

# Function to exit the program
def exit_program():
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
        'c': exit_program,
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

def end_of_process():
    ipt.print_line_break()
    if ipt.yes_no_input("Do you want to generate other file? (Y/N) ") == "y":
        return main_menu()
    else:
        return exit_program()

# Entry point of the program, displays the main menu
if __name__ == '__main__':
    main_menu()