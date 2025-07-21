# pages/2_Journey_Management.py

import streamlit as st
import pandas as pd

# ─── Session Setup ───
if "lang" not in st.session_state:
    st.session_state["lang"] = "🇬🇧 English"
lang = st.session_state["lang"]

# ─── Page Config ───
st.set_page_config(page_title="Journey Management", layout="wide")

# ─── Notification Banner ───
notif_text = {
    "🇬🇧 English": "🧭 AI has updated recommended journey flows for 5 high-risk accounts.",
    "🇹🇭 ไทย": "🧭 ระบบ AI ได้อัปเดตเส้นทางติดตามหนี้สำหรับลูกหนี้กลุ่มเสี่ยง 5 ราย"
}
st.markdown(
    f"""
    <div style='background-color:#ffeaa7;padding:10px;border-radius:8px;border-left:5px solid #fdcb6e;margin-bottom:15px'>
        {notif_text[lang]}
    </div>
    """, unsafe_allow_html=True
)

# ─── Title ───
st.title("🧭 Journey Management" if lang == "🇬🇧 English" else "🧭 การจัดการเส้นทางติดตามหนี้")

# ─── Load Data ───
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ─── Journey Strategy Selector ───
journey_templates = {
    "🇬🇧 English": ["Call → LINE → Wait 3 Days", "SMS → LINE + Call", "LINE → Email → Escalate"],
    "🇹🇭 ไทย": ["โทร → LINE → รอ 3 วัน", "SMS → LINE + โทร", "LINE → อีเมล → ส่งต่อเจ้าหน้าที่"]
}
selected = st.selectbox(
    "📂 Select Journey Strategy" if lang == "🇬🇧 English" else "📂 เลือกกลยุทธ์การติดตาม",
    journey_templates[lang]
)

# ─── Explanation Card ───
st.markdown("---")
st.markdown("### 🤖 AI Recommendation")
reason = {
    "🇬🇧 English": "Based on debtor's past behavior and region success rate, this journey is optimal.",
    "🇹🇭 ไทย": "จากพฤติกรรมลูกหนี้ในอดีต และอัตราการทวงหนี้สำเร็จในแต่ละภูมิภาค ระบบแนะนำเส้นทางนี้"
}
st.info(reason[lang])

# ─── Journey Log Table ───
st.markdown("---")
st.markdown("### 📋 Journey Log" if lang == "🇬🇧 English" else "### 📋 ประวัติเส้นทางติดตาม")

journey_log = df[["account_id", "loan_type", "dpd", "risk_score", "recommended_journey", "ai_confidence"]].copy()
journey_log.columns = (
    ["Account ID", "Loan Type", "DPD", "Risk", "Journey", "Confidence"]
    if lang == "🇬🇧 English"
    else ["บัญชี", "ประเภทสินเชื่อ", "DPD", "ความเสี่ยง", "เส้นทางติดตาม", "ความมั่นใจของ AI"]
)

st.dataframe(journey_log.head(30), use_container_width=True)

# ─── Export Button ───
st.markdown("---")
st.download_button(
    "⬇️ Export Journey Log" if lang == "🇬🇧 English" else "⬇️ ดาวน์โหลดประวัติเส้นทาง",
    data=journey_log.to_csv(index=False),
    file_name="journey_log.csv"
)
