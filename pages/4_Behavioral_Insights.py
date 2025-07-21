# pages/4_Behavioral_Insights.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Session Setup ───
if "lang" not in st.session_state:
    st.session_state["lang"] = "🇬🇧 English"
lang = st.session_state["lang"]

# ─── Page Config ───
st.set_page_config(page_title="Behavioral Insights", layout="wide")

# ─── Notification Banner ───
notif_text = {
    "🇬🇧 English": "📌 AI detected 3 new behavioral clusters with high recovery potential.",
    "🇹🇭 ไทย": "📌 ระบบ AI พบ 3 กลุ่มพฤติกรรมใหม่ที่มีโอกาสกู้คืนหนี้สูง"
}
st.markdown(
    f"""
    <div style='background-color:#ffeaa7;padding:10px;border-radius:8px;border-left:5px solid #fdcb6e;margin-bottom:15px'>
        {notif_text[lang]}
    </div>
    """, unsafe_allow_html=True
)

# ─── Title ───
st.title("🧠 Behavioral Insights" if lang == "🇬🇧 English" else "🧠 การวิเคราะห์พฤติกรรม")
st.subheader("AI clustering & behavioral pattern detection" if lang == "🇬🇧 English" else "การจับกลุ่มพฤติกรรมและวิเคราะห์โดย AI")

# ─── Load Data ───
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ─── Insight Card ───
insight = {
    "🇬🇧 English": """
- Cluster 0 = 'Silent but Pays Late'
- Cluster 1 = 'Responsive but Avoids'
- Cluster 2 = 'High-Risk Ignorers'
""",
    "🇹🇭 ไทย": """
- กลุ่ม 0 = 'เงียบแต่จ่ายช้า'
- กลุ่ม 1 = 'ตอบกลับแต่เลี่ยง'
- กลุ่ม 2 = 'ไม่ตอบเลยและมีความเสี่ยงสูง'
"""
}
st.info(insight[lang])

# ─── Chart: Cluster Distribution ───
st.markdown("### 🔍 Cluster Distribution" if lang == "🇬🇧 English" else "### 🔍 การกระจายของกลุ่มพฤติกรรม")

fig = px.histogram(
    df,
    x="clustering_group",
    color="clustering_group",
    title="Behavioral Cluster Count" if lang == "🇬🇧 English" else "จำนวนลูกหนี้ในแต่ละกลุ่มพฤติกรรม",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(bargap=0.3)
st.plotly_chart(fig, use_container_width=True)

# ─── Table View ───
st.markdown("### 📋 Cluster Sample" if lang == "🇬🇧 English" else "### 📋 ตัวอย่างลูกหนี้แต่ละกลุ่ม")
sample_df = df[["account_id", "dpd", "loan_type", "response_behavior", "clustering_group"]].head(30)
sample_df.columns = (
    ["Account ID", "DPD", "Loan Type", "Behavior", "Cluster"]
    if lang == "🇬🇧 English"
    else ["บัญชี", "DPD", "ประเภท", "พฤติกรรม", "กลุ่ม"]
)
st.dataframe(sample_df, use_container_width=True)

# ─── Export Button ───
st.markdown("---")
st.download_button(
    "⬇️ Export Behavioral Data" if lang == "🇬🇧 English" else "⬇️ ดาวน์โหลดข้อมูลพฤติกรรม",
    data=sample_df.to_csv(index=False),
    file_name="behavioral_insights.csv"
)
