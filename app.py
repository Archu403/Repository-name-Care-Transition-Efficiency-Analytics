import streamlit as st
import pandas as pd
import os

st.title("Care Transition Efficiency & Placement Outcome Analytics")

# DEBUG
st.write("Files available:")
st.write(os.listdir("."))

# Load CSV
df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program(1).csv")













import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Care Transition Analytics",
    layout="wide"
)

st.title("Care Transition Efficiency & Placement Outcome Analytics")

# Load Dataset
df = pd.read_csv(
    "HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program (1).csv"
)

# Remove commas and convert to numeric
cols = [
    'Children apprehended and placed in CBP custody*',
    'Children in CBP custody',
    'Children transferred out of CBP custody',
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in cols:
    df[col] = df[col].astype(str).str.replace(',', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# KPIs
df['Transfer_Efficiency'] = (
    df['Children transferred out of CBP custody']
    /
    df['Children in CBP custody']
)

df['Discharge_Effectiveness'] = (
    df['Children discharged from HHS Care']
    /
    df['Children in HHS Care']
)

df['Backlog'] = (
    df['Children apprehended and placed in CBP custody*']
    -
    df['Children discharged from HHS Care']
)

# Sidebar
st.sidebar.header("Filters")

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# KPI Cards
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Avg Transfer Efficiency",
        round(df['Transfer_Efficiency'].mean(), 2)
    )

with col2:
    st.metric(
        "Avg Discharge Effectiveness",
        round(df['Discharge_Effectiveness'].mean(), 2)
    )

with col3:
    st.metric(
        "Maximum Backlog",
        int(df['Backlog'].max())
    )

# Transfer Trend
st.subheader("Transfer Trend")

st.line_chart(
    df['Children transferred out of CBP custody']
)

# Discharge Trend
st.subheader("Discharge Trend")

st.line_chart(
    df['Children discharged from HHS Care']
)

# Backlog Trend
st.subheader("Backlog Accumulation Trend")

st.line_chart(
    df['Backlog']
)

# CBP vs HHS Care
st.subheader("CBP Custody vs HHS Care")

comparison = df[
    [
        'Children in CBP custody',
        'Children in HHS Care'
    ]
]

st.line_chart(comparison)

# Insights
st.subheader("Key Insights")

st.success(
    """
    • Transfer efficiency indicates how quickly children move from CBP to HHS.

    • Discharge effectiveness measures successful reunification outcomes.

    • Backlog highlights periods where inflow exceeds outflow.

    • Monitoring these KPIs helps identify operational bottlenecks.
    """
)

st.write("Dashboard Completed Sucessfully")
