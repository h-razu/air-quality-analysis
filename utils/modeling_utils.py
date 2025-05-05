import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import gdown
import xgboost as xgb

def load_models():
    model_dir = "models"
    models = {}

    # can't push to github due to size limitations
    # models['RandomForest'] = joblib.load(os.path.join(model_dir, "random_forest_model.pkl"))
    models['AdaBoost'] = joblib.load(os.path.join(model_dir, "ada_boost_model.pkl"))
    models['selected_features'] = joblib.load(os.path.join(model_dir, "selected_features.pkl"))

    xgb_model = xgb.Booster()
    xgb_model.load_model(os.path.join(model_dir, "xgb_model.json"))
    models['XGBoost'] = xgb_model

    # Random Forest Model from Google Drive
    rf_model_path = os.path.join(model_dir, "random_forest_model.pkl")
    if not os.path.exists(rf_model_path):
        url = "https://drive.google.com/uc?id=1cNBMmLE3cwv06C764fIeiz3fyIL08BVE"
        gdown.download(url, rf_model_path, quiet=False)

    models['RandomForest'] = joblib.load(rf_model_path)

    return models

@st.cache_data
def adding_lag_feature(df):
  df = df.sort_values(['station', 'year', 'month'])
  df['PM2.5_lag1'] = df.groupby('station')['PM2.5'].shift(1)
  df['AQI_lag1'] = df.groupby('station')['AQI'].shift(1)
  df.dropna(inplace=True)

  return df

@st.cache_data
def splitting_data_set(df):
  # Split data by station, then chronologically within each station
  train_data_list = []
  test_data_list = []

  # Loop through each station in the dataset
  for station in df['station'].unique():
      station_data = df[df['station'] == station]

      # Ensure the data is sorted by time (timestamp)
      station_data = station_data.sort_index()

      # Determine split index
      split_index = int(len(station_data) * 0.8)

      # Split data for this station using iloc
      train_data_list.append(station_data.iloc[:split_index])
      test_data_list.append(station_data.iloc[split_index:])

  # Combine all the station-specific train and test data
  train_data = pd.concat(train_data_list)
  test_data = pd.concat(test_data_list)

  # Now, you have train_data and test_data with the correct split
  X_train = train_data.drop('AQI', axis=1)
  y_train = train_data['AQI']
  X_test = test_data.drop('AQI', axis=1)
  y_test = test_data['AQI']

  return X_train, y_train, X_test, y_test

@st.cache_data
def feature_encoding(X_train, X_test):
  categorical_cols = ['wd', 'station', 'AQI_category']

  for col in categorical_cols:
      le = LabelEncoder()
      X_train[col] = le.fit_transform(X_train[col])
      X_test[col] = le.transform(X_test[col])

  return X_train, X_test

@st.cache_data
def feature_scaling(X_train, X_test):
  scaler = StandardScaler()
  scaled_cols = X_train.select_dtypes(include=['float64', 'int64']).columns.tolist()

  X_train[scaled_cols] = scaler.fit_transform(X_train[scaled_cols])
  X_test[scaled_cols] = scaler.transform(X_test[scaled_cols])

  return X_train, X_test

@st.cache_data
def execute_data_preprocessing(df):
  df = adding_lag_feature(df)

  X_train, y_train, X_test, y_test = splitting_data_set(df)

  X_train, X_test = feature_encoding(X_train, X_test)

  X_train, X_test = feature_scaling(X_train, X_test)

  return X_train, y_train, X_test, y_test

@st.cache_data
def execute_feature_selection(X_train, y_train):
  # Fit a RandomForestRegressor model
  model = RandomForestRegressor()
  model.fit(X_train, y_train)

  # Get feature importance
  feature_importances = model.feature_importances_

  # Create a DataFrame with features and their importance scores
  importance_df = pd.DataFrame({
      'Feature': X_train.columns,
      'Importance': feature_importances
  })

  # Sort features by importance
  importance_df = importance_df.sort_values(by='Importance', ascending=False)

  return importance_df

def show_model_results(models, model_name, X_test, y_test):
    model = models.get(model_name)

    if model:
        if model_name == "XGBoost":
            dtest = xgb.DMatrix(X_test)
            y_pred = model.predict(dtest)
        else:
            y_pred = model.predict(X_test)

        # Metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Display metrics
        metrics_df = pd.DataFrame({
            "Metric": ["MAE", "MSE", "RMSE", "R2 Score"],
            "Value": [mae, mse, rmse, r2]
        })

        st.markdown("#### 📊 Model Performance Metrics")
        st.table(metrics_df)

        # Actual vs Predicted Plot
        st.markdown("#### 📈 Actual vs Predicted AQI")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x=y_test, y=y_pred, color='green', alpha=0.6, ax=ax)
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
        ax.set_xlabel("Actual AQI")
        ax.set_ylabel("Predicted AQI")
        ax.set_title(f"Actual vs Predicted AQI ({model_name})")
        ax.grid(True)
        plt.tight_layout()
        st.pyplot(fig)


    else:
        st.error(f"❌ {model_name} model not found.")