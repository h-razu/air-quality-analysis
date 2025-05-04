import streamlit as st
from utils.plot_utils import plot_top_feature_importance
from utils.preprocessing import (
    load_data,
    handling_missing_values,
    outlier_handling,
    execute_feature_extraction_operations
)
from utils.modeling_utils import (
    execute_data_preprocessing,
    execute_feature_selection,
    load_models,
    show_model_results
)

def run():
  st.title("Modeling & Prediction")
  st.markdown("This section demonstrates the modeling workflow and predicts AQI based on key features.")

  # Show the progress bar and text
  progress = st.progress(0)
  status_text = st.empty()

  # Load data and processing steps with progress bar
  status_text.text("Loading data...")
  df = load_data()
  progress.progress(7)

  status_text.text("Handling missing values...")
  df = handling_missing_values(df)
  progress.progress(13)

  status_text.text("Handling outliers...")
  df = outlier_handling(df)
  progress.progress(20)

  status_text.text("Extracting features...")
  df = execute_feature_extraction_operations(df)
  progress.progress(50)

  status_text.text("Preprocessing data...")
  X_train, y_train, X_test, y_test = execute_data_preprocessing(df)
  progress.progress(60)

  status_text.text("Feature selection...")
  feature_importances = execute_feature_selection(X_train, y_train)
  progress.progress(90)

  status_text.text("Loading Models...")
  models = load_models()
  progress.progress(100)

  # Hide the progress bar by calling st.empty()
  progress.empty()
  status_text.empty()
  st.success("Loading complete!")

  X_test_selected = X_test[models.get("selected_features")]

  # Sub-navigation inside this page
  sub_page = st.radio(
      "Choose Section",
      ["Preprocessing Steps", "Random Forest", "AdaBoost", "XGBoost"],
      index=0,
      horizontal=True
  )

  if sub_page == "Preprocessing Steps":
      st.subheader("📋 Preprocessing Steps Summary")
      st.markdown("""
      - **Lag Features**: Created lagged versions of key variables to incorporate temporal dynamics crucial for time series modeling.

      - **Train-Test Split**:
          - Data was grouped by **station**, then sorted chronologically within each station.
          - Used an **80/20 split**, training on past data and testing on future records to maintain time-based integrity.
          - This method ensures realistic forecasting and prevents data leakage.

      - **Feature Scaling**:
          - Applied `StandardScaler` to normalize **numerical features**, improving model performance by standardizing input ranges.

      - **Categorical Encoding**:
          - Used `LabelEncoder` to convert **categorical variables** into numeric labels that models can interpret.

      - **Feature Selection**:
          - Employed a **Random Forest model** to determine the most predictive features.
          - Selected the **top 10 important features** based on feature importance scores to optimize model efficiency and reduce overfitting.
      """)

      #plot feature importance
      fig = plot_top_feature_importance(feature_importances)
      st.pyplot(fig)

      #display top feature in table
      top_n = st.slider("Select the number of top features to display", min_value=1, max_value=len(feature_importances), value=10)

      # Sort features by importance and get the top_n features
      top_features = feature_importances.sort_values(by='Importance', ascending=False).head(top_n)

      # Display the top features as a table in Streamlit
      st.subheader(f"Top {top_n} Important Features")
      st.dataframe(top_features)


  elif sub_page == "Random Forest":
      st.header("🌲 Random Forest Model")
      show_model_results(models,"RandomForest", X_test_selected, y_test)
  elif sub_page == "AdaBoost":
      st.header("🚀 AdaBoost Model")
      show_model_results(models, "AdaBoost", X_test_selected, y_test)
  elif sub_page == "XGBoost":
      st.header("⚡ XGBoost Model")
      show_model_results(models, "XGBoost", X_test_selected, y_test)