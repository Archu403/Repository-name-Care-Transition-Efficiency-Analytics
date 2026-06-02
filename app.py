

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
      dtype='object')
Date                                               0
Children apprehended and placed in CBP custody*    0
Children in CBP custody                            0
Children transferred out of CBP custody            0
Children in HHS Care                               0
Children discharged from HHS Care                  0
dtype: int64
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 720 entries, 0 to 719
Data columns (total 6 columns):
 #   Column                                           Non-Null Count  Dtype         
---  ------                                           --------------  -----         
 0   Date                                             720 non-null    datetime64[ns]
 1   Children apprehended and placed in CBP custody*  720 non-null    int64         
 2   Children in CBP custody                          720 non-null    int64         
 3   Children transferred out of CBP custody          720 non-null    int64         
 4   Children in HHS Care                             720 non-null    int64         
 5   Children discharged from HHS Care                720 non-null    int64         
dtypes: datetime64[ns](1), int64(5)
memory usage: 33.9 KB


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


[ ]

Start coding or generate with AI.


df['Transfer_Efficiency'] = (
    df['Children transferred out of CBP custody'] / df['Children in CBP custody']
)

print(df['Transfer_Efficiency'].mean())
0.6910176523134812


df['Discharge_Effectiveness'] = (
    df['Children discharged from HHS Care'] / df['Children in HHS Care']
)

print(df['Discharge_Effectiveness'].mean())
0.023737002796523007


df['Pipeline_Throughput'] = (
    df['Children discharged from HHS Care'] / df['Children apprehended and placed in CBP custody*']
)

print(df['Pipeline_Throughput'].mean())
inf


df['Backlog'] = (
    df['Children apprehended and placed in CBP custody*'] - df['Children discharged from HHS Care']
)

print(df['Backlog'].head())
0   -8
1   -5
2   -3
3   -1
4    4
Name: Backlog, dtype: int64


stability = df['Children discharged from HHS Care'].std()

print("Outcome Stability Score:", stability)
Outcome Stability Score: 125.7028405572817


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
1 2025-12-18             0.120000
2 2025-12-17             0.354839
3 2025-12-16             0.277778
4 2025-12-15             0.214286
5 2025-12-14             0.114286


low_discharge = df[df['Discharge_Effectiveness'] < 0.02]

print(low_discharge[['Date', 'Discharge_Effectiveness']].head())
        Date  Discharge_Effectiveness
0 2025-12-21                 0.005636
1 2025-12-18                 0.006472
2 2025-12-17                 0.004031
3 2025-12-16                 0.003647
4 2025-12-15                 0.002834


low_transfer = df[df['Transfer_Efficiency'] < 0.5]

print("Low Transfer Efficiency Days:")
print(low_transfer[['Date', 'Transfer_Efficiency']].head(10))
Low Transfer Efficiency Days:
         Date  Transfer_Efficiency
1  2025-12-18             0.120000
2  2025-12-17             0.354839
3  2025-12-16             0.277778
4  2025-12-15             0.214286
5  2025-12-14             0.114286
6  2025-12-11             0.191489
7  2025-12-10             0.092593
8  2025-12-09             0.233333
9  2025-12-08             0.333333
11 2025-12-04             0.179487


low_discharge = df[df['Discharge_Effectiveness'] < 0.02]

print("Low Discharge Effectiveness Days:")
print(low_discharge[['Date', 'Discharge_Effectiveness']].head(10))
Low Discharge Effectiveness Days:
        Date  Discharge_Effectiveness
0 2025-12-21                 0.005636
1 2025-12-18                 0.006472
2 2025-12-17                 0.004031
3 2025-12-16                 0.003647
4 2025-12-15                 0.002834
5 2025-12-14                 0.003249
6 2025-12-11                 0.004103
7 2025-12-10                 0.003690
8 2025-12-09                 0.003275
9 2025-12-08                 0.001639


top_backlog = df.sort_values(
    by='Backlog',
    ascending=False
)

print(top_backlog[['Date', 'Backlog']].head(10))
          Date  Backlog
