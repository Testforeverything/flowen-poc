# app.py
import streamlit as st
from PIL import Image
from io import BytesIO
import base64

# ─── Page Config ─────────────────────────────
st.set_page_config(page_title="Flowen: Debt Intelligence Platform", layout="wide")

# ─── Load Logo as Base64 ─────────────────────
def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# ─── Language Toggle (🇬🇧 / 🇹🇭) ───────────────
lang = st.selectbox("🌐 Language / ภาษา", options=["🇬🇧 English", "🇹🇭 ไทย"], index=0)

# ─── Realtime Alert ──────────────────────────
st.markdown(
    """
    <div style='background-color:#ffeaa7;padding:10px;border-radius:8px;border-left:5px solid #fdcb6e'>
        🔔 <b>System Notice:</b> New accounts with High Risk are being added. Review Risk Overview now.
    </div>
    """, unsafe_allow_html=True
)

# ─── Custom Style ─────────────────────────────
st.markdown(f"""
<style>
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F6F8FA;
    }}
    .main-container {{
        padding-top: 20px;
    }}
</style>
<div style='text-align:left; padding:20px 0 10px 0;'>
    <img src='data:image/png;base64,{logo_base64}' width='180'/>
</div>
""", unsafe_allow_html=True)

# ─── Landing Content ─────────────────────────
st.title("📊 Flowen: Debt Intelligence Platform")
st.subheader("AI-Powered Dashboard for Recovery Strategy & Debtor Insights")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 What can you do?")
    st.markdown("""
    - 📌 Monitor real-time debt risk and recovery rates
    - 🧭 Automate journey recommendations based on AI insights
    - 🧠 Analyze behavioral patterns and payment habits
    - 📈 Maximize recovery via personalized engagement
    """)

with col2:
    st.markdown("### 🧩 Available Modules")
    st.success("1️⃣ Risk Overview")
    st.success("2️⃣ Journey Management")
    st.success("3️⃣ Recovery KPI")
    st.success("4️⃣ Behavioral Insights")

st.markdown("---")

# ─── Navigation Buttons ──────────────────────
st.markdown("### 📂 Go to Module:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📊 Risk Overview"):
        st.session_state["page"] = "pages/1_Risk_Overview.py"
        st.info("Navigate using sidebar or menu.")
with col2:
    if st.button("🧭 Journey Management"):
        st.session_state["page"] = "pages/2_Journey_Management.py"
        st.info("Navigate using sidebar or menu.")
with col3:
    if st.button("📈 Recovery KPI"):
        st.session_state["page"] = "pages/3_Recovery_KPI.py"
        st.info("Navigate using sidebar or menu.")
with col4:
    if st.button("🧠 Behavioral Insights"):
        st.session_state["page"] = "pages/4_Behavioral_Insights.py"
        st.info("Navigate using sidebar or menu.")
