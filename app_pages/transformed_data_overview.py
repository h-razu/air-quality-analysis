import streamlit as st
from utils.preprocessing import load_data, execute_feature_extraction_operations, handling_missing_values, outlier_handling

def run():
  st.title("Transformed Data Overview")
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

  st.success("Data Transformed complete!")

  st.write("Transformed Data Preview:")
  st.write(df.head(10))

  # Add a description of the data processing steps
  st.subheader("Data Transforming Overview")
  st.markdown("""
  The data preprocessing steps included the following operations:
  - **Handling Missing Values**: Numerical columns were imputed with the mean value, and categorical columns with the most frequent value.
  - **Outlier Handling**: Outliers in the numerical columns were handled using Winsorization (clipping values to the 1st and 99th percentiles).
  - **Timestamp Creation**: A `timestamp` column was created by combining the year, month, day, and hour columns, and set as the index.
  - **Air Quality Index (AQI) Calculation**: AQI values were calculated for various pollutants (PM2.5, PM10, SO2, NO2, CO, O3) based on predefined breakpoints. The highest AQI among all pollutants was assigned as the final AQI for each record.
  - **AQI Category Creation**: The AQI values were categorized into 6 levels: 'Good', 'Moderate', 'Unhealthy for sensitive group', 'Unhealthy', 'Very Unhealthy', and 'Hazardous'.
  - **Pollution Source Estimation**: Additional columns were created to estimate pollution from vehicles (based on PM2.5, PM10, NO2, CO) and industrial sources (based on SO2, O3).
  """)

  # Download the processed dataset
  csv = df.to_csv(index=False).encode('utf-8')
  st.download_button(
      label="📥 Download Cleaned Data as CSV",
      data=csv,
      file_name='clean_air_quality_data.csv',
      mime='text/csv'
  )