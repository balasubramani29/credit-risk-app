import pandas as pd
from sklearn.preprocessing import LabelEncoder
import streamlit as st

from config.settings import DATA_PATH


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


# =========================================================
# PREPROCESS
# =========================================================
def preprocess(df):

    df = df.copy()

    encoders = {}

    for col in df.columns:

        if df[col].dtype == "object":

            le = LabelEncoder()

            df[col] = le.fit_transform(df[col])

            encoders[col] = le

    return df, encoders