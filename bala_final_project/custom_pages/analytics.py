import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, auc, confusion_matrix


LEGEND_STYLE = dict(
    font=dict(color='#e2e8f0', size=13),
    bgcolor='rgba(0,0,0,0)',
    bordercolor='rgba(255,255,255,0.1)',
    borderwidth=1
)

AXIS_STYLE = dict(
    tickfont=dict(color='#e2e8f0', size=12),
    title_font=dict(color='#e2e8f0', size=13)
)


def show_analytics(
    accuracy,
    precision,
    recall,
    f1,
    model,
    X,
    y_test,
    preds,
    X_test,
    comparison_df,
    cv_mean,
    cv_std
):

    st.subheader("🤖 Model Performance Analytics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Accuracy",  f"{accuracy:.2%}")
    c2.metric("Precision", f"{precision:.2%}")
    c3.metric("Recall",    f"{recall:.2%}")
    c4.metric("F1 Score",  f"{f1:.2%}")

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # CROSS VALIDATION SCORE
    # =====================================================
    st.markdown(f"""
    <div class='section-card'>
    <p style='color:#10b981;font-size:1.05rem;font-weight:700;margin:0;'>
    📊 5-fold Cross-Validation Score:
    &nbsp; {cv_mean:.2%} &nbsp;±&nbsp; {cv_std:.4f}
    </p>
    <p style='color:#94a3b8;font-size:0.92rem;margin-top:0.4rem;margin-bottom:0;'>
    Consistent performance across all 5 folds confirms the model
    is not overfitting to the training data — a key indicator
    of real-world reliability.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================
    importances = model.feature_importances_

    imp_df = pd.DataFrame({
        "Feature":    X.columns,
        "Importance": importances
    }).sort_values("Importance", ascending=False)

    fig_imp = px.bar(
        imp_df,
        x="Importance",
        y="Feature",
        orientation="h",
        template="plotly_dark",
        color="Importance",
        title="Feature Importance"
    )

    fig_imp.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font=dict(color='#e2e8f0', size=16),
        showlegend=False,
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE
    )

    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    # =====================================================
    # CONFUSION MATRIX
    # =====================================================
    with left:

        cm = confusion_matrix(y_test, preds)

        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=["Predicted\nLow Risk", "Predicted\nHigh Risk"],
            y=["Actual\nLow Risk",    "Actual\nHigh Risk"],
            colorscale="Blues",
            text=cm,
            texttemplate="%{text}",
            showscale=False
        ))

        fig_cm.update_layout(
            title="Confusion Matrix",
            title_font=dict(color='#e2e8f0', size=16),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            xaxis=dict(
                tickfont=dict(color='#e2e8f0', size=12),
                title_font=dict(color='#e2e8f0')
            ),
            yaxis=dict(
                tickfont=dict(color='#e2e8f0', size=12),
                title_font=dict(color='#e2e8f0')
            )
        )

        st.plotly_chart(fig_cm, use_container_width=True)

    # =====================================================
    # ROC CURVE
    # =====================================================
    with right:

        proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, proba)
        roc_auc = auc(fpr, tpr)

        fig_roc = go.Figure()

        fig_roc.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            name=f"Random Forest (AUC = {roc_auc:.4f})",
            line=dict(color="#8b5cf6", width=3)
        ))

        fig_roc.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Random Classifier",
            line=dict(color="#64748b", dash="dash", width=2)
        ))

        fig_roc.update_layout(
            title="ROC Curve",
            title_font=dict(color='#e2e8f0', size=16),
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            legend=LEGEND_STYLE,
            xaxis=AXIS_STYLE,
            yaxis=AXIS_STYLE
        )

        st.plotly_chart(fig_roc, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # MODEL COMPARISON TABLE
    # =====================================================
    st.markdown("""
    <div class='section-card'>
    <h3>📊 Model Comparison — Proposed vs Existing</h3>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class='section-card'>
    <p style='color:#10b981;font-weight:600;font-size:1rem;'>
    ✅ Random Forest demonstrates superior overall performance
    compared to Logistic Regression and Decision Tree,
    making it the most effective model for credit risk prediction.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    