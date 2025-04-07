"""
File: app.py
Author: Karina S
Date: 3/24/2025
Resources:
    - Wolf Paulus: Python Syntax
    - Pandas: data frame
        - https://www.w3schools.com/python/pandas/pandas_dataframes.asp
    - Folium: to display the map
        - https://python-visualization.github.io/folium/latest/
    - Streamlit: to make the webpage
        - https://streamlit.io/
    - dotenv: loading and storing api key
        - https://pypi.org/project/python-dotenv/
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from typing import Tuple

load_dotenv()
API_KEY = os.getenv("API_KEY")

cities = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'
]

def fetch_data(city:str) -> Tuple[float, float, float]:
    """ Gets data population and coordinate info from a city name """
    api_url = f'https://api.api-ninjas.com/v1/city?name={city}'
    headers = {'X-Api-Key': API_KEY}
    
    lat = None
    lon = None 
    pop = None

    try:
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data: 
                lat = data[0].get("latitude")
                lon = data[0].get("longitude") 
                pop = data[0].get("population")
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
    
    return lat, lon, pop

def load_city_data(selected_cities:str) -> pd.DataFrame:
    """ returns a pd DataFrame from the loaded data """
    latitude = []
    longitude = []
    population = []
    
    for city in selected_cities:
        lat, lon, pop = fetch_data(city)
        if lat is not None and lon is not None and pop is not None:
            latitude.append(lat)
            longitude.append(lon)
            population.append(pop)
        else:
            latitude.append(None)
            longitude.append(None)
            population.append(None)
    
    data = {
        'city': selected_cities,
        'latitude': latitude,
        'longitude': longitude,
        'population': population
    }
    
    return pd.DataFrame(data)

def create_map(city_data:pd.DataFrame) -> folium.Map:
    """ uses folium to put markers on a map that display the population """
    city_map = folium.Map(zoom_start=5)
    marker_cluster = MarkerCluster().add_to(city_map)

    for idx, row in city_data.iterrows():
        if row['latitude'] and row['longitude']:
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=row['population'] / 100000,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
                popup=f"{row['city']}: {row['population']} people"
            ).add_to(marker_cluster)
    return city_map

def main() -> None:
    """ main function and actual streamlit organization """
    st.title("US City Population")
    selected_cities = st.multiselect("Select cities to display on the map", cities, default=cities)
    city_data = load_city_data(selected_cities)
    city_map = create_map(city_data)
    st.components.v1.html(city_map._repr_html_(), height=600)

if __name__ == "__main__":
    main()