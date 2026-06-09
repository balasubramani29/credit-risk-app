import streamlit as st


def show_about():

    st.markdown("""
    <div class='section-card'>

    <h1 style='font-size:44px;
    font-weight:800;
    margin-bottom:20px;
    color:#60a5fa;'>
    🧠 CreditIQ — AI Credit Risk Intelligence Platform
    </h1>

    <p style='color:#DDE6F2;
    font-size:21px;
    line-height:1.9;
    text-align:justify;'>
    <b>CreditIQ</b> is an advanced AI-powered credit risk
    intelligence platform developed for modern financial
    institutions and supply chain finance ecosystems.
    The system is designed to evaluate applicant creditworthiness
    using interpretable machine learning and Explainable AI (XAI) techniques that improve
    transparency, prediction accuracy, and financial decision-making.
    This project focuses on solving one of the major challenges
    in financial technology:
    <b>accurate and transparent credit risk evaluation.</b>
    Traditional credit assessment systems often rely on manual
    analysis and static scoring models that lack interpretability
    and intelligent automation. CreditIQ overcomes these limitations
    by integrating machine learning algorithms with interactive
    analytics and real-time prediction systems.
    </p>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    🎯 Project Title
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.8;'>
    <b>A Transparent Machine Learning Model for
    Credit Risk Evaluation in Supply Chain Finance</b>
    </p>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    👨‍💻 Project Developed By
    </h2>

    <ul style='list-style:none;
    padding-left:0;
    font-size:20px;
    color:#E8EDF7;
    line-height:2.2;'>
    <li>👤 Aman H</li>
    <li>👤 Anbudaiya Balan R</li>
    <li>👤 Balaji Kumar Thapa L</li>
    <li>👤 Balasubramani L</li>
    </ul>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    📌 Problem Statement
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.9;text-align:justify;'>
    Existing credit risk systems in supply chain finance
    suffer from limited transparency, delayed processing,
    manual dependency, and poor interpretability of predictions.
    Financial organizations require intelligent systems capable
    of evaluating customer financial behavior quickly and accurately
    while also providing explainable results for decision-makers.
    </p>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    🚀 Proposed System
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.9;text-align:justify;'>
    The proposed system introduces an interpretable machine learning
    framework using the Random Forest algorithm for intelligent
    credit risk prediction. The platform provides:
    </p>

    <ul style='line-height:2.2;font-size:19px;color:#E8EDF7;'>
    <li>Real-time credit risk prediction</li>
    <li>Transparent and explainable AI-based decision analysis</li>
    <li>Interactive dashboard visualization</li>
    <li>Automated applicant risk classification</li>
    <li>Prediction history management</li>
    <li>Feature importance analytics</li>
    <li>Intelligent financial behavior analysis</li>
    <li>Improved prediction accuracy using machine learning</li>
    </ul>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    🤖 Machine Learning Model
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.9;text-align:justify;'>
    The system uses the <b>Random Forest Classifier</b>,
    an ensemble machine learning algorithm known for its
    high accuracy, robustness, and interpretability.
    The model uses 5-fold cross validation to ensure
    consistent performance and prevent overfitting.
    It also accounts for the dataset's natural class imbalance
    (79.5% Low Risk vs 20.5% High Risk) by evaluating using
    the ROC-AUC metric — which remains reliable on imbalanced data,
    unlike simple accuracy alone.
    The model analyzes multiple financial parameters such as:
    </p>

    <ul style='line-height:2.2;font-size:19px;color:#E8EDF7;'>
    <li>Loan Amount</li>
    <li>Income Level</li>
    <li>Employment Experience</li>
    <li>Home Ownership Status</li>
    <li>Credit History Length</li>
    <li>Loan Intent</li>
    <li>Historical Defaults</li>
    <li>Interest Rate</li>
    </ul>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    📊 System Modules
    </h2>

    <ul style='line-height:2.2;font-size:19px;color:#E8EDF7;'>
    <li>Secure Login & Registration Module</li>
    <li>Intelligent Dashboard Analytics</li>
    <li>Real-Time Prediction Module with SHAP & LIME Explainability</li>
    <li>Prediction History Management</li>
    <li>Dataset Exploration Module</li>
    <li>Model Performance Analytics with ROC & Cross Validation</li>
    <li>Interactive Visualization System</li>
    <li>What-If Risk Simulator</li>
    <li>Batch CSV Prediction Module</li>
    </ul>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    🛠 Technologies Used
    </h2>

    <ul style='line-height:2.2;font-size:19px;color:#E8EDF7;'>
    <li>Python</li>
    <li>Streamlit</li>
    <li>Scikit-Learn</li>
    <li>SHAP — Global Explainable AI Library</li>
    <li>LIME — Local Explainable AI Library</li>
    <li>Plotly Interactive Charts</li>
    <li>Pandas & NumPy</li>
    <li>Advanced CSS Styling</li>
    <li>Machine Learning Algorithms</li>
    </ul>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    🎓 Academic Contribution
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.9;text-align:justify;'>
    This project demonstrates how interpretable artificial
    intelligence can improve financial risk management systems.
    The platform enhances transparency, automation,
    and decision accuracy in supply chain finance while
    providing a user-friendly enterprise dashboard
    for intelligent credit evaluation.
    The system goes beyond traditional base paper approaches
    by integrating SHAP and LIME explainability techniques, cross-validation,
    ROC-AUC evaluation, multi-model comparison, and
    a live What-If risk simulator — features absent
    in most existing credit risk research implementations.
    </p>

    <br>

    <h2 style='color:#22d3ee;font-weight:700;font-size:28px;'>
    ✅ Conclusion
    </h2>

    <p style='font-size:20px;color:#E8EDF7;line-height:1.9;text-align:justify;'>
    CreditIQ successfully combines machine learning,
    financial analytics, and interactive visualization
    to create a modern intelligent credit risk evaluation system.
    The proposed solution improves efficiency,
    transparency, and prediction capability compared
    to traditional financial risk assessment systems,
    while delivering a fully deployable web application
    suitable for real-world financial decision support.
    </p>

    </div>
    """, unsafe_allow_html=True)
    
    