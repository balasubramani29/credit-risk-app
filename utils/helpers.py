import streamlit as st

def load_css(path):
    with open(path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )