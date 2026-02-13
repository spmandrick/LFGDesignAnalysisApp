import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import openpyxl

#Function to load custom CSS
#def local_css(file_name):
#   with open(file_name) as f:
#       st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Load the CSS file
#local_css("assets/style.css")

LFG = "data/LFG-Logo.jpg"

st.image([LFG], width=250)

st.title("Design Analysis Dashboard")

df = pd.read_excel('data/BoardProdStatus.xlsx', sheet_name='Sheet1', header=3)

df = df[['In Current Production:', 'Ampacity', 'Sections', 'Engineer', 'DIFFICULTY ', 'DESIGN START', 'Design Completed', '# Design Days']]
df = df[df['Engineer'].notna() & df['# Design Days'].notna() & (df['# Design Days'] >= 0)]

# Need to clean up engineer names and difficulty columns!
df = df.replace({'Engineer': {'Niel': 'Neil'}})
df = df.replace({'DIFFICULTY ': {'EASY': 'Easy', 'MEDIUM': 'Medium', 'HARD': 'Hard'}})

st.write(df.groupby('DIFFICULTY ')['# Design Days'].mean().plot(kind='bar'))

st.write(df.groupby('DIFFICULTY ')['# Design Days'].mean().head())

easydf = df[df['DIFFICULTY '] == 'Easy']
mediumdf = df[df['DIFFICULTY '] == 'Medium']
harddf = df[df['DIFFICULTY '] == 'Hard']

st.plotly_chart(px.bar(df.groupby('DIFFICULTY ')['# Design Days'].mean(), y='# Design Days', title='Average Design Days by Difficulty'))
