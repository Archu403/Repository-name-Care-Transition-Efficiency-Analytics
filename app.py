import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Care Transition Analytics", layout="wide")

st.title("📊 Care Transition Efficiency & Placement Outcome Analytics")

# ----------------------------
# LOAD DATA SAFELY
# ----------------------------
DATA_FILE = "HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv"
file_path = os.path.join(os.path.dirname(__file__), DATA_FILE)

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(file_path)
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error("Error loading dataset. Please check file name.")
    st.stop()

# ----------------------------
# BASIC CLEANING
# ----------------------------
df.columns = df.columns.str.strip()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

columns = df.columns.tolist()
selected_column = st.sidebar.selectbox("Choose Column", columns)

# ----------------------------
# KPI CARDS
# ----------------------------
st.subheader("📌 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head())

# ----------------------------
# MISSING VALUES
# ----------------------------
st.subheader("⚠ Missing Values Analysis")
missing_df = df.isnull().sum().reset_index()
missing_df.columns = ["Column", "Missing Values"]

fig1 = px.bar(missing_df, x="Column", y="Missing Values", title="Missing Data per Column")
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# COLUMN ANALYSIS
# ----------------------------
st.subheader(f"📊 Analysis: {selected_column}")

if df[selected_column].dtype == "object":
    
    top_data = df[selected_column].value_counts().head(10).reset_index()
    top_data.columns = [selected_column, "Count"]

    fig2 = px.bar(top_data, x=selected_column, y="Count",
                  title=f"Top Categories in {selected_column}")
    st.plotly_chart(fig2, use_container_width=True)

else:
    fig3 = px.histogram(df, x=selected_column, nbins=30,
                        title=f"Distribution of {selected_column}")
    st.plotly_chart(fig3, use_container_width=True)

    st.write("📌 Summary Statistics")
    st.dataframe(df[selected_column].describe())

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
st.subheader("⬇ Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Clean CSV",
    csv,
    "care_transition_cleaned.csv",
    "text/csv"
)
