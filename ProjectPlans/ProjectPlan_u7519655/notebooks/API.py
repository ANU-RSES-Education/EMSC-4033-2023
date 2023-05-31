#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Set the API endpoint and parameters
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {
    "format": "geojson",
    "starttime": start_time,
    "endtime": end_time,
    "minmagnitude": min_mag,
    "latitude": "-25.27",
    "longitude": "133.77",
    "maxradiuskm": "5000"
}
    
# Make a GET request to the API endpoint
response = requests.get(url, params=params)

# Check if the response was successful
if response.status_code == 200:
    # Parse the response as GeoJSON data
    geojson_data = response.json()
else:
    # Print an error message if the response was unsuccessful
    print("Error: Could not retrieve earthquake data.")
    

