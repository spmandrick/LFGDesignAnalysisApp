import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openpyxl
from datetime import date

LFG = "data/LFG-Logo-Black.png"
#st.image([LFG], width=300)
st.title("LFG Design Analysis Dashboard")

#df = load_data("data/LFG Project Tracker.xlsx", 'Project Tracker', 4)
df = pd.read_excel("data/output_4.28.26.xlsx")

#st.write(df)

df.rename(columns={'QTY': '# Sections'}, inplace=True)

st.header("Quarterly Analysis")

st.write("Last updated 4/28/26.")

quarterly_data = df.groupby(["Quarter", "Difficulty"]).agg({"# Design Days": "mean", "Board": "count"}).reset_index()
quarterly_data.rename(columns={"Board": "Board Count", "# Design Days": "Average Design Days"}, inplace=True)

quarters = sorted(quarterly_data['Quarter'].unique())

fig = px.bar(
    quarterly_data,
    x = "Quarter",
    y = "Board Count",
    color = "Difficulty",
    category_orders={'Difficulty': ['Easy', 'Med', 'Hard']},
    color_discrete_map={'Easy': 'green', 'Med': 'orange', 'Hard': 'red'},
    title = "Quarterly Board Counts"
)

for quarter in quarters:
    board_count = quarterly_data[quarterly_data['Quarter'] == quarter]['Board Count'].sum()
    ave_design_days = quarterly_data[quarterly_data['Quarter'] == quarter]['Average Design Days'].mean()

    quarterly_data.loc[len(quarterly_data)] = [quarter, 'All', ave_design_days, board_count]

fig.add_hline(
    y=80,
    line_dash="dot",       # dashed line
    line_color="black",       # line color
    annotation_text="Target = 80",  # label
    annotation_position="bottom right"
)

st.plotly_chart(fig)

fig = px.line(
    quarterly_data,
    x = "Quarter",
    y = "Average Design Days",
    color = "Difficulty",
    category_orders={'Difficulty': ['Easy', 'Med', 'Hard']},
    color_discrete_map={'Easy': 'green', 'Med': 'orange', 'Hard': 'red', 'All': 'blue'},
    title = "Quarterly Average Design Days"
)

st.plotly_chart(fig)

st.header("Further Design Analysis")

st.subheader("Filter by Time Interval and LFG Engineer")

st.write("These options filter the rest of the plots and charts on this page.")

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

st.multiselect("Filter by LFG Engineer:", options=df['LFG ENG'].unique(), default=df['LFG ENG'].unique(), key='lfg_eng_filter')
df = df[df['LFG ENG'].isin(st.session_state.lfg_eng_filter)]

#ampacities = sorted([int(ampacity) for ampacity in df['Amps'].unique()])
#st.multiselect("Filter by Ampacity:", options=ampacities, default=ampacities, key='amps_filter')
#df = df[df['Amps'].isin(st.session_state.amps_filter)]

st.subheader("Project Timelines and Design Days by Difficulty")

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

st.subheader("Design Days by Number of Sections")

st.write("There does appear to be a correlation between the number of sections and design days, with some outliers. The median design days for 5-section boards is higher than for 4-section boards, etc. The median for 1-section boards is much higher though.")

fig = px.box(
    df, 
    x="# Sections", 
    y="# Design Days", 
    color="# Sections", 
    category_orders={'# Sections': [1, 2, 3, 4, 5]}, 
    color_discrete_map={1: 'purple', 2: 'orange', 3: 'green', 4: 'pink', 5: 'blue'}, 
    title='Design Days by Number of Sections', 
    points = 'all', 
    hover_data=['Board', 'LFG ENG']
)

st.plotly_chart(fig)

st.subheader("Design Days by Ampacity and LFG Engineer")

engineers = df['LFG ENG'].unique()
ampacities = df['Amps'].unique()

for engineer in engineers:
    st.write(f"**Design Days by Ampacity for {engineer}**")
    
    subset = df[(df['LFG ENG'] == engineer)]
    total_boards = subset.shape[0]
    ave_TaT = subset['# Design Days'].mean()

    subset = subset[['Amps', 'Board', '# Design Days']].groupby('Amps').agg({'Board': 'count', '# Design Days': 'mean'}, ).reset_index()

    subset['Amps'] = subset['Amps'].astype(int).round(0)
    subset.loc[len(subset)] = ['All', total_boards, ave_TaT]
    subset['# Design Days'] = subset['# Design Days'].round(1)

    subset.rename(columns={'Board': 'Board Count', '# Design Days': 'Average Design Days'}, inplace=True)

    st.write(subset)