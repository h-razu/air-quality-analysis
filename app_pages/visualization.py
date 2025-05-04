import streamlit as st

from utils.preprocessing import load_data, execute_feature_extraction_operations, handling_missing_values, outlier_handling
from utils.plot_utils import (
    plot_average_aqi_per_year,
    plot_stationwise_aqi,
    plot_monthlywise_aqi_per_year,
    plot_yearly_pollution_trend,
    plot_monthly_pollution_pattern,
    plot_yearly_pollution_contribution,
    plot_pollution_by_station_and_year,
    plot_rainfall_vs_aqi,
    plot_rain_vs_pollution,
    plot_seasonal_temp_dewp,
    plot_correlation_heatmap
)

def run():
  st.title("Data Visualizations")

  progress = st.progress(0)
  status_text = st.empty()

  # Load data and processing steps with progress bar
  status_text.text("Loading data...")
  df = load_data()
  progress.progress(20)

  status_text.text("Handling missing values...")
  df = handling_missing_values(df)
  progress.progress(40)

  status_text.text("Handling outliers...")
  df = outlier_handling(df)
  progress.progress(60)

  status_text.text("Extracting features...")
  df = execute_feature_extraction_operations(df)
  progress.progress(100)

  # Hide the progress bar by calling st.empty()
  progress.empty()
  status_text.empty()
  st.success("Data Fetch complete!")

  # dropdown for options
  option = st.selectbox(
    "Select Trend to Visualize",
    options=[
        "Air Quality Index (AQI) Overview",
        "Vehicle and Industrial Emissions Impact",
        "Impact of Rain",
        "Correlations Heatmap"
        ],
    index=0  # Default is AQI
  )

  if option == "Air Quality Index (AQI) Overview":
      st.subheader("Average AQI per Year")
      fig1 = plot_average_aqi_per_year(df)
      st.pyplot(fig1)

      st.subheader("Average Monthly AQI per Year")
      fig2 = plot_monthlywise_aqi_per_year(df)
      st.pyplot(fig2)

      st.subheader("Average AQI per Year for Each Station")
      fig3 = plot_stationwise_aqi(df)
      st.pyplot(fig3)

  elif option == "Vehicle and Industrial Emissions Impact":
      st.subheader("Yearly Average Pollution Trend")
      fig4 = plot_yearly_pollution_trend(df)
      st.pyplot(fig4)

      st.subheader("Seasonal Pollution Pattern (Monthly Average)")
      fig5 = plot_monthly_pollution_pattern(df)
      st.pyplot(fig5)

      st.subheader("Vehicle vs Industrial Pollution Contribution by Year")
      fig6 = plot_yearly_pollution_contribution(df)
      st.pyplot(fig6)

      st.subheader("Pollution Type Contribution by Station and Year")
      fig7 = plot_pollution_by_station_and_year(df)
      st.pyplot(fig7)

  elif option == "Impact of Rain":
      st.subheader("Rainfall vs AQI")
      fig8 = plot_rainfall_vs_aqi(df)
      st.pyplot(fig8)

      st.subheader("Rain Imapact on Pollutions")
      fig9 = plot_rain_vs_pollution(df)
      st.pyplot(fig9)

      st.subheader("Seasonal Patterns of Temperature and Dewpoint")
      fig10 = plot_seasonal_temp_dewp(df)
      st.pyplot(fig10)

  elif option == "Correlations Heatmap":
      st.subheader("Correlations Heatmap")
      fig11 = plot_correlation_heatmap(df)
      st.pyplot(fig11)
