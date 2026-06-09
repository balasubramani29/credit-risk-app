import streamlit as st
import pandas as pd
import plotly.express as px


LEGEND_STYLE = dict(
    font=dict(color='#e2e8f0', size=13),
    bgcolor='rgba(0,0,0,0)',
    bordercolor='rgba(255,255,255,0.1)',
    borderwidth=1
)


def show_dashboard(
    accuracy,
    low_risk,
    high_risk,
    data,
    model,
    X
):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Model Accuracy</div>
        <div class='metric-value'>{accuracy:.2%}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Low Risk</div>
        <div class='metric-value'>{low_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>High Risk</div>
        <div class='metric-value'>{high_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Dataset Size</div>
        <div class='metric-value'>{len(data)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # =====================================================
    # RISK DISTRIBUTION PIE
    # =====================================================
    with c1:

        risk_df = pd.DataFrame({
            "Risk":  ["Low Risk", "High Risk"],
            "Count": [low_risk,   high_risk]
        })

        fig = px.pie(
            risk_df,
            names="Risk",
            values="Count",
            hole=0.5,
            template="plotly_dark",
            color="Risk",
            color_discrete_map={
                "Low Risk":  "#3b82f6",
                "High Risk": "#ef4444"
            }
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=LEGEND_STYLE
        )

        fig.update_traces(
            textfont_color='white',
            textfont_size=14
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # FEATURE IMPORTANCE BAR
    # =====================================================
    with c2:

        importances = model.feature_importances_

        imp_df = pd.DataFrame({
            "Feature":    X.columns,
            "Importance": importances
        }).sort_values(
            by="Importance",
            ascending=False
        ).head(10)

        fig2 = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation='h',
            template="plotly_dark"
        )

        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis=dict(
                tickfont=dict(color='#e2e8f0', size=12)
            ),
            xaxis=dict(
                tickfont=dict(color='#e2e8f0', size=12)
            )
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    d1, d2 = st.columns(2)

    # =====================================================
    # LOAN INTENT DISTRIBUTION
    # =====================================================
    with d1:

        if "loan_intent" in data.columns:

            intent_df = (
                data["loan_intent"]
                .value_counts()
                .reset_index()
            )

            intent_df.columns = ["Loan Intent", "Count"]

            fig3 = px.bar(
                intent_df,
                x="Loan Intent",
                y="Count",
                template="plotly_dark",
                color="Loan Intent",
                title="Loan Intent Distribution"
            )

            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                title_font=dict(color='#e2e8f0', size=15),
                xaxis=dict(
                    tickfont=dict(color='#e2e8f0', size=11),
                    title_font=dict(color='#e2e8f0')
                ),
                yaxis=dict(
                    tickfont=dict(color='#e2e8f0', size=11),
                    title_font=dict(color='#e2e8f0')
                )
            )

            st.plotly_chart(fig3, use_container_width=True)

    # =====================================================
    # HOME OWNERSHIP PIE
    # =====================================================
    with d2:

        if "person_home_ownership" in data.columns:

            own_df = (
                data["person_home_ownership"]
                .value_counts()
                .reset_index()
            )

            own_df.columns = ["Ownership", "Count"]

            fig4 = px.pie(
                own_df,
                names="Ownership",
                values="Count",
                hole=0.4,
                template="plotly_dark",
                title="Home Ownership Distribution"
            )

            fig4.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(color='#e2e8f0', size=15),
                legend=LEGEND_STYLE
            )

            fig4.update_traces(
                textfont_color='white',
                textfont_size=13
            )

            st.plotly_chart(fig4, use_container_width=True)
            
            