import streamlit as st
import pandas as pd
import numpy as np
import os
from geopy.geocoders import Nominatim

st.set_page_config(layout="wide")

# Somehow some coordinates are out of the New York City Area therefore this filter is inplace
min_lat, max_lat = 40.477399, 40.917577
min_lon, max_lon = -74.259090, -73.700272

@st.cache_data
def load_data():
    data = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv')
    data = data.drop_duplicates()
    copy = data.copy()
    copy = copy.dropna(subset=['LATITUDE', 'LONGITUDE'])
    copy.rename(columns={'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'}, inplace=True)
    copy['CRASH DATE'] = pd.to_datetime(copy['CRASH DATE'])
    nyc_data = copy[(copy['latitude'] >= min_lat) & (copy['latitude'] <= max_lat) & 
                    (copy['longitude'] >= min_lon) & (copy['longitude'] <= max_lon)]
    return nyc_data

nyc_data = load_data()
earliest_year, latest_year = nyc_data['CRASH DATE'].min().year, nyc_data['CRASH DATE'].max().year

with st.container(): 
    st.sidebar.title("Filter Options")
    accident_type = []
    if st.sidebar.checkbox('Pedestrians Involved'):
        accident_type.append('Pedestrians Involved')
    if st.sidebar.checkbox('Cyclists Involved'):
        accident_type.append('Cyclists Involved')
    if st.sidebar.checkbox('Motorists Involved'):
        accident_type.append('Motorists Involved')
    if st.sidebar.checkbox('Three vehicle collisions'):
        accident_type.append('Three vehicle collisions')
    if st.sidebar.checkbox('Four vehicle collisions'):
        accident_type.append('Four vehicle collisions')
    if st.sidebar.checkbox('Five vehicle collisions'):
        accident_type.append('Five vehicle collisions')

    year_range = st.slider('Select the range of years', earliest_year, latest_year, (latest_year - 1, latest_year))
    filtered_data = nyc_data[(nyc_data['CRASH DATE'].dt.year >= year_range[0]) & (nyc_data['CRASH DATE'].dt.year <= year_range[1])]

    if 'Pedestrians Involved' in accident_type:
        filtered_data = filtered_data[filtered_data['NUMBER OF PEDESTRIANS INJURED'] > 0]
    if 'Cyclists Involved' in accident_type:
        filtered_data = filtered_data[filtered_data['NUMBER OF CYCLIST INJURED'] > 0]
    if 'Motorists Involved' in accident_type:
        filtered_data = filtered_data[filtered_data['NUMBER OF MOTORIST INJURED'] > 0]
    if 'Three or more vehicle collisions' in accident_type: 
        filtered_data = filtered_data[
            filtered_data[['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']].notna().sum(axis=1) >= 3
        ]
    if 'Four vehicle collisions' in accident_type: 
        filtered_data = filtered_data[
            filtered_data[['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4']].notna().sum(axis=1) == 4
        ]
    if 'Five vehicle collisions' in accident_type: 
        filtered_data = filtered_data[
            filtered_data[['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']].notna().sum(axis=1) == 5
        ]
    
    # Sample the data to reduce the number of points plotted
    sample_size = min(1000, len(filtered_data))
    sampled_data = filtered_data.sample(n=sample_size)

    st.map(sampled_data, use_container_width=True, size=1)

    st.write("Filtered Data")
    st.dataframe(filtered_data)
