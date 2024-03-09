import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import warnings
warnings.filterwarnings('ignore')
plt.style.use('ggplot')


daily_df = pd.read_csv("FP\day_df.csv")
hourly_df = pd.read_csv("FP\hour_df.csv")

def create_byhour(df):
    byhour_df = df.groupby(by="hour").agg({
        'registered' : 'sum',
        'casual' : 'sum'
    })

    return byhour_df

def create_weather_season_df(df):
    ws_df = df.groupby(by=['season', 'weather']).agg({
    'registered': 'sum',
    'casual': 'sum'
    })
    
    return ws_df

daily_df['date'] = pd.to_datetime(daily_df['date'])
hourly_df['date'] = pd.to_datetime(hourly_df['date'])

min_date = daily_df["date"].min()
max_date = daily_df["date"].max()

with st.sidebar:
    st.image("https://i.pinimg.com/474x/5d/b1/37/5db137e0973b20a77384eff400c7e113.jpg")

    start_date, end_date = st.date_input(
        label='Date Range', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

filtered_daily = daily_df[(daily_df['date'] >= str(start_date)) & (daily_df['date'] <= str(end_date))]
filtered_hourly = hourly_df[(hourly_df['date'] >= str(start_date)) & (hourly_df['date'] <= str(end_date))]

by_hour_df = create_byhour(filtered_hourly)
weather_season_df = create_weather_season_df(filtered_daily)

# ---------------------

st.header('Bike Sharing Dashboard 🚴‍♂️')


st.subheader('Weather and Season Effect')

total_usage = weather_season_df['registered'].sum() + weather_season_df['casual'].sum()

st.metric("Total Rides", value=total_usage)

weather_season_df.plot(kind='bar', title='Weather & Season Effect').figure


st.subheader('Hourly Details')

col1, col2 = st.columns(2)

with col1:
    total_registered = by_hour_df['registered'].sum()
    st.metric("Total Registered Bikers", total_registered)

with col2:
    total_casual = by_hour_df['casual'].sum()
    st.metric("Total Casual Bikers", total_casual)

fig = plt.figure(figsize=(10, 5))
plt.plot(by_hour_df)
plt.xticks(range(24))
plt.legend(['Registered', 'Casual'])

st.pyplot(fig)
