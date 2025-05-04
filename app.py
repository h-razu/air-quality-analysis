import streamlit as st
import importlib.util
import os
import sys

# Set the page title and icon
st.set_page_config(
    page_title="China Air Quality Insights",
    page_icon="🌍",
    layout="wide"
)

st.sidebar.title("Dashboard")

page_names = {
    "Overview": "home",
    "Transform Data Overview" : "transformed_data_overview",
    "Data Visualizations": "visualization",
    "Modeling & Prediction": "modeling_prediction",
    "Insights & Summary": "summary"
}


if "page" not in st.session_state:
    st.session_state.page = "Overview"

page = st.sidebar.radio(
    "Go to",
    list(page_names.keys()),
    index=list(page_names.keys()).index(st.session_state.page)
)

st.session_state.page = page

def load_page(module_name):
    file_path = os.path.join("app_pages", f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    module.run()

# Run the selected page
load_page(page_names[page])
