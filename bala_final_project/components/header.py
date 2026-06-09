import streamlit as st


def show_header():

    st.markdown("""
    <div style='padding:25px 0 10px 0'>

    <h1 class='main-title'>
    💳 Credit Risk Intelligence Dashboard
    </h1>

    <p style='color:#DDE6F2;font-size:18px;'>
    Interpretable Machine Learning Platform
    for Credit Risk Analysis
    </p>

    </div>
    """, unsafe_allow_html=True)

    