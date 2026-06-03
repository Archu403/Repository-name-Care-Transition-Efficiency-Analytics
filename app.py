import streamlit as st
import pandas as pd

st.set_page_config(page_title="Care Transition Dashboard", layout="wide")

st.title("📊 Care Transition Analytics Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program .csv")

    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.success("Dataset loaded successfully!")
st.write("Preview of data:")
st.dataframe(df.head())
st.sidebar.header(" Filters")

column = st.sidebar.selectbox("Choose column to explore", df.columns)

unique_values = df[column].dropna().unique()
selected_value = st.sidebar.selectbox("Select value", unique_values)

filtered_df = df[df[column] == selected_value]

st.write("### Filtered Data")
st.dataframe(filtered_df)
import plotly.express as px

st.write("### 📊 Basic Visualization")

numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 0:
    col = st.selectbox("Choose numeric column for chart", numeric_cols)

    fig = px.histogram(df, x=col, title=f"Distribution of {col}")
    st.plotly_chart(fig)
else:
    st.warning("No numeric columns found for visualization")
import os

@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "HHS_Unaccompanied_Alien_Children_Program.csv")
    return pd.read_csv(file_path)
