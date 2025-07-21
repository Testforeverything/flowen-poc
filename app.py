import streamlit as st
from datetime import datetime

# ---------------------- CONFIG ------------------------
st.set_page_config(page_title="Flowen AI Debt Collection", layout="wide")

# ---------------------- SESSION ------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "🇬🇧 EN"

lang = st.session_state.lang

# ---------------------- UI ------------------------
st.markdown("""
    <style>
    .main-title {font-size: 3em; font-weight: bold; margin-bottom: 0.2em;}
    .subtitle {font-size: 1.3em; color: #555; margin-bottom: 2em;}
    .section-card {
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 2em;
        background-color: #ffffff;
        margin-bottom: 1.5em;
    }
    .lang-toggle {
        position: absolute;
        top: 10px;
        right: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ------------------------
st.image("assets/flowen_logo.png", width=180)
st.markdown(f"<div class='lang-toggle'>🌐 {lang}</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>Flowen: AI Debt Collection Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your intelligent partner for predicting, managing, and recovering debt with next-generation AI.</div>", unsafe_allow_html=True)

# ---------------------- DASHBOARD MODULE LINKS ------------------------
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class='section-card'>
        <h3>📊 Risk Overview</h3>
        <p>Analyze debt risk distribution by score, segment, and loan type.</p>
        <a href="/Risk_Overview" target="_self">Go to Dashboard ➜</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
        <h3>📈 Recovery KPI</h3>
        <p>Monitor channel-wise recovery effectiveness & team performance.</p>
        <a href="/Recovery_KPI" target="_self">Go to Dashboard ➜</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='section-card'>
        <h3>🧭 Journey Management</h3>
        <p>Manage, simulate, and optimize contact strategies by AI Journey Engine.</p>
        <a href="/Journey_Management" target="_self">Go to Dashboard ➜</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
        <h3>🧠 Behavioral Insights</h3>
        <p>Understand debtor behavior, clusters, and actionable insights.</p>
        <a href="/Behavioral_Insights" target="_self">Go to Dashboard ➜</a>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- NOTIFICATION BANNER ------------------------
with st.expander("🔔 Notification Center", expanded=True):
    st.markdown("""
    - [12:01] Debtor ID #10823 has skipped 2 consecutive payments.
    - [12:03] AI recommends escalation for cluster C3 in Northern region.
    - [12:06] Voice Bot engaged with 58 debtors today.
    """)

# ---------------------- FOOTER ------------------------
st.markdown("---")
st.caption(f"© {datetime.now().year} Flowen AI Platform. All rights reserved.")
