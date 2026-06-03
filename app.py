import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG (MODERN UI)
# ----------------------------
st.set_page_config(
    page_title="Care Transition Intelligence Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("🧠 Care Transition Intelligence Dashboard")
st.caption("Analyzing efficiency, backlog formation, and placement outcomes in child care transition system")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ----------------------------
# SIDEBAR FILTERS (CREATIVE TOUCH)
# ----------------------------
st.sidebar.header("🎛️ Control Panel")

numeric_cols = df.select_dtypes(include="number").columns.tolist()

selected_metric = st.sidebar.selectbox(
    "Choose Primary Metric",
    numeric_cols
)

show_raw = st.sidebar.toggle("Show Raw Data")

# ----------------------------
# KPI ENGINE (SMART INSIGHTS)
# ----------------------------
st.markdown("## 📌 System Performance Snapshot")

total = df[selected_metric].sum()
avg = df[selected_metric].mean()
peak = df[selected_metric].max()

col1, col2, col3 = st.columns(3)

col1.metric("Total Volume", f"{total:,.0f}")
col2.metric("Average Flow", f"{avg:,.2f}")
col3.metric("Peak Pressure", f"{peak:,.0f}")

st.divider()

# ----------------------------
# FLOW INTELLIGENCE VIEW
# ----------------------------
st.subheader("🔄 Flow Intelligence (Inflow Pressure Over Time)")

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    flow = df.groupby("Date")[selected_metric].sum().reset_index()

    fig = px.area(
        flow,
        x="Date",
        y=selected_metric,
        title="System Load Over Time (Flow Pressure Curve)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# BACKLOG SIMULATION (CREATIVE KPI)
# ----------------------------
st.subheader("📦 Backlog Pressure Simulation")

df = df.sort_index()
df["cumulative_flow"] = df[selected_metric].cumsum()

fig2 = px.line(
    df,
    y="cumulative_flow",
    title="Accumulated System Load (Backlog Pressure Index)"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# SYSTEM BALANCE ANALYSIS
# ----------------------------
st.subheader("⚖️ System Balance Indicator")

if len(df) > 1:
    trend_change = df[selected_metric].diff().fillna(0)

    fig3 = px.bar(
        x=df.index,
        y=trend_change,
        title="Flow Volatility (Sudden Surges = Bottleneck Risk)"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# OUTCOME DISTRIBUTION (IF AVAILABLE)
# ----------------------------
st.subheader("🏠 Placement / Outcome Distribution")

outcome_cols = [c for c in df.columns if "placement" in c.lower() or "discharge" in c.lower()]

if outcome_cols:
    outcome = df[outcome_cols].sum().reset_index()
    outcome.columns = ["Outcome Type", "Count"]

    fig4 = px.pie(
        outcome,
        names="Outcome Type",
        values="Count",
        title="System Outcome Breakdown"
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No explicit outcome columns detected — using proxy metrics only.")

# ----------------------------
# INSIGHT PANEL (IMPORTANT FOR PROJECT)
# ----------------------------
st.markdown("## 🧠 Key Insights")

st.success("✔ System efficiency depends on flow balance between intake and discharge")
st.warning("⚠ Backlogs form when cumulative inflow exceeds system processing capacity")
st.info("📉 High volatility indicates bottleneck periods and operational stress")

# ----------------------------
# RAW DATA VIEW
# ----------------------------
if show_raw:
    st.subheader("📄 Raw Dataset")
    st.dataframe(df)
