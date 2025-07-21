import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
lang = st.session_state.get("lang", "🇬🇧 EN")
st.session_state["lang"] = lang

# Notification bar
if lang == "🇬🇧 EN":
    st.info("🤖 AI behavioral clustering insights updated.")
else:
    st.info("🤖 อัปเดตการวิเคราะห์พฤติกรรมลูกหนี้โดย AI แล้ว")

# Title
st.title("🧠 Behavioral Insights" if lang == "🇬🇧 EN" else "🧠 การวิเคราะห์พฤติกรรม")

# Clustering Overview
st.subheader("📊 Debtor Clustering" if lang == "🇬🇧 EN" else "📊 การจัดกลุ่มลูกหนี้")

cluster_col = 'clustering_group' if 'clustering_group' in df.columns else 'behavior_group'

fig1 = px.pie(df, names=cluster_col, title="Debtor Behavior Clusters" if lang == "🇬🇧 EN" else "กลุ่มพฤติกรรมลูกหนี้")
st.plotly_chart(fig1, use_container_width=True)

# Breakdown by Cluster
st.subheader("📌 Cluster Breakdown" if lang == "🇬🇧 EN" else "📌 รายละเอียดแต่ละกลุ่ม")
selected_cluster = st.selectbox(
    "Select Cluster" if lang == "🇬🇧 EN" else "เลือกกลุ่มพฤติกรรม",
    df[cluster_col].unique()
)

cluster_df = df[df[cluster_col] == selected_cluster]

col1, col2 = st.columns(2)
col1.metric("Average DPD", f"{cluster_df['dpd'].mean():.1f}")
col2.metric("AI Risk Score", f"{cluster_df['ai_risk_score'].mean():.2f}")

st.dataframe(cluster_df[['customer_id', 'dpd', 'ai_risk_score', 'response_behavior', 'loan_type']].head(10),
             use_container_width=True)

# AI Insight Card
st.subheader("🔍 AI Insights" if lang == "🇬🇧 EN" else "🔍 ข้อสรุปจาก AI")

insight_map = {
    "Group A": "High engagement but slow payments. Recommend soft reminders.",
    "Group B": "Low response and high DPD. Escalation likely needed.",
    "Group C": "Frequent promises but rarely follow through. Suggest stricter follow-up.",
    "กลุ่ม A": "ตอบกลับดีแต่จ่ายช้า → ส่งเตือนแบบอ่อนโยน",
    "กลุ่ม B": "ไม่ตอบ + DPD สูง → ควร Escalate",
    "กลุ่ม C": "ชอบรับปากแต่ไม่จ่าย → ติดตามใกล้ชิด"
}

insight = insight_map.get(selected_cluster, "AI recommends standard follow-up.")
st.success(insight)

# Export
st.download_button("📥 Export Behavioral Data", data=cluster_df.to_csv(index=False),
                   file_name="behavioral_insights_export.csv")
