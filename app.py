

Care_Transition_Project.ipynb
Care_Transition_Project.ipynb_


from google.colab import files
uploaded = files.upload()


import pandas as pd

df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program (1).csv")

df.head()
df.info()
df.describe()


df.isnull().sum()



# Remove commas from all numeric columns

cols = [
    'Children apprehended and placed in CBP custody*',
    'Children in CBP custody',
    'Children transferred out of CBP custody',
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in cols:
    df[col] = df[col].astype(str).str.replace(',', '')
    df[col] = pd.to_numeric(df[col])


import pandas as pd

# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Check column names
print(df.columns)

# Check for missing values
print(df.isnull().sum())

# Remove duplicate rows (if any)
df = df.drop_duplicates()

# Display basic information
df.info()
Index(['Date', 'Children apprehended and placed in CBP custody*',
       'Children in CBP custody', 'Children transferred out of CBP custody',
       'Children in HHS Care', 'Children discharged from HHS Care'],
                 


['Date', 'Children apprehended and placed in CBP custody*', 'Children in CBP custody', 'Children transferred out of CBP custody', 'Children in HHS Care', 'Children discharged from HHS Care']


plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Children in CBP custody'])
plt.title('CBP Custody Trend')
plt.xlabel('Date')
plt.ylabel('Children')
plt.show()



plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Children transferred out of CBP custody'])
plt.title('Transferred to HHS Trend')
plt.xlabel('Date')
plt.ylabel('Children')
plt.show()



plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Children in HHS Care'])
plt.title('HHS Care Trend')
plt.xlabel('Date')
plt.ylabel('Children')
plt.show()




plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Children discharged from HHS Care'])
plt.title('Discharge Trend')
plt.xlabel('Date')
plt.ylabel('Children')
plt.show()



plt.figure(figsize=(12,5))

plt.plot(df['Date'], df['Children apprehended and placed in CBP custody*'],
         label='Apprehended')

plt.plot(df['Date'], df['Children discharged from HHS Care'],
         label='Discharged')

plt.legend()
plt.title('Inflow vs Outflow')
plt.show()



import seaborn as sns

plt.figure(figsize=(8,6))

sns.heatmap(
    df[['Children apprehended and placed in CBP custody*',
        'Children in CBP custody',
        'Children transferred out of CBP custody',
        'Children in HHS Care',
        'Children discharged from HHS Care']].corr(),
    annot=True,
    cmap='coolwarm'
)

plt.title("Correlation Matrix")
plt.show()



plt.figure(figsize=(8,5))

plt.hist(df['Children apprehended and placed in CBP custody*'],
         bins=20)

plt.title('Distribution of Apprehended Children')
plt.show()



plt.figure(figsize=(8,5))

plt.hist(df['Children discharged from HHS Care'],
         bins=20)

plt.title('Distribution of Discharges')
plt.show()



df['Month'] = df['Date'].dt.month_name()

monthly = df.groupby('Month')[[
    'Children apprehended and placed in CBP custody*',
    'Children transferred out of CBP custody',
    'Children discharged from HHS Care'
]].mean()

monthly

Next steps:


monthly.plot(kind='bar',
             figsize=(12,5))

plt.title("Monthly Average Trends")
plt.show()



df['Day'] = df['Date'].dt.day_name()

weekday = df.groupby('Day')[[
    'Children transferred out of CBP custody',
    'Children discharged from HHS Care'
]].mean()

weekday

Next steps:


weekday.plot(kind='bar',
             figsize=(10,5))

plt.title("Weekday Analysis")
plt.show()



df['Backlog'] = (
    df['Children apprehended and placed in CBP custody*']
    -
    df['Children discharged from HHS Care']
)

plt.figure(figsize=(12,5))

plt.plot(df['Date'],
         df['Backlog'])

plt.title('Backlog Trend')
plt.show()




df['Transfer_Efficiency'] = (
    df['Children transferred out of CBP custody'] / df['Children in CBP custody']
)

print(df['Transfer_Efficiency'].mean())


df['Discharge_Effectiveness'] = (
    df['Children discharged from HHS Care'] / df['Children in HHS Care']
)

print(df['Discharge_Effectiveness'].mean())


df['Pipeline_Throughput'] = (
    df['Children discharged from HHS Care'] / df['Children apprehended and placed in CBP custody*']
)

print(df['Pipeline_Throughput'].mean())



df['Backlog'] = (
    df['Children apprehended and placed in CBP custody*'] - df['Children discharged from HHS Care']
)

print(df['Backlog'].head())



stability = df['Children discharged from HHS Care'].std()

print("Outcome Stability Score:", stability)

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Transfer_Efficiency'])
plt.title("Transfer Efficiency Trend")
plt.show()



plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Discharge_Effectiveness'])
plt.title("Discharge Effectiveness Trend")
plt.show()



plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Backlog'])
plt.title("Backlog Accumulation Trend")
plt.show()



low_transfer = df[df['Transfer_Efficiency'] < 0.5]

print(low_transfer[['Date', 'Transfer_Efficiency']].head())
        Date  Transfer_Efficiency

low_discharge = df[df['Discharge_Effectiveness'] < 0.02]

print(low_discharge[['Date', 'Discharge_Effectiveness']].head())
        Date  Discharge_Effectiveness


low_transfer = df[df['Transfer_Efficiency'] < 0.5]

print("Low Transfer Efficiency Days:")
print(low_transfer[['Date', 'Transfer_Efficiency']].head(10))



low_discharge = df[df['Discharge_Effectiveness'] < 0.02]

print("Low Discharge Effectiveness Days:")
print(low_discharge[['Date', 'Discharge_Effectiveness']].head(10))



top_backlog = df.sort_values(
    by='Backlog',
    ascending=False
)

print(top_backlog[['Date', 'Backlog']].head(10))
        

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Backlog'])
plt.title("Backlog Accumulation Trend")
plt.xlabel("Date")
plt.ylabel("Backlog")
plt.show()



%%writefile app.py

import streamlit as st

st.title("Care Transition Efficiency Analytics Dashboard")

st.write("Welcome to the dashboard!")
Overwriting app.py


!ls
 app.py
'HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program (1).csv'
'HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program.csv'
 sample_data


# Summary KPIs

print("===== PROJECT INSIGHTS =====")

print("Average Transfer Efficiency:",
      round(df['Transfer_Efficiency'].mean(), 2))

print("Average Discharge Effectiveness:",
      round(df['Discharge_Effectiveness'].mean(), 2))

print("Average Pipeline Throughput:",
      round(df['Pipeline_Throughput'].mean(), 2))

print("Maximum Backlog:",
      df['Backlog'].max())

print("Minimum Backlog:",
      df['Backlog'].min())

print("Outcome Stability Score:",
      round(df['Children discharged from HHS Care'].std(), 2))





import streamlit as st
import pandas as pd

st.title("Care Transition Efficiency & Placement Outcome Analytics")

df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program - HHS_Unaccompanied_Alien_Children_Program (1).csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Key Metrics")
st.write("Total Records:", len(df))

st.line_chart(df[['Children apprehended and placed in CBP custody*',
                  'Children discharged from HHS Care']])




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

