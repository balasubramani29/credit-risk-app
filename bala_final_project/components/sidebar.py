import streamlit as st
from streamlit_option_menu import option_menu


def show_sidebar():

    with st.sidebar:

        st.markdown(
            "## 🧠 CreditIQ"
        )

        st.markdown(
            f"Welcome **{st.session_state.user_name}**"
        )

        selected = option_menu(
            menu_title=None,

            options=[
                "Dashboard",
                "Prediction",
                "History",
                "Dataset",
                "Model Analytics",
                "About"
            ],

            icons=[
                "bar-chart",
                "activity",
                "clock-history",
                "database",
                "cpu",
                "info-circle"
            ],

            default_index=0
        )

        st.markdown("---")

        if st.button("Logout", use_container_width=True):

            st.session_state.logged_in = False

            st.rerun()

    return selected

    