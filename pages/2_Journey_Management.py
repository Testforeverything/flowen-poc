import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
lang = st.session_state.get("lang", "🇬🇧 EN")
st.session_state["lang"] = lang

# Notification bar
if lang == "🇬🇧 EN":
    st.info("🧠 AI: Recommended follow-up strategies updated.")
else:
    st.info("🧠 AI: ระบบแนะนำกลยุทธ์การติดตามอัปเดตแล้ว")

st.title("🧩 Journey Management" if lang == "🇬🇧 EN" else "🧩 การจัดการเส้นทางติดตาม")

# Funnel Visualization
funnel_stage = df['journey_stage'].value_counts().reset_index()
funnel_stage.columns = ['Stage', 'Count']
fig_funnel = px.funnel(funnel_stage, x='Count', y='Stage',
                       title="Journey Funnel" if lang == "🇬🇧 EN" else "ภาพรวมเส้นทางการติดตาม")
st.plotly_chart(fig_funnel, use_container_width=True)

# AI Journey Recommendation
st.subheader("🤖 AI Strategy Recommendation" if lang == "🇬🇧 EN" else "🤖 คำแนะนำจาก AI")
selected_id = st.selectbox("Select Debtor ID", df['account_id'].unique())
selected_row = df[df['account_id'] == selected_id].iloc[0]

strategy = "Send LINE → Wait 2 days → Call" if selected_row['ai_risk_score'] > 0.7 else "Send SMS only"
confidence = f"{selected_row['ai_confidence']*100:.1f}%"

st.markdown(f"""
- **Strategy**: {strategy}
- **Confidence**: {confidence}
""")

if st.button("🚀 Apply Journey" if lang == "🇬🇧 EN" else "🚀 ใช้กลยุทธ์นี้"):
    st.success("Journey applied." if lang == "🇬🇧 EN" else "กลยุทธ์ถูกใช้งานแล้ว")

# Journey Log Table
st.subheader("📋 Journey Log" if lang == "🇬🇧 EN" else "📋 บันทึกกลยุทธ์")
st.dataframe(df[['account_id', 'journey_stage', 'ai_risk_score', 'response_behavior']].head(10))

# Export
st.download_button("📥 Export Log", data=df.to_csv(index=False), file_name="journey_log_export.csv")
