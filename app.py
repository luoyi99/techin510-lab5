import streamlit as st
import pandas.io.sql as sqlio
import numpy as np
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import datetime
import googlemaps
from db import conn_str, google_map_api_key

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=google_map_api_key)

# Load the data
df = sqlio.read_sql_query("SELECT * FROM events", conn_str)


st.title("Seattle Events")

# Display the first 6 upcoming events
st.subheader("Upcoming Events")

# Filter by category
category_list = np.insert(df['category'].unique(), 0, "All")
category = st.selectbox("Select a category", category_list)

# Advanced filtering
on = st.toggle('Advanced Filtering', False)

if on:
    # Filter by location
    location_list = df['location'].unique()
    location = st.selectbox("Filter by region", location_list)

    # Filter by date
    start_date, end_date = st.date_input(
        "Filter by date range", 
        (df['date'].min(), df['date'].max()),
        df['date'].min(),
        df['date'].max(),
        format="MM/DD/YYYY")
    df['date'] = df['date'].dt.date

# Filter the data
if category == "All":
    filtered_events = df[(df['location'] == location) & (df['date'] >= start_date) & (df['date'] <= end_date)] if on else df
else:
    filtered_events = df[(df['category'] == category) & (df['location'] == location)  & (df['date'] >= start_date) & (df['date'] <= end_date)] if on else df[df['category'] == category]

# Display the first 6 upcoming events after applying the filter
row1 = st.columns(3)
row2 = st.columns(3)
col = row1 + row2
for i in range(6):
    event = filtered_events.iloc[i]
    with col[i]:
        container = st.container(height=170)
        container.markdown(f":green[({event['category']})] **[{event['title']}](%s)**" % event['url'])
        container.markdown(f"*@ {event['venue']} | {event['location']}*")
        container.markdown(event["date"].strftime("%m/%d/%Y, %H:%M"))

# Display the locations of the above 6 upcoming events
st.markdown("**Event Locations**")
map = folium.Map(location=[47.6187576,-122.3], zoom_start=13)
for i in range(6):
    event = filtered_events.iloc[i]
    geocode_result = gmaps.geocode(event["venue"]+", Seattle, WA")
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    title = event['title']
    venue = event['venue']
    folium.Marker([lat, lng], popup=f"Event:{title}, Venue:{venue}").add_to(map)
st_folium(map, width=1200, height=600)


# Display general event stats
st.subheader("General Event Stats")

# Display the number of events by category
st.markdown("**Event Category Distribution**")
st.altair_chart(
    alt.Chart(df)
    .mark_arc()
    .encode(
        theta = "count()",
        color = "category"
    )
    .properties(
        width = 700,
        height = 400
        )
)

# Display the top 10 venues with the most events
st.markdown("**Top 10 Venues With The Most Events**")
venue_counts = df['venue'].value_counts().reset_index()
venue_counts.columns = ['Venue', 'Count'] # Aggregate data by venue and count the number of events for each venue
top_10_venues = venue_counts.head(10) # Select the top 10 venues
st.altair_chart(
    alt.Chart(top_10_venues)
    .mark_bar()
    .encode(
        x='Count',
        y=alt.Y('Venue', sort='-x')
    )
    .properties(
        width=700
    )
)