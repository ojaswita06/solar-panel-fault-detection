# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# ------------------ SETTINGS ------------------
st.set_page_config(page_title="Solar Panel Fault Detection", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(BASE_DIR, "data", "solar_data.csv")

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚡ Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")
fault_filter = st.sidebar.selectbox("Select Fault Status", ["All", "Faulty", "Healthy"])

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df['INVERTER_FAULT'] = df['AC_POWER'].apply(lambda x: 1 if x < 4000 else 0)
    return df

if uploaded_file:
    df = load_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
else:
    df = load_data(DEFAULT_CSV)
    st.sidebar.info(f"Using default CSV: {DEFAULT_CSV}")

# ------------------ VALIDATION ------------------
required_columns = ['DC_POWER', 'AC_POWER', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE']
if not all(col in df.columns for col in required_columns):
    st.error(f"CSV must contain columns: {required_columns}")
    st.stop()

# ------------------ FILTER DATA ------------------
if fault_filter == "Faulty":
    filtered_df = df[df['INVERTER_FAULT'] == 1]
elif fault_filter == "Healthy":
    filtered_df = df[df['INVERTER_FAULT'] == 0]
else:
    filtered_df = df

# ------------------ SUMMARY METRICS ------------------
st.title("☀️ Solar Panel Fault Detection Dashboard")
st.markdown("#### Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Panels", len(df))
col2.metric("Faulty Panels", df['INVERTER_FAULT'].sum(), delta_color="inverse")
col3.metric("Healthy Panels", len(df) - df['INVERTER_FAULT'].sum())

# ------------------ TABS ------------------
tab1, tab2, tab3 = st.tabs(["Original Data", "Fault Data", "Graphs"])

# Original Data Tab
with tab1:
    st.subheader("Original Data")
    st.dataframe(df[required_columns])

# Fault Data Tab
with tab2:
    st.subheader("Data with Fault Highlight")
    def highlight_faults(row):
        return ['background-color: red' if row['INVERTER_FAULT']==1 else 'background-color: #c6f5d9' for _ in row]
    #st.dataframe(filtered_df.style.apply(highlight_faults, axis=1))
    st.dataframe(filtered_df.style.apply(highlight_faults, axis=1)
                            .set_properties(**{'color': 'black'}))


# Graphs Tab
with tab3:
    st.subheader("Power Graphs")
    fig, ax = plt.subplots()
    ax.plot(df['DC_POWER'], label='DC Power', marker='o')
    ax.plot(df['AC_POWER'], label='AC Power', marker='x')
    ax.set_xlabel("Sample")
    ax.set_ylabel("Power")
    ax.set_title("DC vs AC Power")
    ax.legend()
    
    st.pyplot(fig)

    # Scatter plot
    fig2 = px.scatter(df, x='DC_POWER', y='AC_POWER', color='INVERTER_FAULT',
                      labels={'INVERTER_FAULT': 'Fault (1=Yes, 0=No)'},
                      title="DC Power vs AC Power with Faults",
                      color_continuous_scale=px.colors.sequential.Reds)
    st.plotly_chart(fig2, use_container_width=True)

# ------------------ DOWNLOAD BUTTON ------------------
st.sidebar.subheader("📥 Download Data")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download CSV", data=csv, file_name="fault_data.csv", mime="text/csv")

