import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import os

# load the csv file
@st.cache_data
def load_data():
    data_path = os.path.join("data", "air_quality_data_combined.csv")
    df = pd.read_csv(data_path)
    return df

@st.cache_data
def handling_missing_values(df):
  # Impute numerical columns with the mean
  numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns

  # Create an imputer for numerical data
  numerical_imputer = SimpleImputer(strategy='mean')

  # Apply the imputer to the numerical columns
  df[numerical_cols] = numerical_imputer.fit_transform(df[numerical_cols])

  # Impute categorical columns with the mode (most frequent value)
  categorical_cols = df.select_dtypes(include=['object']).columns

  # Create an imputer for categorical data
  categorical_imputer = SimpleImputer(strategy='most_frequent')

  # Apply the imputer to the categorical columns
  df[categorical_cols] = categorical_imputer.fit_transform(df[categorical_cols])

  return df

@st.cache_data
def outlier_handling(df):
  # Select only numerical columns
  numeric_cols = df.select_dtypes(include=['number']).columns.to_list()
  numeric_cols.remove('No') # excluding `No` column
  numeric_cols.remove('year') # excluding `year` column
  numeric_cols.remove('month') # excluding `month` column
  numeric_cols.remove('day') # excluding `day` column
  numeric_cols.remove('hour') # excluding `hour` column

  # Winsorization (1st and 99th percentiles)
  for col in numeric_cols:
      lower = df[col].quantile(0.01)
      upper = df[col].quantile(0.99)
      df[col] = df[col].clip(lower=lower, upper=upper)

  return df

@st.cache_data
def create_timestamp_col(df):
    # Create `timestamp` column
  df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

  # Set `timestamp` as the index
  df = df.set_index('timestamp')

  # Drop `No`, `day`, `hour`
  df = df.drop(['No', 'day', 'hour'], axis=1)

  return df


def calculate_aqi(conc, breakpoints):
    for C_low, C_high, I_low, I_high in breakpoints:
        if C_low <= conc <= C_high:
            return ((I_high - I_low) / (C_high - C_low)) * (conc - C_low) + I_low
    return np.nan

@st.cache_data
def create_aqi_column(df):
  # breakpoint for calculating AQI for each one
  breakpoints_pm25_per_day = [(0, 35, 0, 50), (35, 75, 51, 100), (75, 115, 101, 150), (115, 150, 151, 200),
                      (150, 250, 201, 300), (250, 350, 301, 400), (350, 500, 401, 500)]

  breakpoints_pm10_per_day = [(0, 50, 0, 50), (51, 150, 51, 100), (151, 250, 101, 150), (251, 350, 151, 200),
                      (350, 420, 201, 300), (420, 500, 301, 400), (500, 600, 401, 500)]

  breakpoints_so2_per_hour = [(0, 150, 0, 50), (151, 500, 51, 100), (501, 650, 101, 150), (651, 800, 151, 200),
                     (801, 1600, 201, 300), (1601, 2100, 301, 400), (2100, 2620, 401, 500)]

  breakpoints_no2_per_hour = [(0, 100, 0, 50), (101, 200, 51, 100), (201, 700, 101, 150), (701, 1200, 151, 200),
                     (1201, 2340, 201, 300), (2341, 3090, 301, 400), (3091, 3840, 401, 500)]

  breakpoints_co_per_hour = [(0, 5000, 0, 50), (5001, 10000, 51, 100), (10001, 35000, 101, 150), (35001, 60000, 151, 200),
                    (60001, 90000, 201, 300), (90001, 120000, 301, 400), (120001, 150000, 401, 500)]

  breakpoints_o3_per_hour = [(0, 160, 0, 50), (161, 200, 51, 100), (201, 300, 101, 150), (301, 400, 151, 200),
                    (401, 800, 201, 300), (801, 1000, 301, 400), (1001, 1200, 401, 500)]

  # 24-hour averages for PM2.5 and PM10
  df['PM2.5_24h'] = df['PM2.5'].rolling(window=24, min_periods=1).mean()
  df['PM10_24h'] = df['PM10'].rolling(window=24, min_periods=1).mean()

  # AQI per pollutant
  df['AQI_PM25'] = df['PM2.5_24h'].apply(lambda x: calculate_aqi(x, breakpoints_pm25_per_day))
  df['AQI_PM10'] = df['PM10_24h'].apply(lambda x: calculate_aqi(x, breakpoints_pm10_per_day))
  df['AQI_SO2'] = df['SO2'].apply(lambda x: calculate_aqi(x, breakpoints_so2_per_hour))
  df['AQI_NO2'] = df['NO2'].apply(lambda x: calculate_aqi(x, breakpoints_no2_per_hour))
  df['AQI_CO'] = df['CO'].apply(lambda x: calculate_aqi(x, breakpoints_co_per_hour))
  df['AQI_O3'] = df['O3'].apply(lambda x: calculate_aqi(x, breakpoints_o3_per_hour))

  # Final AQI: max value among all pollutants
  df['AQI'] = df[['AQI_PM25', 'AQI_PM10', 'AQI_SO2', 'AQI_NO2', 'AQI_CO', 'AQI_O3']].max(axis=1).round()

  # Keeping only `AQI` column, droping other column related to calculating AQI
  df.drop(['PM2.5_24h', 'PM10_24h', 'AQI_PM25', 'AQI_PM10', 'AQI_SO2', 'AQI_NO2', 'AQI_CO', 'AQI_O3'], axis=1, inplace=True)

  return df


@st.cache_data
def create_aqi_category_column(df):
  bins = [0, 50, 100, 150, 200, 300, float('inf')]
  labels = ['Good', 'Moderate', 'Unhealthy for sensitive group', 'Unhealthy', 'Very Unhealthy', 'Hazardous']

  df['AQI_category'] = pd.cut(df['AQI'], bins=bins, labels=labels, right=False)

  return df

@st.cache_data
def execute_feature_extraction_operations(df):
  df = create_timestamp_col(df)
  #adding two new columns
  df['vehicle_pollution'] = df[['PM2.5', 'PM10', 'NO2', 'CO']].sum(axis=1)
  df['industrial_pollution'] = df[['SO2', 'O3']].sum(axis=1)
  df = create_aqi_column(df)
  df = create_aqi_category_column(df)

  return df