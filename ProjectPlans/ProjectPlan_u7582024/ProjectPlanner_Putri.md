# Seismic Risk Index Map of Perth, Western Australia Based on Building Vulnerability

## Executive summary

Perth's seismic hazard was previously considered low, but the seismic threat and vulnerability of the Perth Metropolitan Area to earthquake damage have significantly increased due to population growth and increased seismic activity in the east of the city. To mitigate the risk of seismic hazards, it is crucial to understand the physical vulnerability of buildings and infrastructure to these hazards. To assess the level of risk posed by earthquakes in the region, I plan to create an interactive static dashboard that shows seismic risk index map for the Perth area based on the building vulnerability of each suburb. This dashboard includes the Perth seismic hazard map, fragility curve, and damage distribution map. Some of the data showed on the dashboard could be downloaded by user that would be public or academia.

## Goals

This project aims to simplify the process of generating a seismic risk index map by creating a single program that can perform the necessary calculations and visualizations. In order to achieve this main goal, the project can be broken down into the following smaller goals:
  - Create a function to create `xml` files as the input file for risk calculation using `openquake` library
  - Calculate seismic risk based on building vulnerability using `scenario damage assessment` mode from `openquake` library
  - Create a visual representation of the ground shaking intensity in different areas (PGA) of the Perth, Western Australia.
  - Create damage distribution map to identify and spatially represent areas that are particularly vulnerable to seismic hazards
  - Build a static dashboard that contains a report on seismic risk index map of Perth Area for each suburb. The dashboard will have several features that will help user to interact with the dashboard, including:
    1. `Zoom` : Users will be able to zoom in and out of the map to get a more detailed or broader view of the seismic risk index data
    2. `Pan` :  Users will be able to move the map view to different areas of the Perth Area to explore the seismic risk index data for different suburbs.
    3. `Filter` : Users will be able to apply filters to the seismic risk index data, such as by risk level or location, to focus on the areas of interest to them.
    4. `Download` : Users will be able to download the seismic risk index data for their selected suburbs in a variety of formats, such as CSV or JPG, for further analysis or sharing.

## Background and Innovation  

Perth, which hosts 75% of Western Australia's population, is the largest city in the state and the fourth most populous urban area in Australia. However, the city's rapid population growth in recent years has resulted in a corresponding increase in its vulnerability to natural disasters, including seismic hazards.

Seismic hazard in Perth is strongly influence by the south-west seismic zone (SWSZ), a region with high earthquake frequency. The SWSZ is one of the most seismically active areas in Australia, having experienced several earthquakes with local magnitude 5.9 or higher in the past 40 years. This hazard can cause significant damage to buildings and infrastructure, as well as loss of life. In order to mitigate the risk of seismic hazards, we need to understand the physical vulnerability of buildings and infrastructure to these hazards through seismic risk assessment.

Seismic risk assessment involves consodering exposure model, structural vulnerability, and seismic hazard analysis. Here, exposure model is created by identifying distribution of building in each suburb of Perth, including classifying them into residential building and non-residential building. The structural vulnerability to earthquake is defined by the fragility curve, which provides information on the likelihood of a building achieving specific levels of damage grades for each level of the seismic hazard parameter (PGA). Furthermore, seismic hazard analysis is represented by peak ground acceleration for Perth Area.

`OpenQuake Engine` is a software platform designed to help users conduct seismic hazard and risk assessments. It could be accessed through `OpenQuake WebUI`, a web-based user interface that allows users to access and interact with the `OpenQuake Engine`. It also has the `OpenQuake Input Parameter Toolkit` (IPTK) as a tool to help users create and manage input data for seismic hazard and risk assessments. This project will create a program that could create the `input` files and run `scenario damage assessment` calculation programmatically. The output of this program will be visualized into an interactive dashboard that will help users to analyze and interpret the results. In summary, this project will streamline the processes of generating a seismic risk index map into one program.

## Resources & Timeline

Data that will be used include:
  - Darling fault as the source fault
  - Ground Motion Prediction Equation from `Allen (2012)`
  - Fragility curve from HAZUS for wood and unreinforced masonry
  - Building distribution data in Perth from `Open Street Map` data
  - Perth and its suburb boundaries from Australian Bureau of Statistics
 
Main python library that will be used include:
  - `openquake` as a library to calculate seismic hazad and risk assessment
  - `GeoPandas` as a library for working and manipulating geospatial data 
  - `streamlit` as an open-source Python library to create and deploy interactive visualizations and dashboards


## Testing, validation, documentation

### Testing and Validation

Here are some tests to ensure that the dashboard can run smoothly:
  - Test the accessibility: Ensure that the dashboard is accessible to users who visit the website.
  - Test the functionality: Test that all the features and components of the dashboard are working correctly on the published version. Test that all the interactions, filtering, input fields, and download data features are working correctly
    1. Test `map` display: Check that the map is displayed correctly, with the correct boundaries and zoom level. Ensure that the map is centered on the correct location and that the markers or other data points are displayed accurately.
    2. Test `map` interactions: Test that users can interact with the map components, such as zooming in and out, panning, or clicking on markers to see more details. Ensure that the interactions are intuitive and easy to use.
    3. Test `input` and `filter` feature functionality: Ensure that the filtering and input fields are working as intended. For example, test that the filter options are displayed correctly and that users can select the appropriate filters. Test that the input fields accept valid latitude and longitude values and provide appropriate error messages for invalid inputs.
    4. Test `download` feature functionality: Ensure that the download data feature is working as intended. Test that the user can select the appropriate data set to download, and that the download process starts and completes successfully. Test that the downloaded file is in the expected format and contains the expected data.
  - Test the data integration: Ensure that the data integration is working correctly on the published version. Test that the data is being pulled correctly from external data sources and that the data is being displayed accurately on the dashboard.
  - Test the user experience: Test the user experience of the dashboard on the published version. Check that the dashboard is user-friendly and easy to use. Ensure that the feedback messages are clear and helpful and that the dashboard is visually appealing and easy to navigate.

### Documentation

Documentation of this project will consist of:
  - Introduction: Introduce the program, its purpose, and what it is designed to do.
  - Installation: Provide instructions for installing any required software, libraries, or dependencies.
  - Usage: Explain how to use the program and provide any necessary command line arguments, input formats, or other relevant information.
  - Dependencies: List any external libraries, tools, or software that are required to use the program, and provide information about how to install or access them.
  - Program Structure: Describe the overall structure of the program and how it is organized, including any important files, classes, or functions.
  - Program Flow: Outline the sequence of steps that the program follows when it is run, including any key functions or processes that take place.
  - Conclusion: Summarize the key features and benefits of the program, and offer any suggestions or recommendations for using it effectively.

