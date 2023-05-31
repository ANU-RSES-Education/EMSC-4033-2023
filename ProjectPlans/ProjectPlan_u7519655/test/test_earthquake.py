#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pytest
import requests

__name__ = "test_earthquake"

# Test cases for obtain_earthquake_data function
def test_obtain_earthquake_data():
    # Test case: Valid parameters
    response = obtain_earthquake_data('2022-01-01', '2022-01-05', 4.5, 30, 40, -120, -110)
    assert response is not None
    print("Test case 1 passed.")
    # Add additional assertions to validate the structure and fields of the response data

    # Test case: Invalid parameters
    response = obtain_earthquake_data('2022-01-10', '2022-01-05', 4.5, 30, 40, -120, -110)
    assert response is None

def test_obtain_earthquake_data():
    # Test case: Valid parameters
    start_time = '2022-01-01'
    end_time = '2022-01-05'
    min_mag = 4.5
    data = obtain_earthquake_data(start_time, end_time, min_mag)
    assert data is not None
    print("Test case 2 passed.")
    # Add additional assertions to validate the structure and fields of the response data

    # Test case: Invalid parameters
    start_time = '2022-01-10'
    end_time = '2022-01-05'
    min_mag = 4.5
    data = obtain_earthquake_data(start_time, end_time, min_mag)
    assert data is None
    print("Test case 3 passed.")

    # Test cases for map_plotting function
def test_map_plotting():
    # Test case: Check if map is created successfully
    map = map_plotting()
    assert map is not None
    print("Test case 4 passed.")
    # Add additional assertions to validate the structure and format of the map

    # Test case: Check if earthquake data points are correctly plotted
    # Create test earthquake data and provide it to map_plotting function
    earthquake_data = [
        {'latitude': 30, 'longitude': -120, 'magnitude': 5.0},
        {'latitude': 35, 'longitude': -115, 'magnitude': 4.2},
        # Add more test earthquake data points
    ]
    map = map_plotting(earthquake_data)
    assert map is not None
    print("Test case 5 passed.")
    # Add additional assertions to validate the plotted earthquake data points on the map

    # Test case: Check if map is displayed or saved correctly
    # Use a test file name and check if the file is saved successfully
    file_name = 'test_map.png'
    result = map_plotting(earthquake_data, save_file=file_name)
    assert result is True
    # Add additional assertions to validate if the file is saved correctly

# Test cases for input validation functions
def test_validate_latitude():
    # Test case: Valid latitude
    result = validate_latitude(30)
    assert result == 30

    # Test case: Invalid latitude
    result = validate_latitude(500)
    assert result is None
    print("Test case 6 passed.")


def test_validate_longitude():
    # Test case: Valid longitude
    result = validate_longitude(-120)
    assert result == -120

    # Test case: Invalid longitude
    result = validate_longitude(200)
    assert result is None
    print("Test case 7 passed.")
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_earthquake.py'])


# In[ ]:




