# pages/3_Recovery_KPI.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ─── Session Setup ───
if "lang" not in st.session_state:
    st.session_state["lang"] = "🇬🇧 English"
lang = st.session_state["lang"]

# ─── Page Config ───
st.set_page_config(page_title="Recovery KPI", layout="wide")

# ─── Notification Banner ───
notif_text = {
    "🇬🇧 English": "📈 Recovery today reached 320,000 THB from 4 channels.",
    "🇹🇭 ไทย": "📈 วันนี้สามารถกู้คืนหนี้ได้ 320,000 บาทจาก 4 ช่องทาง"
}
st.markdown(
    f"""
    <div style='background-color:#dff9fb;padding:10px;border-radius:8px;border-left:5px solid #00cec9;margin-bottom:15px'>
        {notif_text[lang]}
    </div>
    """, unsafe_allow_html=True
)

# ─── Title ───
st.title("📈 Recovery KPI" if lang == "🇬🇧 English" else "📈 ตัวชี้วัดการกู้คืนหนี้")
st.subheader("Channel performance and overall effectiveness" if lang == "🇬🇧 English" else "ประสิทธิภาพแต่ละช่องทางและภาพรวม")

# ─── Load Data ───
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ─── Mock Recovery KPI Table ───
channels = ["Voice", "LINE", "SMS", "Email"]
recovered_amounts = np.random.randint(60000, 120000, size=4)
success_rate = np.round(np.random.uniform(0.4, 0.75, size=4), 2)

data = pd.DataFrame({
    "Channel": channels,
    "Recovered (THB)": recovered_amounts,
    "Success Rate (%)": success_rate * 100
})

# ─── Bar Chart ───
fig = px.bar(
    data,
    x="Channel",
    y="Recovered (THB)",
    text="Success Rate (%)",
    color="Channel",
    title="Recovery by Channel" if lang == "🇬🇧 English" else "การกู้คืนตามช่องทาง",
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True)

# ─── KPI Cards ───
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="📤 Total Recovered" if lang == "🇬🇧 English" else "📤 ยอดกู้คืนรวม",
        value=f"{data['Recovered (THB)'].sum():,.0f} ฿"
    )
with col2:
    st.metric(
        label="✅ Avg. Success Rate" if lang == "🇬🇧 English" else "✅ อัตราความสำเร็จเฉลี่ย",
        value=f"{data['Success Rate (%)'].mean():.1f}%"
    )
with col3:
    st.metric(
        label="📡 Active Channels" if lang == "🇬🇧 English" else "📡 ช่องทางที่ใช้",
        value=len(channels)
    )

# ─── Export Button ───
st.markdown("---")
st.download_button(
    "⬇️ Export Recovery Report" if lang == "🇬🇧 English" else "⬇️ ดาวน์โหลดรายงานการกู้คืน",
    data=data.to_csv(index=False),
    file_name="recovery_kpi.csv"
)
