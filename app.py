import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Care Transition Analytics Dashboard", layout="wide")

st.title(" Care Transition Efficiency Dashboard")

# ----------------------------
# IMPACT MESSAGE (IMPORTANT)
# ----------------------------
st.success("Built to analyze care transition efficiency and identify system bottlenecks in child welfare flow.")

# ----------------------------


# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.success("Dataset loaded successfully")

# ----------------------------
# KPI SECTION
# ----------------------------
st.markdown("## Key Performance Indicators")

numeric_cols = df.select_dtypes(include="number").columns

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Numeric Fields", len(numeric_cols))

# ----------------------------
# SUMMARY BOX (INTERVIEW BOOST)
# ----------------------------
st.markdown("##  Summary")

st.write(f"""
- Total Records: {len(df)}
- Total Features: {df.shape[1]}
- Numeric Variables: {len(numeric_cols)}
""")

# ----------------------------
# DATA PREVIEW
# ----------------------------
st.markdown("## Dataset Overview")
st.dataframe(df.head())

# ----------------------------
# FILTER SYSTEM
# ----------------------------
st.sidebar.header(" Filters")

cat_cols = df.select_dtypes(include="object").columns

if len(cat_cols) > 0:
    filter_col = st.sidebar.selectbox("Choose Column", cat_cols)
    selected_val = st.sidebar.selectbox("Select Value", df[filter_col].dropna().unique())
    filtered_df = df[df[filter_col] == selected_val]
else:
    filtered_df = df

# ----------------------------
# INSIGHTS SECTION
# ----------------------------
st.markdown("## Key Insights")

st.info("""
This dashboard provides insights into:
- System efficiency in child transfer flow
- Data imbalance between categories
- Potential backlog indicators
- Outcome distribution patterns
""")

# ----------------------------
# VISUALIZATION
# ----------------------------
st.markdown(" Insights Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

with col2:
    if len(numeric_cols) > 0:
        num_col = st.selectbox("Select Numeric Column", numeric_cols)

        fig = px.histogram(
            df,
            x=num_col,
            title=f"Distribution of {num_col}",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# PIE CHART
# ----------------------------
st.markdown(" Outcome Distribution")

if len(cat_cols) > 0:
    pie_col = st.selectbox("Select Category Column", cat_cols)

    pie_df = df[pie_col].value_counts().reset_index()
    pie_df.columns = [pie_col, "count"]

    fig2 = px.pie(pie_df, names=pie_col, values="count", title="Distribution Analysis")
    st.plotly_chart(fig2)

# ----------------------------
# TREND ANALYSIS
# ----------------------------
st.markdown(" Trend Analysis")

for col in df.columns:
    if "year" in col.lower() or "date" in col.lower():
        try:
            trend = df.groupby(col).size().reset_index(name="count")

            fig3 = px.line(
                trend,
                x=col,
                y="count",
                markers=True,
                title="Trend Over Time",
                template="plotly_white"
            )
            st.plotly_chart(fig3)
        except:
            pass

# ----------------------------
# DOWNLOAD REPORT
# ----------------------------
st.markdown("##  Export Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Report (CSV)",
    data=csv,
    file_name="care_transition_report.csv",
    mime="text/csv"
)
