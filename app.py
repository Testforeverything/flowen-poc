# app.py
import streamlit as st
from PIL import Image

# ─── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Flowen AI Dashboard", layout="wide")

# ─── Sidebar Logo and Menu ─────────────────────────────────────────────────────
with st.sidebar:
    logo = Image.open("assets/flowen_logo.png")
    st.image(logo, width=200)

    st.markdown("## 📊 Dashboard Menu")
    page = st.radio(
        "เลือกหน้า / Select Page",
        ["🏠 Home", "📈 Risk Overview", "🧭 Journey Management", "📉 Recovery KPI", "🧠 Behavioral Insights"],
        label_visibility="collapsed"
    )

# ─── Language Toggle & Notification (Top Right) ────────────────────────────────
lang = st.sidebar.selectbox("🌐 Language", ["🇬🇧 English", "🇹🇭 ภาษาไทย"])
st.session_state["lang"] = lang

st.markdown(f"<div style='text-align:right; color:green; font-weight:bold;'>🔔 Notification Center: All systems operational</div>", unsafe_allow_html=True)

# ─── Page Router ───────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.title("🌟 Flowen AI Debt Collection Platform")
    st.markdown("""
        Welcome to **Flowen** — your AI-powered debt recovery assistant.<br>
        Use the menu on the left to navigate through modules.
    """, unsafe_allow_html=True)

elif page == "📈 Risk Overview":
    from pages import page1_risk_overview
    page1_risk_overview.show()

elif page == "🧭 Journey Management":
    from pages import page2_journey_management
    page2_journey_management.show()

elif page == "📉 Recovery KPI":
    from pages import page3_recovery_kpi
    page3_recovery_kpi.show()

elif page == "🧠 Behavioral Insights":
    from pages import page4_behavioral_insights
    page4_behavioral_insights.show()
