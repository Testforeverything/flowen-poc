import streamlit as st
from PIL import Image

# ───── CONFIG ───────────────────────────────────────
st.set_page_config(page_title="Flowen: AI Debt Collection", layout="wide")
if "lang" not in st.session_state:
    st.session_state.lang = "🇬🇧 EN"

# ───── LANGUAGE TOGGLE ──────────────────────────────
lang = st.session_state.lang
lang_choice = st.selectbox("🌐 Language / ภาษา", ["🇬🇧 EN", "🇹🇭 TH"], index=0 if lang == "🇬🇧 EN" else 1)
st.session_state.lang = lang_choice

# ───── HEADER ────────────────────────────────────────
col1, col2 = st.columns([1, 8])
with col1:
    st.image("assets/flowen_logo.png", width=100)
with col2:
    st.markdown(f"""
    ## {"Flowen: AI Debt Collection Platform" if lang == "🇬🇧 EN" else "Flowen: แพลตฟอร์ม AI ติดตามหนี้"}
    {":robot_face: Intelligent Recovery Engine with Real-time Insights" if lang == "🇬🇧 EN" else ":robot_face: ระบบติดตามหนี้อัจฉริยะ พร้อมข้อมูลเรียลไทม์"}
    """)

st.markdown("---")

# ───── NAVIGATION BUTTONS ────────────────────────────
st.markdown("### 🔎 Dashboard Modules" if lang == "🇬🇧 EN" else "### 🔎 หน้าหลักของระบบ")

colA, colB, colC, colD = st.columns(4)

with colA:
    if st.button("📊 Risk Overview"):
        st.switch_page("pages/1_Risk_Overview.py")

with colB:
    if st.button("📍 Journey Management"):
        st.switch_page("pages/2_Journey_Management.py")

with colC:
    if st.button("📈 Recovery KPI"):
        st.switch_page("pages/3_Recovery_KPI.py")

with colD:
    if st.button("🧠 Behavioral Insights"):
        st.switch_page("pages/4_Behavioral_Insights.py")

st.markdown("---")

# ───── LANDING INFO ─────────────────────────────────
st.subheader("✨ Platform Capabilities" if lang == "🇬🇧 EN" else "✨ ความสามารถของแพลตฟอร์ม")

st.markdown("""
- ✅ Predict debtor risk using AI scoring
- 🤖 Recommend best debt collection journeys
- 📞 Simulate LINE/Voice bot for training/demo
- 📊 Visualize behavior, KPI, and segment insights
- 📤 Assign debtor into journey with one click
""") if lang == "🇬🇧 EN" else st.markdown("""
- ✅ คาดการณ์ความเสี่ยงลูกหนี้ด้วย AI
- 🤖 แนะนำกลยุทธ์ติดตามที่เหมาะสม
- 📞 จำลองบอทสนทนา LINE/Voice เพื่อใช้งาน
- 📊 วิเคราะห์พฤติกรรมและสถิติการติดตาม
- 📤 ส่งลูกหนี้เข้าสู่กลยุทธ์ได้ทันที
""")

# ───── FOOTER ───────────────────────────────────────
st.markdown("---")
st.caption("© 2025 Flowen.ai | Prototype for Demo Use")