259 2024-12-02      121
410 2024-04-23      118
464 2024-02-06      113
409 2024-04-24       99
405 2024-04-30       85
286 2024-10-22       71
301 2024-09-30       71
256 2024-12-05       68
459 2024-02-13       67
395 2024-05-14       60


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
===== PROJECT INSIGHTS =====
Average Transfer Efficiency: 0.69
Average Discharge Effectiveness: 0.02
Average Pipeline Throughput: inf
Maximum Backlog: 121
Minimum Backlog: -447
Outcome Stability Score: 125.7


!pip install streamlit
Collecting streamlit
  Downloading streamlit-1.58.0-py3-none-any.whl.metadata (9.6 kB)
Requirement already satisfied: altair!=5.4.0,!=5.4.1,<7,>=4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.5.0)
Requirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (1.9.0)
Requirement already satisfied: cachetools<8,>=5.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.2.6)
Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (8.4.0)
Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.12/dist-packages (from streamlit) (3.1.50)
Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.0.2)
Requirement already satisfied: packaging>=20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (26.2)
Requirement already satisfied: pandas<4,>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.2.2)
Requirement already satisfied: pillow<13,>=7.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (11.3.0)
Collecting pydeck<1,>=0.8.0b4 (from streamlit)
  Downloading pydeck-0.9.2-py2.py3-none-any.whl.metadata (4.2 kB)
Requirement already satisfied: protobuf<8,>=3.20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.29.6)
Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (18.1.0)
Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.32.4)
Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (9.1.4)
Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.10.2)
Requirement already satisfied: typing-extensions<5,>=4.10.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (4.15.0)
Requirement already satisfied: starlette>=0.40.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.52.1)
Requirement already satisfied: uvicorn>=0.30.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.47.0)
Requirement already satisfied: httptools>=0.6.3 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.7.1)
Requirement already satisfied: anyio>=4.0.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (4.13.0)
Requirement already satisfied: python-multipart>=0.0.10 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.0.29)
Requirement already satisfied: websockets>=12.0.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (15.0.1)
Requirement already satisfied: itsdangerous>=2.1.2 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.2.0)
Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.0.0)
Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.1.6)
Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (4.26.0)
Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2.21.2)
Requirement already satisfied: idna>=2.8 in /usr/local/lib/python3.12/dist-packages (from anyio>=4.0.0->streamlit) (3.15)
Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.12/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)
Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/dist-packages (from pandas<4,>=1.4.0->streamlit) (2026.2)
Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (3.4.7)
Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2026.5.20)
Requirement already satisfied: h11>=0.8 in /usr/local/lib/python3.12/dist-packages (from uvicorn>=0.30.0->streamlit) (0.16.0)
Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.12/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.3)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.0.3)
Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (26.1.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.37.0)
Requirement already satisfied: rpds-py>=0.25.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.30.0)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->pandas<4,>=1.4.0->streamlit) (1.17.0)
Downloading streamlit-1.58.0-py3-none-any.whl (9.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.2/9.2 MB 63.3 MB/s eta 0:00:00
Downloading pydeck-0.9.2-py2.py3-none-any.whl (11.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.3/11.3 MB 83.4 MB/s eta 0:00:00
Installing collected packages: pydeck, streamlit
Successfully installed pydeck-0.9.2 streamlit-1.58.0


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
2026-06-02 08:02:51.459 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.460 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.461 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.468 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.469 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.470 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.473 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.474 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.474 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.476 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.476 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.477 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.477 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.479 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.479 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.480 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.481 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.481 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.558 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.559 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:02:51.560 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
DeltaGenerator()


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

st.write("Dashboard Completed Successfully")
2026-06-02 08:05:26.524 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.526 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.527 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.528 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.544 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.545 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.548 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.548 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.549 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.550 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.555 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.555 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.556 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.558 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.559 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.560 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.562 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.562 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.563 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.564 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.566 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.568 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.569 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.570 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.572 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.573 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.574 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.575 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.575 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.577 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.578 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.578 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.642 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.643 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.645 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.648 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.649 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.650 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.711 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.712 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.715 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.716 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.717 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.720 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.782 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.783 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.785 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.786 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.789 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.789 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.867 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.868 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.869 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.871 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.874 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.875 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.930 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.931 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.933 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.934 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.935 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
2026-06-02 08:05:26.937 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.
Colab paid products - Cancel contracts here
