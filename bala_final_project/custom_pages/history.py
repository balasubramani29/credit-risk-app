import streamlit as st
import pandas as pd
from components.db_auth import (
    load_prediction_history,
    clear_prediction_history
)


def show_history():

    st.subheader("Prediction History")

    # Load from database permanently
    db_history = load_prediction_history(
        st.session_state.user_name
    )

    # Merge with current session history
    all_records = list(db_history)

    if len(all_records) == 0:

        st.info(
            "No prediction history available. "
            "Make a prediction to see results here."
        )

    else:

        hist_df = pd.DataFrame(all_records)

        st.dataframe(
            hist_df,
            width='stretch',
            height=500
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            csv = hist_df.to_csv(index=False)

            st.download_button(
                "Download History",
                csv,
                "prediction_history.csv",
                "text/csv",
                use_container_width=True
            )

        with col2:

            if st.button(
                "Clear History",
                use_container_width=True
            ):

                clear_prediction_history(
                    st.session_state.user_name
                )

                st.success(
                    "History cleared successfully."
                )

                st.rerun()