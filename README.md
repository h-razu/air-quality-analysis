# 🌍 China Air Quality Insights Dashboard

This Streamlit web application provides an interactive analysis and prediction of air quality in various Chinese cities between 2013 and 2017. The goal of this project is to uncover pollution patterns, estimate AQI levels, and provide actionable insights using machine learning.

## 🔍 Project Overview

The dataset includes hourly air quality measurements such as PM2.5, PM10, SO2, NO2, CO, and O3, along with weather data and city information. It was cleaned and processed through several steps including handling missing values, outlier treatment, and feature engineering.

### ✅ Key Processing Steps

- **Missing Values Handling**: Numerical features were filled with the mean, categorical with the mode.
- **Outlier Treatment**: Winsorization was used to clip extreme values.
- **Feature Engineering**: Created a timestamp field, calculated AQI for multiple pollutants, assigned AQI categories, and estimated pollution sources (vehicle and industrial).
- **Lag Features**: Generated lag features to capture temporal trends.
- **Feature Encoding & Scaling**: Used `LabelEncoder` for categoricals and `StandardScaler` for numerics.
- **Feature Selection**: Random Forest was used to identify the top 10 most important features.

### 📊 Visualizations

Interactive plots help users explore:

- AQI trends by year and station
- Monthly AQI variations
- Vehicle and industrial pollution patterns

### 🤖 Modeling & Prediction

Three regression models were trained to predict AQI:

- **Random Forest Regressor**
- **AdaBoost Regressor**
- **XGBoost Regressor**

Data was split by station and time to prevent data leakage, ensuring realistic time-series forecasting. Each model was evaluated using metrics such as MAE, MSE, RMSE, and R² Score. A scatter plot visualizes predicted vs. actual AQI values.

### 📌 Features of the App

- Selectable trend-based visualizations
- Downloadable processed dataset
- Sub-page navigation under Modeling for easy comparison
- Performance metrics table and AQI prediction graph
- Summary of insights drawn from the data and modeling
