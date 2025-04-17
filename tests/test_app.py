"""
File: test_app.py
Author: Karina S
Date: 3/24/2025
Resources:
    - Patch
        - https://docs.python.org/3/library/unittest.mock.html
        - https://codilime.com/blog/testing-apis-with-pytest-mocks-in-python/#using-fixtures-for-reusable-mocks
    - Getting data from pd
        - https://www.w3schools.com/python/pandas/ref_df_iloc.asp
"""    

import pytest
from unittest.mock import Mock
import pandas as pd
import folium
from src.app import fetch_data, load_city_data, create_map

# Mock data for different cities, so that I don't use an API call every time
mock_city_data = {
    'New York': (40.7128, -74.0060, 8419600),
    'Los Angeles': (34.0522, -118.2437, 3980400),
}

def mock_get(*args, **kwargs) -> Mock:
    """ if the city (from api call) is part of the mock_city_data, returns a simulated response """
    # for my ref: args[0] is the url
    city_name = args[0].split('=')[-1]
        
    if city_name in mock_city_data:
        lat, lon, pop = mock_city_data[city_name]
        return Mock(status_code=200, json=lambda: [{"latitude": lat, "longitude": lon, "population": pop}])
    return Mock(status_code=500, json=lambda: [])

@pytest.mark.parametrize("city, expected_lat, expected_lon, expected_pop", [
    ("New York", 40.7128, -74.0060, 8419600),
    ("Los Angeles", 34.0522, -118.2437, 3980400),
    ("Albequerque", None, None, None)
])
def test_fetch_data(city:str, expected_lat:float, expected_lon:float, expected_pop:float, mocker) -> None:
    """ Test the fetch_data function with a mock API call """
    mocker.patch("requests.get", side_effect=mock_get)
    
    lat, lon, pop = fetch_data(city)
    assert lat == expected_lat
    assert lon == expected_lon
    assert pop == expected_pop

@pytest.mark.parametrize("city, expected_lat, expected_lon, expected_pop", [
    ("New York", 40.7128, -74.0060, 8419600),
    ("Los Angeles", 34.0522, -118.2437, 3980400),
    ("Albequerque", None, None, None)
])
def test_load_city_data(city:str, expected_lat:float, expected_lon:float, expected_pop:float, mocker) -> None:
    """ Test load_city_data function with multiple cities using return_value """

    mocker.patch("app.fetch_data", return_value=mock_city_data.get(city, (None, None, None)))
    city_data = load_city_data([city])
    city_row = city_data[city_data['city'] == city].iloc[0]
    
    assert city_row['latitude'] == expected_lat
    assert city_row['longitude'] == expected_lon
    assert city_row['population'] == expected_pop

def test_create_map() -> None:
    """ Test create_map function """
    
    data = {
        'city': ['New York', 'Los Angeles'],
        'latitude': [40.7128, 34.0522],
        'longitude': [-74.0060, -118.2437],
        'population': [8419600, 3980400]
    }
    city_data = pd.DataFrame(data)
    city_map = create_map(city_data)
    
    assert isinstance(city_map, folium.Map)
    assert len(city_map._children) > 0