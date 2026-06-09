import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import shap
from datetime import datetime


def show_prediction(
    data,
    encoders,
    model,
    X_test
):

    st.subheader(
        "🎯 Real-Time Credit Risk Prediction"
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:

        inputs = {}

        label_map = {
            "person_income": "person_annual_income"
        }

        SKIP_COLS = {"loan_status", "loan_percent_income"}

        for col in data.columns:

            if col in SKIP_COLS:
                inputs[col] = float(data[col].mean())
                continue

            display_label = label_map.get(col, col)

            if data[col].dtype == "object":

                inputs[col] = st.selectbox(
                    display_label,
                    data[col].unique()
                )

            elif col == "loan_amnt":

                inputs[col] = st.number_input(
                    display_label,
                    0.0,
                    10000000.0,
                    float(data[col].mean())
                )

            else:

                inputs[col] = st.number_input(
                    display_label,
                    float(data[col].min()),
                    float(data[col].max()),
                    float(data[col].mean())
                )

        input_df = pd.DataFrame([inputs])

    with col2:

        st.markdown("""
        <div class='section-card'>
        <h3>🧠 AI Risk Engine</h3>
        <p style='color:#DDE6F2'>
        The interpretable machine learning model
        analyzes customer financial behavior and
        predicts credit risk probability with
        intelligent decision analytics.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # PREPARE INPUT
    # =====================================================
    test = input_df.copy()

    test = test.drop(
        columns=[
            c for c in ["loan_status"]
            if c in test.columns
        ]
    )

    for col in test.columns:
        if col in encoders:
            test[col] = encoders[col].transform(test[col])

    # =====================================================
    # PREDICT BUTTON
    # =====================================================
    if st.button("Analyze Credit Risk"):

        pred       = model.predict(test)[0]
        prob       = model.predict_proba(test)[0][1]
        risk_score = prob * 100

        record = inputs.copy()
        record["Risk Score"]  = f"{risk_score:.2f}%"
        record["Prediction"]  = "High Risk" if pred == 1 else "Low Risk"
        record["User"]        = st.session_state.user_name
        record["Timestamp"]   = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        st.session_state.history.append(record)

        from components.db_auth import save_prediction_record
        save_prediction_record(
            user=st.session_state.user_name,
            timestamp=record["Timestamp"],
            record=record
        )

        st.markdown("<br>", unsafe_allow_html=True)

        r1, r2 = st.columns([1, 1])

        # -------------------------------------------------
        # LEFT — GAUGE CHART
        # -------------------------------------------------
        with r1:

            if pred == 1:
                st.error(f"⚠ HIGH RISK : {risk_score:.2f}%")
            else:
                st.success(
                    f"✅ LOW RISK : {(100 - risk_score):.2f}%"
                )

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={'text': "Risk Probability"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar':  {'color': "#ef4444"},
                    'steps': [
                        {'range': [0,  40],  'color': "#10b981"},
                        {'range': [40, 70],  'color': "#f59e0b"},
                        {'range': [70, 100], 'color': "#ef4444"}
                    ]
                }
            ))

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------------------------
        # RIGHT — AI DECISION ANALYSIS
        # -------------------------------------------------
        with r2:

            st.markdown("""
            <div class='section-card'>
            <h3>📌 AI Decision Analysis</h3>
            <p style='color:#DDE6F2;'>
            The model prediction is based on:
            </p>
            <ul>
            <li>Loan Amount</li>
            <li>Credit History</li>
            <li>Income Stability</li>
            <li>Employment Length</li>
            <li>Interest Rate</li>
            <li>Historical Defaults</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------
        # FULL WIDTH — SHAP CHART
        # -------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class='section-card'>
        <h3>🔍 SHAP — Global Feature Explanation</h3>
        <p style='color:#DDE6F2;'>
        SHAP explains which features had the most impact
        on this prediction and in which direction —
        toward High Risk or Low Risk.
        </p>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Generating SHAP explanation..."):

            explainer   = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(test)

            n_features = len(test.columns)
            shap_arr   = np.array(shap_values)

            if isinstance(shap_values, list):
                shap_vals = np.array(shap_values[1][0]).flatten()

            elif shap_arr.ndim == 3 and shap_arr.shape[-1] == 2:
                shap_vals = shap_arr[0, :, 1].flatten()

            elif shap_arr.ndim == 3 and shap_arr.shape[0] == 2:
                shap_vals = shap_arr[1, 0, :].flatten()

            elif shap_arr.ndim == 2:
                shap_vals = shap_arr[0, :].flatten()

            else:
                shap_vals = shap_arr.flatten()

            shap_vals = shap_vals[:n_features]

            shap_df = pd.DataFrame({
                "Feature":    test.columns.tolist(),
                "SHAP Value": shap_vals.tolist()
            }).sort_values("SHAP Value", key=abs, ascending=True)

            colors = [
                "#ef4444" if v > 0 else "#10b981"
                for v in shap_df["SHAP Value"]
            ]

            fig_shap = go.Figure(go.Bar(
                x=shap_df["SHAP Value"],
                y=shap_df["Feature"],
                orientation="h",
                marker_color=colors
            ))

            fig_shap.update_layout(
                title="SHAP Feature Impact — What drove this prediction?",
                xaxis_title="Impact on Prediction",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=500
            )

            st.plotly_chart(fig_shap, use_container_width=True)

            st.markdown("""
            <p style='color:#94a3b8;font-size:0.88rem;'>
            🔴 Red = pushes toward High Risk &nbsp;|&nbsp;
            🟢 Green = pushes toward Low Risk
            </p>
            """, unsafe_allow_html=True)

        # -------------------------------------------------
        # LIME EXPLANATION
        # -------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class='section-card'>
        <h3>🧪 LIME — Local Prediction Explanation</h3>
        <p style='color:#DDE6F2;'>
        LIME explains this individual prediction by showing
        which features pushed the decision toward
        High Risk or Low Risk locally.
        </p>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Generating LIME explanation..."):

            try:

                import lime
                import lime.lime_tabular

                lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                    training_data=X_test.values,
                    feature_names=test.columns.tolist(),
                    class_names=["Low Risk", "High Risk"],
                    mode="classification"
                )

                lime_exp = lime_explainer.explain_instance(
                    data_row=test.values[0],
                    predict_fn=model.predict_proba,
                    num_features=10
                )

                lime_list = lime_exp.as_list()

                lime_df = pd.DataFrame(
                    lime_list,
                    columns=["Feature Condition", "Impact"]
                ).sort_values("Impact", ascending=True)

                lime_colors = [
                    "#ef4444" if v > 0 else "#10b981"
                    for v in lime_df["Impact"]
                ]

                fig_lime = go.Figure(go.Bar(
                    x=lime_df["Impact"],
                    y=lime_df["Feature Condition"],
                    orientation="h",
                    marker_color=lime_colors
                ))

                fig_lime.update_layout(
                    title="LIME Local Feature Contributions",
                    xaxis_title="Local Impact on Prediction",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=450
                )

                st.plotly_chart(
                    fig_lime,
                    use_container_width=True
                )

                st.markdown("""
                <p style='color:#94a3b8;font-size:0.88rem;'>
                🔴 Red = pushes toward High Risk &nbsp;|&nbsp;
                🟢 Green = pushes toward Low Risk &nbsp;|&nbsp;
                LIME analyses this specific prediction locally.
                </p>
                """, unsafe_allow_html=True)

            except Exception as e:

                st.warning(
                    f"LIME explanation unavailable: {str(e)}"
                )

    # =====================================================
    # WHAT-IF SIMULATOR
    # =====================================================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    <h3>🔬 What-If Risk Simulator</h3>
    <p style='color:#DDE6F2;'>
    Adjust the sliders below — the risk result
    updates instantly using your trained
    Random Forest model.
    </p>
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3 = st.columns(3)

    with w1:
        sim_income = st.slider(
            "Annual Income",
            10000, 200000,
            int(data["person_income"].mean()),
            step=1000
        )
        sim_loan = st.slider(
            "Loan Amount",
            500, 50000,
            int(data["loan_amnt"].mean()),
            step=500
        )

    with w2:
        sim_rate = st.slider(
            "Interest Rate (%)",
            5.0, 30.0,
            float(data["loan_int_rate"].mean()),
            step=0.5
        )
        sim_emp = st.slider(
            "Employment Length (years)",
            0, 40,
            int(data["person_emp_length"].mean())
        )

    with w3:
        sim_hist = st.slider(
            "Credit History Length (years)",
            0, 30,
            int(data["cb_person_cred_hist_length"].mean())
        )
        sim_percent = st.slider(
            "Loan % of Income",
            0.01, 0.99,
            float(data["loan_percent_income"].mean()),
            step=0.01
        )

    sim_input = input_df.copy()
    sim_input["person_income"]              = sim_income
    sim_input["loan_amnt"]                  = sim_loan
    sim_input["loan_int_rate"]              = sim_rate
    sim_input["person_emp_length"]          = sim_emp
    sim_input["cb_person_cred_hist_length"] = sim_hist
    sim_input["loan_percent_income"]        = sim_percent

    sim_test = sim_input.copy()
    sim_test = sim_test.drop(
        columns=[
            c for c in ["loan_status"]
            if c in sim_test.columns
        ]
    )

    for col in sim_test.columns:
        if col in encoders:
            sim_test[col] = encoders[col].transform(
                sim_test[col]
            )

    sim_prob = model.predict_proba(sim_test)[0][1] * 100
    sim_pred = model.predict(sim_test)[0]

    st.markdown("<br>", unsafe_allow_html=True)

    if sim_pred == 1:
        st.error(
            f"⚠ Simulated Result: HIGH RISK "
            f"— {sim_prob:.2f}% probability"
        )
    else:
        st.success(
            f"✅ Simulated Result: LOW RISK "
            f"— {(100 - sim_prob):.2f}% safe score"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # BATCH CSV PREDICTION
    # =====================================================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    <h3>📂 Batch Prediction — Upload CSV</h3>
    <p style='color:#DDE6F2;'>
    Upload a CSV file with multiple applicants
    to predict credit risk for all at once.
    </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload applicant CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        batch_df = pd.read_csv(uploaded_file)

        # ─── Required columns ────────────────────────────
        REQUIRED_COLS = [
            'person_age',
            'person_income',
            'person_home_ownership',
            'person_emp_length',
            'loan_intent',
            'loan_grade',
            'loan_amnt',
            'loan_int_rate',
            'cb_person_default_on_file',
            'cb_person_cred_hist_length'
        ]

        # ─── Validate columns ────────────────────────────
        missing_cols = [
            c for c in REQUIRED_COLS
            if c not in batch_df.columns
        ]

        if missing_cols:

            st.error(
                "Your CSV has wrong column names. "
                "Please use the exact column names below."
            )

            st.markdown("""
            <div class='section-card'>
            <h3>Required CSV Column Names</h3>
            <p style='color:#DDE6F2;'>
            Your CSV file must have exactly these column names:
            </p>
            </div>
            """, unsafe_allow_html=True)

            st.code(
                "person_age\n"
                "person_income\n"
                "person_home_ownership\n"
                "person_emp_length\n"
                "loan_intent\n"
                "loan_grade\n"
                "loan_amnt\n"
                "loan_int_rate\n"
                "cb_person_default_on_file\n"
                "cb_person_cred_hist_length"
            )

            st.markdown("""
            <div class='section-card'>
            <p style='color:#f59e0b;font-weight:600;'>
            Download the sample CSV below,
            fill your data and upload again.
            </p>
            </div>
            """, unsafe_allow_html=True)

            # Provide sample CSV for download
            sample_data = pd.DataFrame([{
                'person_age': 25,
                'person_income': 50000,
                'person_home_ownership': 'RENT',
                'person_emp_length': 3,
                'loan_intent': 'PERSONAL',
                'loan_grade': 'B',
                'loan_amnt': 10000,
                'loan_int_rate': 11.5,
                'cb_person_default_on_file': 'N',
                'cb_person_cred_hist_length': 3
            }])

            st.download_button(
                label="⬇ Download Sample CSV Template",
                data=sample_data.to_csv(index=False).encode("utf-8"),
                file_name="creditiq_sample_template.csv",
                mime="text/csv"
            )

        else:

            st.markdown("**Preview of uploaded data:**")
            st.dataframe(batch_df.head(), use_container_width=True)

            batch_processed = batch_df.copy()

            if "loan_status" in batch_processed.columns:
                batch_processed = batch_processed.drop(
                    columns=["loan_status"]
                )

            if "loan_percent_income" not in batch_processed.columns:
                if (
                    "loan_amnt"     in batch_processed.columns and
                    "person_income" in batch_processed.columns
                ):
                    batch_processed["loan_percent_income"] = (
                        batch_processed["loan_amnt"] /
                        batch_processed["person_income"]
                    )

            for col in batch_processed.columns:
                if col in encoders:
                    batch_processed[col] = encoders[col].transform(
                        batch_processed[col]
                    )

            with st.spinner("Running predictions..."):

                batch_processed = batch_processed[
                    model.feature_names_in_
                ]

                batch_preds = model.predict(batch_processed)
                batch_proba = (
                    model.predict_proba(batch_processed)[:, 1] * 100
                )

            batch_df["Risk Score (%)"] = batch_proba.round(2)
            batch_df["Prediction"]     = [
                "High Risk" if p == 1 else "Low Risk"
                for p in batch_preds
            ]

            st.markdown("**Prediction Results:**")
            st.dataframe(batch_df, use_container_width=True)

            csv_output = batch_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇ Download Results CSV",
                data=csv_output,
                file_name="creditiq_batch_results.csv",
                mime="text/csv"
            )
        
        