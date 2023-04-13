import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

path = "uber-raw-data-apr14.csv"
df = pd.read_csv(path, delimiter = ",")

def get_dom(dt):
    return dt.day 

df['dom'] = pd.to_datetime(df['Date/Time']).map(get_dom)

def get_hour(dt):
    return dt.hour

def count_rows(rows):
    return len(rows)

by_date = df.groupby('dom').apply(count_rows)

df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
df['dom'] = df['Date/Time'].dt.day

by_date = df.groupby('dom').size()

st.title('Uber Pickups Data Study')
st.write('This data is from Uber pickups in April 2014, we will be analysing the dataset and extracting relative information from it.')

st.write('Pickups per day of month')
chart_data = pd.DataFrame({'count': by_date})
chart_data.index.name = 'day'

st.line_chart(chart_data, use_container_width=True)

chart_data = pd.DataFrame({'count': by_date})
chart_data.index.name = 'day'

st.write('Plotting the same data in a bar chart')
st.bar_chart(chart_data)

def get_weekday(dt):
    return dt.weekday()

df['weekday'] = df['Date/Time'].map(get_weekday)

by_weekday = df.groupby('weekday').size()

chart_data = pd.DataFrame({'count': by_weekday})
chart_data.index.name = 'weekday'

weekdays = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon']

chart_data.index = weekdays

st.write('Frequency by Weekday - Uber - April 2014')
st.bar_chart(chart_data)

fig, ax = plt.subplots(figsize=(15, 15))
ax.hist(df.weekday, bins=7, rwidth=0.8, range=(-0.5, 6.5))
ax.set_xlabel("Days of the week")
ax.set_ylabel("Frequency")
ax.set_title("Frequency by Weekdays - Uber - April 2014")

st.pyplot(fig)


df["Date/Time"] = pd.to_datetime(df["Date/Time"])
df["hour"] = df["Date/Time"].dt.hour

by_hour = df.groupby('hour').size()

chart_data = pd.DataFrame({'count': by_hour})
chart_data.index.name = 'hour'

fig, ax = plt.subplots()
ax.hist(chart_data.index, bins=24, weights=chart_data["count"], range=(-0.5, 23.5))
ax.set_xlabel('Hour of the day')
ax.set_ylabel('Frequency')
ax.set_title('Frequency by Hour - Uber - April 2014')
st.pyplot(fig)

def count_rows(x):
    return len(x)

df2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()

st.write(df2)

df2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()

fig, ax = plt.subplots()
sns.heatmap(df2, linewidths=0.5, ax=ax)


st.pyplot(fig)

def plot_latitude_histogram():
    fig, ax = plt.subplots()
    ax.hist(df['Lat'], bins=100, range=(40.5, 41), color='r', alpha=0.5, label='Latitude')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Frequency')
    ax.set_title('Lattitude - Uber - April 2014')
    st.pyplot(fig)


st.title('Affichage du graphique de latitude')
plot_latitude_histogram()

def plot_longitude_histogram():
    fig, ax = plt.subplots()
    ax.hist(df['Lon'], bins=100, range=(-74.1, -73.9), color='g', alpha=0.5, label='Longitude')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Frequency')
    ax.set_title('Longitude - Uber - April 2014')
    st.pyplot(fig)

st.title('Affichage du graphique de longitude')
plot_longitude_histogram()

def plot_latitude_longitude_histogram():
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    ax.set_title('Longitude and Latitude distribution - Uber - April 2014', fontsize=15)
    ax.hist(df['Lon'], bins=100, range=(-74.1, -73.9), color='g', alpha=0.5, label='Longitude')
    ax.legend(loc='best')
    ax2 = ax.twiny()
    ax2.hist(df['Lat'], bins=100, range=(40.5, 41), color='r', alpha=0.5, label='Latitude')
    ax2.legend(loc='upper left')
    ax.set_xlabel('Longitude')
    ax2.set_xlabel('Latitude')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

st.title('Affichage du graphique de latitude et longitude')
plot_latitude_longitude_histogram()

def plot_scatter():
    fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
    ax.set_title('Scatter plot - Uber - April 2014')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.scatter(df['Lat'], df['Lon'], s=0.8, alpha=0.4)
    ax.set_ylim(-74.1, -73.8)
    ax.set_xlim(40.7, 40.9)
    st.pyplot(fig)

st.title('Affichage du graphique en nuage de points')
plot_scatter()

dico = {0:'yellow', 1:'yellow', 2:'blue', 3:'yellow', 4:'yellow', 5:'yellow', 6:'yellow'}

def plot_scatter_weekday():
    fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
    ax.set_title('Scatter Plot - Uber - April 2014')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.scatter(df['Lat'], df['Lon'], s=0.7, alpha=0.4, c=df['weekday'].map(dico))
    ax.set_ylim(-74.1, -73.8)
    ax.set_xlim(40.7, 40.9)
    st.pyplot(fig)

st.title('Affichage du graphique en nuage de points en fonction du jour de la semaine')
plot_scatter_weekday()

DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
LAND_COVER = [[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]

INITIAL_VIEW_STATE = pdk.ViewState(latitude=49.254, longitude=-123.13, zoom=11, max_zoom=16, pitch=45, bearing=0)

polygon = pdk.Layer(
    "PolygonLayer",
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="-",
    get_fill_color=[0, 0, 0, 20],
)

geojson = pdk.Layer(
    "GeoJsonLayer",
    DATA_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.valuePerSqm / 20",
    get_fill_color="[255, 255, properties.growth * 255]",
    get_line_color=[255, 255, 255],
)

st.pydeck_chart(pdk.Deck(layers=[polygon, geojson], initial_view_state=INITIAL_VIEW_STATE).to_html())

pipreqs --encoding=utf8