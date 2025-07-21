# pages/1_Risk_Overview.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Session Setup ───
if "lang" not in st.session_state:
    st.session_state["lang"] = "🇬🇧 English"
lang = st.session_state["lang"]

# ─── Page Config ───
st.set_page_config(page_title="Risk Overview", layout="wide")

# ─── Notification Banner ───
notif_text = {
    "🇬🇧 English": "📢 Reminder: 12 high-risk accounts require follow-up today.",
    "🇹🇭 ไทย": "📢 แจ้งเตือน: พบลูกหนี้กลุ่มเสี่ยง 12 รายควรติดตามวันนี้"
}
st.markdown(
    f"""
    <div style='background-color:#ffeaa7;padding:10px;border-radius:8px;border-left:5px solid #fdcb6e;margin-bottom:15px'>
        {notif_text[lang]}
    </div>
    """, unsafe_allow_html=True
)

# ─── Title ───
if lang == "🇬🇧 English":
    st.title("📊 Risk Overview")
    st.subheader("Portfolio Risk Distribution and Segmentation")
else:
    st.title("📊 ภาพรวมความเสี่ยง")
    st.subheader("การกระจายและการแบ่งกลุ่มความเสี่ยงของลูกหนี้")

# ─── Load Data ───
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ─── Layout ───
col1, col2, col3 = st.columns(3)

# ─── Pie: Risk Level Breakdown ───
with col1:
    risk_pie = df["risk_score"].value_counts().reset_index()
    fig = px.pie(
        risk_pie,
        names="index",
        values="risk_score",
        title="Risk Score Distribution" if lang == "🇬🇧 English" else "การกระจายคะแนนความเสี่ยง",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig, use_container_width=True)

# ─── Bar: Segmentation ───
with col2:
    segment = df["clustering_group"].value_counts().reset_index()
    fig2 = px.bar(
        segment,
        x="index",
        y="clustering_group",
        title="Behavioral Segmentation" if lang == "🇬🇧 English" else "การแบ่งกลุ่มพฤติกรรม",
        labels={"index": "Cluster", "clustering_group": "Count"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig2, use_container_width=True)

# ─── Donut: Region Breakdown ───
with col3:
    region = df["region"].value_counts().reset_index()
    fig3 = px.pie(
        region,
        names="index",
        values="region",
        hole=0.4,
        title="By Region" if lang == "🇬🇧 English" else "ตามภูมิภาค",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig3, use_container_width=True)

# ─── KPI Card ───
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="🟡 Avg. Risk Score" if lang == "🇬🇧 English" else "🟡 คะแนนความเสี่ยงเฉลี่ย",
        value=round(df["risk_score"].mean(), 2)
    )
with col2:
    st.metric(
        label="📌 High Risk %", 
        value=f"{(df['risk_score'] >= 8).mean() * 100:.1f}%" if lang == "🇬🇧 English" else f"{(df['risk_score'] >= 8).mean() * 100:.1f}%"
    )
with col3:
    st.metric(
        label="📍 Unique Regions" if lang == "🇬🇧 English" else "📍 ภูมิภาคทั้งหมด",
        value=df["region"].nunique()
    )

# ─── Export Button ───
st.markdown("---")
if lang == "🇬🇧 English":
    st.download_button("⬇️ Export CSV", data=df.to_csv(index=False), file_name="risk_overview.csv")
else:
    st.download_button("⬇️ ดาวน์โหลดข้อมูล CSV", data=df.to_csv(index=False), file_name="risk_overview.csv")
