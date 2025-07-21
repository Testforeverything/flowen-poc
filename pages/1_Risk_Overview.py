import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# Set language
lang = st.session_state.get("lang", "🇬🇧 EN")
st.session_state["lang"] = lang

# Notification bar
if lang == "🇬🇧 EN":
    st.info("🔔 New alert: 12 high-risk debtors need escalation.")
else:
    st.info("🔔 แจ้งเตือน: ลูกหนี้ความเสี่ยงสูง 12 รายต้อง Escalate")

# Page title
st.title("📊 Risk Overview" if lang == "🇬🇧 EN" else "📊 ภาพรวมความเสี่ยง")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Debtors" if lang == "🇬🇧 EN" else "จำนวนลูกหนี้ทั้งหมด", len(df))
col2.metric("Avg Risk Score", f"{df['ai_risk_score'].mean():.2f}")
col3.metric("High Risk %", f"{(df['ai_risk_score'] > 0.7).mean() * 100:.1f}%")

# Pie chart of risk group
risk_group_count = df['clustering_group'].value_counts().reset_index()
risk_group_count.columns = ['Group', 'Count']
fig_pie = px.pie(risk_group_count, names='Group', values='Count', hole=0.4,
                 title="Risk Group Distribution" if lang == "🇬🇧 EN" else "การกระจายกลุ่มความเสี่ยง")
st.plotly_chart(fig_pie, use_container_width=True)

# Bar chart by Region
region_risk = df.groupby('region')['ai_risk_score'].mean().reset_index()
fig_bar = px.bar(region_risk, x='region', y='ai_risk_score',
                 title="Avg Risk Score by Region" if lang == "🇬🇧 EN" else "คะแนนความเสี่ยงเฉลี่ยตามภูมิภาค")
st.plotly_chart(fig_bar, use_container_width=True)

# Export
st.download_button("📥 Export CSV", data=df.to_csv(index=False), file_name="risk_overview_export.csv")
