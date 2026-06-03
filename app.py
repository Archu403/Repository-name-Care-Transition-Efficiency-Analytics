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

st.title(" Care Transition Efficiency & Placement Outcome Analytics")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv"
    )

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(df["Date"])

    # Convert HHS Care column if stored as text
    df["Children in HHS Care"] = pd.to_numeric(
        df["Children in HHS Care"],
        errors="coerce"
    )

    return df

df = load_data()


# ----------------------------
# DATE FILTER
# ----------------------------
st.sidebar.header("Date Range")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date)
)

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date))
        &
        (df["Date"] <= pd.to_datetime(end_date))
    ]
else:
    filtered_df = df.copy()

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_cbp = filtered_df[
    "Children apprehended and placed in CBP custody*"
].sum()

total_custody = filtered_df[
    "Children in CBP custody"
].sum()

total_transfer = filtered_df[
    "Children transferred out of CBP custody"
].sum()

total_hhs = filtered_df[
    "Children in HHS Care"
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
# KPI CARDS
# ----------------------------
st.markdown("##  Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Children Apprehended", f"{total_cbp:,.0f}")

with col2:
    st.metric("Transferred to HHS", f"{total_transfer:,.0f}")

with col3:
    st.metric("Discharged", f"{total_discharge:,.0f}")

with col4:
    st.metric("Backlog", f"{backlog:,.0f}")

# ----------------------------
# RATIO TOGGLE
# ----------------------------
st.markdown("##  Efficiency Metrics")

metric_option = st.selectbox(
    "Select Metric",
    [
        "Transfer Efficiency",
        "Discharge Efficiency"
    ]
)

if metric_option == "Transfer Efficiency":
    st.metric(
        "Transfer Efficiency",
        f"{transfer_efficiency:.2f}%"
    )

if metric_option == "Discharge Efficiency":
    st.metric(
        "Discharge Efficiency",
        f"{discharge_efficiency:.2f}%"
    )

# ----------------------------
# ALERTS
# ----------------------------
st.markdown(" Threshold Alerts")

if transfer_efficiency < 80:
    st.error(
        f"Transfer Efficiency is low ({transfer_efficiency:.2f}%)"
    )
else:
    st.success(
        f"Transfer Efficiency is healthy ({transfer_efficiency:.2f}%)"
    )

if discharge_efficiency < 80:
    st.warning(
        f"Discharge Efficiency is low ({discharge_efficiency:.2f}%)"
    )
else:
    st.success(
        f"Discharge Efficiency is healthy ({discharge_efficiency:.2f}%)"
    )

# ----------------------------
# CARE PIPELINE FLOW
# ----------------------------
st.markdown(" Care Pipeline Flow Visualization")

flow_df = pd.DataFrame({
    "Stage": [
        "Apprehended",
        "Transferred",
        "Discharged"
    ],
    "Children": [
        total_cbp,
        total_transfer,
        total_discharge
    ]
})

fig_flow = px.bar(
    flow_df,
    x="Stage",
    y="Children",
    title="Care Pipeline Flow"
)

st.plotly_chart(fig_flow, use_container_width=True)

# ----------------------------
# BOTTLENECK DETECTION
# ----------------------------
st.markdown("##  Bottleneck Detection")

filtered_df = filtered_df.copy()

filtered_df["Backlog"] = (
    filtered_df["Children apprehended and placed in CBP custody*"]
    -
    filtered_df["Children transferred out of CBP custody"]
)

fig_backlog = px.line(
    filtered_df,
    x="Date",
    y="Backlog",
    markers=True,
    title="Backlog Trend Over Time"
)

st.plotly_chart(fig_backlog, use_container_width=True)

# ----------------------------
# OUTCOME TREND ANALYSIS
# ----------------------------
st.markdown("##  Outcome Trend Analysis")

trend_df = filtered_df.melt(
    id_vars="Date",
    value_vars=[
        "Children apprehended and placed in CBP custody*",
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ],
    var_name="Metric",
    value_name="Count"
)

fig_trend = px.line(
    trend_df,
    x="Date",
    y="Count",
    color="Metric",
    markers=True,
    title="Outcome Trends Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.markdown("##  Data Overview")

st.dataframe(filtered_df)

# Create report copy
report_df = filtered_df.copy()

# Format date
report_df["Date"] = pd.to_datetime(
    report_df["Date"]
).dt.strftime("%d-%m-%Y")

# Convert to CSV
csv = report_df.to_csv(index=False).encode("utf-8")

# Download button
st.download_button(
    label="⬇️ Download Filtered Report",
    data=csv,
    file_name="care_transition_report.csv",
    mime="text/csv"
)
