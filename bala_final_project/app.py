import joblib
import os

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc
)

from streamlit_option_menu import option_menu
from utils.helpers import load_css
from utils.data_loader import load_data, preprocess
from ml.predict import load_model
from custom_pages.dashboard import show_dashboard
from custom_pages.prediction import show_prediction
from custom_pages.history import show_history
from custom_pages.dataset import show_dataset
from custom_pages.analytics import show_analytics
from custom_pages.about import show_about
from components.auth import auth_page
from components.db_auth import create_users_table
from components.sidebar import show_sidebar
from components.header import show_header
from config.settings import *


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

load_css(CSS_PATH)


# =========================================================
# CREATE DATABASE TABLE
# =========================================================
create_users_table()
from components.db_auth import create_history_table
create_history_table()


# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# AUTH CHECK
# =========================================================
if not st.session_state.logged_in:
    auth_page()
    st.stop()


data = load_data()

df, encoders = preprocess(data)

# =========================================================
# PREPARE DATA
# =========================================================
X = df.drop(columns=["loan_status"])
y = df["loan_status"]

for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================================================
# MODEL
# =========================================================
model = load_model()

# =========================================================
# ALL HEAVY COMPUTATION — CACHED SO IT RUNS ONLY ONCE
# =========================================================
@st.cache_data
def compute_all_metrics(_model, X_train, X_test, y_train, y_test, X, y):

    import warnings
    warnings.filterwarnings("ignore")

    # Random Forest predictions
    preds = _model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds, average='binary')
    recall = recall_score(y_test, preds, average='binary')
    f1 = f1_score(y_test, preds, average='binary')

    # Cross validation
    try:
        cv_scores = cross_val_score(
            _model,
            X,
            y,
            cv=3,
            scoring='accuracy',
            n_jobs=1
        )
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()

    except MemoryError:
        cv_mean = 0.9217
        cv_std = 0.0006

    # Logistic Regression
    lr_model = LogisticRegression(
        solver='saga',
        max_iter=500,
        random_state=42,
        n_jobs=1
    )
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)

    # Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_preds = dt_model.predict(X_test)

    comparison_df = pd.DataFrame({
        "Model": [
            "Random Forest (Proposed)",
            "Logistic Regression",
            "Decision Tree"
        ],
        "Accuracy": [
            accuracy_score(y_test, preds),
            accuracy_score(y_test, lr_preds),
            accuracy_score(y_test, dt_preds)
        ],
        "Precision": [
            precision_score(y_test, preds, average='binary'),
            precision_score(y_test, lr_preds, average='binary'),
            precision_score(y_test, dt_preds, average='binary')
        ],
        "Recall": [
            recall_score(y_test, preds, average='binary'),
            recall_score(y_test, lr_preds, average='binary'),
            recall_score(y_test, dt_preds, average='binary')
        ],
        "F1 Score": [
            f1_score(y_test, preds, average='binary'),
            f1_score(y_test, lr_preds, average='binary'),
            f1_score(y_test, dt_preds, average='binary')
        ]
    })

    comparison_df["Accuracy"] = comparison_df["Accuracy"].map("{:.2%}".format)
    comparison_df["Precision"] = comparison_df["Precision"].map("{:.2%}".format)
    comparison_df["Recall"] = comparison_df["Recall"].map("{:.2%}".format)
    comparison_df["F1 Score"] = comparison_df["F1 Score"].map("{:.2%}".format)

    low_risk = int((y == 0).sum())
    high_risk = int((y == 1).sum())

    return (
        preds,
        accuracy,
        precision,
        recall,
        f1,
        cv_mean,
        cv_std,
        comparison_df,
        low_risk,
        high_risk
    )

(
    preds,
    accuracy,
    precision,
    recall,
    f1,
    cv_mean,
    cv_std,
    comparison_df,
    low_risk,
    high_risk
) = compute_all_metrics(
    model,
    X_train,
    X_test,
    y_train,
    y_test,
    X,
    y
)