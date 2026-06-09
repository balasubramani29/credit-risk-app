import joblib
import streamlit as st

from config.settings import MODEL_PATH


# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)