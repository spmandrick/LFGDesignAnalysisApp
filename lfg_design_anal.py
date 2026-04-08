import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openpyxl
from datetime import date
from data_cleaner import load_data, clean_data

LFG = "data/LFG-Logo-Black.png"
#st.image([LFG], width=300)
st.title("LFG Design Analysis Dashboard")

df = load_data("data/LFG Project Tracker.xlsx", 'Project Tracker', 4)

st.write("**Choose a time interval to filter by:**")

start_date = st.date_input(
    "Time interval start date:",
    value=date(2025, 12, 1),  # Default date
    min_value=date(2024, 1, 1),  # Earliest selectable date
    max_value=date(2030, 12, 31),  # Latest selectable date
    format="MM/DD/YYYY"
)

end_date = st.date_input(
    "Time interval end date:",
    value=date.today(),  # Default date
    min_value=date(2024, 1, 1),  # Earliest selectable date
    max_value=date(2030, 12, 31),  # Latest selectable date
    format="MM/DD/YYYY"
)

df = df[df['Design Start Date'] >= pd.to_datetime(start_date)]
df = df[df['Design Start Date'] <= pd.to_datetime(end_date)]
df = clean_data(df)

st.multiselect("Filter by LFG Engineer:", options=df['LFG ENG'].unique(), default=df['LFG ENG'].unique(), key='lfg_eng_filter')
df = df[df['LFG ENG'].isin(st.session_state.lfg_eng_filter)]

ampacities = sorted([int(ampacity) for ampacity in df['Amps'].unique()])
st.multiselect("Filter by Ampacity:", options=ampacities, default=ampacities, key='amps_filter')
df = df[df['Amps'].isin(st.session_state.amps_filter)]

#st.write(df)

fig = px.timeline(
    df, 
    x_start='Design Start Date', 
    x_end='Design End Date', 
    y='Board', 
    color='Difficulty', 
    category_orders={'Difficulty': ['Easy', 'Med', 'Hard']}, 
    color_discrete_map={'Easy': 'green', 'Med': 'orange', 'Hard': 'red'}, 
    title='Project Timelines', 
    hover_data=['LFG ENG']
)

for d in fig.data:
    d.width = 0.9

fig.update_yaxes(showticklabels=False)
st.plotly_chart(fig)


fig = px.box(
    df, 
    x="Difficulty", 
    y="# Design Days", 
    color="Difficulty", 
    category_orders={'Difficulty': ['Easy', 'Med', 'Hard']}, 
    color_discrete_map={'Easy': 'green', 'Med': 'orange', 'Hard': 'red'}, 
    title='Design Days by Difficulty', 
    points = 'all', 
    hover_data=['Board', 'LFG ENG']
)

st.plotly_chart(fig)