import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Care Transition Dashboard", layout="wide")

st.title("Care Transition Efficiency & Placement Outcome Analytics")

# ----------------------------
# LOAD DATA SAFELY
# ----------------------------
DATA_FILE = "HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv"

file_path = os.path.join(os.path.dirname(__file__), DATA_FILE)

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

try:
    df = load_data(file_path)
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error("❌ Error loading dataset. Check file name or path.")
    st.stop()

# ----------------------------
# BASIC CLEANING
# ----------------------------
st.subheader("Dataset Overview")

st.write("Shape:", df.shape)
st.dataframe(df.head())

# Show missing values
st.subheader("Missing Values")
st.dataframe(df.isnull().sum())

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

columns = df.columns.tolist()
selected_column = st.sidebar.selectbox("Select column for analysis", columns)

# ----------------------------
# BASIC ANALYSIS
# ----------------------------
st.subheader(f"Analysis of: {selected_column}")

if df[selected_column].dtype == "object":
    st.write("Top categories:")

    value_counts = df[selected_column].value_counts().head(10)

    fig, ax = plt.subplots()
    value_counts.plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.write("Statistical Summary")
    st.write(df[selected_column].describe())

    fig, ax = plt.subplots()
    ax.hist(df[selected_column].dropna(), bins=20)
    st.pyplot(fig)

# ----------------------------
# FULL DATA DOWNLOAD
# ----------------------------
st.subheader("Download Cleaned Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "cleaned_data.csv",
    "text/csv"
)
