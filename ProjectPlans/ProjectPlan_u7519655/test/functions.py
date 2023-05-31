#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def obtain_earthquake_data(start_time, end_time, min_mag):
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    params = {
        'format': 'geojson',
        'starttime': start_time,
        'endtime': end_time,
        'minmagnitude': min_mag
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def map_plotting():
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([110, 160, -45, -10], crs=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()
    plt.show()

def validate_latitude(latitude):
    if -90 <= latitude <= 90:
        return True
    else:
        return False

def validate_longitude(longitude):
    if -90 <= longitude <= 90:
        return True
    else:
        return False
    

