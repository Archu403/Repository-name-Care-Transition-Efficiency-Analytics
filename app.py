import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Care Transition Dashboard", layout="wide")

st.title("📊 Care Transition Efficiency Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.success("Data loaded successfully")

# ----------------------------
# KPI SECTION (POWER BI STYLE)
# ----------------------------
st.markdown("## 📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        st.metric("Numeric Fields", len(numeric_cols))
    else:
        st.metric("Numeric Fields", 0)

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.markdown("## 📄 Dataset Overview")
st.dataframe(df.head())

# ----------------------------
# FILTER (CATEGORICAL ONLY)
# ----------------------------
st.sidebar.header("🔍 Filters")

cat_cols = df.select_dtypes(include="object").columns

if len(cat_cols) > 0:
    filter_col = st.sidebar.selectbox("Select Category Column", cat_cols)
    selected_val = st.sidebar.selectbox("Select Value", df[filter_col].dropna().unique())

    filtered_df = df[df[filter_col] == selected_val]
else:
    filtered_df = df

# ----------------------------
# VISUALIZATION SECTION
# ----------------------------
st.markdown("## 📊 Insights Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

with col2:
    if len(numeric_cols) > 0:
        num_col = st.selectbox("Select Metric for Analysis", numeric_cols)

        fig = px.histogram(
            df,
            x=num_col,
            title=f"Distribution of {num_col}",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# TREND ANALYSIS (if date/year exists)
# ----------------------------
st.markdown("## 📈 Trend Analysis")

for col in df.columns:
    if "year" in col.lower() or "date" in col.lower():
        try:
            trend_df = df.groupby(col).size().reset_index(name="count")

            fig2 = px.line(
                trend_df,
                x=col,
                y="count",
                title="Trend Over Time",
                markers=True,
                template="plotly_white"
            )
            st.plotly_chart(fig2, use_container_width=True)
        except:
            pass

# ----------------------------
# DOWNLOAD REPORT (PRO FEATURE)
# ----------------------------
st.markdown("## 📥 Export Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Filtered Report (CSV)",
    data=csv,
    file_name="care_transition_report.csv",
    mime="text/csv"
)
