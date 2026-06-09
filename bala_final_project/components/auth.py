import streamlit as st
import re

from components.pass_check import (
    is_strong_password,
    hash_password,
    verify_password
)

from components.db_auth import (
    register_user,
    login_user
)


# =========================================================
# EMAIL VALIDATION
# =========================================================
def _is_valid_email(email: str) -> bool:

    return bool(
        re.match(r"[^@]+@[^@]+\.[^@]+", email)
    )


# =========================================================
# AUTH PAGE
# =========================================================
def auth_page():

    # =====================================================
    # SESSION STATES
    # =====================================================
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    # =====================================================
    # MAIN LAYOUT
    # =====================================================
    left, right = st.columns([1.08, 0.92], gap="medium")

    # =====================================================
    # LEFT PANEL
    # =====================================================
    with left:

        html_content = """<div class="ultra-brand-panel">
<div class="floating-circle one"></div>
<div class="floating-circle two"></div>
<div class="floating-circle three"></div>
<div class="brand-content">
<div class="brand-badge">AI Powered Credit Intelligence</div>
<div class="brand-title">CreditIQ</div>
<div class="brand-headline">Transparent Machine Learning<br>for Credit Risk Analysis</div>
<div class="brand-description">Advanced AI-driven platform for supply chain finance,
intelligent credit evaluation, explainable analytics,
and real-time financial risk prediction.</div>
<div class="feature-list">
<div class="feature-item">✦ Explainable AI Predictions</div>
<div class="feature-item">✦ Real-time Risk Analytics</div>
<div class="feature-item">✦ Secure Financial Intelligence</div>
<div class="feature-item">✦ Random Forest ML Engine</div>
<div class="feature-item">✦ Interactive Financial Dashboard</div>
</div>
</div>
</div>"""

        st.markdown(html_content, unsafe_allow_html=True)

    # =====================================================
    # RIGHT PANEL
    # =====================================================
    with right:

        if st.session_state.auth_mode == "login":
            _login_form()

        else:
            _register_form()


# =========================================================
# LOGIN FORM
# =========================================================
def _login_form():

    st.markdown("""
    <div class="auth-header-title">
        Welcome Back
    </div>
    <div class="auth-header-tagline">
        Sign in to continue to CreditIQ
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):

        email = st.text_input(
            "Email Address",
            placeholder="you@company.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        submit = st.form_submit_button("Sign In")

        if submit:

            email = email.strip()

            if not email or not password:
                st.warning("Please fill in all fields.")

            else:

                user = login_user(email)

                if user:

                    name, hashed_password = user

                    if verify_password(password, hashed_password):

                        st.session_state.logged_in = True
                        st.session_state.user_name = name
                        st.rerun()

                    else:
                        st.error("Incorrect password.")

                else:
                    st.error("Account not found.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;
              color:#94a3b8;
              font-size:0.85rem;'>
    Don't have an account?
    </p>
    """, unsafe_allow_html=True)

    if st.button(
        "Create Free Account",
        key="go_register",
        use_container_width=True
    ):
        st.session_state.auth_mode = "register"
        st.rerun()

    st.markdown("""
    <p style='text-align:center;
              color:#64748b;
              font-size:0.78rem;
              margin-top:1.5rem;'>
    Demo Login · admin@creditiq.com / Admin@123
    </p>
    """, unsafe_allow_html=True)


# =========================================================
# REGISTER FORM
# =========================================================
def _register_form():

    st.markdown("""
    <div class="auth-header-title">
        Create Account
    </div>
    <div class="auth-header-tagline">
        Get started with CreditIQ today
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=True):

        name = st.text_input(
            "Full Name",
            placeholder="Your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="you@company.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Strong password required"
        )

        st.markdown("""
        <p style='color:#94a3b8;
                  font-size:0.78rem;
                  margin-top:0.3rem;'>
        Password must contain uppercase,
        lowercase, number and special character.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        submit = st.form_submit_button("Create Account")

        if submit:

            name  = name.strip()
            email = email.strip()

            if not name or not email or not password:
                st.warning("Please fill in all fields.")

            elif not _is_valid_email(email):
                st.warning("Please enter a valid email.")

            elif not is_strong_password(password):
                st.error(
                    "Weak password. "
                    "Use uppercase, lowercase, "
                    "number and special character."
                )

            else:

                hashed_password = hash_password(password)
                success = register_user(name, email, hashed_password)

                if success:
                    st.success("Account created successfully!")
                    st.session_state.auth_mode = "login"
                    st.rerun()

                else:
                    st.error("Account already exists.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;
              color:#94a3b8;
              font-size:0.85rem;'>
    Already have an account?
    </p>
    """, unsafe_allow_html=True)

    if st.button(
        "Back to Sign In",
        key="go_login",
        use_container_width=True
    ):
        st.session_state.auth_mode = "login"
        st.rerun()