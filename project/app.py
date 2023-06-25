"""
Streamlit Web App
"""
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk


# load dataset
DATA_URL = (
"/Users/ryanharrington/streamlit/project/data/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlist dashboard that can be used to"
            " analyze motor vehicle collisions in NYC")

@st.cache(persist=True)
def load_data(nrows:int) ->pd.DataFrame:
    """
    Load Data
    """
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'},inplace=True)

    return data

# main
my_data = load_data(nrows=100000)

st.header("Where are the most people injured in NYC?")
injured_people = st.slider(label="Number of persons injured in motor vehicle collisions", min_value=0, max_value=19)
st.map(my_data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of day?")
hour = st.sidebar.slider('Hour to look at', min_value=0, max_value=23)
my_data = my_data[my_data['date/time'].dt.hour==hour]

st.markdown(f'Vehicle collisions between {hour} and {hour + 1}')
midpoint = (np.average(my_data['latitude']), np.average(my_data['longitude']))

st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50
    }
))


if st.checkbox('Show Raw Data', value=False):
    st.subheader('Raw Data')
    st.write(my_data)

# https://github.com/rya000667/streamlit.git