import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Care Transition Dashboard", layout="wide")

st.title("📊 Care Transition Efficiency & Placement Outcome Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        return df
    return None

df = load_data()

if df is None:
    st.warning("Please upload your dataset to continue.")
    st.stop()

# ----------------------------
# CLEAN COLUMN NAMES
# ----------------------------
df.columns = df.columns.str.strip()

st.subheader("📌 Data Preview")
st.dataframe(df.head())

# ----------------------------
# YOUR EXACT COLUMNS
# ----------------------------
cbp_col = "Children apprehended and placed in CBP custody*"
transfer_col = "Children transferred out of CBP custody"
hhs_col = "Children discharged from HHS Care"

# ----------------------------
# CHECK COLUMNS EXIST
# ----------------------------
missing_cols = [col for col in [cbp_col, transfer_col, hhs_col] if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns in dataset: {missing_cols}")
    st.stop()

# ----------------------------
# KPIs
# ----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_cbp = df[cbp_col].sum()
total_transfer = df[transfer_col].sum()
total_hhs = df[hhs_col].sum()

backlog = total_transfer - total_hhs

col1.metric("CBP Apprehensions", f"{total_cbp:,.0f}")
col2.metric("Transferred Out of CBP", f"{total_transfer:,.0f}")
col3.metric("HHS Discharges", f"{total_hhs:,.0f}")
col4.metric("Estimated Backlog", f"{backlog:,.0f}")

# ----------------------------
# TRENDS OVER TIME (IF DATE EXISTS)
# ----------------------------
st.subheader("📈 Trend Analysis")

# Try to find date column
date_col = None
for c in df.columns:
    if "date" in c.lower() or "month" in c.lower() or "year" in c.lower():
        date_col = c
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    fig1 = px.line(df, x=date_col, y=cbp_col, title="CBP Apprehensions Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(df, x=date_col, y=transfer_col, title="Transfers Out of CBP Over Time")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(df, x=date_col, y=hhs_col, title="HHS Discharges Over Time")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("No date column found. Showing summary charts instead.")

    fig = px.bar(
        x=["CBP", "Transferred", "HHS Discharged"],
        y=[total_cbp, total_transfer, total_hhs],
        title="Overall System Summary"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# SYSTEM FLOW VISUAL
# ----------------------------
st.subheader("🔄 System Flow Insight")

flow_df = pd.DataFrame({
    "Stage": ["CBP Custody", "Transferred", "HHS Care"],
    "Count": [total_cbp, total_transfer, total_hhs]
})

fig_flow = px.funnel(flow_df, x="Count", y="Stage", title="Care Transition Flow")
st.plotly_chart(fig_flow, use_container_width=True)

# ----------------------------
# RAW DATA
# ----------------------------
st.subheader("📄 Raw Data")
st.dataframe(df)
