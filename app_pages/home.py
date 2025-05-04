import streamlit as st
from utils.preprocessing import load_data

def run():
  st.title("Air Quality Insights Across Multiple Sites in China")
  st.markdown("""
  <div style='text-align: justify'>
  This project focuses on analyzing air quality data from five randomly selected monitoring stations across China, chosen from a set of twelve available
  sites. The analysis explores temporal trends, seasonal variations, and source-wise pollution contributions (vehicle vs. industrial) to understand
  patterns in AQI and associated pollutants. Various meteorological factors such as temperature, rain, and dewpoint are also examined to study their
  potential impact on pollution levels.
  </div>
  """, unsafe_allow_html=True)

  st.subheader("🎯 Project Objectives")
  st.markdown("""
    - **Analyze Air Quality Trends:** Examine temporal AQI patterns on daily, monthly, and yearly scales.
    - **Compare Multi-Site Data:** Utilize data from five randomly selected stations to understand geographic variation.
    - **Identify Key Pollution Contributors:** Assess vehicle and industrial emissions separately.
    - **Study Environmental Influence:** Analyze the role of weather (rain, temperature, dewpoint, wind) on AQI.
    - **Visualize and Communicate Insights:** Use interactive plots to highlight patterns and anomalies.
    - **Support Decision-Making:** Help inform environmental policy and raise public awareness through data insights.
    """)

  st.subheader("📚 Dataset Overview")
  st.markdown("""
   <div style='text-align: justify'>
    This dataset contains hourly air quality and meteorological data collected from 12 monitoring stations in Beijing over a period of four years (March 1, 2013 – February 28, 2017).

    #### Key Components:
    - **Air pollutants:**
      PM2.5, PM10, SO₂, NO₂, CO, and O₃
    - **Meteorological data:**
      Wind speed (Wspd), Rainfall (Rain), Temperature (Temp), Dew point (Dewp), and Atmospheric pressure (Pre)

    #### Data Sources:
    - **Air quality data**: Beijing Municipal Environmental Monitoring Center
    - **Weather data**: Matched from the nearest weather stations by the China Meteorological Administration
    </div>
    """, unsafe_allow_html=True)


  with st.spinner('Loading data...'):
    df = load_data()

  # Show dataset shape
  st.markdown(f"#### 📐 Dataset Size:")
  st.write(f"- Total Rows: **{df.shape[0]}**")
  st.write(f"- Total Columns: **{df.shape[1]}**")

  # Station used to analyze this project
  st.markdown("#### 🏙️ Monitoring Stations Used in This Analysis:")
  for station in df['station'].unique():
        st.markdown(f"- {station}")

  # Load and display top 5 rows
  st.subheader("📊 Sample Data")
  st.dataframe(df.head(10))