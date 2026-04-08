import pandas as pd
import openpyxl
import streamlit as st

PT = "data/LFG Project Tracker.xlsx"

def load_data(data_path, sht_name='Sheet 1', header=1):
    df = pd.read_excel(data_path, sheet_name=sht_name, header=header)
    return df

def clean_data(df):
    df = df[df['Type'] == 'Switchboards']
    df['Board'] = df['Equipment'].astype(str) + ' ' + df['Project Name'].astype(str)
    df = df[['Board', 'Project Name', 'Job #', 'Equipment', 'Description', 'QTY', 'Amps', 'LFG ENG', 'Design Start Date', 'Design End Date', '# Design Days', 'Difficulty']]
    df = df[df['Design End Date'].notna()]
    df = df.replace({'Difficulty': {'Hard ': 'Hard', 'Medium ': 'Med', 'Easy ': 'Easy'}})
    df['Design Start Date'] = pd.to_datetime(df['Design Start Date'], errors='coerce')
    df['Design End Date'] = pd.to_datetime(df['Design End Date'], errors='coerce')
    df.sort_values(by=['Design Start Date','Design End Date'], inplace=True)
    return df