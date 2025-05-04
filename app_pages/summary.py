import streamlit as st

def run():
  st.markdown("""
  ### 🌍 Analysis Summary & Key Insights

  This project analyzes multi-year air quality data from five randomly selected monitoring stations in China, offering a detailed exploration of pollution trends, contributing sources, and environmental impacts. The data spans from **2013 to 2017**, covering critical pollutants like **PM2.5, PM10, NO₂, SO₂, CO, and O₃**. The objective was to uncover temporal patterns, identify major contributors to pollution (vehicle vs. industrial), and assess how weather conditions such as **rainfall, temperature, and dewpoint** influence air quality.

  #### 🔍 Key Insights:

  - **AQI Trends**: AQI varied seasonally and annually, with higher pollution levels in **winter months**, especially **January and December**. The year **2014** showed relatively better AQI across most stations.
  - **Source-wise Contribution**: **Vehicle-related pollution** was generally more dominant than industrial, particularly in urban areas, as reflected by stacked and comparative visualizations.
  - **Rain’s Effect on Pollution**: **Rainfall had a lagged effect**, reducing AQI typically **1–2 days after** rainfall events.
  - **Station Variation**: Significant variation in AQI was observed across stations, indicating **geographical and urbanization-based** pollution disparities.
  - **Meteorological Impact**: Combining features like **temperature, dewpoint, and rain** revealed seasonal pollution patterns — higher pollution in **colder months** due to temperature inversion and limited dispersion.
  - **Outlier Handling**: Outliers in variables like **rainfall** were treated using **winsorization** to preserve data quality without loss of useful observations.

  """)