import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# Load data
df = pd.read_csv("flowen_mock_data_1000.csv")

# Language toggle with flag
lang_col1, lang_col2 = st.columns([0.1, 0.9])
with lang_col1:
    lang = st.selectbox("", ["🇬🇧 EN", "🇹🇭 TH"])

# Title
st.markdown(f"<h2 style='margin-bottom: 0;'>📊 Flowen - {'Debt Collection Dashboard' if lang=='🇬🇧 EN' else 'แดชบอร์ดบริหารการติดตามหนี้'}</h2>", unsafe_allow_html=True)

# KPI Cards
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Accounts" if lang == "🇬🇧 EN" else "บัญชีทั้งหมด", len(df))
with kpi2:
    st.metric("Avg. Risk Score", round(df['ai_risk_score'].mean(), 2))
with kpi3:
    if "status" in df.columns:
        escalated_count = df[df['status'] == 'Escalate'].shape[0]
    else:
        escalated_count = "N/A"
    st.metric("Escalated", escalated_count)

st.markdown("---")

# Charts
chart1, chart2 = st.columns(2)
with chart1:
    fig1 = px.histogram(
        df, x="ai_risk_score", nbins=20,
        title="Risk Score Distribution" if lang == "🇬🇧 EN" else "การกระจายของคะแนนความเสี่ยง"
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart2:
    if "risk_level" in df.columns:
        donut = df['risk_level'].value_counts().reset_index()
        fig2 = px.pie(
            donut, names='index', values='risk_level', hole=0.4,
            title="Risk Level Breakdown" if lang == "🇬🇧 EN" else "สัดส่วนระดับความเสี่ยง"
        )
        st.plotly_chart(fig2, use_container_width=True)

# Data Table Section
st.markdown("### 📋 Debtor Accounts" if lang == "🇬🇧 EN" else "📋 รายการบัญชีลูกหนี้")
selected_cols = ["account_id", "loan_type", "dpd", "dpd_bucket", "ai_risk_score", "risk_level", "income_level"]
if "status" in df.columns:
    selected_cols.append("status")

available_cols = [col for col in selected_cols if col in df.columns]
st.dataframe(df[available_cols], use_container_width=True)
