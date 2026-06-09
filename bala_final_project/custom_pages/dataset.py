import streamlit as st


def show_dataset(data):

    st.subheader("🗄 Dataset Explorer")

    st.dataframe(
        data,
        use_container_width=True,
        height=650
    )