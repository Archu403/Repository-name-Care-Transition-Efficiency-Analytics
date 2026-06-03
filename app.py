import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Care Transition Analytics Dashboard",
    layout="wide"
)

st.title("📊 Care Transition Efficiency & Placement Outcome Analytics")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv"
    )
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ----------------------------
# PROBLEM STATEMENT
# ----------------------------
st.markdown("## 📌 Problem Statement")

st.info("""
This dashboard evaluates care transition efficiency by tracking:
• Children entering CBP custody
• Transfers from CBP to HHS
• Discharges from HHS care

The goal is to identify bottlenecks, monitor transfer efficiency,
track discharge performance, and analyze outcome trends over time.
""")

# ----------------------------
# DATE / YEAR FILTER
# ----------------------------
st.sidebar.header("📅 Year Filter")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (
        int(df["Year"].min()),
        int(df["Year"].max())
    )
)

filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_cbp = filtered_df[
    "Children apprehended and placed in CBP custody*"
].sum()

total_transfer = filtered_df[
    "Children transferred out of CBP custody"
].sum()

total_discharge = filtered_df[
    "Children discharged from HHS Care"
].sum()

transfer_efficiency = (
    total_transfer / total_cbp * 100
    if total_cbp > 0 else 0
)

discharge_efficiency = (
    total_discharge / total_transfer * 100
    if total_transfer > 0 else 0
)

backlog = total_cbp - total_transfer

# ----------------------------
# KPI SECTION
# ----------------------------
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Children in CBP", f"{total_cbp:,.0f}")

with col2:
    st.metric("Transferred to HHS", f"{total_transfer:,.0f}")

with col3:
    st.metric("Discharged", f"{total_discharge:,.0f}")

with col4:
    st.metric("Backlog", f"{backlog:,.0f}")

# ----------------------------
# EFFICIENCY PANEL
# ----------------------------
st.markdown("## ⚡ Transfer & Discharge Efficiency")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Transfer Efficiency",
        f"{transfer_efficiency:.2f}%"
    )

with c2:
    st.metric(
        "Discharge Efficiency",
        f"{discharge_efficiency:.2f}%"
    )

# ----------------------------
# THRESHOLD ALERTS
# ----------------------------
st.markdown("## 🚨 Alerts")

if transfer_efficiency < 80:
    st.error("⚠️ Transfer Efficiency below 80%")
else:
    st.success("✅ Transfer Efficiency healthy")

if discharge_efficiency < 80:
    st.warning("⚠️ Discharge Efficiency below 80%")
else:
    st.success("✅ Discharge Efficiency healthy")

# ----------------------------
# CARE PIPELINE FLOW
# ----------------------------
st.markdown("## 🔄 Care Pipeline Flow Visualization")

flow_df = pd.DataFrame({
    "Stage": [
        "CBP Custody",
        "Transferred",
        "Discharged"
    ],
    "Children": [
        total_cbp,
        total_transfer,
        total_discharge
    ]
})

fig1 = px.bar(
    flow_df,
    x="Stage",
    y="Children",
    title="Care Pipeline Flow"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# BOTTLENECK DETECTION
# ----------------------------
st.markdown("## 🚧 Bottleneck Detection")

filtered_df["Backlog"] = (
    filtered_df["Children apprehended and placed in CBP custody*"]
    -
    filtered_df["Children transferred out of CBP custody"]
)

fig2 = px.bar(
    filtered_df,
    x="Year",
    y="Backlog",
    title="Backlog by Year"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# OUTCOME TREND ANALYSIS
# ----------------------------
st.markdown("## 📈 Outcome Trend Analysis")

trend_df = filtered_df.melt(
    id_vars="Year",
    value_vars=[
        "Children apprehended and placed in CBP custody*",
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ],
    var_name="Metric",
    value_name="Count"
)

fig3 = px.line(
    trend_df,
    x="Year",
    y="Count",
    color="Metric",
    markers=True,
    title="Care Outcome Trends Over Time"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.markdown("## 📄 Data Overview")

st.dataframe(filtered_df)

# ----------------------------
# DOWNLOAD REPORT
# ----------------------------
st.markdown("## 📥 Download Report")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download CSV Report",
    csv,
    "care_transition_report.csv",
    "text/csv"
)
